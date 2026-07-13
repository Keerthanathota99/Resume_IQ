from flask import Flask, render_template, request, send_file
from resume_parser import extract_text
from skill_match import find_skills
from company_skills import company_skills
from ats_score import calculate_ats_score
from suggestions import get_suggestions
from pdf_report import create_pdf
from ai_feedback import generate_feedback

import os
import re
app = Flask(__name__)

import os
print(os.getcwd())
print(app.static_folder)
# -------------------- Upload Folder --------------------

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

PDF_FOLDER = "reports"
app.config["PDF_FOLDER"] = PDF_FOLDER

os.makedirs(PDF_FOLDER, exist_ok=True)

# -------------------- Splash Screen --------------------

@app.route("/")
def splash():
    return render_template("splash.html")


# -------------------- Login --------------------

@app.route("/login")
def login():
    return render_template("login.html")


# -------------------- Register --------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        return render_template("login.html")

    return render_template("register.html")


# -------------------- Home --------------------

@app.route("/home")
def home():
    return render_template("index.html")


# -------------------- Feedback --------------------

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")
    

# -------------------- Download PDF Report --------------------

@app.route("/download-report/<path:filename>")
def download_report(filename):

    return send_file(
        filename,
        as_attachment=True
    )

# -------------------- Loading --------------------

@app.route("/loading")
def loading():
    return render_template("loading.html")


# -------------------- Upload Resume --------------------

@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file selected."

    file = request.files["resume"]

    if file.filename == "":
        return "Please choose a file."

    company = request.form["company"]
    job_description = request.form["job_description"]
    job_role = request.form.get("job_role", "")

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # -------------------- Extract Resume --------------------

    resume_text = extract_text(filepath)

    resume_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', resume_text)
    resume_text = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', resume_text)
    resume_text = re.sub(r'\s+', ' ', resume_text)

    # -------------------- Resume Skills --------------------

    skills = find_skills(resume_text)
    skills = list(set(skills))
    
    resume_score = calculate_ats_score(
        skills,
        resume_text
    )

    # -------------------- Required Skills --------------------

    company_required = company_skills.get(
        company.lower(),
        []
    )

    jd_skills = find_skills(job_description)

    required_skills = list(
        set(company_required + jd_skills)
    )

    print("\n========== DEBUG ==========")
    print("Resume Skills :", skills)
    print("Required Skills :", required_skills)
    print("===========================\n")
        # -------------------- Convert to Lowercase --------------------

    skills = list(set([s.lower() for s in skills]))
    required_skills = list(set([s.lower() for s in required_skills]))

    # -------------------- Skill Matching --------------------

    matched = []
    missing = []

    for skill in required_skills:
        if skill in skills:
            matched.append(skill)
        else:
            missing.append(skill)

    # -------------------- Job Match Score --------------------

    if len(required_skills) > 0:
        match_percent = int(
            (len(matched) / len(required_skills)) * 100
        )
    else:
        match_percent = 0

    # -------------------- Final ATS Score --------------------

    ats_score = int(
        (resume_score * 0.4) +
        (match_percent * 0.6)
    )

    if ats_score > 100:
        ats_score = 100

    if ats_score < 0:
        ats_score = 0

    # -------------------- Resume Status --------------------

    if ats_score >= 85:
        status = "Excellent Match"

    elif ats_score >= 70:
        status = "Good Match"

    elif ats_score >= 50:
        status = "Average Match"

    else:
        status = "Needs Improvement"

    # -------------------- Suggestions --------------------

    suggestions = get_suggestions(missing)

    if ats_score < 60:
        suggestions.append(
            "Improve your resume summary."
        )

    if "github" not in resume_text.lower():
        suggestions.append(
            "Add your GitHub profile."
        )

    if "linkedin" not in resume_text.lower():
        suggestions.append(
            "Add your LinkedIn profile."
        )

    if "project" not in resume_text.lower():
        suggestions.append(
            "Add at least 2 academic or personal projects."
        )

    if "internship" not in resume_text.lower():
        suggestions.append(
            "Mention internships or practical experience."
        )

    print("\n========== RESULT ==========")
    print("Matched Skills :", matched)
    print("Missing Skills :", missing)
    print("Resume Score :", resume_score)
    print("Job Match :", match_percent)
    print("Final ATS :", ats_score)
    print("Status :", status)
    print("============================\n")

        # -------------------- AI Feedback --------------------

    ai_feedback = generate_feedback(
        ats_score,
        matched,
        missing
    )

        # -------------------- Generate PDF Report --------------------

    pdf_path = create_pdf(
        filename=file.filename,
        company=company,
        ats_score=ats_score,
        match_percent=match_percent,
        skills=skills,
        missing_skills=missing,
        suggestions=suggestions
    )

    # -------------------- Result Page --------------------

    return render_template(
    "result.html",
    company=company,
    ats_score=ats_score,
    resume_score=resume_score,
    match_percent=match_percent,
    matched_skills=matched,
    missing_skills=missing,
    suggestions=suggestions,
    job_description=job_description,
    status=status,
    resume_skills=skills,
    ai_feedback=ai_feedback,
    pdf_path=pdf_path
)


# -------------------- Run Flask --------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )