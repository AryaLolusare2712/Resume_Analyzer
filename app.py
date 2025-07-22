import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from utils import extract_pdf_text
from prompts import resume_analysis_prompt
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash")

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <form action="/analyze" enctype="multipart/form-data" method="post">
        Resume (PDF): <input type="file" name="resume" accept=".pdf"/><br>
        Job Description: <textarea name="jd" rows="10" cols="50"></textarea><br>
        <input type="submit"/>
    </form>
    """


@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), jd: str = Form(...)):
    try:
        file_bytes = await resume.read()
        resume_text = extract_pdf_text(file_bytes)

        prompt = resume_analysis_prompt.format(resume=resume_text, jd=jd)
        response = model.generate_content(prompt)

        return {
            "markdown": response.text  # this is raw markdown string
        }

    except Exception as e:
        return {"error": str(e)}
