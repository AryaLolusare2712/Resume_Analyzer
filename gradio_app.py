import os
import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader
import io
from prompts import resume_analysis_prompt

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

# PDF Text Extraction
def extract_pdf_text(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    return "\n".join([page.extract_text() or "" for page in reader.pages])

# Core Resume Analyzer Function
def analyze_resume(resume_file, job_description):
    try:
        # Read and extract text
        with open(resume_file.name, "rb") as f:
            file_bytes = f.read()

        resume_text = extract_pdf_text(file_bytes)

        # Format prompt
        prompt = resume_analysis_prompt.format(resume=resume_text, jd=job_description)
        response = model.generate_content(prompt)

        return response.text  # Markdown will be rendered as HTML in Gradio

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Gradio Interface
with gr.Blocks(title="Resume Analyzer") as demo:
    gr.Markdown("# 📄 Resume Analyzer using Gemini 1.5 Flash")
    gr.Markdown("Upload your resume and paste a job description to receive AI-generated feedback and match score.")

    with gr.Row():
        resume_file = gr.File(label="📎 Upload Resume (PDF)", file_types=[".pdf"])
        job_desc = gr.Textbox(label="📝 Paste Job Description", lines=10, placeholder="Enter job description here...")

    analyze_btn = gr.Button("🚀 Analyze")

    output = gr.Markdown("### Output will appear here...")

    analyze_btn.click(analyze_resume, inputs=[resume_file, job_desc], outputs=output)

# Launch
if __name__ == "__main__":
    demo.launch()
