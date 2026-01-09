import streamlit as st
import pandas as pd

# ---------------- PAGE SETUP ----------------
st.set_page_config(
    page_title="Calorie & Diet Planner",
    layout="centered"
)

st.title("🔥 Calorie & Diet Planner 🔥")
st.caption("by Nehar Lalla")

# ---------------- USER INPUTS ----------------
st.subheader("Personal Details")

gender = st.selectbox("Gender", ["Male", "Female"])

age = st.number_input(
    "Age",
    min_value=15,
    max_value=80,
    value=21
)

height = st.number_input(
    "Height (cm)",
    min_value=140,
    max_value=220,
    value=181
)

weight = st.number_input(
    "Current weight (kg)",
    min_value=40.0,
    max_value=200.0,
    value=80.0
)

# ---------------- ACTIVITY ----------------
st.subheader("Activity Level")

activity_levels = {
    "1–3x / week": 1.375,
    "4–5x / week": 1.47,
    "Daily / intense": 1.58,
    "6–7x intense": 1.75,
    "Very intense / physical job": 1.9
}

activity_label = st.selectbox(
    "Select your activity level",
    activity_levels.keys()
)

activity_factor = activity_levels[activity_label]

# ---------------- DIET GOAL ----------------
st.subheader("Diet Goal")

diet_days = st.number_input(
    "How many days do you want to diet for?",
    min_value=7,
    max_value=365,
    value=42
)

goal_weight = st.number_input(
    "Goal weight (kg)",
    min_value=40.0,
    max_value=weight,
    value=max(weight - 5, 40.0)
)

# ---------------- BMR CALCULATION ----------------
if gender == "Male":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# ---------------- TDEE & DEFICIT ----------------
tdee = bmr * activity_factor

weight_to_lose = weight - goal_weight
total_deficit = weight_to_lose * 7700
daily_deficit = total_deficit / diet_days if diet_days > 0 else 0

target_calories = tdee - daily_deficit

# ---------------- OUTPUTS ----------------
st.subheader("Results")

st.metric("BMR", f"{int(bmr)} kcal/day")
st.metric("TDEE (Maintenance)", f"{int(tdee)} kcal/day")
st.metric("Required Daily Deficit", f"{int(daily_deficit)} kcal/day")
st.metric("Target Calories", f"{int(target_calories)} kcal/day")

# ---------------- SAFETY WARNINGS ----------------
if daily_deficit > 1200:
    st.warning(
        "⚠️ This deficit is very aggressive. "
        "Consider increasing your diet duration."
    )

if target_calories < 1200:
    st.error(
        "❗ Target calories are very low. "
        "This may not be sustainable or safe."
    )

# ---------------- DAILY TRACKING ----------------
st.subheader("Daily Calorie Tracking")

days = list(range(1, diet_days + 1))
calories_logged = []

for d in days:
    calories_logged.append(
        st.number_input(
            f"Day {d}",
            min_value=0,
            value=0,
            key=f"day_{d}"
        )
    )

# ---------------- CHART ----------------
if diet_days > 0:
    chart_df = pd.DataFrame({
        "Day": days,
        "Calories Eaten": calories_logged,
        "Target Calories": [target_calories] * len(days)
    })

    st.line_chart(chart_df.set_index("Day"))
