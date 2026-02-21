import streamlit as st
import random
import plotly.express as px
import pandas as pd
import time

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(layout="wide")
st.title("🚀 KAIROS - AI Experience Engine")

# ---------------------------
# SIDEBAR SETTINGS
# ---------------------------
st.sidebar.header("Settings")

channel = st.sidebar.selectbox(
    "Select Channel",
    ["WhatsApp", "Email", "Voice", "Website Chat"]
)

demo_mode = st.sidebar.toggle("🎬 Demo Mode")

# ---------------------------
# SESSION STATE INIT
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# LAYOUT
# ---------------------------
col1, col2 = st.columns([2,1])

# ===========================
# CHAT SECTION
# ===========================
with col1:
    st.subheader(f"💬 Conversation - {channel}")

    user_input = st.text_input("Type your message")

    if st.button("Send"):

        if demo_mode:
            emotion = "Angry"
            confidence = 92
            risk = 85
            ai_response = "We understand your frustration. Let me escalate this immediately."
        else:
            emotion = random.choice(["Happy", "Neutral", "Angry"])
            confidence = random.randint(75, 98)
            risk = random.randint(10, 95)
            ai_response = "Thank you for your message. We are analyzing your request."

        st.session_state.messages.append(("User", user_input))
        st.session_state.messages.append(("AI", ai_response))

        # Store metrics
        st.session_state.emotion = emotion
        st.session_state.confidence = confidence
        st.session_state.risk = risk

    # Display conversation
    for sender, message in st.session_state.messages:
        if sender == "User":
            st.markdown(f"🧑 **You:** {message}")
        else:
            st.markdown(f"🤖 **AI:** {message}")

# ===========================
# INSIGHT PANEL
# ===========================
with col2:
    st.subheader("📊 Emotion Insights")

    if "emotion" in st.session_state:
        st.metric("Detected Emotion", st.session_state.emotion)
        st.metric("Confidence Score", f"{st.session_state.confidence}%")
        st.metric("Escalation Risk", f"{st.session_state.risk}%")

        # Smart alerts
        if st.session_state.emotion == "Angry":
            st.error("⚠ Angry user detected")

        if st.session_state.risk > 70:
            st.error("🚨 High Escalation Risk")

# ===========================
# DASHBOARD SECTION
# ===========================
st.divider()
st.subheader("📈 Real-Time Analytics Dashboard")

if demo_mode:
    emotion_scores = [2, 3, 4, 5, 5, 4, 5]
else:
    emotion_scores = [random.randint(1,5) for _ in range(7)]

data = pd.DataFrame({
    "Time": list(range(1, 8)),
    "Emotion Score": emotion_scores
})

fig = px.line(data, x="Time", y="Emotion Score", title="Emotion Trend Over Time")
st.plotly_chart(fig)

# ===========================
# VOICE SIMULATION
# ===========================
# ===========================
# VOICE INTERFACE
# ===========================
st.divider()
st.subheader("🎤 Voice Input (Demo Mode)")

if st.button("🎙 Record Voice"):
    # Simulate recording animation
    st.info("Recording...")
    time.sleep(1.5)
    st.success("Transcription: I am very frustrated with your service.")
    st.warning("Detected Emotion: Angry")
    


# ===========================
# ACTIVE USERS + SATISFACTION
# ===========================
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.metric("Active Users", random.randint(10, 100))

with col4:
    st.metric("Customer Satisfaction", f"{random.randint(70,100)}%")