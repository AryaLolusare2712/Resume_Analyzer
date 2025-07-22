resume_analysis_prompt = """
You are a professional resume reviewer.

Given:
- Resume: {resume}
- Job Description: {jd}

Tasks:
1. Score how well the resume matches the job description (0–100%).
2. List the missing skills or keywords.
3. Provide 3–5 personalized improvement suggestions.

📝 Return your response in **Markdown format** as:
## ✅ Match Score: XX%

### 🧠 Missing Skills or Keywords:
- ...
- ...

### 🔧 Suggestions to Improve:
- ...
- ...
"""
