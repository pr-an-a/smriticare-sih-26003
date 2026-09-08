# SIH 2026 — CareConnect / SmritiCare

## PROJECT CONTEXT

This file is the project's continuity document.

Update it at meaningful milestones so development can resume easily in a new ChatGPT conversation.

---

# 1. PROJECT OVERVIEW

## SIH Problem Statement

**SIH 26003**

AI-powered cognitive gaming and memory assistance platform for elderly dementia patients in the North Eastern Region.

## Project Name

**CareConnect**

## Patient-facing Product Name

**SmritiCare**

## Project Goal

Build an elderly-friendly prototype that provides:

* Cognitive games
* Adaptive difficulty
* Memory assistance
* Daily routine reminders
* Voice interaction
* Multilingual/regional-language interaction
* Patient progress tracking
* Caregiver monitoring
* Longitudinal activity history
* Culturally familiar interactions
* Personal-memory-based cognitive personalization
* Family/caregiver memory interaction
* AI-assisted conversation prompts
* Future low-connectivity/offline support

The platform is a **prototype** and is **not a clinically validated diagnostic tool**.

---

# 2. USER DEVELOPMENT PREFERENCE

The user is a beginner and does not code independently.

Development should follow a **vibe-coding workflow**.

For every coding milestone:

1. Explain what we are building.
2. Give the exact file to open.
3. Give the complete replacement file/code whenever a file must be modified.
4. Tell the user exactly where to paste it.
5. Give the exact terminal command.
6. Tell the user what result to expect.
7. Test the feature.
8. Wait for the user to confirm it works.
9. Update this context at meaningful milestones.
10. Only then move to the next feature.

## Important coding preference

When modifying a file:

**Always provide the COMPLETE updated file.**

Do not give instructions such as:

* "add these lines"
* "replace this function"
* "insert this snippet"

The user prefers one complete selectable code block.

---

# 3. DEVELOPMENT ENVIRONMENT

## Hardware

MacBook Air M3

## Operating System

macOS

## Editor

VS Code

## Python

Python 3.14.2

## Backend

Python + Flask

## Database

SQLite

## Frontend

HTML + CSS + JavaScript

## Charts

Chart.js

## AI

Groq API with Qwen 3.6 27B

## Voice

* Browser Web Speech API
* Local eSpeak NG for Assamese

## Version Control

Git installed.

---

# 4. PROJECT LOCATION

```text
/Users/pranathividiyala/Desktop/Coding/sih-26003
```

---

# 5. CURRENT PROJECT STRUCTURE

```text
sih-26003/

├── PROJECT_CONTEXT.md
├── app.py
├── ai_helper.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── careconnect.db
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── result.html
│   ├── memory-game.html
│   ├── attention-game.html
│   ├── recall-game.html
│   ├── object-match.html
│   └── caregiver-dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   ├── espeak/
│   └── images/
│
├── uploads/
└── venv/
```

---

# 6. COMPLETED MILESTONES

## Milestone 1 — Initial Project Setup

**Status: DONE**

Flask application, templates, static files, environment and SQLite database foundation established.

---

## Milestone 2 — Patient Home Screen

**Status: DONE**

Patient-facing SmritiCare home screen created.

Includes:

* Namaste greeting
* Medicine reminder area
* Cognitive activity cards
* Quick help
* Voice assistant
* Navigation

---

## Milestone 3 — Voice Assistant Foundation

**Status: DONE AND TESTED**

Voice interaction and navigation commands implemented.

Supported concepts include:

* Greeting
* Help
* Memory activity
* Attention activity
* Daily Recall
* Object Match
* Dashboard
* Caregiver Dashboard
* Drink Water / Water reminder
* Other navigation commands

Voice assistant was tested successfully.

---

## Milestone 4 — SQLite Database

**Status: DONE**

SQLite database created:

```text
careconnect.db
```

Patient and cognitive-result storage implemented.

---

## Milestone 5 — Patient-Specific Cognitive Results

**Status: DONE**

Cognitive activity results are associated with the current patient.

---

## Milestone 6 — Memory Game

**Status: DONE AND TESTED**

Memory activity implemented.

---

## Milestone 7 — Adaptive Memory

**Status: DONE AND TESTED**

Memory difficulty adapts according to previous performance.

---

## Milestone 8 — Attention Activity

**Status: DONE AND TESTED**

Attention/focus activity implemented.

---

## Milestone 9 — Adaptive Attention

**Status: DONE AND TESTED**

Attention difficulty adapts according to previous performance.

---

## Milestone 10 — Patient Longitudinal Dashboard

**Status: DONE**

Patient dashboard shows cognitive performance over time.

---

## Milestone 11 — Daily Recall Activity

**Status: DONE AND TESTED**

Daily Recall activity implemented.

---

## Milestone 12 — Adaptive Daily Recall

**Status: DONE AND TESTED**

Daily Recall difficulty adapts based on previous performance.

---

## Milestone 13 — Object Match Activity

**Status: DONE AND TESTED**

Object Match activity implemented.

---

## Milestone 14 — Adaptive Object Match

**Status: DONE AND TESTED**

Object Match difficulty adapts according to previous performance.

---

## Milestone 15 — Patient Dashboard with Four Activities

**Status: DONE AND TESTED**

Patient dashboard supports:

* Memory
* Attention
* Daily Recall
* Object Match

---

## Milestone 16 — Caregiver Dashboard

**Status: DONE AND TESTED**

Caregiver dashboard implemented.

Currently includes:

* Patient name
* Patient age
* Total sessions
* Recent average
* Improvement
* Consistency
* Memory performance
* Attention performance
* Daily Recall performance
* Object Match performance
* Cognitive performance trend chart
* Performance observations
* Areas to practice
* Progress summary
* Recent sessions
* Daily reminder manager
* Personal Memory Profile
* Memory Circle
* AI Conversation Bridge
* Non-diagnostic safety note

---

## Milestone 17 — Reminder Backend

**Status: DONE**

SQLite reminder system implemented.

Table:

```text
reminders
```

Fields:

```text
id
patient_id
title
category
reminder_time
notes
completed
created_at
```

APIs:

```text
GET    /api/reminders
POST   /api/reminders
PUT    /api/reminders/<id>/complete
DELETE /api/reminders/<id>
```

Note:

The current reminder model behaves as a prototype reminder system. It does not yet contain explicit recurrence/date fields.

---

## Milestone 18 — Caregiver Reminder Manager UI

**Status: DONE AND TESTED**

Caregiver can:

* Create reminders
* Enter reminder title
* Select category
* Set time
* Add optional notes
* View reminders
* Mark reminders completed
* Delete reminders

Supported categories:

* Medicine 💊
* Water 💧
* Meal 🍲
* Appointment 📅
* Activity 🌸
* Other 🔔

Tested successfully:

```text
Add Reminder
      ↓
Reminder appears
      ↓
Mark Done
      ↓
Delete Reminder
```

---

## Milestone 19 — Patient-side Daily Reminders

**Status: DONE AND TESTED**

SmritiCare retrieves reminders using:

```text
GET /api/reminders
```

Reminders appear under:

```text
Today's Reminders ⏰
```

Each reminder can display:

* Category icon
* Reminder title
* Time
* Optional notes
* Completion state

Patient can press Done.

Completion uses:

```text
PUT /api/reminders/<id>/complete
```

After completion:

* Reminder changes to completed state
* Check mark appears
* Confirmation message is shown
* Voice confirmation is spoken
* Completion is saved through the backend

The complete caregiver-to-patient reminder flow was tested successfully.

---

## Milestone 20 — Voice Reminder Integration

**Status: DONE AND TESTED**

The voice assistant was connected to the reminder system.

The patient can ask for reminders using natural commands such as:

```text
"What are my reminders?"
"Show my reminders."
"What do I need to do today?"
```

SmritiCare retrieves current reminders from:

```text
/api/reminders
```

and reads them aloud using the existing voice system.

The existing voice navigation commands were preserved.

---

## Milestone 21 — Multilingual Voice Assistant

**Status: DONE**

Multilingual/regional voice interaction was implemented sufficiently for the prototype/demo.

Assamese local voice output is supported using:

```text
static/espeak/
```

and local eSpeak NG.

The system avoids depending entirely on cloud TTS for regional-language playback.

---

## Milestone 22 — Offline Mode

**Status: PARTIALLY IMPLEMENTED / NOT DEMO-READY**

Offline/low-connectivity support has been explored but is not currently considered reliable enough for the main demo.

Do not spend significant time on this until the core product story is complete.

Future goal:

* Core cognitive activities should remain usable without internet.
* Locally available functionality should continue during connectivity loss.
* Data should eventually synchronize when connectivity returns.

---

## Milestone 23 — Personal Memory Profile Backend

**Status: DONE**

SQLite table:

```text
memory_profiles
```

Stores:

* Favorite foods
* Favorite places
* Favorite festivals
* Important people
* Favorite songs
* Hobbies
* Childhood memories
* Meaningful objects

The profile is associated with the patient.

---

## Milestone 24 — Personal Memory Profile Caregiver UI

**Status: DONE AND TESTED**

Caregiver can enter meaningful information about the patient.

The information is stored in SQLite and becomes available to the personalization engine.

---

## Milestone 25 — AI Personalization Engine

**Status: DONE AND TESTED**

The Personal Memory Profile was connected to an AI personalization engine.

Backend endpoint:

```text
GET /api/personalized-prompt
```

The endpoint:

1. Retrieves the current patient.
2. Retrieves the patient's memory profile.
3. Sends available personal memories to Groq.
4. Requests one simple personal-memory question.
5. Requires the question to use an actual fact from the profile.
6. Returns:

```text
question
answer
memory_source
```

Current model:

```text
qwen/qwen3.6-27b
```

The implementation uses:

* Groq API
* JSON response format
* `reasoning_effort="none"`
* Python JSON parsing
* python-dotenv

The actual:

```text
GROQ_API_KEY
```

remains in `.env`.

**Never commit the API key to GitHub.**

---

## Milestone 26 — Personalized Recall Integration

**Status: DONE AND TESTED**

The existing Recall activity was enhanced with personalized recall.

Flow:

```text
Personal Memory Profile
        ↓
AI Personalization Engine
        ↓
Personalized Recall Question
        ↓
Patient Answers
        ↓
Answer Evaluation
        ↓
Existing Result Saving
        ↓
Adaptive Difficulty Preserved
```

The system normalizes answers by ignoring:

* Capitalization
* Punctuation
* Extra spaces

The result is saved using:

```text
/api/save-result
```

### Important fallback behavior

AI personalization must never become a single point of failure.

If:

* Memory Profile does not exist
* Profile has no usable memories
* Groq API fails
* Internet connection fails
* AI returns invalid data

the existing normal Recall activity continues.

Normal Recall still supports:

* Easy
* Medium
* Hard
* Story-based recall
* Multiple-choice questions
* Accuracy scoring
* Response-time measurement
* Adaptive difficulty
* SQLite result saving

---

## Milestone 27 — Memory Circle Patient UI + Backend

**Status: DONE AND TESTED**

Memory Circle was introduced as a social/reminiscence feature.

Patient flow:

```text
Patient opens SmritiCare
        ↓
Opens Memory Circle
        ↓
Writes a meaningful memory
        ↓
Clicks Share Memory
        ↓
Memory saved to SQLite
```

The patient-facing Memory Circle card is expandable.

Patient can enter a personal memory/story.

Backend table:

```text
memory_circle
```

Fields:

```text
id
patient_id
memory_text
response_text
created_at
response_at
```

APIs:

```text
GET  /api/memory-circle
POST /api/memory-circle
PUT  /api/memory-circle/<id>/response
```

---

## Milestone 28 — Memory Circle Caregiver UI

**Status: DONE AND TESTED**

Caregiver dashboard allows caregivers/family members to:

* View patient memories
* Read the original memory
* See date/time
* Enter a family response
* Submit the response
* View the saved family response

End-to-end flow:

```text
PATIENT
  ↓
Shares memory
  ↓
SQLite
  ↓
CAREGIVER DASHBOARD
  ↓
Family responds
  ↓
SQLite
```

The feature is intentionally simple.

It is not a social network or real-time messaging platform.

---

## Milestone 29 — AI Conversation Bridge

**Status: DONE AND TESTED**

The AI Conversation Bridge connects Memory Circle with the existing AI personalization architecture.

### Purpose

Turn a patient's shared memory and the family response into a simple conversation starter.

Flow:

```text
Patient shares personal memory
        ↓
Family/caregiver responds
        ↓
AI receives:
    - patient memory
    - family response
    - personal memory profile
        ↓
AI generates a gentle conversation question
        ↓
Caregiver can view/read it aloud
        ↓
Patient and family have an opportunity
for further conversation
```

Backend endpoint:

```text
GET /api/memory-circle/<memory_id>/conversation-prompt
```

The backend uses:

```text
generate_conversation_prompt()
```

from:

```text
ai_helper.py
```

The AI returns:

```text
question
conversation_source
```

The caregiver frontend reads:

```text
data.question
```

### Important integration bug that was fixed

The frontend originally expected:

```text
data.prompt
```

while the backend returned:

```text
data.question
```

The frontend was corrected to use:

```text
data.question
```

### Testing

The feature was successfully tested after fixing a saved-file issue.

The Flask route was verified to be registered correctly.

The working flow is:

```text
Memory Circle
      ↓
Family Response
      ↓
Generate Conversation Prompt
      ↓
AI-generated question
      ↓
Read Aloud
```

---

# 7. CURRENT API ARCHITECTURE

## Patient

```text
GET /api/patient
PUT /api/patient
```

## Cognitive Results

```text
POST /api/save-result
GET  /api/cognitive-history
```

## Reminders

```text
GET    /api/reminders
POST   /api/reminders
PUT    /api/reminders/<id>/complete
DELETE /api/reminders/<id>
```

## Personal Memory Profile

```text
GET /api/memory-profile
PUT /api/memory-profile
```

## AI Personalization

```text
GET /api/personalized-prompt
```

## Memory Circle

```text
GET  /api/memory-circle
POST /api/memory-circle
PUT  /api/memory-circle/<id>/response
```

## AI Conversation Bridge

```text
GET /api/memory-circle/<memory_id>/conversation-prompt
```

---

# 8. CURRENT COGNITIVE ACTIVITIES

## Memory

Route:

```text
/memory-game
```

Purpose:

Remembering familiar objects.

Adaptive difficulty:

**YES**

---

## Attention

Route:

```text
/attention-game
```

Purpose:

Focused attention and target matching.

Adaptive difficulty:

**YES**

---

## Daily Recall

Route:

```text
/recall-game
```

Purpose:

Remembering details from short everyday stories.

Adaptive difficulty:

**YES**

Personalized mode:

**YES**

---

## Object Match

Route:

```text
/object-match
```

Purpose:

Recognizing and matching familiar everyday objects.

Adaptive difficulty:

**YES**

---

# 9. CURRENT DASHBOARDS

## Patient Dashboard

Route:

```text
/dashboard
```

Shows cognitive performance history.

---

## Caregiver Dashboard

Route:

```text
/caregiver-dashboard
```

Shows:

* Patient information
* Overall cognitive activity metrics
* Four activity performance cards
* Performance trend
* Observations
* Areas to practice
* Progress summary
* Recent sessions
* Daily reminders
* Personal Memory Profile
* Memory Circle
* Family responses
* AI Conversation Bridge

---

# 10. CURRENT REMINDER ARCHITECTURE

```text
CAREGIVER
    │
    │ creates reminder
    ▼
SQLite reminders table
    │
    │ GET /api/reminders
    ▼
SMRITICARE PATIENT HOME
    │
    │ displays reminder
    ▼
PATIENT
    │
    │ presses Done
    ▼
PUT /api/reminders/<id>/complete
    │
    ▼
SQLite updated
```

This is a working prototype.

---

# 11. CURRENT PERSONALIZATION ARCHITECTURE

The project now has two different forms of personalization.

## A. Adaptive Difficulty

Answers:

> "How difficult should the next activity be?"

The system uses previous activity performance.

```text
Past performance
      ↓
Difficulty adjustment
      ↓
Next activity
```

## B. Personal Memory Personalization

Answers:

> "What content is meaningful and familiar to this particular person?"

```text
Patient's personal memories
      ↓
AI understands memory context
      ↓
Personalized cognitive prompt
      ↓
Patient engages with familiar content
```

These are different concepts and should both be highlighted during the SIH presentation.

---

# 12. CURRENT PRODUCT PHILOSOPHY

The project's strongest product principle is:

> **AI should be a bridge to human interaction, not a replacement for it.**

The system should not primarily behave like an AI companion that replaces family interaction.

Instead, AI should:

* Personalize cognitive activities
* Use meaningful patient memories
* Help create familiar engagement
* Connect patient memories with family responses
* Generate conversation starters
* Encourage opportunities for human conversation

The goal is to make technology feel more personal while keeping family/caregiver interaction at the center.

---

# 13. CURRENT CORE PRODUCT STORY

The strongest current product flow is:

```text
PERSONAL MEMORY PROFILE
        ↓
AI PERSONALIZATION
        ↓
FAMILIAR COGNITIVE ACTIVITY
        ↓
ADAPTIVE DIFFICULTY
        ↓
PATIENT ENGAGEMENT
        ↓
MEMORY CIRCLE
        ↓
FAMILY RESPONSE
        ↓
AI CONVERSATION BRIDGE
        ↓
CONVERSATION OPPORTUNITY
```

This should be presented as one connected system rather than as a collection of unrelated features.

---

# 14. MAIN DIFFERENTIATOR

The project should NOT be positioned simply as:

> "An AI-powered dementia app with games."

That description is too generic.

The stronger positioning is:

> **SmritiCare personalizes cognitive engagement around what is familiar and meaningful to each elderly person, rather than only changing difficulty levels.**

The system combines:

```text
Personal familiarity
        +
Adaptive difficulty
        +
Cognitive activities
        +
Family interaction
        +
AI conversation support
```

The distinction is:

```text
Traditional adaptive system:
"How hard should the next activity be?"

SmritiCare:
"How hard should it be?"
+
"What content is meaningful to this person?"
+
"How can that memory become an opportunity for family interaction?"
```

---

# 15. MEMORY-TO-MEANING LOOP

The current product direction is called the:

**Memory-to-Meaning Loop**

```text
Caregiver records meaningful memories
        ↓
SmritiCare builds a personal memory profile
        ↓
AI creates familiar cognitive engagement
        ↓
Patient interacts with the activity
        ↓
Patient shares a real memory/story
        ↓
Family responds
        ↓
AI creates a gentle conversation starter
        ↓
Patient + family continue the conversation
```

This is the central innovation direction.

---

# 16. NER / CULTURAL PERSONALIZATION DIRECTION

The project must specifically address the North Eastern Region requirement without inventing a huge database of fake cultural information.

The planned approach is a small curated **NER Familiarity Layer**.

Potential categories:

* Food
* Festivals
* Traditions
* Places
* Music
* Sounds
* Household objects
* Regional everyday life
* Languages

The purpose is not to claim exhaustive cultural coverage.

The purpose is to allow cognitive activities to use **familiar regional themes** where appropriate.

The important principle is:

> **Cultural familiarity should improve the relevance of the activity, not merely decorate the interface.**

The same activity should eventually be able to use:

```text
Generic content
        ↓
Regionally familiar content
        ↓
Personally familiar content
```

This creates a second personalization dimension beyond difficulty.

---

# 17. NER PERSONALIZATION — PLANNED ARCHITECTURE

The intended architecture is:

```text
Personal Memory Profile
        +
Regional Familiarity
        +
Past Performance
        ↓
Personalized Cognitive Engagement
```

Where:

### Past Performance

Controls:

```text
difficulty
```

### Personal Memory

Controls:

```text
meaningful/familiar content
```

### Regional Familiarity

Controls:

```text
cultural relevance
```

This distinction should be preserved in the final system.

---

# 18. WHAT NOT TO BUILD

To avoid feature creep, do NOT add random AI features such as:

* Generic chatbot
* AI therapist
* Emotion detection
* Face recognition
* Disease prediction
* Dementia diagnosis
* Medical cognitive scoring
* Blockchain
* 3D games
* AI summaries with no product purpose
* Another dashboard
* Large social-network functionality
* Unnecessary sensors

The project already has sufficient functionality.

New features must strengthen the central product story.

---

# 19. OFFLINE / LOW-CONNECTIVITY STRATEGY

Offline support is currently incomplete.

Do not allow offline mode to consume excessive development time before the main demo story is stable.

The eventual target is:

```text
Internet available
       ↓
Full AI + synchronization

Internet unavailable
       ↓
Core games/reminders/local functionality continue
       ↓
Data stored locally

Internet restored
       ↓
Data synchronization
```

For the current prototype, do not claim fully functional offline synchronization unless it has been properly implemented and tested.

---

# 20. AI SAFETY / PRODUCT CLAIMS

The project should be described as:

* Cognitive engagement
* Activity assistance
* Memory assistance
* Caregiver support
* Performance tracking
* Routine/reminder support
* Family interaction support
* Personalized engagement

Avoid claiming that the prototype:

* Diagnoses dementia
* Detects dementia
* Measures medical cognitive decline
* Replaces doctors
* Replaces caregivers
* Clinically validates memory improvement
* Treats dementia
* Treats loneliness
* Provides medical diagnosis
* Provides medical treatment

Correct positioning:

> **"SmritiCare is an AI-enabled cognitive engagement and memory assistance prototype. It is not a clinically validated diagnostic or treatment system."**

Caregiver dashboard language should remain cautious:

> These results show activity performance and engagement over time. They are intended to help caregivers notice changes and support regular cognitive activities. They are not a medical diagnosis and should not replace professional medical evaluation.

---

# 21. CURRENT IMPLEMENTATION LIMITATIONS

## Reminder recurrence

The current reminder table does not have explicit recurrence/date fields.

Therefore the prototype should not claim a fully featured recurring reminder scheduler.

---

## Offline mode

Partially implemented but not demo-ready.

---

## Memory Circle responses

Caregivers can respond to memories.

Already-responded memories do not currently have a dedicated "Edit Response" interface.

This is acceptable for the current MVP and should not be prioritized unless there is significant extra time.

---

## AI dependency

AI personalization depends on Groq when generating personalized prompts.

Fallback behavior exists for Personalized Recall.

AI failure should not prevent the core cognitive activities from functioning.

---

# 22. CURRENT PROJECT STATUS

## Core cognitive system

✅ COMPLETE

## Adaptive cognitive activities

✅ COMPLETE

## Patient dashboard

✅ COMPLETE

## Caregiver dashboard

✅ COMPLETE

## Reminder backend

✅ COMPLETE

## Caregiver reminder manager

✅ COMPLETE

## Patient reminder display

✅ COMPLETE

## Patient reminder completion

✅ COMPLETE

## Voice reminder integration

✅ COMPLETE

## Multilingual/regional voice support

✅ COMPLETE FOR CURRENT PROTOTYPE

## Personal Memory Profile

✅ COMPLETE

## AI Personalization Engine

✅ COMPLETE

## Personalized Recall

✅ COMPLETE

## Memory Circle patient experience

✅ COMPLETE

## Memory Circle caregiver experience

✅ COMPLETE

## AI Conversation Bridge

✅ COMPLETE AND TESTED

## Offline mode

🟡 PARTIALLY IMPLEMENTED / NOT DEMO-READY

## NER Familiarity Layer

🔜 NEXT PRIORITY

## Final UI/UX polish

🔜 LATER

## Final testing

🔜 LATER

## SIH demo preparation

🔜 LATER

## Presentation/PPT

🔜 LATER

---

# 23. CURRENT WORKING TECHNICAL ARCHITECTURE

```text
                    SMRITICARE
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 Cognitive Games    Reminders      Memory Circle
        │               │                │
        ▼               ▼                ▼
 Performance        SQLite          Family Response
        │                                │
        ▼                                ▼
 Adaptive Engine                  AI Conversation Bridge
        │                                │
        └───────────────┬────────────────┘
                        ▼
              Personal Memory Profile
                        │
                        ▼
                AI Personalization
                        │
                        ▼
             Personalized Engagement
```

---

# 24. MAIN AI FUNCTIONS

Implemented in:

```text
ai_helper.py
```

## Personalization

```text
generate_personalized_prompt(memory_profile)
```

Purpose:

Generate a simple personal-memory cognitive question using an actual fact from the patient's memory profile.

---

## Conversation Bridge

```text
generate_conversation_prompt(
    memory_text,
    caregiver_response,
    memory_profile
)
```

Purpose:

Generate a simple conversation question based primarily on:

* Patient's shared memory
* Family response

and optionally:

* Personal Memory Profile

The AI must not invent personal information.

---

# 25. CURRENT AI MODEL

```text
qwen/qwen3.6-27b
```

Provider:

```text
Groq
```

API key:

```text
GROQ_API_KEY
```

stored only in:

```text
.env
```

Never expose or commit the actual key.

---

# 26. DEMO STORY DIRECTION

The final demo should NOT simply consist of clicking through every feature.

It should tell one coherent story.

Recommended narrative:

```text
1. Introduce an elderly user.

2. Caregiver creates a Personal Memory Profile.

3. Show a personalized cognitive activity.

4. Demonstrate that the system uses familiar content.

5. Show adaptive difficulty.

6. Show a caregiver viewing performance.

7. Show a reminder.

8. Demonstrate voice interaction.

9. Patient shares a meaningful memory.

10. Family responds.

11. AI Conversation Bridge generates a conversation starter.

12. Explain that AI is being used to strengthen
    human interaction rather than replace it.
```

The Memory-to-Meaning loop should be the centerpiece of the demo.

---

# 27. PRESENTATION POSITIONING

Avoid presenting the project as:

> Games + AI + Voice + Reminders + Dashboard.

Instead present it as:

> **A personalized cognitive engagement platform that learns what is familiar and meaningful to each elderly person and uses that context to make activities and family interaction more relevant.**

Key explanation:

> Adaptive difficulty answers **how challenging** an activity should be.

> Personal memory personalization answers **what content is meaningful and familiar**.

> Memory Circle + AI Conversation Bridge answers **how technology can turn those memories into opportunities for family conversation**.

---

# 28. CORE PITCH

Recommended central pitch:

> **"SmritiCare doesn't use AI simply to replace human interaction. It uses AI to personalize cognitive activities around each person's memories and generate meaningful conversation prompts from those memories, so technology becomes a bridge between the elderly person and their family rather than another source of isolation."**

Alternative short pitch:

> **"We don't just adapt the difficulty. We adapt the experience to the person."**

---

# 29. DEVELOPMENT RULES

## Rule 1

Do not unnecessarily rewrite working components.

## Rule 2

When adding a feature, preserve existing functionality.

## Rule 3

Test every milestone before moving forward.

## Rule 4

Use complete file replacements when modifying files.

## Rule 5

Keep the prototype simple enough to demo reliably.

## Rule 6

Do not prioritize visual perfection before core functionality is complete.

## Rule 7

Perform a dedicated UI/UX polish phase near the end.

## Rule 8

Do not add a feature merely because it sounds "AI-powered."

Every AI feature must have a clear user/product purpose.

## Rule 9

Do not make medical or clinical claims.

## Rule 10

Avoid feature creep.

A new feature should strengthen the Memory-to-Meaning / personalized-engagement story.

---

# 30. TESTING RULE

After every major feature:

```text
Build
  ↓
Run Flask
  ↓
Open feature
  ↓
Test manually
  ↓
Fix errors
  ↓
User confirms "works"
  ↓
Update PROJECT_CONTEXT.md
  ↓
Next milestone
```

---

# 31. LAST VERIFIED MILESTONE

**Milestone 29 — AI Conversation Bridge**

Status:

**DONE AND TESTED**

Verified flow:

```text
Patient shares memory                 ✅
        ↓
Caregiver sees memory                 ✅
        ↓
Caregiver adds family response        ✅
        ↓
AI Conversation Bridge appears       ✅
        ↓
Generate Conversation Prompt          ✅
        ↓
Backend generates AI question        ✅
        ↓
Question displayed                    ✅
        ↓
Read Aloud                            ✅
```

Important frontend/backend integration issue fixed:

```text
Frontend originally:
data.prompt

Backend:
data.question

Fixed frontend:
data.question
```

The Flask route was also confirmed to be saved and registered correctly.

---

# 32. NEXT DEVELOPMENT MILESTONE

## Milestone 30 — NER Familiarity Layer

**Status: NEXT PRIORITY**

### Goal

Strengthen the project's North Eastern Region specificity and make cultural familiarity a real part of personalization rather than a superficial UI element.

### Planned concept

Create a small curated regional familiarity dataset covering categories such as:

```text
Food
Festivals
Traditions
Places
Music
Objects
Everyday life
Languages
```

The dataset should be:

* Small
* Reliable
* Curated
* Easy to demo
* Easy to extend
* Clearly connected to cognitive activities

### Important constraint

Do not attempt to create an enormous cultural knowledge base.

The prototype only needs enough carefully selected content to demonstrate the concept convincingly.

### Intended personalization model

```text
Past Performance
       ↓
Difficulty

Personal Memory
       ↓
Personal Familiarity

Regional Familiarity
       ↓
Cultural Relevance
```

Together:

```text
Past Performance
+
Personal Memory
+
Regional Familiarity
        ↓
Personalized Cognitive Engagement
```

---

# 33. NEXT IMPLEMENTATION TARGET

The NER layer should eventually be connected to **one existing cognitive activity first**.

Do not modify all four games simultaneously.

Recommended first target:

**Recall**

Reason:

Recall already supports:

* Adaptive difficulty
* Personal Memory Profile
* AI personalization

Therefore it is the safest place to demonstrate the additional regional-familiarity dimension.

Potential future flow:

```text
Caregiver Profile
        ↓
Region/Familiarity Selection
        ↓
Personal Memory + NER Familiarity
        ↓
AI Personalized Recall
        ↓
Patient answers
        ↓
Result saved
        ↓
Adaptive difficulty preserved
```

Only after this works should other games be considered.

---

# 34. WHAT TO DO BEFORE ADDING MORE FEATURES

Before major new coding:

1. Keep current working system stable.
2. Update this context after meaningful milestones.
3. Strengthen the NER story.
4. Implement the smallest useful NER dataset.
5. Connect it to one existing activity.
6. Test it.
7. Evaluate the demo value.
8. Only then consider further expansion.

Do not start another unrelated feature.

---

# 35. CURRENT PROJECT PHILOSOPHY

Build functionality first.

Then strengthen the product story.

Then polish the UI.

The current priority order is:

```text
Reliable functionality
        ↓
Meaningful personalization
        ↓
NER/cultural relevance
        ↓
Complete integration
        ↓
Testing
        ↓
UI/UX polish
        ↓
Demo story
        ↓
Presentation
```

The project should feel like **one coherent product**, not a collection of disconnected features.

---

# FINAL CURRENT STATUS

**CareConnect / SmritiCare is now a substantial working prototype.**

The major cognitive, adaptive, reminder, voice, dashboard, personal-memory, family-interaction and AI-personalization foundations are implemented.

The main remaining product-development priority is **not simply adding more features**.

It is to make the existing system more distinctive through:

**Personal familiarity + Regional familiarity + Adaptive difficulty + Human interaction**

with the central idea:

> **Personalize the meaning, not just the difficulty.**
