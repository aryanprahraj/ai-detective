<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Framework-Streamlit-red.svg" alt="Framework">
  <img src="https://img.shields.io/badge/OpenAI-GPT--Powered-green.svg" alt="OpenAI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

# 🕵️‍♂️ AI Detective — Truth Finder & Misinformation Checker

**AI Detective** is an AI-powered fact-checking web app built with **Streamlit**, **OpenAI**, and **SerpAPI**.  
It verifies the authenticity of text or image-based claims in seconds — whether from social media, news, or anywhere online.

---

## 🚀 Features

✅ Verify any claim or statement (e.g. “NASA says the Sun will go dark for 3 days”).  
🧠 AI searches for credible sources and returns:  
- Verdict → ✅ True / ❌ False / ⚠️ Misleading / ❓ Unverifiable  
- Confidence Level  
- Explanation & Cited Sources  
- Corrected or clarified version of the claim  

🖼️ Upload screenshots or posts — the app extracts text using **OCR (Tesseract)** and verifies the claim automatically.  

---

## ⚙️ How It Works

1. Paste a claim **or upload a screenshot**.  
2. The app extracts text (for images).  
3. It performs a **web search via SerpAPI** for relevant evidence.  
4. **OpenAI GPT** evaluates all gathered information and returns:
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

   🌐 **Live Demo:** [AI Detective App](https://ai-detective-aryanprahraj.streamlit.app)

