# 🕵️‍♂️ AI Detective — Misinformation & Truth Finder

A simple AI-powered fact-checking web app built with **Streamlit** and **OpenAI**.

## 🔍 How it works
- You paste any claim (from Twitter, news, etc.).
- The app searches the web for evidence using SerpAPI.
- OpenAI analyzes the claim + evidence and gives:
  - Verdict (True / False / Misleading / etc.)
  - Confidence score
  - Explanation
  - Corrected version of the claim

## 🚀 Run locally
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
