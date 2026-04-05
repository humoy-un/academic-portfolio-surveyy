import streamlit as st
from datetime import datetime
import json

# ---------------- QUESTIONS ---------------- #
questions = [
    ("How often do you update your academic portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("How effective is your current portfolio for visualizing progress?", ["Not effective","Slightly effective","Moderately effective","Very effective","Extremely effective"], [0,1,2,3,4]),
    ("Do you set clear academic goals in your portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("How confident are you in tracking your academic progress?", ["Not confident","Slightly confident","Moderately confident","Very confident","Extremely confident"], [0,1,2,3,4]),
    ("How often do you review your past academic achievements?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does your portfolio help you identify your strengths and weaknesses?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("How organized is your academic portfolio?", ["Very disorganized","Disorganized","Neutral","Organized","Very organized"], [0,1,2,3,4]),
    ("How often do you use visual tools (charts, graphs) in your portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does portfolio building motivate you to improve academically?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("How easy is it for you to find past work in your portfolio?", ["Very difficult","Difficult","Neutral","Easy","Very easy"], [0,1,2,3,4]),
    ("How often do you share your portfolio with mentors or peers?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does your portfolio reflect your academic growth over time?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("How satisfied are you with your current portfolio system?", ["Very unsatisfied","Unsatisfied","Neutral","Satisfied","Very satisfied"], [0,1,2,3,4]),
    ("How often do you add new evidence of learning to your portfolio?", ["Never","Rarely","Sometimes","Often","Always"], [0,1,2,3,4]),
    ("Does portfolio building help you plan your future academic steps?", ["Not at all","Slightly","Moderately","Very much","Completely"], [0,1,2,3,4]),
    ("Overall, how effective is your portfolio for visualizing academic progress?", ["Not effective","Slightly effective","Moderately effective","Very effective","Extremely effective"], [0,1,2,3,4])
]

# ---------------- FUNCTIONS ---------------- #
def get_effectiveness_level(score):
    if score <= 12:
        return "Very Low Effectiveness", "Needs Urgent Revision"
    elif score <= 24:
        return "Low Effectiveness", "Below Average"
    elif score <= 36:
        return "Moderate Effectiveness", "Satisfactory"
    elif score <= 48:
        return "Good Effectiveness", "Good"
    elif score <= 60:
        return "High Effectiveness", "Very Good"
    else:
        return "Excellent Effectiveness", "Excellent"

def valid_name(s):
    return s and all(c.isalpha() or c in "-' " for c in s)

def valid_dob(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%d-%m-%y")
        return dob <= datetime.now()
    except:
        return False

# ---------------- SESSION STATE ---------------- #
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.user = {}

# ---------------- UI ---------------- #
st.title("🎓 Academic Portfolio Survey")

# ----------- STEP 0: USER INFO ----------- #
if st.session_state.step == 0:
    st.subheader("Enter Your Information")

    surname = st.text_input("Surname")
    given = st.text_input("Given Name")
    dob = st.text_input("Date of Birth (DD-MM-YY)", "01-01-01")
    sid = st.text_input("Student ID (5 digits)", "12345")

    if st.button("Start Survey"):
        if not valid_name(surname):
            st.error("Invalid surname")
        elif not valid_name(given):
            st.error("Invalid given name")
        elif not valid_dob(dob):
            st.error("Invalid DOB format")
        elif not (sid.isdigit() and len(sid) == 5):
            st.error("Student ID must be 5 digits")
        else:
            st.session_state.user = {
                "name": f"{given} {surname}",
                "dob": dob,
                "sid": "000" + sid
            }
            st.session_state.step = 1
            st.rerun()

# ----------- QUESTIONS ----------- #
elif 1 <= st.session_state.step <= len(questions):
    q_index = st.session_state.step - 1
    q_text, options, scores = questions[q_index]

    st.subheader(f"Question {st.session_state.step} of {len(questions)}")
    answer = st.radio(q_text, options)

    if st.button("Next"):
        score = scores[options.index(answer)]
        st.session_state.score += score
        st.session_state.step += 1
        st.rerun()

# ----------- RESULTS ----------- #
else:
    st.subheader("📊 Results")

    result, status = get_effectiveness_level(st.session_state.score)

    st.write(f"**Name:** {st.session_state.user['name']}")
    st.write(f"**DOB:** {st.session_state.user['dob']}")
    st.write(f"**Student ID:** {st.session_state.user['sid']}")
    st.write(f"**Score:** {st.session_state.score}/64")
    st.write(f"**Status:** {status}")
    st.write(f"**Assessment:** {result}")

    # Recommendation
    if st.session_state.score <= 12:
        rec = "Improve portfolio structure and update regularly."
    elif st.session_state.score <= 24:
        rec = "Update more often and use charts."
    elif st.session_state.score <= 36:
        rec = "Add visual elements and clearer goals."
    elif st.session_state.score <= 48:
        rec = "Good work! Maintain it."
    else:
        rec = "Excellent! Share your methods."

    st.info(f"💡 Recommendation: {rec}")

    # Download results
    data = {
        "name": st.session_state.user['name'],
        "dob": st.session_state.user['dob'],
        "student_id": st.session_state.user['sid'],
        "score": st.session_state.score,
        "status": status,
        "assessment": result
    }

    st.download_button(
        label="Download Results (JSON)",
        data=json.dumps(data, indent=2),
        file_name="results.json",
        mime="application/json"
    )

    if st.button("Restart"):
        st.session_state.step = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.user = {}
        st.rerun()