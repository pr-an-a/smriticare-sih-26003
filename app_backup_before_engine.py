from flask import Flask, render_template, request, jsonify
from ai_helper import (
    generate_personalized_prompt,
    evaluate_personalized_answer,
    generate_conversation_prompt
)
import json
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

CULTURAL_LIBRARY_PATH = os.path.join(
    os.path.dirname(__file__),
    "cultural_data",
    "ner_memory_library.json"
)


def load_cultural_library():
    """
    Load the optional North Eastern Region cultural memory library.

    The library provides cultural context for personalization.
    It is not used as a source for medical diagnosis or evaluation.
    """

    try:
        with open(
            CULTURAL_LIBRARY_PATH,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except Exception as error:
        print(
            "Cultural library error:",
            error
        )

        return {}


DATABASE = "careconnect.db"

# ------------------------------------------------------------
# Recent personalized questions
#
# This prevents the AI from repeatedly generating the same
# question during the current application session.
# ------------------------------------------------------------

recent_personalized_questions = []


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cognitive_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_type TEXT NOT NULL,
            difficulty TEXT,
            objects_shown INTEGER,
            correct_answers INTEGER,
            incorrect_answers INTEGER,
            missed_answers INTEGER,
            response_time REAL,
            memory_score REAL,
            timestamp TEXT NOT NULL,
            patient_id INTEGER
        )
    """)

    cursor.execute("PRAGMA table_info(cognitive_results)")
    columns = [column["name"] for column in cursor.fetchall()]

    if "patient_id" not in columns:
        cursor.execute("""
            ALTER TABLE cognitive_results
            ADD COLUMN patient_id INTEGER
        """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            notes TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)

    # Personal Memory Profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER UNIQUE,
            favorite_foods TEXT,
            favorite_places TEXT,
            favorite_festivals TEXT,
            important_people TEXT,
            favorite_songs TEXT,
            hobbies TEXT,
            childhood_memories TEXT,
            meaningful_objects TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    # ------------------------------------------------------------
    # Add region column to older databases if it does not exist.
    # This keeps the existing careconnect.db compatible.
    # ------------------------------------------------------------

    cursor.execute("PRAGMA table_info(memory_profiles)")
    memory_profile_columns = [
        column["name"]
        for column in cursor.fetchall()
    ]

    if "region" not in memory_profile_columns:
        cursor.execute("""
            ALTER TABLE memory_profiles
            ADD COLUMN region TEXT
        """)


# ============================================================
# AI PERSONALIZED ANSWER EVALUATION
# ============================================================


@app.route("/api/evaluate-personalized-answer", methods=["POST"])
def evaluate_personalized_answer_api():
    """
    Evaluate a patient's personalized-memory answer by meaning
    rather than exact wording.

    The expected answer is kept on the server and is never
    shown directly to the patient.

    This feature provides activity feedback only.
    It does not diagnose or medically evaluate the patient.
    """

    data = request.get_json() or {}

    question = str(
        data.get("question", "")
    ).strip()

    expected_answer = str(
        data.get("expected_answer", "")
    ).strip()

    patient_answer = str(
        data.get("patient_answer", "")
    ).strip()

    memory_source = str(
        data.get("memory_source", "")
    ).strip()

    if not question:
        return jsonify({
            "success": False,
            "message": "Question is required"
        }), 400

    if not expected_answer:
        return jsonify({
            "success": False,
            "message": "Expected answer is required"
        }), 400

    if not patient_answer:
        return jsonify({
            "success": False,
            "message": "Patient answer is required"
        }), 400

    result = evaluate_personalized_answer(
        question=question,
        expected_answer=expected_answer,
        patient_answer=patient_answer,
        memory_source=memory_source
    )

    if not result.get("success"):
        return jsonify(result), 500

    return jsonify(result)
    # Memory Circle
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_circle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            memory_text TEXT NOT NULL,
            response_text TEXT,
            created_at TEXT NOT NULL,
            response_at TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        )
    """)

    cursor.execute("SELECT COUNT(*) AS count FROM patients")
    patient_count = cursor.fetchone()["count"]

    if patient_count == 0:
        cursor.execute("""
            INSERT INTO patients (name, age, created_at)
            VALUES (?, ?, ?)
        """, (
            "Demo Patient",
            65,
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/caregiver-dashboard")
def caregiver_dashboard():
    return render_template("caregiver-dashboard.html")


@app.route("/memory-game")
def memory_game():
    return render_template("memory-game.html")


@app.route("/attention-game")
def attention_game():
    return render_template("attention-game.html")


@app.route("/recall-game")
def recall_game():
    return render_template("recall-game.html")


@app.route("/object-match")
def object_match():
    return render_template("object-match.html")


# ============================================================
# PATIENT
# ============================================================


@app.route("/api/patient", methods=["GET"])
def get_patient():
    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id, name, age, created_at
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    conn.close()

    if patient is None:
        return jsonify({
            "success": False,
            "message": "No patient found"
        }), 404

    return jsonify({
        "success": True,
        "patient": dict(patient)
    })


@app.route("/api/patient", methods=["PUT"])
def update_patient():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    age = data.get("age")

    if not name:
        return jsonify({
            "success": False,
            "message": "Patient name is required"
        }), 400

    try:
        age = int(age)
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "message": "Age must be a number"
        }), 400

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        cursor = conn.execute("""
            INSERT INTO patients (name, age, created_at)
            VALUES (?, ?, ?)
        """, (
            name,
            age,
            datetime.now().isoformat()
        ))

        patient_id = cursor.lastrowid

    else:
        patient_id = patient["id"]

        conn.execute("""
            UPDATE patients
            SET name = ?, age = ?
            WHERE id = ?
        """, (
            name,
            age,
            patient_id
        ))

    conn.commit()

    updated_patient = conn.execute("""
        SELECT id, name, age, created_at
        FROM patients
        WHERE id = ?
    """, (patient_id,)).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "patient": dict(updated_patient)
    })


# ============================================================
# COGNITIVE RESULTS
# ============================================================


@app.route("/api/save-result", methods=["POST"])
def save_result():
    data = request.get_json() or {}

    activity_type = data.get("activity_type")
    difficulty = data.get("difficulty")
    objects_shown = data.get("objects_shown", 0)
    correct_answers = data.get("correct_answers", 0)
    incorrect_answers = data.get("incorrect_answers", 0)
    missed_answers = data.get("missed_answers", 0)
    response_time = data.get("response_time", 0)
    memory_score = data.get("memory_score", 0)

    if not activity_type:
        return jsonify({
            "success": False,
            "message": "Activity type is required"
        }), 400

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    patient_id = patient["id"] if patient else None

    conn.execute("""
        INSERT INTO cognitive_results (
            activity_type,
            difficulty,
            objects_shown,
            correct_answers,
            incorrect_answers,
            missed_answers,
            response_time,
            memory_score,
            timestamp,
            patient_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        activity_type,
        difficulty,
        objects_shown,
        correct_answers,
        incorrect_answers,
        missed_answers,
        response_time,
        memory_score,
        datetime.now().isoformat(),
        patient_id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Result saved successfully"
    })


@app.route("/api/cognitive-history", methods=["GET"])
def cognitive_history():
    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": True,
            "history": []
        })

    patient_id = patient["id"]

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
            timestamp,
            patient_id
        FROM cognitive_results
        WHERE patient_id = ?
        ORDER BY timestamp DESC
    """, (patient_id,)).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "history": [dict(result) for result in results]
    })


# ============================================================
# REMINDERS
# ============================================================


@app.route("/api/reminders", methods=["GET"])
def get_reminders():
    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": True,
            "reminders": []
        })

    reminders = conn.execute("""
        SELECT
            id,
            patient_id,
            title,
            category,
            reminder_time,
            notes,
            completed,
            created_at
        FROM reminders
        WHERE patient_id = ?
        ORDER BY reminder_time ASC
    """, (patient["id"],)).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "reminders": [dict(reminder) for reminder in reminders]
    })


@app.route("/api/reminders", methods=["POST"])
def create_reminder():
    data = request.get_json() or {}

    title = data.get("title", "").strip()
    category = data.get("category", "").strip()
    reminder_time = data.get("reminder_time", "").strip()
    notes = data.get("notes", "").strip()

    if not title:
        return jsonify({
            "success": False,
            "message": "Reminder title is required"
        }), 400

    if not category:
        return jsonify({
            "success": False,
            "message": "Reminder category is required"
        }), 400

    if not reminder_time:
        return jsonify({
            "success": False,
            "message": "Reminder time is required"
        }), 400

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "No patient found"
        }), 404

    cursor = conn.execute("""
        INSERT INTO reminders (
            patient_id,
            title,
            category,
            reminder_time,
            notes,
            completed,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        patient["id"],
        title,
        category,
        reminder_time,
        notes,
        0,
        datetime.now().isoformat()
    ))

    conn.commit()

    reminder = conn.execute("""
        SELECT
            id,
            patient_id,
            title,
            category,
            reminder_time,
            notes,
            completed,
            created_at
        FROM reminders
        WHERE id = ?
    """, (cursor.lastrowid,)).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "message": "Reminder created successfully",
        "reminder": dict(reminder)
    })


@app.route("/api/reminders/<int:reminder_id>/complete", methods=["PUT"])
def complete_reminder(reminder_id):
    conn = get_db_connection()

    reminder = conn.execute("""
        SELECT id
        FROM reminders
        WHERE id = ?
    """, (reminder_id,)).fetchone()

    if reminder is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "Reminder not found"
        }), 404

    conn.execute("""
        UPDATE reminders
        SET completed = 1
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()

    updated_reminder = conn.execute("""
        SELECT
            id,
            patient_id,
            title,
            category,
            reminder_time,
            notes,
            completed,
            created_at
        FROM reminders
        WHERE id = ?
    """, (reminder_id,)).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "message": "Reminder marked as completed",
        "reminder": dict(updated_reminder)
    })


@app.route("/api/reminders/<int:reminder_id>", methods=["DELETE"])
def delete_reminder(reminder_id):
    conn = get_db_connection()

    reminder = conn.execute("""
        SELECT id
        FROM reminders
        WHERE id = ?
    """, (reminder_id,)).fetchone()

    if reminder is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "Reminder not found"
        }), 404

    conn.execute("""
        DELETE FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Reminder deleted successfully"
    })


# ============================================================
# PERSONAL MEMORY PROFILE
# ============================================================


@app.route("/api/memory-profile", methods=["GET"])
def get_memory_profile():
    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "No patient found"
        }), 404

    profile = conn.execute("""
        SELECT
            id,
            patient_id,
            region,
            favorite_foods,
            favorite_places,
            favorite_festivals,
            important_people,
            favorite_songs,
            hobbies,
            childhood_memories,
            meaningful_objects,
            created_at,
            updated_at
        FROM memory_profiles
        WHERE patient_id = ?
    """, (patient["id"],)).fetchone()

    conn.close()

    if profile is None:
        return jsonify({
            "success": True,
            "profile": None
        })

    return jsonify({
        "success": True,
        "profile": dict(profile)
    })


@app.route("/api/memory-profile", methods=["PUT"])
def update_memory_profile():
    data = request.get_json() or {}

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "No patient found"
        }), 404

    patient_id = patient["id"]
    now = datetime.now().isoformat()

    region = data.get("region", "").strip().lower()

    favorite_foods = data.get(
        "favorite_foods",
        ""
    ).strip()

    favorite_places = data.get(
        "favorite_places",
        ""
    ).strip()

    favorite_festivals = data.get(
        "favorite_festivals",
        ""
    ).strip()

    important_people = data.get(
        "important_people",
        ""
    ).strip()

    favorite_songs = data.get(
        "favorite_songs",
        ""
    ).strip()

    hobbies = data.get(
        "hobbies",
        ""
    ).strip()

    childhood_memories = data.get(
        "childhood_memories",
        ""
    ).strip()

    meaningful_objects = data.get(
        "meaningful_objects",
        ""
    ).strip()

    existing_profile = conn.execute("""
        SELECT id
        FROM memory_profiles
        WHERE patient_id = ?
    """, (patient_id,)).fetchone()

    if existing_profile is None:

        cursor = conn.execute("""
            INSERT INTO memory_profiles (
                patient_id,
                region,
                favorite_foods,
                favorite_places,
                favorite_festivals,
                important_people,
                favorite_songs,
                hobbies,
                childhood_memories,
                meaningful_objects,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            region,
            favorite_foods,
            favorite_places,
            favorite_festivals,
            important_people,
            favorite_songs,
            hobbies,
            childhood_memories,
            meaningful_objects,
            now,
            now
        ))

        profile_id = cursor.lastrowid

    else:

        profile_id = existing_profile["id"]

        conn.execute("""
            UPDATE memory_profiles
            SET
                region = ?,
                favorite_foods = ?,
                favorite_places = ?,
                favorite_festivals = ?,
                important_people = ?,
                favorite_songs = ?,
                hobbies = ?,
                childhood_memories = ?,
                meaningful_objects = ?,
                updated_at = ?
            WHERE patient_id = ?
        """, (
            region,
            favorite_foods,
            favorite_places,
            favorite_festivals,
            important_people,
            favorite_songs,
            hobbies,
            childhood_memories,
            meaningful_objects,
            now,
            patient_id
        ))

    conn.commit()

    profile = conn.execute("""
        SELECT
            id,
            patient_id,
            region,
            favorite_foods,
            favorite_places,
            favorite_festivals,
            important_people,
            favorite_songs,
            hobbies,
            childhood_memories,
            meaningful_objects,
            created_at,
            updated_at
        FROM memory_profiles
        WHERE id = ?
    """, (profile_id,)).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "message": "Memory profile saved successfully",
        "profile": dict(profile)
    })


# ============================================================
# AI PERSONALIZED PROMPT
# ============================================================


@app.route("/api/personalized-prompt", methods=["GET"])
def personalized_prompt():
    """
    Generate a personal-memory cognitive question.

    The patient's own memory profile remains the primary source.
    If a North Eastern Region is selected, the matching cultural
    library is supplied only as optional contextual information.

    Recent questions are supplied to the AI so that consecutive
    rounds do not repeatedly ask the same question.
    """

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "No patient found"
        }), 404

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
    """, (patient["id"],)).fetchone()

    conn.close()

    if profile is None:
        return jsonify({
            "success": False,
            "message": "No personal memory profile found"
        }), 404

    profile_dict = dict(profile)

    # --------------------------------------------------------
    # Load cultural context based on selected region.
    # --------------------------------------------------------

    cultural_context = None

    region = profile_dict.get("region")

    if region:
        cultural_library = load_cultural_library()

        if isinstance(cultural_library, dict):
            cultural_context = cultural_library.get(
                region.lower()
            )

    # --------------------------------------------------------
    # Remove region from the personal profile sent to the AI.
    # Region is contextual information, not a personal memory.
    # --------------------------------------------------------

    personal_memory = {
        key: value
        for key, value in profile_dict.items()
        if key != "region"
    }

    # --------------------------------------------------------
    # Determine the current round.
    # The frontend already sends ?round=...
    # --------------------------------------------------------

    round_value = request.args.get("round", "")

    try:
        round_number = int(round_value) % 6
    except (TypeError, ValueError):
        round_number = 0

    variation_hints = [
        "Choose a different memory category from recent rounds when possible.",
        "Ask about a different aspect of the patient's memories when possible.",
        "Use a different memory category and make the wording fresh.",
        "Create a different short recall question from another personal memory.",
        "Prefer a different personal-memory fact than the recent questions.",
        "Use fresh wording and avoid repeating the structure of recent questions."
    ]

    variation_hint = variation_hints[round_number]

    # Make a copy so the AI never receives a reference to the
    # live Python list.
    previous_questions = list(recent_personalized_questions)

    result = generate_personalized_prompt(
        personal_memory,
        cultural_context=cultural_context,
        previous_questions=previous_questions,
        variation_hint=variation_hint
    )

    if not result.get("success"):
        return jsonify(result), 500

    question = result.get("question", "").strip()

    # --------------------------------------------------------
    # Safety net:
    # If the AI somehow returned a question that exactly
    # matches a recent question, retry once with a stronger
    # variation instruction.
    # --------------------------------------------------------

    normalized_question = " ".join(
        question.lower().split()
    )

    normalized_previous = {
        " ".join(q.lower().split())
        for q in previous_questions
    }

    if normalized_question in normalized_previous:

        stronger_hint = (
            "The generated question was repeated. "
            "You MUST create a different question now. "
            "Change the memory category if another category "
            "is available. If only one category is available, "
            "ask about a different aspect of that same memory "
            "and use clearly different wording."
        )

        retry_result = generate_personalized_prompt(
            personal_memory,
            cultural_context=cultural_context,
            previous_questions=previous_questions,
            variation_hint=stronger_hint
        )

        if retry_result.get("success"):
            result = retry_result
            question = result.get(
                "question",
                ""
            ).strip()

    # --------------------------------------------------------
    # Store the new question for future rounds.
    # Keep only the most recent five.
    # --------------------------------------------------------

    if question:
        recent_personalized_questions.append(question)

        if len(recent_personalized_questions) > 5:
            recent_personalized_questions.pop(0)

    # Add useful transparency for the frontend/demo.
    result["cultural_context_used"] = bool(cultural_context)

    if region:
        result["region"] = region

    result["round"] = round_value

    return jsonify(result)


# ============================================================
# MEMORY CIRCLE
# ============================================================


@app.route("/api/memory-circle", methods=["GET"])
def get_memory_circle():
    """
    Return all memories shared by the current patient.
    """

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": True,
            "memories": []
        })

    memories = conn.execute("""
        SELECT
            id,
            patient_id,
            memory_text,
            response_text,
            created_at,
            response_at
        FROM memory_circle
        WHERE patient_id = ?
        ORDER BY created_at DESC
    """, (patient["id"],)).fetchall()

    conn.close()

    return jsonify({
        "success": True,
        "memories": [dict(memory) for memory in memories]
    })


@app.route("/api/memory-circle", methods=["POST"])
def create_memory_circle():
    """
    Save a new memory/story shared by the patient.
    """

    data = request.get_json() or {}

    memory_text = data.get(
        "memory_text",
        ""
    ).strip()

    if not memory_text:
        return jsonify({
            "success": False,
            "message": "Memory text is required"
        }), 400

    conn = get_db_connection()

    patient = conn.execute("""
        SELECT id
        FROM patients
        ORDER BY id
        LIMIT 1
    """).fetchone()

    if patient is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "No patient found"
        }), 404

    created_at = datetime.now().isoformat()

    cursor = conn.execute("""
        INSERT INTO memory_circle (
            patient_id,
            memory_text,
            response_text,
            created_at,
            response_at
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        patient["id"],
        memory_text,
        None,
        created_at,
        None
    ))

    memory_id = cursor.lastrowid

    conn.commit()

    memory = conn.execute("""
        SELECT
            id,
            patient_id,
            memory_text,
            response_text,
            created_at,
            response_at
        FROM memory_circle
        WHERE id = ?
    """, (memory_id,)).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "message": "Memory shared successfully",
        "memory": dict(memory)
    })


@app.route(
    "/api/memory-circle/<int:memory_id>/response",
    methods=["PUT"]
)
def add_memory_response(memory_id):
    """
    Add or update a caregiver/family response
    to a patient's shared memory.
    """

    data = request.get_json() or {}

    response_text = data.get(
        "response_text",
        ""
    ).strip()

    if not response_text:
        return jsonify({
            "success": False,
            "message": "Response text is required"
        }), 400

    conn = get_db_connection()

    memory = conn.execute("""
        SELECT id
        FROM memory_circle
        WHERE id = ?
    """, (memory_id,)).fetchone()

    if memory is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "Memory not found"
        }), 404

    response_at = datetime.now().isoformat()

    conn.execute("""
        UPDATE memory_circle
        SET
            response_text = ?,
            response_at = ?
        WHERE id = ?
    """, (
        response_text,
        response_at,
        memory_id
    ))

    conn.commit()

    updated_memory = conn.execute("""
        SELECT
            id,
            patient_id,
            memory_text,
            response_text,
            created_at,
            response_at
        FROM memory_circle
        WHERE id = ?
    """, (memory_id,)).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "message": "Family response saved successfully",
        "memory": dict(updated_memory)
    })


# ============================================================
# MEMORY CIRCLE — AI CONVERSATION BRIDGE
# ============================================================


@app.route(
    "/api/memory-circle/<int:memory_id>/conversation-prompt",
    methods=["GET"]
)
def memory_circle_conversation_prompt(memory_id):
    """
    Generate one simple conversation question using:
    - the patient's shared memory
    - the family/caregiver response
    - the patient's personal memory profile

    This creates an opportunity for further human conversation.
    It does not diagnose or medically evaluate the patient.
    """

    conn = get_db_connection()

    memory = conn.execute("""
        SELECT
            id,
            patient_id,
            memory_text,
            response_text
        FROM memory_circle
        WHERE id = ?
    """, (memory_id,)).fetchone()

    if memory is None:
        conn.close()

        return jsonify({
            "success": False,
            "message": "Memory not found"
        }), 404

    if not memory["response_text"]:
        conn.close()

        return jsonify({
            "success": False,
            "message": "A family response is required before generating a conversation prompt."
        }), 400

    profile = conn.execute("""
        SELECT
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
    """, (memory["patient_id"],)).fetchone()

    conn.close()

    memory_profile = dict(profile) if profile else None

    result = generate_conversation_prompt(
        memory["memory_text"],
        memory["response_text"],
        memory_profile
    )

    if not result.get("success"):
        return jsonify(result), 500

    return jsonify(result)


# ============================================================
# START APPLICATION
# ============================================================


if __name__ == "__main__":
    init_db()

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )