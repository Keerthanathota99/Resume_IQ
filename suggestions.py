def get_suggestions(missing_skills):

    suggestions = []

    if missing_skills:

        suggestions.append(
            "Add the missing technical skills relevant to the job."
        )

        suggestions.append(
            "Include projects demonstrating these skills."
        )

        suggestions.append(
            "Use job description keywords naturally in your resume."
        )

        suggestions.append(
            "Highlight measurable achievements."
        )

        suggestions.append(
            "Tailor your resume for every company."
        )

        suggestions.append(
            "Missing Skills: " + ", ".join(missing_skills)
        )

    else:

        suggestions.append(
            "Excellent! Your resume matches the required skills."
        )

        suggestions.append(
            "Keep your projects and certifications updated."
        )

        suggestions.append(
            "Maintain ATS-friendly formatting."
        )

    return suggestions