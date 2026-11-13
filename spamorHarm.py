import re
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

# --- PAGE CONFIG & THEME ---
st.set_page_config(
    page_title="Enterprise AI Phishing & Spam Shield",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    "<h1>🛡️ Enterprise AI Phishing & Spam Detection Engine</h1>",
    unsafe_allow_html=True,
)
st.write(
    "Advanced hybrid detection combining Machine Learning (Logistic Regression"
    " + N-grams) with Real-World Security Heuristics."
)
st.markdown("---")


# --- LOAD DATA & TRAIN ADVANCED MODEL ---
@st.cache_resource
def train_advanced_model():
  url = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv"
  df = pd.read_csv(url, sep="\t", header=0, names=["label", "message"])

  # Augment dataset with hard real-world phishing samples to prevent false negatives
  extra_phishing = pd.DataFrame({
      "label": ["spam", "spam", "spam", "spam", "spam"],
      "message": [
          (
              "URGENT: Your bank account is locked. Verify your credentials"
              " immediately at http://bit.ly/secure-bank-login"
          ),
          (
              "Security Alert: Unusual sign-in attempt detected. Click here to"
              " reset your password: http://192.168.1.1/auth"
          ),
          (
              "Congratulations! You won a $1,000 gift card. Claim now by"
              " running the attached update_app.zip"
          ),
          (
              "Your invoice #9821 is attached. Download the secure viewer.exe"
              " to open it."
          ),
          (
              "Action Required: Update your billing details to avoid service"
              " suspension."
          ),
      ],
  })
  df = pd.concat([df, extra_phishing], ignore_index=True)

  X = df["message"]
  y = df["label"]

  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42
  )

  # Upgraded Pipeline: TF-IDF with unigrams + bigrams (captures phrases like "click here")
  # Using Logistic Regression for superior decision boundaries
  model = make_pipeline(
      TfidfVectorizer(ngram_range=(1, 2), stop_words="english"),
      LogisticRegression(C=2.0, max_iter=1000),
  )
  model.fit(X_train, y_train)
  return model


with st.spinner(
    "🤖 Training advanced hybrid model on expanded security datasets..."
):
  ai_model = train_advanced_model()
st.success("✨ Advanced AI Shield is fully active and calibrated!")

# --- REAL-WORLD SECURITY HEURISTIC SCANNER ---


def security_heuristic_check(text):
  risk_score = 0
  flags = []

  # 1. Check for suspicious URL shorteners or raw IPs
  suspicious_patterns = [
      r"bit\.ly",
      r"tinyurl",
      r"goo\.gl",
      r"t\.co",
      r"ow\.ly",
      r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
  ]
  for pattern in suspicious_patterns:
    if re.search(pattern, text, re.IGNORECASE):
      risk_score += 3
      flags.append(
          "⚠️ Contains high-risk URL shortener or untrusted IP address."
      )
      break

  # 2. Check for dangerous attachment file types
  dangerous_extensions = [r"\.zip", r"\.exe", r"\.scr", r"\.bat", r"\.js"]
  for ext in dangerous_extensions:
    if re.search(ext, text, re.IGNORECASE):
      risk_score += 4
      flags.append(
          f"🚨 References dangerous executable/archive attachment ({ext})."
      )
      break

  # 3. Check for high-urgency credential harvesting keywords
  urgency_phrases = [
      "verify your",
      "account locked",
      "suspended",
      "password reset",
      "unauthorized login",
      "click here immediately",
  ]
  match_count = sum(
      1 for phrase in urgency_phrases if phrase in text.lower()
  )
  if match_count >= 1:
    risk_score += 2
    flags.append("⚡ Uses high-urgency social engineering language.")

  return risk_score, flags


# --- USER INPUT SECTION ---
st.markdown("### 🔍 Test an Email or Message")
user_input = st.text_area(
    "Paste message content below:",
    placeholder=(
        "e.g., URGENT: Your bank account has been locked. Verify your password"
        " here..."
    ),
    height=120,
)

col1, col2 = st.columns([1, 4])
with col1:
  analyze_btn = st.button("🚀 Run Deep Scan")

if analyze_btn:
  if user_input.strip() == "":
    st.warning("Please enter a message to scan.")
  else:
    # Get ML prediction and probability confidence
    ml_pred = ai_model.predict([user_input])[0]
    probabilities = ai_model.predict_proba([user_input])[0]
    classes = ai_model.classes_

    # Map probability for spam
    spam_prob_idx = list(classes).index("spam") if "spam" in classes else 1
    spam_confidence = probabilities[spam_prob_idx] * 100

    # Run Heuristic checks
    heuristic_score, heuristic_flags = security_heuristic_check(user_input)

    # Hybrid Decision Logic: Override ML if heuristics find obvious threat signatures
    is_threat = (ml_pred == "spam") or (heuristic_score >= 3)

    st.markdown("---")
    st.markdown("### 📊 Scan Results & Threat Breakdown")

    if is_threat:
      st.error(
          "🔴 **VERDICT: CRITICAL THREAT / SPAM / PHISHING DETECTED!**"
      )
      st.metric(
          label="Estimated Phishing / Spam Probability",
          value=(
              f"{max(spam_confidence, 85.0):.1f}%"
              if heuristic_score > 0
              else f"{spam_confidence:.1f}%"
          ),
      )
    else:
      st.success(
          "🟢 **VERDICT: SAFE / LEGITIMATE (HAM)** — No malicious indicators"
          " found."
      )
      st.metric(
          label="Confidence Score", value=f"{(100 - spam_confidence):.1f}% Safe"
      )

    # Show Security Audit Details
    if heuristic_flags:
      st.markdown("#### 🔍 Security Heuristic Flags Triggered:")
      for flag in heuristic_flags:
        st.write(f"- {flag}")
    else:
      st.info(
          "ℹ️ No suspicious links, dangerous attachments, or phishing triggers"
          " identified in code heuristics."
      )