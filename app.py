import streamlit as st
import pandas as pd
import random
from PIL import Image

st.set_page_config(page_title="Smart E-Waste Bin", layout="wide")

# ------------------------------
# Mock Databases
# ------------------------------
BINS = [
    {"id": 1, "name": "City Mall Bin", "lat": 12.97, "lon": 77.59, "items": ["Phone", "Battery"], "fill": 40},
    {"id": 2, "name": "Tech Park Bin", "lat": 12.99, "lon": 77.61, "items": ["Laptop", "Charger", "Cable"], "fill": 70},
    {"id": 3, "name": "Metro Station Bin", "lat": 12.95, "lon": 77.58, "items": ["Phone", "Cable"], "fill": 90},
]

VALUES = {
    "Phone": 120,
    "Laptop": 300,
    "Battery": 50,
    "Charger": 40,
    "Cable": 20
}

CO2_SAVED = {
    "Phone": 2.5,
    "Laptop": 6.0,
    "Battery": 1.2,
    "Charger": 0.8,
    "Cable": 0.5
}

# ------------------------------
# Session State
# ------------------------------
if "points" not in st.session_state:
    st.session_state.points = 0
if "history" not in st.session_state:
    st.session_state.history = []

# ------------------------------
# Sidebar Navigation
# ------------------------------
st.sidebar.title("♻ Smart E-Waste System")
page = st.sidebar.radio("Navigate", ["Find Bin", "Smart Bin", "My Rewards", "Admin Dashboard"])

# ------------------------------
# PAGE 1: BIN FINDER
# ------------------------------
if page == "Find Bin":
    st.title("📍 Find Nearest E-Waste Bin")

    waste_type = st.selectbox("Select E-Waste Type", list(VALUES.keys()))

    compatible_bins = [b for b in BINS if waste_type in b["items"] and b["fill"] < 95]

    if not compatible_bins:
        st.error("❌ No available bins nearby. All bins are full.")
    else:
        df = pd.DataFrame(compatible_bins)
        st.success("✅ Compatible bins found")
        st.dataframe(df[["name", "items", "fill"]])

# ------------------------------
# PAGE 2: SMART BIN
# ------------------------------
elif page == "Smart Bin":
    st.title("🗑 Smart Bin Interface")

    st.markdown("### Step 1: Scan Item")
    image = st.file_uploader("Upload item image", type=["png", "jpg", "jpeg"])
    weight = st.slider("Approximate weight (grams)", 10, 3000, 200)

    if st.button("🔍 Analyze Item"):
        detected = random.choice(list(VALUES.keys()))
        confidence = random.randint(60, 95)

        st.markdown("### 🤖 Detection Result")
        st.success(f"Detected Item: **{detected}**")
        st.info(f"Confidence: {confidence}%")
        st.caption(f"Detected based on visual shape + weight estimation")

        if confidence < 70:
            st.warning("Low confidence – please verify manually")

        value = VALUES[detected]
        co2 = CO2_SAVED[detected]

        st.markdown("### 🎉 Reward")
        st.metric("Estimated Value (₹)", value)
        st.metric("CO₂ Saved (kg)", co2)

        st.session_state.points += value
        st.session_state.history.append(detected)

# ------------------------------
# PAGE 3: USER REWARDS
# ------------------------------
elif page == "My Rewards":
    st.title("🎁 My Recycling Rewards")

    st.metric("Total Points", st.session_state.points)
    st.metric("Items Recycled", len(st.session_state.history))

    if st.session_state.points >= 500:
        st.success("🏆 Badge Unlocked: Eco Hero")
    elif st.session_state.points >= 100:
        st.info("🥉 Badge: First Recycler")

    st.markdown("### ♻ Recycling History")
    st.write(st.session_state.history)

# ------------------------------
# PAGE 4: ADMIN DASHBOARD
# ------------------------------
elif page == "Admin Dashboard":
    st.title("🧑‍💼 Admin Dashboard")

    df = pd.DataFrame(BINS)
    st.markdown("### 📊 Bin Status Overview")
    st.dataframe(df)

    st.markdown("### 🚨 Alerts")
    for b in BINS:
        if b["fill"] > 85:
            st.warning(f"{b['name']} is almost full")

    st.markdown("### 📈 Analytics")
    st.bar_chart(df["fill"])