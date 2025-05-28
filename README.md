# Project: SustainIQ 

### Project Overview

**SustainIQ** is a personalized sustainability tracker and goal‑setting platform built with **Flask**. The app helps users live more environmentally conscious lives by combining user‑generated eco‑goals, habit tracking, and **AI‑powered advice**.

Users can:
- Register and log in
- Ask open-ended sustainability questions to an AI assistant
- Log daily eco-friendly actions (ex. biking to work)
- Track their progress over time
- Set and manage custom sustainability goals

The dashboard presents **visual insights** like category breakdowns and weekly progress charts, making eco‑conscious living both actionable and motivating.

---

### Logged-In User Features

- Submit sustainability questions to the AI assistant
- Log eco-friendly actions for progress tracking
- Create, edit, and save personal sustainability goals
- View personalized dashboard (saved goals, recent actions, charts)
- Save AI-generated suggestions for later review

---

### Forms Used

- **RegistrationForm:** Username, email, password, confirm password
- **LoginForm:** Email and password for authentication
- **AIQuestionForm:** Textarea for open-ended AI queries
- **EcoActionForm:** Description and category dropdown (energy, waste, transport, food, water, other)
- **GoalForm:** Title, description, and optional target date

---

### Routes / Blueprints

#### auth (/auth):
- /register (GET/POST) — User signup
- /login (GET/POST) — User authentication
- /logout (GET) — End session

#### ai (/ai):
- /ask (GET/POST) — Render AI question form and submit prompt to OpenAI
- /history (GET) — List past questions and responses
- /view/<suggestion_id> (GET) — View a specific AI suggestion
- /save/<suggestion_id> (GET) — Mark a suggestion as saved

#### tracker (/tracker)
- /log-action (GET/POST) — Log a new eco‑action
- /actions-history (GET) — View full history of actions
- /set-goal (GET/POST) — Create a new sustainability goal
- /update-goal/<goal_id>/<status> (GET) — Change goal status (in progress, completed, abandoned)

#### dashboard (/dashboard)
- /home (GET) — Show the user’s dashboard with stats, charts, recent actions, active goals, and saved tips

---

### MongoDB Collections

- **users**: _id, username, email, password_hash, created_at
- **eco_actions**: user_id, action_text, category, timestamp
- **sustainability_goals**: user_id, title, description, status, created_at, target_date
- **ai_suggestions**: user_id, question, response, timestamp, saved

---

### APIs

I integrated **GROQ’s hosted endpoint** using the requests Python library to power the AI assistant, SustainIQ.

- When users submit questions, their prompts are sent to the **LLaMA 4 Scout 17B** model via a POST request.
- The model generates tailored, real-time sustainability advice.
- These responses are saved to MongoDB along with user IDs and timestamps.

This adds **interactivity, context-aware guidance, and personalized insights** beyond static web content.

