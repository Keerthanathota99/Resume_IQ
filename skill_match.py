import re

# Master Skills Database
SKILLS = [

    # Programming
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "php", "ruby", "go", "swift", "kotlin", "r",

    # Web
    "html", "css", "bootstrap", "tailwind", "react",
    "angular", "vue", "node.js", "express", "flask",
    "django", "fastapi",

    # Database
    "mysql", "sql", "postgresql", "mongodb",
    "oracle", "sqlite", "firebase",

    # Data Science
    "numpy", "pandas", "matplotlib",
    "scikit-learn", "tensorflow", "keras",
    "opencv", "machine learning",
    "deep learning", "data science",

    # Cloud
    "aws", "azure", "gcp",
    "docker", "kubernetes",

    # Tools
    "git", "github", "linux",
    "postman", "jira",

    # Soft Skills
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "critical thinking"
]


def find_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(pattern, text):
            found.append(skill)

    return sorted(list(set(found)))