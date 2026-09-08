import sqlite3
from datetime import datetime, timedelta


DATABASE = "careconnect.db"


# ============================================================
# DATABASE
# ============================================================

def get_db_connection():
    """
    Create a SQLite connection with dictionary-like rows.
    """

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    return conn


# ============================================================
# PERFORMANCE ANALYSIS
# ============================================================

def get_recent_results(patient_id, limit=20):
    """
    Return the most recent cognitive activity results
    for one patient.
    """

    conn = get_db_connection()

    results = conn.execute("""
        SELECT
            id,
            activity_type,
            difficulty,
            objects_shown,
            correct_answers,
            incorrect_answers,
            missed_answers,
            response_time,
            memory_score,
            timestamp
        FROM cognitive_results
        WHERE patient_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (
        patient_id,
        limit
    )).fetchall()

    conn.close()

    return [dict(result) for result in results]


def calculate_activity_statistics(results):
    """
    Calculate simple performance statistics for each activity.

    This is an activity-engagement analysis, not a medical
    or clinical assessment.
    """

    activity_names = [
        "memory",
        "attention",
        "recall",
        "object_match"
    ]

    statistics = {}

    for activity in activity_names:

        activity_results = [
            result
            for result in results
            if result.get("activity_type") == activity
        ]

        if not activity_results:
            statistics[activity] = {
                "attempts": 0,
                "average_score": None,
                "recent_score": None,
                "trend": "no_data"
            }

            continue

        scores = [
            float(result.get("memory_score", 0))
            for result in activity_results
        ]

        average_score = sum(scores) / len(scores)

        recent_score = scores[0]

        if len(scores) >= 3:

            recent_average = sum(scores[:3]) / 3
            older_scores = scores[3:]

            if older_scores:
                older_average = sum(older_scores) / len(older_scores)

                difference = recent_average - older_average

                if difference >= 8:
                    trend = "improving"

                elif difference <= -8:
                    trend = "declining"

                else:
                    trend = "stable"

            else:
                trend = "stable"

        elif len(scores) == 2:

            difference = scores[0] - scores[1]

            if difference >= 8:
                trend = "improving"

            elif difference <= -8:
                trend = "declining"

            else:
                trend = "stable"

        else:
            trend = "new"

        statistics[activity] = {
            "attempts": len(scores),
            "average_score": round(average_score, 1),
            "recent_score": round(recent_score, 1),
            "trend": trend
        }

    return statistics


# ============================================================
# ACTIVITY SELECTION
# ============================================================

def choose_next_activity(statistics):
    """
    Choose the next cognitive activity using recent
    performance history.

    Priority:
    1. Activities with declining performance
    2. Activities with lower recent performance
    3. Activities that have not been practiced yet
    4. Otherwise rotate between activities

    This is not a medical recommendation.
    """

    activity_order = [
        "recall",
        "memory",
        "attention",
        "object_match"
    ]

    # --------------------------------------------------------
    # First priority:
    # Find an activity whose recent performance is declining.
    # --------------------------------------------------------

    declining = [
        activity
        for activity in activity_order
        if statistics[activity]["trend"] == "declining"
    ]

    if declining:

        declining.sort(
            key=lambda activity: (
                statistics[activity]["recent_score"]
                if statistics[activity]["recent_score"] is not None
                else 101
            )
        )

        return declining[0]

    # --------------------------------------------------------
    # Second priority:
    # Find activities with the lowest recent score.
    # --------------------------------------------------------

    available_scores = [
        (
            activity,
            statistics[activity]["recent_score"]
        )
        for activity in activity_order
        if statistics[activity]["recent_score"] is not None
    ]

    if available_scores:

        available_scores.sort(
            key=lambda item: item[1]
        )

        lowest_activity, lowest_score = available_scores[0]

        if lowest_score < 80:
            return lowest_activity

    # --------------------------------------------------------
    # Third priority:
    # Prefer activities that have never been attempted.
    # --------------------------------------------------------

    for activity in activity_order:

        if statistics[activity]["attempts"] == 0:
            return activity

    # --------------------------------------------------------
    # Final fallback:
    # Choose the activity with the oldest/latest practice
    # pattern by simply using the lowest average score.
    # --------------------------------------------------------

    practiced = [
        (
            activity,
            statistics[activity]["average_score"]
        )
        for activity in activity_order
        if statistics[activity]["average_score"] is not None
    ]

    if practiced:

        practiced.sort(
            key=lambda item: item[1]
        )

        return practiced[0][0]

    return "recall"


# ============================================================
# DIFFICULTY SELECTION
# ============================================================

def choose_difficulty(activity_statistics):
    """
    Choose a simple adaptive difficulty for one activity.

    The goal is to keep activities personalized without making
    a clinical judgment about the patient.
    """

    attempts = activity_statistics.get(
        "attempts",
        0
    )

    recent_score = activity_statistics.get(
        "recent_score"
    )

    trend = activity_statistics.get(
        "trend",
        "no_data"
    )

    # New activity → start gently.
    if attempts == 0 or recent_score is None:
        return "easy"

    # Strong recent performance → challenge slightly more.
    if recent_score >= 85:

        if trend == "improving":
            return "hard"

        return "medium"

    # Moderate performance → stay around medium.
    if recent_score >= 60:
        return "medium"

    # Lower recent performance → return to easier practice.
    return "easy"


# ============================================================
# PERSONAL MEMORY ANALYSIS
# ============================================================

def get_memory_profile(patient_id):
    """
    Retrieve the patient's personal memory profile.
    """

    conn = get_db_connection()

    profile = conn.execute("""
        SELECT
            region,
            favorite_foods,
            favorite_places,
            favorite_festivals,
            important_people,
            favorite_songs,
            hobbies,
            childhood_memories,
            meaningful_objects
        FROM memory_profiles
        WHERE patient_id = ?
    """, (
        patient_id,
    )).fetchone()

    conn.close()

    if profile is None:
        return None

    return dict(profile)


def get_available_memory_categories(profile):
    """
    Determine which personal-memory categories actually contain
    information.

    Empty categories are never selected for personalization.
    """

    if not profile:
        return []

    category_mapping = {
        "favorite_foods": "favorite_foods",
        "favorite_places": "favorite_places",
        "favorite_festivals": "favorite_festivals",
        "important_people": "important_people",
        "favorite_songs": "favorite_songs",
        "hobbies": "hobbies",
        "childhood_memories": "childhood_memories",
        "meaningful_objects": "meaningful_objects"
    }

    available = []

    for field, category in category_mapping.items():

        value = profile.get(field)

        if isinstance(value, str) and value.strip():
            available.append(category)

    return available


# ============================================================
# PERSONALIZATION STRATEGY
# ============================================================

def choose_memory_category(
    profile,
    activity_type
):
    """
    Choose the most useful personal-memory category for the
    recommended activity.

    The mapping is intentionally simple and explainable.
    """

    available = get_available_memory_categories(
        profile
    )

    if not available:
        return None

    # --------------------------------------------------------
    # Activity-specific preferences
    # --------------------------------------------------------

    preferred_categories = {

        "recall": [
            "childhood_memories",
            "important_people",
            "favorite_places",
            "favorite_festivals",
            "favorite_songs",
            "hobbies",
            "favorite_foods",
            "meaningful_objects"
        ],

        "memory": [
            "meaningful_objects",
            "favorite_foods",
            "favorite_places",
            "favorite_festivals",
            "important_people",
            "hobbies",
            "favorite_songs",
            "childhood_memories"
        ],

        "object_match": [
            "meaningful_objects",
            "favorite_foods",
            "favorite_places",
            "hobbies",
            "favorite_festivals",
            "important_people",
            "favorite_songs",
            "childhood_memories"
        ],

        "attention": [
            "favorite_foods",
            "meaningful_objects",
            "favorite_festivals",
            "favorite_places",
            "hobbies",
            "important_people",
            "favorite_songs",
            "childhood_memories"
        ]
    }

    preferred = preferred_categories.get(
        activity_type,
        available
    )

    for category in preferred:

        if category in available:
            return category

    return available[0]


# ============================================================
# ENGINE
# ============================================================

def build_cognitive_plan(patient_id):
    """
    Build one explainable personalized cognitive plan.

    Returns:
        - recommended activity
        - recommended difficulty
        - personal memory category
        - performance statistics
        - personalization availability

    This engine is designed for prototype-level cognitive
    engagement and personalization. It is not a diagnostic
    system.
    """

    results = get_recent_results(
        patient_id,
        limit=20
    )

    statistics = calculate_activity_statistics(
        results
    )

    next_activity = choose_next_activity(
        statistics
    )

    activity_statistics = statistics[
        next_activity
    ]

    difficulty = choose_difficulty(
        activity_statistics
    )

    profile = get_memory_profile(
        patient_id
    )

    memory_category = choose_memory_category(
        profile,
        next_activity
    )

    region = None

    if profile:
        region = profile.get(
            "region"
        )

    return {
        "success": True,

        "patient_id": patient_id,

        "recommended_activity": next_activity,

        "recommended_difficulty": difficulty,

        "personal_memory_category":
            memory_category,

        "region": region,

        "personalization_available":
            bool(memory_category),

        "activity_statistics":
            statistics,

        "recent_result_count":
            len(results),

        "generated_at":
            datetime.now().isoformat()
    }


# ============================================================
# HUMAN-READABLE EXPLANATION
# ============================================================

def explain_plan(plan):
    """
    Produce a short explanation of why the engine selected
    the current activity.

    This is useful for the caregiver dashboard/demo.
    """

    activity = plan.get(
        "recommended_activity",
        "recall"
    )

    difficulty = plan.get(
        "recommended_difficulty",
        "easy"
    )

    category = plan.get(
        "personal_memory_category"
    )

    statistics = plan.get(
        "activity_statistics",
        {}
    )

    activity_stats = statistics.get(
        activity,
        {}
    )

    trend = activity_stats.get(
        "trend",
        "no_data"
    )

    score = activity_stats.get(
        "recent_score"
    )

    if trend == "declining":
        reason = (
            "Recent performance in this activity has been "
            "lower than earlier attempts."
        )

    elif score is not None and score < 80:
        reason = (
            "This activity has a lower recent performance "
            "score, so the engine is giving it more practice."
        )

    elif activity_stats.get("attempts", 0) == 0:
        reason = (
            "This activity has not been practiced yet."
        )

    else:
        reason = (
            "The engine selected this activity based on the "
            "patient's recent activity history."
        )

    if category:
        personalization_reason = (
            f" Personal content can use the patient's "
            f"{category.replace('_', ' ')}."
        )

    else:
        personalization_reason = (
            " No personal memory category is currently "
            "available for this activity."
        )

    return (
        f"Recommended {activity.replace('_', ' ').title()} "
        f"at {difficulty.title()} difficulty. "
        f"{reason}"
        f"{personalization_reason}"
    )