import streamlit as st
import time
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key='my_api_key_here')

def get_ai_analysis(prompt, model="gpt-3.5-turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an AI expert in water pollution analysis."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def contact_authorities(location, trash_type, issue_duration):
    # Here, you'd integrate APIs or contact points for relevant authorities (fake response as a placeholder)
    authorities_contacted = f"Local authorities and cleanup agencies contacted for the issue at {location}, related to {trash_type}, with an ongoing issue duration of {issue_duration} days."
    return authorities_contacted

# Streamlit Interface
st.title("Water Pollution Reporter")
st.markdown("""
This tool helps users identify and analyze water pollution issues by uploading images and providing descriptions. 
AI will analyze the pollution type and offer recommendations for reporting or mitigating the issue.
""")

# Image Upload Section (Feature 2)
uploaded_file = st.file_uploader("Upload an image of the polluted water source", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    st.success("Image uploaded successfully!")

# User Input for Description (Feature 1 & 2)
location = st.text_input("Location of the issue", placeholder="e.g., Riverside, Lake Shore")
trash_type = st.text_input("Type of pollution or trash", placeholder="e.g., sewage leakage, plastic waste")
issue_duration = st.number_input("Duration of the issue (in days)", min_value=1, max_value=365, value=1)
description = st.text_area("Describe the issue in the image", placeholder="E.g., There is sewage leakage from a pipe into the lake.")

if st.button("Analyze Pollution"):
    if uploaded_file and description:
        with st.spinner("Analyzing pollution..."):
            time.sleep(2)
            ai_prompt = f"Analyze the following water pollution issue based on this description: {description}. Provide insights on the pollution type and possible solutions."
            analysis_result = get_ai_analysis(ai_prompt)
            st.subheader("AI Analysis:")
            st.write(analysis_result)
            
            # Feature 1: Contact local authorities and cleanup agencies
            authorities_response = contact_authorities(location, trash_type, issue_duration)
            st.write(f"Authorities response: {authorities_response}")
            
            # Feature 3: Thank the user and give reporting tips
            st.success("Thank you for reporting the issue!")
            st.write("""
            Tips for reporting future instances:
            1. Always capture a clear image or video of the pollution.
            2. Provide specific details about the location and type of pollution.
            3. Report regularly to local authorities to ensure timely action.
            """)
    else:
        st.warning("Please upload an image and provide a description before analyzing.")

# Additional Resources (Feature 3)
with st.expander("More Resources"):
    st.write("Learn more about water pollution and how to take action:")
    st.link_button("EPA Water Pollution Guide", "https://www.epa.gov/nps")
    st.link_button("UN Water Quality Portal", "https://www.unwater.org/")
