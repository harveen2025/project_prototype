import streamlit as st
import time
import os
import pandas as pd
from openai import OpenAI

# Load datasets
dumping_data = pd.read_csv("data/dumping_types.csv")
tips_data = pd.read_csv("data/reporting_tips.csv")

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Function to analyze pollution
def get_ai_analysis(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI expert in illegal dumping analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Contact local agencies based on selected dump types
def contact_authorities(location, selected_types):
    agencies = dumping_data[dumping_data['type'].isin(selected_types)]['disposal_agency'].unique()
    agency_list = ", ".join(agencies)
    return f"Local authorities and cleanup agencies contacted at **{location}**: {agency_list}."

# Get tips based on selected dump types
def get_reporting_tips(selected_types):
    categories = dumping_data[dumping_data['type'].isin(selected_types)]['category'].unique()
    matched_tips = tips_data[tips_data['category'].isin(categories)]
    return matched_tips['tips'].tolist()

# Streamlit CSS Background & Heading
page_element="""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.pexels.com/photos/15265064/pexels-photo-15265064/free-photo-of-seagulls-on-the-shore.jpeg");
    background-size: cover;
}

[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}

[data-testid="stSidebar"] {
    background-color: white;
    text-align: center;
}

[data-testid="stSidebar"] p {
    line-height: 1.75;
}

[data-testid="stMain"] p {
    font-size: 1.2em;
}
[data-testid="stExpander"]{
    background-color: transparent;
}

{
    background-color: lightsteelblue;
}

[data-testid="stExpander"],
[data-testid="stFileUploaderDropzone"],
[data-testid="stNumberInputContainer"] div, 
[data-testid="stNumberInputContainer"] div button, 
.st-ay, .st-aw  {
    background-color: lightsteelblue;
    color: black;
}

p {
    font-weight: bold;
}

summary:hover {
    color: steelblue !important;
}

[data-testid="stMarkdown"] {
    background-color: rgba(255, 255, 255, .80);
    padding: 10px;
    border-radius: 10px;
}

button:hover, button:focus {
    background-color: steelblue !important;
    border-color: white !important;
    color: white !important;
}
</style>
"""
st.markdown(page_element, unsafe_allow_html=True)

col1, col2, col3 = st.sidebar.columns([1, 1, 1])
with col2:
    st.sidebar.title("WELCOME!")
    st.sidebar.image("images/aqua.PNG")
    st.sidebar.divider()
    st.sidebar.markdown("Aqua Alert was made to help local communities care for their waterways using an accessible and intuitive app!")
    st.sidebar.markdown("For a demo of our app, please visit this link here: -insert link in the future-.")

# Streamlit UI
st.title("AquaAlert: Illegal Dumping Reporting Tool")
st.subheader("🌊 Protecting Our Waterways Together")
st.markdown("AI-powered tool to report illegal dumping, contact agencies, and learn how to reduce pollution.")

# Feature 2: Upload Image
uploaded_file = st.file_uploader("📸 Upload an image of the dumping site", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# Feature 1: Location & Checklist for Dump Type
location = st.text_input("📍 Enter the location of the issue")

st.markdown("**✅ Select all types of dumping observed:**")
selected_types = st.multiselect("Types of Waste", options=dumping_data["type"].tolist())

issue_duration = st.number_input("🕐 Duration of the issue (days)", min_value=1, max_value=365, value=1)
description = st.text_area("📝 Describe the situation briefly")

if st.button("🚀 Analyze & Report"):
    if uploaded_file and selected_types and location:
        with st.spinner("Analyzing and contacting local agencies..."):
            time.sleep(2)
            
            # AI Analysis
            ai_prompt = f"""
            Analyze this illegal dumping report. The location is {location}, types of waste are {', '.join(selected_types)}, issue duration is {issue_duration} days.
            User description: {description}.
            What kind of pollution is it? Suggest potential mitigation actions.
            """
            analysis_result = get_ai_analysis(ai_prompt)

            # Display Results
            st.subheader("🧠 AI Analysis:")
            st.write(analysis_result)

            st.subheader("📡 Authority Contacted:")
            st.success(contact_authorities(location, selected_types))

            st.subheader("💡 Reporting Tips:")
            for tip in get_reporting_tips(selected_types):
                st.markdown(f"- {tip}")

            st.success("✅ Thank you for your report!")
    else:
        st.warning("Please complete all fields and upload an image.")

# Expandable for extra resources
with st.expander("🔗 More Resources"):
    st.link_button("EPA Waste Management", "https://www.epa.gov/smm")
    st.link_button("UN SDG 6: Clean Water & Sanitation", "https://sdgs.un.org/goals/goal6")
