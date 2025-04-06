# ♟️ Chess with Gemini AI

This project is an interactive chess game where **two AI agents** play against each other using **Google's Gemini AI**. Built with **Python**, **Streamlit**, and **python-chess**, this app runs directly in your browser — and the **moves are printed live in the VS Code terminal** during execution for full traceability.

---

## 🚀 Features

- 🤖 Two AI agents play a chess game against each other
- 🔐 Gemini AI integration with secure API key handling
- ♟️ Plays AI vs AI chess using UCI notation
- 🖥️ All moves are displayed in the VS Code terminal
- 📜 Real-time SVG board rendering in Streamlit
- 🕹️ Adjustable max turns for short or extended matches
- 💬 Debug prints for every move with full board state

---

## 🛠️ Tech Stack

- [Python 3.x](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [python-chess](https://pypi.org/project/python-chess/)
- [Google Generative AI SDK](https://github.com/google/generative-ai-python)

---

## 🧪 Demo

![chess preview](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/ChessBoard.svg/1200px-ChessBoard.svg.png)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chess-gemini-ai.git
cd chess-gemini-ai

#2. Create a Virtual Environment

python -m venv .venv
# On Windows
.\.venv\Scripts\activate
# On Mac/Linux
source .venv/bin/activate


#3. Install Dependencies
pip install -r requirements.txt

#4. Add Your Gemini API Key
Option 1: Directly enter the key in the Streamlit sidebar

Option 2: Use a .env file (optional)

GEMINI_API_KEY=your_gemini_api_key_here

#5. Run the Streamlit App

streamlit run chess_gemini.py

#📦 Requirements

streamlit
python-chess
google-generativeai

#📁 How to Organize All Files

chess-gemini-ai/
│
├── chess_gemini.py         # Your main Streamlit app
├── README.md               # This file (project documentation)
├── requirements.txt        # Required Python libraries
├── .gitignore              # Files to ignore in GitHub
├── .env                    # (Optional) API Key - NOT uploaded to GitHub


#✅ Example .gitignore:
.env
.venv/
__pycache__/


#📋 How to Use

1.Enter your Gemini API Key

2.Choose the number of turns

3.Click Start AI Game

4.Two AI agents will play chess against each other

5.Watch the moves live on the board and in the VS Code terminal

6.Click Reset Game anytime to restart
