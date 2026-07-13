def generate_feedback(ats_score, matched_skills, missing_skills):

    strengths = ""

    if matched_skills:
        strengths = ", ".join(matched_skills[:6])
    else:
        strengths = "No major technical skills detected"

    improvements = ""

    if missing_skills:
        improvements = ", ".join(missing_skills[:6])
    else:
        improvements = "No critical missing skills"

    if ats_score >= 85:

        summary = (
            "Excellent resume. Your profile strongly matches "
            "the job requirements."
        )

    elif ats_score >= 70:

        summary = (
            "Good resume with strong technical skills. "
            "A few improvements can increase your ATS score."
        )

    elif ats_score >= 50:

        summary = (
            "Average resume. Consider adding more relevant "
            "projects and skills."
        )

    else:

        summary = (
            "Your resume needs significant improvements "
            "to increase interview chances."
        )

    recommendation = []

    if missing_skills:
        recommendation.append(
            "Add the missing technical skills in projects."
        )

    recommendation.append(
        "Use measurable achievements."
    )

    recommendation.append(
        "Keep resume within one page."
    )

    recommendation.append(
        "Maintain ATS-friendly formatting."
    )

    return {
        "summary": summary,
        "strengths": strengths,
        "improvements": improvements,
        "recommendation": recommendation
    }