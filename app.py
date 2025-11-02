# app.py — AI Detective (Final Compact UI Version)
import os
import json
import hashlib
import requests
import streamlit as st
from openai import OpenAI
import re
from PIL import Image
import pytesseract  # OCR

# ---- CONFIG ----
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

# ---- PAGE SETUP ----
st.set_page_config(page_title="AI Detective — Truth Finder", layout="centered")

# ---- GLOBAL STYLE ----
st.markdown("""
    <style>
        body { background-color:#0f172a; color:#ffffff; }
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            max-width: 900px !important;
        }
        textarea, input, .stTextArea textarea {
            background-color:#1e293b !important;
            color:#f8fafc !important;
            border-radius:8px !important;
            border:1px solid #334155 !important;
            caret-color:#ffffff !important;
        }
        textarea:focus {
            border:1px solid #60a5fa !important;
            box-shadow:0 0 10px #3b82f6 !important;
        }
        ::placeholder { color:#94a3b8 !important; }
        .stButton button {
            background-color:#2563eb !important;
            color:white !important;
            border-radius:8px !important;
            font-weight:bold !important;
            transition:0.3s;
            padding:6px 20px !important;
            height:42px !important;
        }
        .stButton button:hover {
            background-color:#1e40af !important;
            transform:scale(1.02);
        }
        .stMarkdown h3, .stMarkdown h4, .stMarkdown h2 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.4rem !important;
        }
        img {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.markdown("""
<div style='text-align:center; padding:25px 10px; background:radial-gradient(circle at top, #111827 0%, #0f172a 100%);
border-radius:12px; color:white;'>
    <span style='font-size:40px;'>🕵️‍♂️</span>
    <h1 style='font-size:36px; font-weight:700; margin-bottom:4px;'>AI Detective</h1>
    <p style='font-size:15px; color:#cbd5e1; margin:0;'>Your AI for piecing together facts and debunking misinformation.</p>
    <div style='font-size:13px; color:#94a3b8; font-style:italic;'>By Aryan Prahraj</div>
</div>
""", unsafe_allow_html=True)

# ---- CACHE ----
CACHE_FILE = "factcheck_cache.json"
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f: return json.load(f)
        except: return {}
    return {}
def save_cache(data):
    with open(CACHE_FILE, "w") as f: json.dump(data, f, indent=2)
cache = load_cache()

def hash_claim(c): return hashlib.sha256(c.strip().lower().encode()).hexdigest()

# ---- IMAGE UPLOAD + OCR ----
st.markdown("### 🖼️ Upload a screenshot (optional)")
uploaded_file = st.file_uploader(
    "Upload image (PNG, JPG, JPEG)",
    type=["png", "jpg", "jpeg"],
    help="Upload a post or screenshot to extract and verify a claim."
)
claim_from_image = ""

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_container_width=True)
    with st.spinner("🧠 Reading text from image..."):
        try:
            extracted_text = pytesseract.image_to_string(image)
            if extracted_text.strip():
                claim_from_image = extracted_text.strip().split("\n")[0]
                st.success("✅ Claim extracted from image:")
                st.markdown(f"<div style='color:#cbd5e1;font-size:15px;'><b>{claim_from_image}</b></div>", unsafe_allow_html=True)
            else:
                st.warning("Couldn't detect readable text. Please try a clearer image.")
        except Exception as e:
            st.error(f"OCR failed: {e}")

# ---- MANUAL CLAIM INPUT ----
st.markdown("### ✍️ Or type/paste a claim manually")
claim_input = st.text_area(
    "Enter a claim:",
    value=claim_from_image,
    placeholder="e.g. 'NASA says the Sun will go dark for 3 days next month.'",
    height=90
).strip()

strict_mode = st.checkbox("🧩 Strict Mode (check exactly as written, don’t auto-correct)", value=False)

# ---- MAIN ----
if st.button("🔍 Check Claim"):
    if not claim_input:
        st.warning("Please enter a claim or upload an image first.")
        st.stop()

    claim_hash = hash_claim(claim_input)

    if claim_hash in cache:
        st.info("⚡ Cached result found — no tokens used!")
        result_data = cache[claim_hash]
    else:
        with st.spinner("🔎 Searching Google and analyzing claim..."):
            results = []
            if SERPAPI_KEY:
                try:
                    params = {"q": claim_input, "engine": "google", "num": 8, "api_key": SERPAPI_KEY}
                    resp = requests.get("https://serpapi.com/search.json", params=params, timeout=15)
                    j = resp.json()
                    for r in j.get("organic_results", [])[:8]:
                        results.append({
                            "title": r.get("title", ""),
                            "snippet": r.get("snippet", ""),
                            "link": r.get("link", "")
                        })
                except Exception as e:
                    st.error(f"Search failed: {e}")
            else:
                st.error("Missing SERPAPI_API_KEY — please set it.")
                st.stop()

            evidence = ""
            for r in results:
                evidence += f"TITLE: {r['title']}\nSNIPPET: {r['snippet']}\nLINK: {r['link']}\n\n"

            prompt = f"""
You are an expert fact-checker AI.
Determine if the following claim is True, False, or Unverifiable based on the Google snippets provided.
Return result in this exact format:

Verdict: [True / False / Unverifiable]
Confidence: [0–100]
Explanation: [1–3 sentences]
Sources: [list of relevant links]

CLAIM:
\"\"\"{claim_input}\"\"\"

SNIPPETS:
{evidence}
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=600
                )
                result_data = response.choices[0].message.content.strip()
                cache[claim_hash] = result_data
                save_cache(cache)
            except Exception as e:
                st.error(f"OpenAI error: {e}")
                result_data = None

    result_text = json.dumps(result_data, indent=2) if isinstance(result_data, dict) else str(result_data)

    st.markdown("### 🧩 Claim")
    st.info(claim_input)

    verdict = re.search(r"Verdict:\s*(.*)", result_text)
    conf = re.search(r"Confidence:\s*(\d+)", result_text)
    expl = re.search(r"Explanation:\s*(.*)", result_text, re.DOTALL)
    srcs = re.findall(r"(https?://[^\s]+)", result_text)

    verdict_txt = verdict.group(1).strip() if verdict else "Unverifiable"
    conf_val = int(conf.group(1)) if conf else 50
    explanation = expl.group(1).strip() if expl else "No explanation provided."

    color_map = {"True": "#16a34a", "False": "#dc2626", "Unverifiable": "#facc15"}
    bar_color = color_map.get(verdict_txt.split()[0], "#6b7280")

    st.markdown(f"#### 🧠 Verdict: <span style='color:{bar_color};font-weight:700'>{verdict_txt}</span>", unsafe_allow_html=True)
    st.progress(conf_val / 100)
    st.caption(f"Confidence Level: {conf_val}%")

    st.markdown("#### 📘 Explanation")
    st.write(explanation)

    if srcs:
        st.markdown("#### 🔗 Verified Sources")
        src_html = "".join([
            f"<a href='{s}' target='_blank'><button style='margin:3px;background:#2563eb;color:white;border:none;padding:6px 10px;border-radius:6px;'>{s.split('/')[2]}</button></a>"
            for s in srcs])
        st.markdown(src_html, unsafe_allow_html=True)
    else:
        st.markdown("_No relevant sources found._")
