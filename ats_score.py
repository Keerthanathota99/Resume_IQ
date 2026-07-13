import re

def calculate_ats_score(skills, resume_text):

    text = resume_text.lower()
    score = 0

    # =========================
    # 1. Skills (30 Marks)
    # =========================
    score += min(len(skills) * 3, 30)

    # =========================
    # 2. Education (10 Marks)
    # =========================
    education_words = [
        "b.tech", "b.e", "m.tech",
        "bachelor", "master",
        "degree", "education",
        "bsc", "b.sc", "mca", "bca"
    ]

    if any(word in text for word in education_words):
        score += 10

    # =========================
    # 3. Projects (15 Marks)
    # =========================
    if "project" in text or "projects" in text:
        score += 15

    # =========================
    # 4. Experience (15 Marks)
    # =========================
    if any(word in text for word in [
        "experience",
        "internship",
        "intern",
        "worked"
    ]):
        score += 15

    # =========================
    # 5. Certifications (10 Marks)
    # =========================
    if any(word in text for word in [
        "certificate",
        "certification",
        "certifications"
    ]):
        score += 10

    # =========================
    # 6. Contact Details (10 Marks)
    # =========================
    if "@" in text:
        score += 5

    if re.search(r"\d{10}", text):
        score += 5

    # =========================
    # 7. Resume Sections (10 Marks)
    # =========================
    sections = [
        "objective",
        "summary",
        "skills",
        "education",
        "projects",
        "experience"
    ]

    count = sum(1 for section in sections if section in text)

    score += min(count * 2, 10)

    return min(score, 100)