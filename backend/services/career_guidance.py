
"""
Knowletive Psychometric Platform
Career guidance catalogue for Indian students.

Public functions retained for compatibility:
- get_strengths()
- get_career_guidance()
- _as_number()
"""

import re


INTELLIGENCE_LABELS = {
    "logical_mathematical": "Logical-Mathematical Intelligence",
    "interpersonal": "Interpersonal Intelligence",
    "bodily_kinesthetic": "Bodily-Kinesthetic Intelligence",
    "verbal_linguistic": "Verbal-Linguistic Intelligence",
    "musical": "Musical Intelligence",
    "naturalist": "Naturalist Intelligence",
    "spatial_visual": "Spatial-Visual Intelligence",
    "intrapersonal": "Intrapersonal Intelligence",
}

RIASEC_LABELS = {
    "realistic": "Realistic",
    "investigative": "Investigative",
    "artistic": "Artistic",
    "social": "Social",
    "enterprising": "Enterprising",
    "conventional": "Conventional",
}


# Detailed starter profiles. Extend this catalogue without changing
# the public functions below.
CAREER_GUIDANCE = {
    "Data Scientist / ML Engineer": {
        "field": "Data Science, Artificial Intelligence and Analytics",
        "summary": (
            "Uses statistics, programming and data to solve problems, "
            "identify patterns and build predictive models. These are "
            "related but distinct career paths."
        ),
        "skills": [
            "Python programming",
            "SQL and database concepts",
            "Statistics and probability",
            "Data cleaning and visualization",
            "Machine learning fundamentals",
            "Problem-solving and communication",
        ],
        "technologies": [
            "Python, Pandas and NumPy",
            "SQL and PostgreSQL",
            "Matplotlib or Power BI",
            "Scikit-learn",
            "Git and GitHub",
        ],
        "projects": [
            "Student performance analysis dashboard",
            "House-price prediction model",
            "Customer segmentation analysis",
            "Build and document a machine-learning project",
        ],
        "pathways": [
            "After Class 10: choose a suitable stream based on your interests and school options.",
            "After Class 12: consider a relevant degree such as B.Tech, B.Sc. Statistics, Mathematics, Computer Science or Data Science.",
            "Build programming, statistics, SQL and project skills alongside your degree.",
            "Create a portfolio and apply for internships or entry-level analytics roles.",
        ],
        "roles": [
            "Data Analyst",
            "Business Intelligence Analyst",
            "Junior Data Scientist",
            "Machine Learning Engineer",
            "Analytics Consultant",
        ],
    },
    "Software Engineer": {
        "field": "Software Development and Engineering",
        "summary": (
            "Designs, develops, tests and maintains applications, "
            "websites, APIs and software systems."
        ),
        "skills": [
            "Programming fundamentals",
            "Data structures and algorithms",
            "Object-oriented programming",
            "Databases and SQL",
            "Testing and debugging",
            "Teamwork and version control",
        ],
        "technologies": [
            "Python, Java or JavaScript",
            "HTML, CSS and React",
            "FastAPI or another backend framework",
            "SQL and PostgreSQL",
            "Git and GitHub",
        ],
        "projects": [
            "Responsive personal portfolio website",
            "Task-management application",
            "CRUD application connected to a database",
            "Documented full-stack application",
        ],
        "pathways": [
            "Consider B.Tech/B.E. in Computer Science, IT or a related branch, or another suitable degree or diploma route.",
            "Learn one programming language well and practise problem-solving.",
            "Build projects, learn Git and understand databases and APIs.",
            "Apply for internships, trainee developer and junior software roles.",
        ],
        "roles": [
            "Frontend Developer",
            "Backend Developer",
            "Full-Stack Developer",
            "QA Automation Engineer",
            "Software Engineer",
        ],
    },
    "Cybersecurity / Ethical Hacker": {
        "field": "Cybersecurity and Information Security",
        "summary": (
            "Protects systems, applications and networks by identifying "
            "security weaknesses and helping organisations reduce risk."
        ),
        "skills": [
            "Networking fundamentals",
            "Linux and operating systems",
            "Python or scripting",
            "Web security basics",
            "Log analysis and troubleshooting",
            "Ethical conduct and documentation",
        ],
        "technologies": [
            "Linux",
            "Networking tools",
            "Python",
            "Wireshark",
            "OWASP learning resources",
            "Virtual machines and authorised labs",
        ],
        "projects": [
            "Build a home cybersecurity lab",
            "Analyse sample security logs",
            "Document a web security lab exercise",
            "Create a basic security checklist for a demo application",
        ],
        "pathways": [
            "Consider a degree or diploma in Computer Science, IT, Cybersecurity or a related area.",
            "Learn networking, Linux, operating systems and scripting.",
            "Practise only in systems and labs where you have permission.",
            "Explore internships and entry-level security or IT support roles.",
        ],
        "roles": [
            "Security Analyst",
            "SOC Analyst",
            "Penetration Tester",
            "Security Engineer",
            "Incident Response Analyst",
        ],
    },
}


# Career keywords are used to provide a relevant starting guide when a
# scoring title is not yet in the detailed catalogue.
DOMAIN_RULES = [
    (
        ["doctor", "mbbs", "physician", "pediatrician", "surgeon"],
        "Healthcare and Medicine",
        "Studies human health, diagnoses conditions and provides medical care. Clinical practice requires the applicable recognised qualifications and registration.",
        ["Biology and chemistry foundations", "Scientific reasoning", "Communication and empathy", "Attention to detail"],
        ["MBBS and applicable recognised medical training", "Clinical exposure through approved programmes", "Required registration and licensing"],
        ["General medical practice", "Specialist medical practice after further training", "Clinical research"],
    ),
    (
        ["nurse", "nursing"],
        "Nursing and Patient Care",
        "Supports patients through clinical care, monitoring, education and coordination with healthcare teams.",
        ["Biology foundations", "Patient communication", "Observation", "Teamwork and responsibility"],
        ["Relevant recognised nursing programme", "Required clinical training", "Applicable registration"],
        ["Staff Nurse", "Specialist Nurse", "Nurse Educator", "Nursing Administrator"],
    ),
    (
        ["psychologist", "counselor", "counsellor", "mental health"],
        "Psychology and Counselling",
        "Studies behaviour and mental processes. The permitted scope of practice depends on the qualification, role and applicable regulations.",
        ["Listening and communication", "Research literacy", "Ethical judgement", "Understanding human behaviour"],
        ["Relevant psychology degree", "Further recognised study or supervised training where required", "Verify professional requirements for the intended role"],
        ["Psychology Research Assistant", "Counselling-related roles subject to qualifications", "Organisational Psychology roles", "Further specialist training"],
    ),
    (
        ["teacher", "professor", "education counselor", "education counsellor"],
        "Education and Teaching",
        "Supports learning through teaching, curriculum planning, assessment or educational guidance.",
        ["Subject knowledge", "Communication", "Lesson planning", "Patience and organisation"],
        ["Relevant subject or education degree", "Teacher-training qualification where applicable", "Eligibility tests or recruitment requirements where applicable"],
        ["Teacher", "Academic Coordinator", "Education Content Developer", "School Leadership after experience"],
    ),
    (
        ["chartered accountant", "accountant", "finance", "bank", "actuary", "tax", "investment", "economist", "cfa", "cma", "company secretary"],
        "Commerce, Finance and Accounting",
        "Works with financial records, analysis, reporting, risk, taxation or investment decisions, depending on the chosen specialisation.",
        ["Numerical reasoning", "Excel and spreadsheet analysis", "Accounting fundamentals", "Accuracy and ethics"],
        ["Relevant commerce, finance, economics or mathematics study", "Professional qualifications where required for the target role", "Internships and practical financial analysis"],
        ["Accounts Executive", "Financial Analyst", "Audit or Tax roles", "Banking roles", "Qualified specialist roles"],
    ),
    (
        ["lawyer", "advocate", "legal", "compliance"],
        "Law and Legal Services",
        "Interprets laws, researches cases, prepares legal documents and advises or represents clients within the permitted scope of practice.",
        ["Reading and writing", "Research", "Reasoning and argument", "Ethics and attention to detail"],
        ["Recognised law degree route", "Applicable professional enrolment and examination requirements for legal practice", "Internships and practical experience"],
        ["Legal Associate", "Corporate Legal Roles", "Compliance Analyst", "Advocate after required steps"],
    ),
    (
        ["ias", "ips", "ifs", "civil services", "government officer", "bank po", "government clerk", "rbi", "sebi", "forest officer"],
        "Government and Public Service",
        "Contributes to administration, public services, regulation or policy through competitive recruitment and role-specific training.",
        ["General awareness", "Reasoning", "Writing and communication", "Discipline and analytical thinking"],
        ["Check the latest official notification for each examination", "Meet the specified age, education and other eligibility criteria", "Prepare for the relevant selection stages"],
        ["Administrative Services", "Regulatory or Banking Roles", "Public-sector specialist roles", "Other eligible government positions"],
    ),
    (
        ["engineer", "engineering", "robotics", "automation", "drone", "automobile", "aeronautical"],
        "Engineering and Technology",
        "Applies mathematics, science and design principles to develop, operate or improve products, infrastructure and technical systems.",
        ["Mathematics and science", "Technical problem-solving", "Design and testing", "Teamwork"],
        ["Relevant engineering degree or diploma", "Practical laboratory and project experience", "Role-specific software or technical skills"],
        ["Graduate Engineer Trainee", "Design Engineer", "Testing Engineer", "Specialist Engineer with experience"],
    ),
    (
        ["architect", "interior designer", "urban planner"],
        "Architecture and the Built Environment",
        "Plans buildings, spaces or urban environments while considering function, design, safety and applicable regulations.",
        ["Spatial reasoning", "Drawing and visualisation", "Design thinking", "Communication"],
        ["Check the recognised qualification and registration requirements for the intended profession", "Develop design portfolio", "Learn relevant design tools"],
        ["Architectural Assistant", "Interior Designer", "Urban Planning-related roles", "Design Consultant"],
    ),
    (
        ["graphic designer", "ui", "ux", "animator", "vfx", "illustrator", "fashion designer", "photographer", "cartoonist"],
        "Design, Animation and Creative Industries",
        "Creates visual communication, digital experiences, products or media for clients, audiences and organisations.",
        ["Visual communication", "Creative problem-solving", "Portfolio development", "Feedback and collaboration"],
        ["Build a portfolio of original work", "Learn tools relevant to your chosen specialisation", "Practise design fundamentals and project briefs"],
        ["Graphic Designer", "UI/UX Designer", "Animator", "Illustrator", "Fashion or Media Design roles"],
    ),
    (
        ["journalist", "writer", "author", "content creator", "copywriter", "reporter", "podcast", "radio jockey", "translator"],
        "Media, Writing and Communication",
        "Creates, verifies, edits or presents information and stories for different audiences and platforms.",
        ["Writing and editing", "Research and fact-checking", "Communication", "Audience awareness"],
        ["Develop writing or media samples", "Practise editing and research", "Consider relevant media, language or communication study"],
        ["Content Writer", "Copywriter", "Reporter", "Editor", "Scriptwriter", "Presenter"],
    ),
    (
        ["film director", "cinematographer", "actor", "music", "singer", "dancer", "choreographer", "sound engineer", "composer"],
        "Performing Arts, Film and Music",
        "Creates or performs artistic work through music, film, theatre, dance, sound or related production.",
        ["Creative practice", "Discipline and rehearsal", "Collaboration", "Portfolio or showreel development"],
        ["Structured practice or relevant arts training", "Build a portfolio, demo reel or performance record", "Gain experience through supervised projects and auditions"],
        ["Assistant or Junior Production Roles", "Performer", "Sound or Music Production Roles", "Independent Creative Work"],
    ),
    (
        ["entrepreneur", "startup", "ceo", "manager", "management consultant", "sales", "business development", "real estate developer", "marketing"],
        "Business, Management and Entrepreneurship",
        "Develops products, serves customers, manages teams or resources, and helps organisations grow.",
        ["Communication and negotiation", "Financial literacy", "Planning", "Decision-making and teamwork"],
        ["Study business fundamentals", "Gain experience through projects, internships or entry-level roles", "Learn customer research, budgeting and business operations"],
        ["Sales or Business Development Executive", "Operations Coordinator", "Management Trainee", "Founder after validating a business idea"],
    ),
    (
        ["veterinary", "animal", "agricultural", "agronomist", "horticulture", "marine biologist", "wildlife", "environmental", "geologist", "esg", "forest"],
        "Environment, Agriculture and Life Sciences",
        "Studies living systems, animals, natural resources, agriculture or environmental challenges.",
        ["Biology and environmental science", "Observation and research", "Data collection", "Fieldwork and reporting"],
        ["Choose a relevant recognised degree or diploma", "Build laboratory, fieldwork or research experience", "Check licensing or recruitment requirements for regulated roles"],
        ["Research Assistant", "Environmental Analyst", "Agriculture-related Specialist", "Field Officer", "Relevant laboratory roles"],
    ),
    (
        ["pilot", "aviation", "cabin crew", "air traffic", "merchant navy", "navy", "army", "defence", "sportsperson", "athlete", "fitness trainer", "physiotherapist", "sports coach"],
        "Aviation, Defence, Sports and Fitness",
        "Combines specialised training with operational, physical, safety or performance requirements, depending on the profession.",
        ["Discipline and teamwork", "Physical or technical readiness as applicable", "Situational awareness", "Communication"],
        ["Verify official age, education, medical and training requirements", "Complete the approved qualification or selection process for the chosen role", "Maintain relevant fitness or practical skills"],
        ["Trainee or Assistant Roles", "Qualified Operational Roles", "Specialist Roles after additional training"],
    ),
]


def _as_number(value):
    """Safely convert a value to float."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _normalise_title(title):
    """Normalise titles for case-insensitive catalogue matching."""
    return re.sub(r"\s+", " ", str(title or "").strip()).casefold()


def get_strengths(intelligence, riasec, limit=3):
    """Return the strongest intelligence and RIASEC dimensions."""
    intelligence = intelligence or {}
    riasec = riasec or {}

    intelligence_scores = sorted(
        (
            (INTELLIGENCE_LABELS.get(key, key.replace("_", " ").title()), _as_number(value))
            for key, value in intelligence.items()
        ),
        key=lambda item: item[1],
        reverse=True,
    )

    riasec_scores = sorted(
        (
            (RIASEC_LABELS.get(key, key.replace("_", " ").title()), _as_number(value))
            for key, value in riasec.items()
        ),
        key=lambda item: item[1],
        reverse=True,
    )

    return {
        "intelligence": intelligence_scores[:max(0, limit)],
        "riasec": riasec_scores[:max(0, limit)],
    }


def _make_general_guidance(career_title):
    """Generate a relevant starter guide for catalogue titles without a
    detailed profile. This is exploratory guidance, not verified career
    research or an eligibility determination.
    """
    title = str(career_title or "Career exploration").strip()
    title_lower = title.casefold()

    selected = None
    for keywords, field, summary, skills, pathways, roles in DOMAIN_RULES:
        if any(keyword in title_lower for keyword in keywords):
            selected = (field, summary, skills, pathways, roles)
            break

    if selected:
        field, summary, skills, pathways, roles = selected
    else:
        field = "Career Exploration"
        summary = (
            f"{title} is a career option to investigate further. "
            "Check the day-to-day work, recognised qualifications, entry "
            "requirements, training costs and current opportunities before "
            "choosing this path."
        )
        skills = [
            "Communication and teamwork",
            "Problem-solving",
            "Digital and research literacy",
            "Professional ethics",
            "Role-specific practical skills",
        ]
        pathways = [
            "Identify the recognised qualifications and eligibility requirements for this exact role.",
            "Compare suitable courses, institutions, duration and total fees using official sources.",
            "Build relevant projects, practical experience or a portfolio.",
            "Check current job descriptions and speak with professionals in the field.",
        ]
        roles = [
            title,
            f"Junior or Trainee {title}",
            f"Specialist {title} after relevant training and experience",
        ]

    return {
        "field": field,
        "summary": summary,
        "skills": skills,
        "technologies": [
            "Use tools and software relevant to the chosen specialisation",
            "Develop digital literacy and documentation skills",
            "Confirm commonly used tools from current job descriptions",
        ],
        "projects": [
            f"Complete a beginner project related to {title}",
            "Create a portfolio or documented practical assignment",
            "Review a real-world problem and propose a solution",
        ],
        "pathways": pathways,
        "roles": roles,
        "catalogue_status": "needs_career_specific_research",
        "research_note": (
            "This is general exploratory guidance. Confirm exact qualifications, "
            "eligibility, fees, course recognition, licensing and employment "
            "requirements with official institutions or regulators."
        ),
    }


def get_career_guidance(career_title):
    """Return career-specific guidance or a domain-matched starter profile."""
    if not career_title:
        return _make_general_guidance("Career exploration")

    requested = _normalise_title(career_title)

    for known_title, profile in CAREER_GUIDANCE.items():
        if _normalise_title(known_title) == requested:
            result = dict(profile)
            result["catalogue_status"] = "starter_profile"
            result["research_note"] = (
                "Review current official course, eligibility and employment "
                "requirements before making an education or career decision."
            )
            return result

    return _make_general_guidance(career_title)
