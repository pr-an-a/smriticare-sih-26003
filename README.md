# 🧠 SmritiCare

AI-powered cognitive gaming and memory assistance platform for elderly dementia patients in the North Eastern Region (SIH PS 26003).

**Live app:** *[Add deployment link]* | **Demo video:** *[Watch here]*

## Problem

The North Eastern Region (NER) is witnessing a gradual rise in age-related cognitive disorders such as dementia and memory loss. Families in remote and rural communities often face difficulties accessing specialized neurological care, cognitive therapy, and continuous elderly support because of geographical and healthcare infrastructure barriers.

For elderly people experiencing cognitive decline, memory loss, confusion, anxiety, and social isolation can significantly affect daily life. At the same time, caregivers may struggle with continuous monitoring, meaningful engagement, reminders, and understanding changes in cognitive performance.

There is a need for affordable, accessible, culturally inclusive digital support that can complement existing care — particularly for elderly communities in the North Eastern Region.

## Solution

SmritiCare is a voice-accessible cognitive engagement and memory assistance platform connecting the **elderly user, their memories, cognitive activities, and caregiver** in one system.

1. The patient completes adaptive cognitive activities targeting memory, attention, recall, and recognition.
2. SmritiCare tracks performance over time through a Personal Cognitive Engine.
3. The system identifies longitudinal patterns such as improving, declining, or stable performance and adjusts activity difficulty accordingly.
4. AI uses the patient's personal memory profile to generate meaningful reminiscence questions and evaluate responses.
5. Voice interaction allows elderly users to interact naturally through spoken commands and receive spoken responses.
6. Family members can contribute memories through the Memory Circle, creating opportunities for meaningful conversations.
7. Caregivers can monitor progress, manage reminders, maintain the patient's memory profile, and respond to shared memories through the caregiver dashboard.

## Features

* 🧠 **Four Adaptive Cognitive Activities:** Memory, Attention, Daily Recall, and Object Match with performance-based difficulty adjustment.
* 📈 **Personal Cognitive Engine:** Tracks longitudinal activity performance and identifies improving, declining, or stable trends.
* 🤖 **AI Personalization:** Uses the patient's actual life history to create personalized reminiscence questions and evaluate responses.
* 🗣️ **Voice Assistant & Intent Understanding:** Spoken commands can be used to request water, check reminders, start activities, access progress, interact with Memory Circle, and contact the caregiver.
* 🌍 **Multilingual Voice Interaction:** English, Hindi, and Assamese language support with localized speech recognition and text-to-speech.
* 💜 **Memory Circle:** Enables family members and caregivers to share memories and continue conversations with the elderly user.
* 🖼️ **Personal Memory Shelf:** Stores meaningful photos and life memories that can become part of the patient's personalized engagement experience.
* 📊 **Caregiver Dashboard:** Provides cognitive performance summaries, longitudinal trends, observations, recent activity, reminders, memory information, and caregiver interaction tools.
* ⏰ **Daily Reminders:** Supports reminders for medicines, hydration, meals, appointments, and other daily activities.
* 🔔 **Caregiver Assistance:** Provides a mechanism for the patient to request caregiver attention through the voice interface.
* 📱 **Elderly-Friendly Interface:** Designed around large interactive elements, simple navigation, readable layouts, and voice-assisted interaction.

## Tech Stack

* **Backend:** Python, Flask, SQLite
* **AI & NLP:** Groq API with Qwen model for personalization, answer evaluation, and voice intent processing
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Visualization:** Chart.js
* **Accessibility:** Web Speech API (`SpeechRecognition` and `SpeechSynthesis`)
* **Storage:** SQLite database with local file storage for memory-gallery images
* **PWA Support:** Service-worker based application caching shell

## Project Structure

```text
smriticare/
├── app.py                       # Flask application, routes, APIs & database setup
├── ai_helper.py                 # Groq AI integration and language/voice processing
├── cognitive_engine.py          # Longitudinal performance analysis & adaptive difficulty
├── requirements.txt             # Python dependencies
├── cultural_data/
│   └── ner_memory_library.json  # Regional cultural context data
├── uploads/
│   └── memories/                # Uploaded patient memory photographs
├── templates/
│   ├── index.html               # Patient home, reminders, Memory Circle & voice assistant
│   ├── dashboard.html           # Patient progress & Personal Cognitive Journey
│   ├── caregiver-dashboard.html # Caregiver analytics & memory management
│   ├── memory-game.html         # Adaptive memory activity
│   ├── attention-game.html      # Attention and focus activity
│   ├── recall-game.html         # Daily and personal recall activity
│   └── object-match.html        # Everyday object recognition activity
└── static/
    ├── css/
    │   └── style.css            # Global styling
    └── js/
        └── service-worker.js     # PWA caching shell
```

## Installation (Local)

```bash
git clone https://github.com/pr-an-a/smriticare.git
cd smriticare
python -m venv venv
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

pip install -r requirements.txt

echo "GROQ_API_KEY=your_key_here" > .env

python app.py
```

Visit:

```text
http://127.0.0.1:5000
```

## Environment Variables

| Variable       | Description                                                                                                     |
| -------------- | --------------------------------------------------------------------------------------------------------------- |
| `GROQ_API_KEY` | API key used for AI personalization, reminiscence processing, answer evaluation, and voice intent understanding |

## How It Works

```text
             ┌─────────────────────┐
             │    Elderly User     │
             └──────────┬──────────┘
                        │
              Voice / Touch / Games
                        │
                        ▼
             ┌─────────────────────┐
             │     SmritiCare      │
             │                     │
             │ Cognitive Activities│
             │ Memory Assistance   │
             │ Voice Interaction   │
             │ Reminders           │
             └──────────┬──────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│ Personal Cognitive  │     │   Personal Memory   │
│      Engine         │     │       Profile       │
│                     │     │                     │
│ Performance trends  │     │ Photos & memories   │
│ Difficulty scaling  │     │ AI reminiscence     │
└──────────┬──────────┘     └──────────┬──────────┘
           │                           │
           └─────────────┬─────────────┘
                         ▼
              ┌─────────────────────┐
              │ Caregiver Dashboard │
              │                     │
              │ Progress            │
              │ Reminders           │
              │ Memories            │
              │ Memory Circle       │
              └─────────────────────┘
```

## Personalization

SmritiCare is designed around the idea that cognitive engagement should become **more personal over time**.

The platform combines:

* Longitudinal cognitive-performance data
* Recent activity results
* Adaptive difficulty
* Patient-specific memory information
* Personalized reminiscence questions
* Voice interaction
* Caregiver observations
* Family-shared memories

This allows the platform to move beyond generic cognitive games toward a more **person-centered engagement loop**.

## North Eastern Region Focus

SmritiCare incorporates a cultural-context layer intended to support more familiar and meaningful cognitive engagement for elderly users in the North Eastern Region.

The current prototype includes:

* Assamese language support
* Regional cultural context data
* Personalized memory content
* Familiar everyday objects and situations
* Voice-assisted interaction suitable for users who may find conventional interfaces difficult

The current implementation is a prototype foundation; deeper regional personalization and dialect-specific support remain areas for future development.

## Future Improvements

* Offline-first operation with local AI/model fallback for low-connectivity environments
* Advanced regional dialect and speech-recognition tuning for remote NER communities
* Secure authentication and encrypted multi-user data isolation
* Native mobile/tablet application
* Healthcare-worker integration
* More advanced cognitive-performance analytics
* Wearable integration for additional safety and health signals
* Larger culturally curated NER memory and activity libraries

## Medical Disclaimer

SmritiCare is designed as a **supportive cognitive engagement, memory assistance, and caregiver-support platform**.

It is **not a medical diagnostic tool**, does not diagnose dementia or other neurological conditions, and should not replace professional medical evaluation, neurological assessment, or prescribed treatment.

## Acknowledgements

Built using the **Groq API** for fast language-model inference and the **Web Speech API** for accessible voice interaction.

Developed as a prototype for **Smart India Hackathon 2026 — Problem Statement 26003**.

---

**SmritiCare — Personalize. Engage. Remember. Connect. Adapt.**
