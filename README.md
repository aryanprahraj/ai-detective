# 🕵️‍♂️ AI Detective — Truth Finder & Misinformation Checker

**AI Detective** is an AI-powered fact-checking web app built with **Streamlit**, **OpenAI**, and **SerpAPI**.  
It helps verify the authenticity of text or image-based claims in seconds — whether from social media, news, or anywhere online.

---

## 🚀 Features

✅ Check any claim or statement (e.g. “NASA says the Sun will go dark for 3 days”).  
🧠 AI analyzes context, searches the web for credible evidence, and returns:  
- Verdict (✅ True / ❌ False / ⚠️ Misleading / ❓ Unverifiable)  
- Confidence Level  
- Explanation & Sources  
- Corrected or clarified version of the claim  

🖼️ Upload screenshots or images — the app extracts text and verifies the claim automatically.

---

## ⚙️ How It Works

1. You paste a claim **or upload a screenshot**.
2. The app extracts key info (OCR for images).
3. It performs a **web search via SerpAPI** for related articles and sources.
4. **OpenAI GPT model** evaluates the evidence and generates:
   - Verdict  
   - Confidence level  
   - Explanation  
   - Verified sources  

---

## 💻 Run Locally

1. **Clone this repo:**
   ```bash
   git clone https://github.com/aryanprahraj/ai-detective.git
   cd ai-detective
