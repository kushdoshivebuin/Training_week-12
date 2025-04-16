import streamlit as st
import google.generativeai as genai
import fitz  
import tempfile
import json
import re

genai.configure(api_key="API KEY")

model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name

    doc = fitz.open(tmp_file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_resume_score(resume_text: str, job_desc: str):
    prompt = f"""
    You are an AI Resume Screening Assistant.

    Evaluate how well this resume matches the job description.

    Reply ONLY in valid JSON like this:
    {{
      "score": 85,
      "feedback": "Strong match in Python and Django, but lacks cloud experience."
    }}

    Resume:
    {resume_text}

    Job Description:
    {job_desc}
    """

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        cleaned = re.sub(r'“|”', '"', raw_text)  
        cleaned = re.sub(r"’", "'", cleaned)     

        if cleaned.startswith("```json"):
            cleaned = cleaned.strip("```json").strip("```").strip()

        result = json.loads(cleaned)
        return result.get("score", 0), result.get("feedback", "No feedback found.")

    except Exception as e:
        return 0, f"Failed to parse Gemini's response.\n\n**Raw Output:**\n```\n{raw_text}\n```\n\n**Error:** {str(e)}"


st.set_page_config(page_title="AI Resume Checker", layout="centered")
st.title("🤖 AI Resume Checker (Gemini-Powered)")

st.markdown("Upload your resume and paste the job description.")

uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])
job_desc = st.text_area("Paste the Job Description here", height=200, placeholder="Paste job description here...")

if st.button("Check Match"):
    if not uploaded_file or not job_desc.strip():
        st.warning("Please upload your resume and enter a job description.")
    else:
        with st.spinner("Analyzing resume with Gemini..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            score, feedback = get_resume_score(resume_text, job_desc)
            st.success(f"Match Score: {score}/100")
            st.markdown(f"**Feedback:**\n{feedback}")
