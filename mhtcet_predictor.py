import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="MHT-CET 2025 Predictor", layout="centered")

st.title("🎯 MHT-CET 2025 Percentile & Rank Predictor")
st.subheader("Based on official 2025 data")
st.caption("An initiative by **Jay Kshirsagar (Counsellor)**")
st.markdown("For updates, tips & personal counselling, follow us on Instagram, contact **Edu Guide** on :red[Instagram:@edu_guide_studs],do follow us if use the predictor this will motivate us to continue our free service.")
st.markdown("Refresh the page for every prediction so u will see no erros,Peace :)")
st.markdown("For any error during prediction please contact on above instagram id")

PCM_TOTAL = 422863
PCB_TOTAL = 282737
CSV_FILENAME = "cet_predictions.csv"

# Initialize session state defaults once
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "percentile" not in st.session_state:
    st.session_state.percentile = None
if "rank" not in st.session_state:
    st.session_state.rank = None
if "total" not in st.session_state:
    st.session_state.total = None
if "subject_scores" not in st.session_state:
    st.session_state.subject_scores = None
if "group" not in st.session_state:
    st.session_state.group = "PCM (Engineering)"
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Bar Chart"
if "mumbai_admit" not in st.session_state:
    st.session_state.mumbai_admit = "No"

# --- Group Selection ---
group = st.radio("Select your group:", ["PCM (Engineering)", "PCB (Pharmacy/Biology)"], key="group")

with st.form("predictor_form", clear_on_submit=False):
    name = st.text_input("Enter your name (optional):", key="name")

    st.markdown("#### 🧪 Physics & Chemistry (1 mark each, 50 questions)")
    physics = st.number_input("Physics Marks (out of 50):", min_value=0, max_value=50, value=25, key="physics")
    chemistry = st.number_input("Chemistry Marks (out of 50):", min_value=0, max_value=50, value=25, key="chemistry")

    if group == "PCM (Engineering)":
        st.markdown("#### 🧮 Mathematics (2 marks each, 50 questions, max 100 marks)")
        math = st.number_input("Mathematics Marks (out of 100):", min_value=0, max_value=100, value=50, key="math")
        total = physics + chemistry + math
        subject_scores = {"Physics": physics, "Chemistry": chemistry, "Mathematics": math}
        candidate_count = PCM_TOTAL
        max_marks = {"Physics": 50, "Chemistry": 50, "Mathematics": 100}
    else:
        st.markdown("#### 🧬 Biology (1 mark each, 100 questions)")
        biology = st.number_input("Biology Marks (out of 100):", min_value=0, max_value=100, value=50, key="biology")
        total = physics + chemistry + biology
        subject_scores = {"Physics": physics, "Chemistry": chemistry, "Biology": biology}
        candidate_count = PCB_TOTAL
        max_marks = {"Physics": 50, "Chemistry": 50, "Biology": 100}

    submit = st.form_submit_button("Predict Result")

if submit:
    # Calculate rank & percentile
    rank = round((1 - total / 200) * candidate_count)
    percentile = round((candidate_count - rank) / candidate_count * 100, 4)

    # Save in session state
    st.session_state.percentile = percentile
    st.session_state.rank = rank
    st.session_state.total = total
    st.session_state.subject_scores = subject_scores
    st.session_state.submitted = True

    # Save user data to CSV
    user_data = {
        "Name": name,
        "Group": group,
        "Physics": physics,
        "Chemistry": chemistry,
        "Mathematics" if group == "PCM (Engineering)" else "Biology":
            math if group == "PCM (Engineering)" else biology,
        "Total Marks": total,
        "Percentile": percentile,
        "Estimated Rank": rank,
    }
    df_entry = pd.DataFrame([user_data])
    if os.path.exists(CSV_FILENAME):
        df_entry.to_csv(CSV_FILENAME, mode='a', header=False, index=False)
    else:
        df_entry.to_csv(CSV_FILENAME, index=False)

if st.session_state.submitted:
    st.success(f"🧠 Estimated Percentile: **{st.session_state.percentile}%**")
    st.info(f"📊 Approximate Rank: **{st.session_state.rank:,} out of {candidate_count:,}**")

    st.markdown("### 📊 Subject-wise Percentile Performance")

    # Calculate subject-wise percentile %
    subject_percentiles = {subj: round((score / max_marks[subj]) * 100, 2)
                           for subj, score in st.session_state.subject_scores.items()}

    df_chart = pd.DataFrame([subject_percentiles])

    chart_type = st.radio("Select chart type:", ["Bar Chart", "Line Chart"], horizontal=True, key="chart_type")

    if chart_type == "Bar Chart":
        st.bar_chart(df_chart)
    else:
        st.line_chart(df_chart)

    st.markdown("### 📈 Your Position Among All Candidates")

    x = np.linspace(0, 100, 1000)
    y = np.linspace(1, candidate_count, 1000)
    percentile_idx = np.argmin(np.abs(x - st.session_state.percentile))
    percentile_rank_y = y[percentile_idx]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axvline(x=st.session_state.percentile, color='red', linestyle='--')
    ax.scatter([st.session_state.percentile], [percentile_rank_y], color='red', zorder=5)
    ax.set_title("Percentile Rank Curve")
    ax.set_xlabel("Percentile")
    ax.set_ylabel("Rank (Lower is Better)")
    ax.invert_yaxis()
    st.pyplot(fig)

    st.markdown("### 🎓 Taking Admission in Mumbai University?")
    mumbai_admit = st.radio("Do you want guidance for Mumbai University admission?", ["No", "Yes"], key="mumbai_admit")

    if mumbai_admit == "Yes":
        st.success("🎉 Join our **Free Webinar** on Mumbai University Engineering College Admissions!")
        st.markdown("[👉 Click here to Join WhatsApp Group for serious students who want to take admission under Mumbai University College](https://chat.whatsapp.com/G5tLmoyRKJE4CjmegIGbBa)")
        st.markdown("📝 Interested in **Option Form Filling & College Selection Guidance**?")
        if st.button("🎯 I want personalised college guidance"):  
         st.markdown("📌 [Fill this short form to get started](https://forms.gle/tLzGyd6dxBvABnnu5)")
st.markdown("For personalized guidance, contact **Edu Guide** on :red[Instagram]:[@edu_guide_studs](https://www.instagram.com/edu_guide_studs/?igsh=MTdwb2p5ZnVtbGZqbA%3D%3D)")
