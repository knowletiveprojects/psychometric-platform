
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



# Exact career profiles aligned with CAREER_PROFILES in scoring.py.
CAREER_GUIDANCE.update({
    'Data Scientist / ML Engineer': {
        'field': 'Data Science and Artificial Intelligence',
        'summary': 'Uses statistics, programming and machine learning to find patterns, build predictive models and support decisions.',
        'skills': 'Python, statistics, probability, SQL, data storytelling',
        'technologies': 'Python, Pandas, NumPy, SQL, scikit-learn, Git',
        'projects': 'Analyse a public dataset; build a prediction model; publish a reproducible notebook',
        'pathways': 'After Class 12 consider CS, mathematics, statistics, engineering or data-science study; learn Python and SQL; build 3 portfolio projects; seek analytics or ML internships.',
        'roles': ['Data Analyst', 'BI Analyst', 'Data Scientist', 'ML Engineer', 'Applied AI Specialist'],
    },
    'Software Engineer': {
        'field': 'Software Development',
        'summary': 'Designs, builds, tests and maintains reliable applications, APIs and systems used by people and organisations.',
        'skills': 'Programming, algorithms, debugging, system design, teamwork',
        'technologies': 'Python/Java/JavaScript, Git, SQL, APIs, testing tools',
        'projects': 'Build a CRUD web app; write automated tests; deploy a documented portfolio project',
        'pathways': 'Choose a suitable CS/IT degree, diploma or alternative learning route; master one language; learn databases and APIs; build and deploy projects; apply for internships.',
        'roles': ['Frontend Developer', 'Backend Developer', 'Full-Stack Developer', 'QA Automation Engineer', 'Software Engineer'],
    },
    'Chartered Accountant (CA)': {
        'field': 'Accounting, Audit and Taxation',
        'summary': 'Analyses accounts, audits records, supports tax compliance and advises organisations on financial controls.',
        'skills': 'Accounting, numerical accuracy, ethics, communication, analytical thinking',
        'technologies': 'Spreadsheets, accounting software, tax and audit tools',
        'projects': 'Prepare sample financial statements; create a budget variance analysis; study an anonymised audit case',
        'pathways': 'Review the current ICAI CA route and eligibility; plan Foundation/Intermediate/Final stages and practical training; practise accounting and Excel; verify current exam rules and fees with ICAI.',
        'roles': ['Audit Associate', 'Tax Associate', 'Financial Reporting Specialist', 'Internal Auditor', 'Chartered Accountant'],
    },
    'Doctor / General Physician': {
        'field': 'Medicine and Clinical Care',
        'summary': 'Assesses symptoms, diagnoses illness, treats patients and coordinates preventive and continuing care.',
        'skills': 'Biology, chemistry, patient communication, sound judgement, empathy',
        'technologies': 'Clinical record systems, evidence-based medical references',
        'projects': 'Create a health-education project from reputable public sources; practise science communication',
        'pathways': 'Check current NEET-UG and recognised medical admission requirements; complete the approved medical degree and required clinical training; obtain applicable registration; pursue further specialisation only through recognised routes.',
        'roles': ['Medical Student', 'Intern', 'General Physician after required qualification', 'Clinical Research Associate', 'Specialist after further training'],
    },
    'Lawyer / Advocate': {
        'field': 'Law and Legal Practice',
        'summary': 'Researches legislation and case law, drafts documents, analyses disputes and advises clients within the permitted scope of practice.',
        'skills': 'Reading, writing, argument, research, ethics',
        'technologies': 'Legal databases, document tools, citation methods',
        'projects': 'Write a case brief from a public judgment; prepare a mock contract checklist; participate in a moot court',
        'pathways': 'Compare recognised 5-year or graduate-entry law routes; build legal writing and research skills; complete internships; verify current Bar Council enrolment and practice requirements.',
        'roles': ['Legal Intern', 'Legal Associate', 'Litigation Associate', 'Corporate Legal Executive', 'Advocate after required enrolment'],
    },
    'Journalist / News Anchor': {
        'field': 'Journalism and Broadcast Media',
        'summary': 'Finds, verifies and communicates news through reporting, interviews, writing, audio or video presentation.',
        'skills': 'Research, fact-checking, interviewing, clear writing, composure',
        'technologies': 'Audio/video editing, newsroom tools, research and verification tools',
        'projects': 'Produce a sourced news explainer; conduct an ethical interview; create a short audio bulletin',
        'pathways': 'Practise reporting and media ethics; build a portfolio of verified stories; learn multimedia production; seek newsroom internships or campus media experience.',
        'roles': ['Reporting Intern', 'Reporter', 'Copy Editor', 'News Producer', 'Anchor with experience'],
    },
    'Entrepreneur / Startup Founder': {
        'field': 'Entrepreneurship and Business',
        'summary': 'Identifies a customer problem, tests a solution, manages costs and develops a sustainable business model.',
        'skills': 'Customer discovery, communication, financial literacy, resilience, decision-making',
        'technologies': 'Spreadsheets, analytics, payment and customer-management tools',
        'projects': 'Interview 10 potential customers; create a low-cost prototype; calculate unit economics',
        'pathways': 'Start with a small validated problem; interview users; test a minimum viable product; track cash flow; understand legal, tax and registration obligations before scaling.',
        'roles': ['Business Development Associate', 'Operations Associate', 'Product or Growth Roles', 'Small Business Owner', 'Startup Founder'],
    },
    'Psychologist / Counselor': {
        'field': 'Psychology and Counselling',
        'summary': 'Studies behaviour and supports people through assessment, research or counselling within the qualifications and scope permitted for the role.',
        'skills': 'Listening, research literacy, empathy, boundaries, ethical judgement',
        'technologies': 'Research methods, survey tools, documentation tools',
        'projects': 'Review a psychology research paper; design an ethical anonymous wellbeing survey; practise reflective listening scenarios',
        'pathways': 'Study psychology at degree level; investigate the further recognised qualifications and supervised practice required for the intended role; verify professional regulations before offering services.',
        'roles': ['Research Assistant', 'HR/People Research Associate', 'Counselling-related roles subject to qualifications', 'Psychology Postgraduate Student', 'Qualified specialist subject to requirements'],
    },
    'Architect / Urban Planner': {
        'field': 'Architecture and Urban Planning',
        'summary': 'Plans buildings, public spaces or urban systems by balancing function, safety, sustainability, design and regulations.',
        'skills': 'Spatial reasoning, drawing, mathematics, design, collaboration',
        'technologies': 'CAD/BIM, GIS, 3D modelling and presentation tools',
        'projects': 'Design a small accessible space; map a neighbourhood walkability issue; create a model and design rationale',
        'pathways': 'Check recognised architecture/planning degree routes and professional registration requirements; develop drawing and digital design skills; build a portfolio; seek studio or planning internships.',
        'roles': ['Design Intern', 'Architectural Assistant', 'Urban Planning Assistant', 'BIM/CAD Specialist', 'Architect or Planner after required qualifications'],
    },
    'Graphic Designer / UI-UX Designer': {
        'field': 'Visual and Digital Product Design',
        'summary': 'Creates visual identities and digital experiences that communicate clearly and help users complete tasks.',
        'skills': 'Visual hierarchy, typography, user empathy, prototyping, critique',
        'technologies': 'Figma or equivalent, vector tools, prototyping and accessibility checkers',
        'projects': 'Redesign a confusing form; create a small brand system; test a prototype with users',
        'pathways': 'Learn design fundamentals and accessibility; build case studies explaining the problem, process and outcome; seek supervised portfolio reviews and internships.',
        'roles': ['Graphic Designer', 'UI Designer', 'UX Research Assistant', 'Product Designer', 'Design Lead with experience'],
    },
    'Film Director / Cinematographer': {
        'field': 'Film and Screen Production',
        'summary': 'Develops a visual story and coordinates performance, camera, lighting, sound and production decisions.',
        'skills': 'Storytelling, visual composition, planning, leadership, collaboration',
        'technologies': 'Camera and lighting equipment, editing software, storyboarding tools',
        'projects': 'Shoot a 60-second short film; storyboard a scene; create a production plan and edit breakdown',
        'pathways': 'Practise with small productions; learn shot design, sound and editing; assemble a showreel; gain set experience and build reliable creative collaborations.',
        'roles': ['Production Assistant', 'Assistant Camera', 'Video Editor', 'Assistant Director', 'Director/Cinematographer with experience'],
    },
    'Sports Coach / Athlete': {
        'field': 'Sports Performance and Coaching',
        'summary': 'Develops athletic performance or helps others improve technique, fitness, tactics and safe training habits.',
        'skills': 'Discipline, movement skills, communication, observation, resilience',
        'technologies': 'Sport-specific equipment, performance logs, video analysis',
        'projects': 'Create a safe training log; analyse technique footage with consent; plan a beginner practice session',
        'pathways': 'Choose a sport and measurable training goals; seek qualified coaching; track progress and recovery; verify recognised coaching certifications and competition pathways.',
        'roles': ['Athlete Development Trainee', 'Assistant Coach', 'Fitness/Sport Programme Assistant', 'Certified Coach', 'Performance Specialist'],
    },
    'Army / Defence Officer': {
        'field': 'Defence and Armed Services',
        'summary': 'Serves in military leadership or technical/operational roles through competitive selection, training and strict service standards.',
        'skills': 'Leadership, fitness, teamwork, discipline, situational judgement',
        'technologies': 'Role-specific technical systems, fitness and aptitude preparation resources',
        'projects': 'Build a safe fitness baseline; practise team leadership; maintain an eligibility and preparation checklist',
        'pathways': 'Check current official NDA/CDS or service-specific notifications; verify age, education, medical and physical standards; prepare for written tests, selection stages and approved training.',
        'roles': ['Officer Cadet', 'Commissioned Officer after selection and training', 'Technical or operational specialisation', 'Leadership appointments with service experience'],
    },
    'HR Manager / Corporate Trainer': {
        'field': 'Human Resources and Learning',
        'summary': 'Supports hiring, employee development, workplace processes and learning programmes aligned with organisational needs.',
        'skills': 'Listening, facilitation, communication, conflict resolution, confidentiality',
        'technologies': 'HRIS, spreadsheets, learning-management systems, survey tools',
        'projects': 'Design an onboarding checklist; create a short training module; analyse anonymised survey feedback',
        'pathways': 'Study HR, psychology, business or a related field; practise interviewing and facilitation; learn employment basics and data privacy; seek HR or learning internships.',
        'roles': ['Recruitment Coordinator', 'HR Executive', 'Learning Coordinator', 'HR Business Partner', 'HR Manager with experience'],
    },
    'Teacher / Professor': {
        'field': 'Education and Teaching',
        'summary': 'Plans learning, explains concepts, assesses progress and adapts instruction to students and subject requirements.',
        'skills': 'Subject knowledge, explanation, patience, assessment, classroom management',
        'technologies': 'Lesson-planning tools, learning platforms, presentation and assessment tools',
        'projects': 'Create a lesson plan; build a rubric; teach a short lesson and reflect on feedback',
        'pathways': 'Choose the subject and age group; verify current teacher-training, eligibility-test and recruitment rules; gain supervised teaching experience; pursue higher study for academic roles as required.',
        'roles': ['Teaching Assistant', 'School Teacher subject to eligibility', 'Academic Coordinator', 'Lecturer/Professor subject to required qualifications'],
    },
    'Civil Engineer': {
        'field': 'Civil and Infrastructure Engineering',
        'summary': 'Plans, designs, constructs or maintains buildings, transport, water and other infrastructure while meeting safety standards.',
        'skills': 'Mathematics, physics, spatial reasoning, planning, safety awareness',
        'technologies': 'CAD/BIM, surveying tools, spreadsheets, structural analysis tools',
        'projects': 'Create a small site-layout model; estimate quantities for a sample project; study a public infrastructure case',
        'pathways': 'Compare recognised civil engineering degree/diploma routes; strengthen maths and mechanics; learn drawings and safety; seek site/lab internships; verify any role-specific registration rules.',
        'roles': ['Site Engineer Trainee', 'Quantity Surveying Assistant', 'Design Engineer', 'Project Engineer', 'Civil Engineer with experience'],
    },
    'Music Producer / Sound Engineer': {
        'field': 'Music Production and Audio Engineering',
        'summary': 'Records, edits, mixes or produces sound for music, film, games, live events and digital media.',
        'skills': 'Listening, rhythm, technical curiosity, collaboration, attention to detail',
        'technologies': 'DAW software, microphones, audio interfaces, monitoring tools',
        'projects': 'Record and mix a short track; create a sound-effects reel; document a basic mixing workflow',
        'pathways': 'Practise listening and audio fundamentals; learn recording, editing and mixing; build a diverse demo reel; gain experience through supervised sessions or small productions.',
        'roles': ['Studio Assistant', 'Audio Editor', 'Live Sound Assistant', 'Music Producer', 'Sound Engineer with experience'],
    },
    'Environmental Scientist / ESG Analyst': {
        'field': 'Environment, Sustainability and ESG',
        'summary': 'Measures environmental conditions or evaluates sustainability risks, reporting and improvement opportunities for organisations.',
        'skills': 'Natural science, data analysis, field observation, report writing, systems thinking',
        'technologies': 'GIS, spreadsheets, environmental sampling and reporting tools',
        'projects': 'Analyse a public air/water dataset; map local waste issues; write a sourced sustainability brief',
        'pathways': 'Study environmental science, engineering, ecology or related subjects; gain field/data skills; learn applicable reporting frameworks; seek research, lab or sustainability internships.',
        'roles': ['Field/Lab Assistant', 'Environmental Analyst', 'Sustainability Coordinator', 'ESG Analyst', 'Environmental Specialist'],
    },
    'IAS / IPS Officer (Civil Services)': {
        'field': 'Civil Services and Public Administration',
        'summary': 'Works in public administration, policy implementation, law-and-order leadership or other duties defined by the service and posting.',
        'skills': 'Reading, writing, analysis, judgement, public service orientation',
        'technologies': 'Official syllabus, current-affairs notes, answer-writing practice',
        'projects': 'Write a policy brief on a local issue; compare two government programme reports; practise structured essay answers',
        'pathways': 'Read the latest UPSC notification and syllabus; verify eligibility and exam stages; build consistent study and answer-writing habits; use official sources and avoid guaranteed-selection claims.',
        'roles': ['Civil Services Aspirant', 'Selected candidate after competitive process and training', 'Administrative or police service roles subject to allocation'],
    },
    'Fashion Designer': {
        'field': 'Fashion and Textile Design',
        'summary': 'Develops clothing or textile concepts from research and sketches through materials, construction, fitting and presentation.',
        'skills': 'Visual creativity, material knowledge, trend research, detail, communication',
        'technologies': 'Sketching tools, pattern-making, CAD, sewing and portfolio tools',
        'projects': 'Create a capsule collection concept; document fabric choices; produce a prototype and process portfolio',
        'pathways': 'Learn drawing, textiles and construction; compare recognised design courses; build a process-led portfolio; gain production, styling or design internships.',
        'roles': ['Design Assistant', 'Textile/Print Assistant', 'Fashion Stylist Assistant', 'Fashion Designer', 'Design/Collection Lead with experience'],
    },
    'Pilot / Aviation Officer': {
        'field': 'Aviation Operations',
        'summary': 'Operates or supports aircraft and aviation systems under strict safety, medical, licensing and operational requirements.',
        'skills': 'Mathematics, situational awareness, communication, discipline, decision-making',
        'technologies': 'Approved simulators, aviation theory materials, checklists',
        'projects': 'Research an aviation role and its licence requirements; practise a structured checklist exercise; learn aviation weather basics',
        'pathways': 'Before paying fees, verify the regulator-approved training route, medical standards, licence requirements and total costs; compare approved providers and maintain academic and safety discipline.',
        'roles': ['Aviation Trainee', 'Flight Training Candidate subject to eligibility', 'Licensed Pilot after required training and checks', 'Aviation Operations Roles'],
    },
    'Bank PO / Finance Officer': {
        'field': 'Banking and Financial Services',
        'summary': 'Handles customer financial needs, banking operations, risk controls or financial analysis according to role and employer.',
        'skills': 'Numerical reasoning, accuracy, communication, ethics, decision-making',
        'technologies': 'Spreadsheets, financial statements, banking systems and aptitude practice',
        'projects': 'Build a personal-budget model; analyse a sample balance sheet; practise data interpretation questions',
        'pathways': 'Check current bank recruitment notifications and eligibility; strengthen quantitative aptitude, reasoning and English; learn banking basics and compliance; practise timed mock tests.',
        'roles': ['Banking Exam Candidate', 'Probationary Officer after selection', 'Credit/Operations Officer', 'Branch or Relationship Manager with experience'],
    },
    'Veterinary Doctor': {
        'field': 'Veterinary Medicine and Animal Health',
        'summary': 'Diagnoses and treats animal illness, supports welfare and public health, and may work in clinics, farms, laboratories or government services.',
        'skills': 'Biology, animal handling, observation, empathy, scientific reasoning',
        'technologies': 'Clinical records, diagnostic tools, laboratory equipment',
        'projects': 'Prepare an evidence-based animal-welfare information sheet; learn zoonosis prevention from official sources',
        'pathways': 'Check current veterinary admission requirements and recognised degree routes; complete required clinical training and registration; gain supervised animal-care exposure; verify public-service recruitment rules.',
        'roles': ['Veterinary Student', 'Clinical Intern', 'Veterinary Officer subject to eligibility', 'Veterinary Practitioner after required qualification', 'Specialist with further training'],
    },
    'Content Writer / Author': {
        'field': 'Writing, Publishing and Content Strategy',
        'summary': 'Researches and shapes information or stories into clear content for readers, brands, publications or digital platforms.',
        'skills': 'Writing, editing, research, audience awareness, fact-checking',
        'technologies': 'Word processors, editorial tools, content-management systems, analytics',
        'projects': 'Publish three sourced explainers; edit a draft for clarity; create a portfolio across formats',
        'pathways': 'Practise writing and editing; choose a niche; verify facts and permissions; build a portfolio; seek editorial feedback, internships or freelance briefs.',
        'roles': ['Writing Intern', 'Content Writer', 'Copywriter/Editor', 'Content Strategist', 'Author with a developed body of work'],
    },
    'Cybersecurity / Ethical Hacker': {
        'field': 'Cybersecurity and Information Security',
        'summary': 'Finds and helps remediate weaknesses in systems, networks and applications through authorised testing and defensive security work.',
        'skills': 'Networking, Linux, scripting, investigation, documentation, ethics',
        'technologies': 'Linux, Wireshark, safe virtual labs, OWASP learning resources',
        'projects': 'Analyse sample logs; harden a test virtual machine; write a vulnerability report for an authorised lab',
        'pathways': 'Learn networking and operating systems; practise only in permitted labs; document findings and remediation; build security fundamentals before pursuing role-relevant certifications or internships.',
        'roles': ['IT Support/Security Trainee', 'SOC Analyst', 'Security Analyst', 'Penetration Tester with authorised scope', 'Security Engineer'],
    },
})


# Automatically expanded exact-title catalogue: covers every title listed in CAREER_MAP.
CAREER_GUIDANCE.update({'Financial Analyst / CFA': {'field': 'Finance, Accounting and Governance',
                             'summary': 'Financial Analyst / CFA: Works with financial records, analysis, '
                                        'risk, regulation, markets or organisational decisions.',
                             'skills': ['Numeracy and analytical reasoning',
                                        'Excel/spreadsheets and data interpretation',
                                        'Accuracy, confidentiality and professional ethics',
                                        'Financial reporting, regulation or research relevant to the role'],
                             'technologies': ['Tools and methods used in Financial Analyst / CFA',
                                              'Spreadsheets, digital research and clear documentation where '
                                              'relevant',
                                              'Role-specific platforms confirmed from current job '
                                              'descriptions'],
                             'projects': ['Complete a beginner project or practical exercise related to '
                                          'Financial Analyst / CFA',
                                          'Create a portfolio, case study or documented practical assignment '
                                          'for Financial Analyst / CFA',
                                          'Analyse a real-world challenge relevant to Financial Analyst / '
                                          'CFA and present a safe, evidence-based solution'],
                             'pathways': ['Check the official qualification or recruitment route (for '
                                          'example, professional-body exams or public recruitment notices).',
                                          'Build accounting, finance, economics, spreadsheet and analytical '
                                          'foundations as appropriate.',
                                          'Practise with case studies, financial models or compliant sample '
                                          'reports.',
                                          'Verify current exam rules, eligibility, registration and '
                                          'role-specific certifications from official sources.'],
                             'roles': ['Financial Analyst / CFA',
                                       'Junior / Trainee Financial Analyst / CFA',
                                       'Specialist or senior Financial Analyst / CFA after required training '
                                       'and experience'],
                             'indicative_salary_india': 'Compensation varies by qualification, employer, '
                                                        'city, performance and experience; public-sector pay '
                                                        'follows official notices.',
                             'education_cost_india': 'Include professional-body registration, exam attempts, '
                                                     'coaching if chosen, study materials and degree '
                                                     'tuition; official fees change.',
                             'future_outlook': 'For Financial Analyst / CFA, assess current demand using '
                                               'recent India-based job listings, official recruitment '
                                               'notices and relevant industry reports; outlook is not '
                                               'guaranteed.',
                             'recommended_next_steps': ['Read current official qualification and eligibility '
                                                        'rules for Financial Analyst / CFA.',
                                                        'Compare at least three recognised training routes '
                                                        'for Financial Analyst / CFA, including total fees '
                                                        'and duration.',
                                                        'Complete one relevant project, portfolio piece, '
                                                        'field exercise or supervised placement for '
                                                        'Financial Analyst / CFA.',
                                                        'Speak to a working professional and review recent '
                                                        'vacancies before committing to a course.'],
                             'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                             'research_note': 'Role-specific starter guidance generated from the career '
                                              'catalogue category. Verify licensing, eligibility, salaries, '
                                              'course fees and outlook with official/current sources.'},
 'Research Scientist (ISRO/DRDO)': {'field': 'Environment, Agriculture and Scientific Research',
                                    'summary': 'Research Scientist (ISRO/DRDO): Uses scientific methods, '
                                               'fieldwork, laboratory work or evidence analysis to '
                                               'understand natural systems and solve specialised problems.',
                                    'skills': ['Biology, chemistry, physics or earth-science foundations as '
                                               'relevant',
                                               'Data collection, observation and analysis',
                                               'Laboratory/field safety and accurate records',
                                               'Scientific writing and evidence evaluation'],
                                    'technologies': ['Tools and methods used in Research Scientist '
                                                     '(ISRO/DRDO)',
                                                     'Spreadsheets, digital research and clear documentation '
                                                     'where relevant',
                                                     'Role-specific platforms confirmed from current job '
                                                     'descriptions'],
                                    'projects': ['Complete a beginner project or practical exercise related '
                                                 'to Research Scientist (ISRO/DRDO)',
                                                 'Create a portfolio, case study or documented practical '
                                                 'assignment for Research Scientist (ISRO/DRDO)',
                                                 'Analyse a real-world challenge relevant to Research '
                                                 'Scientist (ISRO/DRDO) and present a safe, evidence-based '
                                                 'solution'],
                                    'pathways': ['Identify the exact specialisation and required science '
                                                 'subjects.',
                                                 'Choose a recognised relevant degree and check whether '
                                                 'postgraduate study is expected.',
                                                 'Build field, lab, data-analysis or research experience '
                                                 'under appropriate supervision.',
                                                 'Check government recruitment, research fellowship and '
                                                 'professional registration requirements where applicable.'],
                                    'roles': ['Research Scientist (ISRO/DRDO)',
                                              'Junior / Trainee Research Scientist (ISRO/DRDO)',
                                              'Specialist or senior Research Scientist (ISRO/DRDO) after '
                                              'required training and experience'],
                                    'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                               'research funding, government recruitment and '
                                                               'location.',
                                    'education_cost_india': 'Budget for tuition, lab/fieldwork, equipment, '
                                                            'travel and postgraduate study; use official '
                                                            'institution fee schedules.',
                                    'future_outlook': 'For Research Scientist (ISRO/DRDO), assess current '
                                                      'demand using recent India-based job listings, '
                                                      'official recruitment notices and relevant industry '
                                                      'reports; outlook is not guaranteed.',
                                    'recommended_next_steps': ['Read current official qualification and '
                                                               'eligibility rules for Research Scientist '
                                                               '(ISRO/DRDO).',
                                                               'Compare at least three recognised training '
                                                               'routes for Research Scientist (ISRO/DRDO), '
                                                               'including total fees and duration.',
                                                               'Complete one relevant project, portfolio '
                                                               'piece, field exercise or supervised '
                                                               'placement for Research Scientist '
                                                               '(ISRO/DRDO).',
                                                               'Speak to a working professional and review '
                                                               'recent vacancies before committing to a '
                                                               'course.'],
                                    'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                    'research_note': 'Role-specific starter guidance generated from the '
                                                     'career catalogue category. Verify licensing, '
                                                     'eligibility, salaries, course fees and outlook with '
                                                     'official/current sources.'},
 'Actuary / Actuarial Science': {'field': 'Engineering, Technology and Applied Science',
                                 'summary': 'Actuary / Actuarial Science: Applies technical knowledge to '
                                            'design, build, analyse, secure or operate systems and solve '
                                            'practical problems.',
                                 'skills': ['Mathematics and technical fundamentals',
                                            'Structured problem-solving and troubleshooting',
                                            'Role-specific software, tools or laboratory practice',
                                            'Project documentation, teamwork and safety'],
                                 'technologies': ['Tools and methods used in Actuary / Actuarial Science',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Actuary / Actuarial Science',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Actuary / Actuarial Science',
                                              'Analyse a real-world challenge relevant to Actuary / '
                                              'Actuarial Science and present a safe, evidence-based '
                                              'solution'],
                                 'pathways': ['Compare accredited degree, diploma and approved alternative '
                                              'routes for the exact specialisation.',
                                              'Build foundations in mathematics, science and the relevant '
                                              'technical tools.',
                                              'Complete documented practical projects or supervised lab '
                                              'work.',
                                              'Check role-specific licences, certifications and current job '
                                              'descriptions before applying.'],
                                 'roles': ['Actuary / Actuarial Science',
                                           'Junior / Trainee Actuary / Actuarial Science',
                                           'Specialist or senior Actuary / Actuarial Science after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Demand and pay differ by specialisation, '
                                                            'skills, city and industry; check current job '
                                                            'postings and salary surveys.',
                                 'education_cost_india': 'Costs depend on institution, equipment, software, '
                                                         'lab access, certification and whether a licence or '
                                                         'flight/sea training is required.',
                                 'future_outlook': 'For Actuary / Actuarial Science, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Actuary / Actuarial '
                                                            'Science.',
                                                            'Compare at least three recognised training '
                                                            'routes for Actuary / Actuarial Science, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Actuary / Actuarial Science.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Business Analytics Specialist': {'field': 'Engineering, Technology and Applied Science',
                                   'summary': 'Business Analytics Specialist: Applies technical knowledge to '
                                              'design, build, analyse, secure or operate systems and solve '
                                              'practical problems.',
                                   'skills': ['Mathematics and technical fundamentals',
                                              'Structured problem-solving and troubleshooting',
                                              'Role-specific software, tools or laboratory practice',
                                              'Project documentation, teamwork and safety'],
                                   'technologies': ['Tools and methods used in Business Analytics Specialist',
                                                    'Spreadsheets, digital research and clear documentation '
                                                    'where relevant',
                                                    'Role-specific platforms confirmed from current job '
                                                    'descriptions'],
                                   'projects': ['Complete a beginner project or practical exercise related '
                                                'to Business Analytics Specialist',
                                                'Create a portfolio, case study or documented practical '
                                                'assignment for Business Analytics Specialist',
                                                'Analyse a real-world challenge relevant to Business '
                                                'Analytics Specialist and present a safe, evidence-based '
                                                'solution'],
                                   'pathways': ['Compare accredited degree, diploma and approved alternative '
                                                'routes for the exact specialisation.',
                                                'Build foundations in mathematics, science and the relevant '
                                                'technical tools.',
                                                'Complete documented practical projects or supervised lab '
                                                'work.',
                                                'Check role-specific licences, certifications and current '
                                                'job descriptions before applying.'],
                                   'roles': ['Business Analytics Specialist',
                                             'Junior / Trainee Business Analytics Specialist',
                                             'Specialist or senior Business Analytics Specialist after '
                                             'required training and experience'],
                                   'indicative_salary_india': 'Demand and pay differ by specialisation, '
                                                              'skills, city and industry; check current job '
                                                              'postings and salary surveys.',
                                   'education_cost_india': 'Costs depend on institution, equipment, '
                                                           'software, lab access, certification and whether '
                                                           'a licence or flight/sea training is required.',
                                   'future_outlook': 'For Business Analytics Specialist, assess current '
                                                     'demand using recent India-based job listings, official '
                                                     'recruitment notices and relevant industry reports; '
                                                     'outlook is not guaranteed.',
                                   'recommended_next_steps': ['Read current official qualification and '
                                                              'eligibility rules for Business Analytics '
                                                              'Specialist.',
                                                              'Compare at least three recognised training '
                                                              'routes for Business Analytics Specialist, '
                                                              'including total fees and duration.',
                                                              'Complete one relevant project, portfolio '
                                                              'piece, field exercise or supervised placement '
                                                              'for Business Analytics Specialist.',
                                                              'Speak to a working professional and review '
                                                              'recent vacancies before committing to a '
                                                              'course.'],
                                   'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                   'research_note': 'Role-specific starter guidance generated from the '
                                                    'career catalogue category. Verify licensing, '
                                                    'eligibility, salaries, course fees and outlook with '
                                                    'official/current sources.'},
 'Economist / Policy Analyst': {'field': 'Finance, Accounting and Governance',
                                'summary': 'Economist / Policy Analyst: Works with financial records, '
                                           'analysis, risk, regulation, markets or organisational decisions.',
                                'skills': ['Numeracy and analytical reasoning',
                                           'Excel/spreadsheets and data interpretation',
                                           'Accuracy, confidentiality and professional ethics',
                                           'Financial reporting, regulation or research relevant to the '
                                           'role'],
                                'technologies': ['Tools and methods used in Economist / Policy Analyst',
                                                 'Spreadsheets, digital research and clear documentation '
                                                 'where relevant',
                                                 'Role-specific platforms confirmed from current job '
                                                 'descriptions'],
                                'projects': ['Complete a beginner project or practical exercise related to '
                                             'Economist / Policy Analyst',
                                             'Create a portfolio, case study or documented practical '
                                             'assignment for Economist / Policy Analyst',
                                             'Analyse a real-world challenge relevant to Economist / Policy '
                                             'Analyst and present a safe, evidence-based solution'],
                                'pathways': ['Check the official qualification or recruitment route (for '
                                             'example, professional-body exams or public recruitment '
                                             'notices).',
                                             'Build accounting, finance, economics, spreadsheet and '
                                             'analytical foundations as appropriate.',
                                             'Practise with case studies, financial models or compliant '
                                             'sample reports.',
                                             'Verify current exam rules, eligibility, registration and '
                                             'role-specific certifications from official sources.'],
                                'roles': ['Economist / Policy Analyst',
                                          'Junior / Trainee Economist / Policy Analyst',
                                          'Specialist or senior Economist / Policy Analyst after required '
                                          'training and experience'],
                                'indicative_salary_india': 'Compensation varies by qualification, employer, '
                                                           'city, performance and experience; public-sector '
                                                           'pay follows official notices.',
                                'education_cost_india': 'Include professional-body registration, exam '
                                                        'attempts, coaching if chosen, study materials and '
                                                        'degree tuition; official fees change.',
                                'future_outlook': 'For Economist / Policy Analyst, assess current demand '
                                                  'using recent India-based job listings, official '
                                                  'recruitment notices and relevant industry reports; '
                                                  'outlook is not guaranteed.',
                                'recommended_next_steps': ['Read current official qualification and '
                                                           'eligibility rules for Economist / Policy '
                                                           'Analyst.',
                                                           'Compare at least three recognised training '
                                                           'routes for Economist / Policy Analyst, including '
                                                           'total fees and duration.',
                                                           'Complete one relevant project, portfolio piece, '
                                                           'field exercise or supervised placement for '
                                                           'Economist / Policy Analyst.',
                                                           'Speak to a working professional and review '
                                                           'recent vacancies before committing to a course.'],
                                'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                'research_note': 'Role-specific starter guidance generated from the career '
                                                 'catalogue category. Verify licensing, eligibility, '
                                                 'salaries, course fees and outlook with official/current '
                                                 'sources.'},
 'HR / Talent Acquisition Manager': {'field': 'Business, Management and Entrepreneurship',
                                     'summary': 'HR / Talent Acquisition Manager: Coordinates people, '
                                                'customers, services, operations or business growth using '
                                                'commercial judgement and measurable goals.',
                                     'skills': ['Communication, negotiation and teamwork',
                                                'Planning, budgeting and data-informed decisions',
                                                'Customer or stakeholder understanding',
                                                'Digital tools and professional ethics'],
                                     'technologies': ['Tools and methods used in HR / Talent Acquisition '
                                                      'Manager',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to HR / Talent Acquisition Manager',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for HR / Talent Acquisition Manager',
                                                  'Analyse a real-world challenge relevant to HR / Talent '
                                                  'Acquisition Manager and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Learn the industry and target role through a relevant '
                                                  'degree, diploma or practical experience.',
                                                  'Build evidence through internships, sales/service '
                                                  'projects or a small validated business experiment.',
                                                  'Practise spreadsheets, presentations, customer research '
                                                  'and project planning.',
                                                  'Review entry-level job descriptions and speak with '
                                                  'practitioners in the target sector.'],
                                     'roles': ['HR / Talent Acquisition Manager',
                                               'Junior / Trainee HR / Talent Acquisition Manager',
                                               'Specialist or senior HR / Talent Acquisition Manager after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Pay varies widely by industry, location, '
                                                                'seniority, targets and whether income is '
                                                                'salaried or entrepreneurial.',
                                     'education_cost_india': 'Costs depend on degree/course choice; '
                                                             'entrepreneurship also requires a separate '
                                                             'business budget and risk planning.',
                                     'future_outlook': 'For HR / Talent Acquisition Manager, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for HR / Talent '
                                                                'Acquisition Manager.',
                                                                'Compare at least three recognised training '
                                                                'routes for HR / Talent Acquisition Manager, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for HR / Talent Acquisition '
                                                                'Manager.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'School Teacher / Government Teacher': {'field': 'Education, Training and Research',
                                         'summary': 'School Teacher / Government Teacher: Supports learning, '
                                                    'assessment, research or professional development '
                                                    'through subject expertise and structured communication.',
                                         'skills': ['Subject knowledge and clear explanation',
                                                    'Lesson, training or research planning',
                                                    'Feedback, assessment and learner support',
                                                    'Digital learning tools and professional ethics'],
                                         'technologies': ['Tools and methods used in School Teacher / '
                                                          'Government Teacher',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to School Teacher / Government Teacher',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for School Teacher / Government '
                                                      'Teacher',
                                                      'Analyse a real-world challenge relevant to School '
                                                      'Teacher / Government Teacher and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Choose the subject and age/group you want to work '
                                                      'with.',
                                                      'Check recognised teacher-training, postgraduate, '
                                                      'eligibility-test or research requirements for the '
                                                      'target role.',
                                                      'Create sample lessons, training materials, research '
                                                      'work or a teaching portfolio.',
                                                      'Gain supervised teaching/training experience and '
                                                      'check current recruitment criteria.'],
                                         'roles': ['School Teacher / Government Teacher',
                                                   'Junior / Trainee School Teacher / Government Teacher',
                                                   'Specialist or senior School Teacher / Government Teacher '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Opportunities depend on subject, '
                                                                    'institution, qualifications, location '
                                                                    'and public/private recruitment cycles.',
                                         'education_cost_india': 'Costs depend on degree, teacher-training '
                                                                 'qualification, eligibility tests, research '
                                                                 'fees and institution; confirm official fee '
                                                                 'schedules.',
                                         'future_outlook': 'For School Teacher / Government Teacher, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for School Teacher / '
                                                                    'Government Teacher.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for School Teacher / '
                                                                    'Government Teacher, including total '
                                                                    'fees and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for School Teacher '
                                                                    '/ Government Teacher.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Education Counselor / Career Counselor': {'field': 'Education, Training and Research',
                                            'summary': 'Education Counselor / Career Counselor: Supports '
                                                       'learning, assessment, research or professional '
                                                       'development through subject expertise and structured '
                                                       'communication.',
                                            'skills': ['Subject knowledge and clear explanation',
                                                       'Lesson, training or research planning',
                                                       'Feedback, assessment and learner support',
                                                       'Digital learning tools and professional ethics'],
                                            'technologies': ['Tools and methods used in Education Counselor '
                                                             '/ Career Counselor',
                                                             'Spreadsheets, digital research and clear '
                                                             'documentation where relevant',
                                                             'Role-specific platforms confirmed from current '
                                                             'job descriptions'],
                                            'projects': ['Complete a beginner project or practical exercise '
                                                         'related to Education Counselor / Career Counselor',
                                                         'Create a portfolio, case study or documented '
                                                         'practical assignment for Education Counselor / '
                                                         'Career Counselor',
                                                         'Analyse a real-world challenge relevant to '
                                                         'Education Counselor / Career Counselor and present '
                                                         'a safe, evidence-based solution'],
                                            'pathways': ['Choose the subject and age/group you want to work '
                                                         'with.',
                                                         'Check recognised teacher-training, postgraduate, '
                                                         'eligibility-test or research requirements for the '
                                                         'target role.',
                                                         'Create sample lessons, training materials, '
                                                         'research work or a teaching portfolio.',
                                                         'Gain supervised teaching/training experience and '
                                                         'check current recruitment criteria.'],
                                            'roles': ['Education Counselor / Career Counselor',
                                                      'Junior / Trainee Education Counselor / Career '
                                                      'Counselor',
                                                      'Specialist or senior Education Counselor / Career '
                                                      'Counselor after required training and experience'],
                                            'indicative_salary_india': 'Opportunities depend on subject, '
                                                                       'institution, qualifications, '
                                                                       'location and public/private '
                                                                       'recruitment cycles.',
                                            'education_cost_india': 'Costs depend on degree, '
                                                                    'teacher-training qualification, '
                                                                    'eligibility tests, research fees and '
                                                                    'institution; confirm official fee '
                                                                    'schedules.',
                                            'future_outlook': 'For Education Counselor / Career Counselor, '
                                                              'assess current demand using recent '
                                                              'India-based job listings, official '
                                                              'recruitment notices and relevant industry '
                                                              'reports; outlook is not guaranteed.',
                                            'recommended_next_steps': ['Read current official qualification '
                                                                       'and eligibility rules for Education '
                                                                       'Counselor / Career Counselor.',
                                                                       'Compare at least three recognised '
                                                                       'training routes for Education '
                                                                       'Counselor / Career Counselor, '
                                                                       'including total fees and duration.',
                                                                       'Complete one relevant project, '
                                                                       'portfolio piece, field exercise or '
                                                                       'supervised placement for Education '
                                                                       'Counselor / Career Counselor.',
                                                                       'Speak to a working professional and '
                                                                       'review recent vacancies before '
                                                                       'committing to a course.'],
                                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                            'research_note': 'Role-specific starter guidance generated from '
                                                             'the career catalogue category. Verify '
                                                             'licensing, eligibility, salaries, course fees '
                                                             'and outlook with official/current sources.'},
 'Corporate Trainer': {'field': 'Education, Training and Research',
                       'summary': 'Corporate Trainer: Supports learning, assessment, research or '
                                  'professional development through subject expertise and structured '
                                  'communication.',
                       'skills': ['Subject knowledge and clear explanation',
                                  'Lesson, training or research planning',
                                  'Feedback, assessment and learner support',
                                  'Digital learning tools and professional ethics'],
                       'technologies': ['Tools and methods used in Corporate Trainer',
                                        'Spreadsheets, digital research and clear documentation where '
                                        'relevant',
                                        'Role-specific platforms confirmed from current job descriptions'],
                       'projects': ['Complete a beginner project or practical exercise related to Corporate '
                                    'Trainer',
                                    'Create a portfolio, case study or documented practical assignment for '
                                    'Corporate Trainer',
                                    'Analyse a real-world challenge relevant to Corporate Trainer and '
                                    'present a safe, evidence-based solution'],
                       'pathways': ['Choose the subject and age/group you want to work with.',
                                    'Check recognised teacher-training, postgraduate, eligibility-test or '
                                    'research requirements for the target role.',
                                    'Create sample lessons, training materials, research work or a teaching '
                                    'portfolio.',
                                    'Gain supervised teaching/training experience and check current '
                                    'recruitment criteria.'],
                       'roles': ['Corporate Trainer',
                                 'Junior / Trainee Corporate Trainer',
                                 'Specialist or senior Corporate Trainer after required training and '
                                 'experience'],
                       'indicative_salary_india': 'Opportunities depend on subject, institution, '
                                                  'qualifications, location and public/private recruitment '
                                                  'cycles.',
                       'education_cost_india': 'Costs depend on degree, teacher-training qualification, '
                                               'eligibility tests, research fees and institution; confirm '
                                               'official fee schedules.',
                       'future_outlook': 'For Corporate Trainer, assess current demand using recent '
                                         'India-based job listings, official recruitment notices and '
                                         'relevant industry reports; outlook is not guaranteed.',
                       'recommended_next_steps': ['Read current official qualification and eligibility rules '
                                                  'for Corporate Trainer.',
                                                  'Compare at least three recognised training routes for '
                                                  'Corporate Trainer, including total fees and duration.',
                                                  'Complete one relevant project, portfolio piece, field '
                                                  'exercise or supervised placement for Corporate Trainer.',
                                                  'Speak to a working professional and review recent '
                                                  'vacancies before committing to a course.'],
                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                       'research_note': 'Role-specific starter guidance generated from the career catalogue '
                                        'category. Verify licensing, eligibility, salaries, course fees and '
                                        'outlook with official/current sources.'},
 'Hotel Manager / Hospitality Manager': {'field': 'Business, Management and Entrepreneurship',
                                         'summary': 'Hotel Manager / Hospitality Manager: Coordinates '
                                                    'people, customers, services, operations or business '
                                                    'growth using commercial judgement and measurable goals.',
                                         'skills': ['Communication, negotiation and teamwork',
                                                    'Planning, budgeting and data-informed decisions',
                                                    'Customer or stakeholder understanding',
                                                    'Digital tools and professional ethics'],
                                         'technologies': ['Tools and methods used in Hotel Manager / '
                                                          'Hospitality Manager',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Hotel Manager / Hospitality Manager',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Hotel Manager / Hospitality '
                                                      'Manager',
                                                      'Analyse a real-world challenge relevant to Hotel '
                                                      'Manager / Hospitality Manager and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Learn the industry and target role through a relevant '
                                                      'degree, diploma or practical experience.',
                                                      'Build evidence through internships, sales/service '
                                                      'projects or a small validated business experiment.',
                                                      'Practise spreadsheets, presentations, customer '
                                                      'research and project planning.',
                                                      'Review entry-level job descriptions and speak with '
                                                      'practitioners in the target sector.'],
                                         'roles': ['Hotel Manager / Hospitality Manager',
                                                   'Junior / Trainee Hotel Manager / Hospitality Manager',
                                                   'Specialist or senior Hotel Manager / Hospitality Manager '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Pay varies widely by industry, '
                                                                    'location, seniority, targets and '
                                                                    'whether income is salaried or '
                                                                    'entrepreneurial.',
                                         'education_cost_india': 'Costs depend on degree/course choice; '
                                                                 'entrepreneurship also requires a separate '
                                                                 'business budget and risk planning.',
                                         'future_outlook': 'For Hotel Manager / Hospitality Manager, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Hotel Manager / '
                                                                    'Hospitality Manager.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Hotel Manager / '
                                                                    'Hospitality Manager, including total '
                                                                    'fees and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Hotel Manager '
                                                                    '/ Hospitality Manager.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Public Relations Executive': {'field': 'Creative Media, Communication and Design',
                                'summary': 'Public Relations Executive: Creates stories, experiences, '
                                           'visuals, performances or communication materials for a defined '
                                           'audience.',
                                'skills': ['Creative development and audience awareness',
                                           'Portfolio-building and revision from feedback',
                                           'Communication, collaboration and deadlines',
                                           'Relevant production, design, language or editing tools'],
                                'technologies': ['Tools and methods used in Public Relations Executive',
                                                 'Spreadsheets, digital research and clear documentation '
                                                 'where relevant',
                                                 'Role-specific platforms confirmed from current job '
                                                 'descriptions'],
                                'projects': ['Complete a beginner project or practical exercise related to '
                                             'Public Relations Executive',
                                             'Create a portfolio, case study or documented practical '
                                             'assignment for Public Relations Executive',
                                             'Analyse a real-world challenge relevant to Public Relations '
                                             'Executive and present a safe, evidence-based solution'],
                                'pathways': ['Study the craft through a suitable course, mentorship or '
                                             'structured self-learning route.',
                                             'Build a portfolio/showreel with original work relevant to the '
                                             'target role.',
                                             'Practise with realistic briefs and document your creative '
                                             'process.',
                                             'Seek internships, auditions, commissions or entry-level '
                                             'projects; check contract and copyright basics.'],
                                'roles': ['Public Relations Executive',
                                          'Junior / Trainee Public Relations Executive',
                                          'Specialist or senior Public Relations Executive after required '
                                          'training and experience'],
                                'indicative_salary_india': 'Income may be project-based or variable; results '
                                                           'depend on portfolio quality, network, niche and '
                                                           'experience.',
                                'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                        'formal design/media programmes; budget for '
                                                        'software, equipment, materials and production.',
                                'future_outlook': 'For Public Relations Executive, assess current demand '
                                                  'using recent India-based job listings, official '
                                                  'recruitment notices and relevant industry reports; '
                                                  'outlook is not guaranteed.',
                                'recommended_next_steps': ['Read current official qualification and '
                                                           'eligibility rules for Public Relations '
                                                           'Executive.',
                                                           'Compare at least three recognised training '
                                                           'routes for Public Relations Executive, including '
                                                           'total fees and duration.',
                                                           'Complete one relevant project, portfolio piece, '
                                                           'field exercise or supervised placement for '
                                                           'Public Relations Executive.',
                                                           'Speak to a working professional and review '
                                                           'recent vacancies before committing to a course.'],
                                'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                'research_note': 'Role-specific starter guidance generated from the career '
                                                 'catalogue category. Verify licensing, eligibility, '
                                                 'salaries, course fees and outlook with official/current '
                                                 'sources.'},
 'Social Worker / NGO Officer': {'field': 'Public Service, Defence and Social Impact',
                                 'summary': 'Social Worker / NGO Officer: Serves communities or public '
                                            'institutions through administration, protection, policy, '
                                            'development or disciplined operational work.',
                                 'skills': ['Communication and public-service orientation',
                                            'Ethical judgement and accountability',
                                            'Role-specific general knowledge, fitness or subject preparation',
                                            'Planning, teamwork and decision-making'],
                                 'technologies': ['Tools and methods used in Social Worker / NGO Officer',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Social Worker / NGO Officer',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Social Worker / NGO Officer',
                                              'Analyse a real-world challenge relevant to Social Worker / '
                                              'NGO Officer and present a safe, evidence-based solution'],
                                 'pathways': ['Read the latest official eligibility, age, education, medical '
                                              'and selection criteria for the exact post.',
                                              'Plan degree choices and exam preparation around the official '
                                              'recruitment route.',
                                              'For uniformed services, assess physical and medical standards '
                                              'early.',
                                              'Use official notifications for dates, syllabus, selection '
                                              'stages and pay details.'],
                                 'roles': ['Social Worker / NGO Officer',
                                           'Junior / Trainee Social Worker / NGO Officer',
                                           'Specialist or senior Social Worker / NGO Officer after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Vacancies and pay depend on official '
                                                            'recruitment cycles, rank, cadre, allowances and '
                                                            'service rules.',
                                 'education_cost_india': 'Preparation expenses vary; include exam fees, '
                                                         'study materials, coaching if chosen, travel and '
                                                         'medical/fitness preparation.',
                                 'future_outlook': 'For Social Worker / NGO Officer, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Social Worker / NGO '
                                                            'Officer.',
                                                            'Compare at least three recognised training '
                                                            'routes for Social Worker / NGO Officer, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Social Worker / NGO Officer.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Sales & Marketing Manager': {'field': 'Business, Management and Entrepreneurship',
                               'summary': 'Sales & Marketing Manager: Coordinates people, customers, '
                                          'services, operations or business growth using commercial '
                                          'judgement and measurable goals.',
                               'skills': ['Communication, negotiation and teamwork',
                                          'Planning, budgeting and data-informed decisions',
                                          'Customer or stakeholder understanding',
                                          'Digital tools and professional ethics'],
                               'technologies': ['Tools and methods used in Sales & Marketing Manager',
                                                'Spreadsheets, digital research and clear documentation '
                                                'where relevant',
                                                'Role-specific platforms confirmed from current job '
                                                'descriptions'],
                               'projects': ['Complete a beginner project or practical exercise related to '
                                            'Sales & Marketing Manager',
                                            'Create a portfolio, case study or documented practical '
                                            'assignment for Sales & Marketing Manager',
                                            'Analyse a real-world challenge relevant to Sales & Marketing '
                                            'Manager and present a safe, evidence-based solution'],
                               'pathways': ['Learn the industry and target role through a relevant degree, '
                                            'diploma or practical experience.',
                                            'Build evidence through internships, sales/service projects or a '
                                            'small validated business experiment.',
                                            'Practise spreadsheets, presentations, customer research and '
                                            'project planning.',
                                            'Review entry-level job descriptions and speak with '
                                            'practitioners in the target sector.'],
                               'roles': ['Sales & Marketing Manager',
                                         'Junior / Trainee Sales & Marketing Manager',
                                         'Specialist or senior Sales & Marketing Manager after required '
                                         'training and experience'],
                               'indicative_salary_india': 'Pay varies widely by industry, location, '
                                                          'seniority, targets and whether income is salaried '
                                                          'or entrepreneurial.',
                               'education_cost_india': 'Costs depend on degree/course choice; '
                                                       'entrepreneurship also requires a separate business '
                                                       'budget and risk planning.',
                               'future_outlook': 'For Sales & Marketing Manager, assess current demand using '
                                                 'recent India-based job listings, official recruitment '
                                                 'notices and relevant industry reports; outlook is not '
                                                 'guaranteed.',
                               'recommended_next_steps': ['Read current official qualification and '
                                                          'eligibility rules for Sales & Marketing Manager.',
                                                          'Compare at least three recognised training routes '
                                                          'for Sales & Marketing Manager, including total '
                                                          'fees and duration.',
                                                          'Complete one relevant project, portfolio piece, '
                                                          'field exercise or supervised placement for Sales '
                                                          '& Marketing Manager.',
                                                          'Speak to a working professional and review recent '
                                                          'vacancies before committing to a course.'],
                               'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                               'research_note': 'Role-specific starter guidance generated from the career '
                                                'catalogue category. Verify licensing, eligibility, '
                                                'salaries, course fees and outlook with official/current '
                                                'sources.'},
 'Sports Coach / Athletic Coach': {'field': 'Sports, Fitness and Performance',
                                   'summary': 'Sports Coach / Athletic Coach: Develops physical performance, '
                                              'teaches movement, supports safe training or competes in a '
                                              'sport.',
                                   'skills': ['Sport-specific technique and physical conditioning',
                                              'Training design and performance tracking',
                                              'Injury prevention and safety awareness',
                                              'Motivation, communication and discipline'],
                                   'technologies': ['Tools and methods used in Sports Coach / Athletic Coach',
                                                    'Spreadsheets, digital research and clear documentation '
                                                    'where relevant',
                                                    'Role-specific platforms confirmed from current job '
                                                    'descriptions'],
                                   'projects': ['Complete a beginner project or practical exercise related '
                                                'to Sports Coach / Athletic Coach',
                                                'Create a portfolio, case study or documented practical '
                                                'assignment for Sports Coach / Athletic Coach',
                                                'Analyse a real-world challenge relevant to Sports Coach / '
                                                'Athletic Coach and present a safe, evidence-based solution'],
                                   'pathways': ['Choose a sport or fitness specialisation and understand its '
                                                'recognised coaching/certification route.',
                                                'Train consistently with qualified supervision and maintain '
                                                'a performance record.',
                                                'Complete relevant first-aid/safety and coaching '
                                                'qualifications where appropriate.',
                                                'Build experience through clubs, academies, schools or '
                                                'supervised fitness settings.'],
                                   'roles': ['Sports Coach / Athletic Coach',
                                             'Junior / Trainee Sports Coach / Athletic Coach',
                                             'Specialist or senior Sports Coach / Athletic Coach after '
                                             'required training and experience'],
                                   'indicative_salary_india': 'Income ranges from variable competition/prize '
                                                              'earnings to salaried coaching and fitness '
                                                              'roles.',
                                   'education_cost_india': 'Costs may include coaching qualifications, '
                                                           'equipment, facilities, travel, competition fees '
                                                           'and ongoing training.',
                                   'future_outlook': 'For Sports Coach / Athletic Coach, assess current '
                                                     'demand using recent India-based job listings, official '
                                                     'recruitment notices and relevant industry reports; '
                                                     'outlook is not guaranteed.',
                                   'recommended_next_steps': ['Read current official qualification and '
                                                              'eligibility rules for Sports Coach / Athletic '
                                                              'Coach.',
                                                              'Compare at least three recognised training '
                                                              'routes for Sports Coach / Athletic Coach, '
                                                              'including total fees and duration.',
                                                              'Complete one relevant project, portfolio '
                                                              'piece, field exercise or supervised placement '
                                                              'for Sports Coach / Athletic Coach.',
                                                              'Speak to a working professional and review '
                                                              'recent vacancies before committing to a '
                                                              'course.'],
                                   'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                   'research_note': 'Role-specific starter guidance generated from the '
                                                    'career catalogue category. Verify licensing, '
                                                    'eligibility, salaries, course fees and outlook with '
                                                    'official/current sources.'},
 'Physiotherapist / Sports Physiotherapist': {'field': 'Healthcare and Life Sciences',
                                              'summary': 'Physiotherapist / Sports Physiotherapist: Patient '
                                                         'care, clinical knowledge, evidence-based practice, '
                                                         'ethical judgement and clear communication.',
                                              'skills': ['Biology and health-science foundations',
                                                         'Careful observation and documentation',
                                                         'Communication with patients or teams',
                                                         'Ethics, safety and evidence-based decision-making'],
                                              'technologies': ['Tools and methods used in Physiotherapist / '
                                                               'Sports Physiotherapist',
                                                               'Spreadsheets, digital research and clear '
                                                               'documentation where relevant',
                                                               'Role-specific platforms confirmed from '
                                                               'current job descriptions'],
                                              'projects': ['Complete a beginner project or practical '
                                                           'exercise related to Physiotherapist / Sports '
                                                           'Physiotherapist',
                                                           'Create a portfolio, case study or documented '
                                                           'practical assignment for Physiotherapist / '
                                                           'Sports Physiotherapist',
                                                           'Analyse a real-world challenge relevant to '
                                                           'Physiotherapist / Sports Physiotherapist and '
                                                           'present a safe, evidence-based solution'],
                                              'pathways': ['Investigate the recognised health-science route '
                                                           'and entrance requirements for this exact '
                                                           'profession.',
                                                           'Complete the required accredited degree and '
                                                           'supervised clinical training.',
                                                           'Check registration/licensing rules with the '
                                                           'relevant Indian regulator or council.',
                                                           'Build experience through approved clinical '
                                                           'placements and continuing education.'],
                                              'roles': ['Physiotherapist / Sports Physiotherapist',
                                                        'Junior / Trainee Physiotherapist / Sports '
                                                        'Physiotherapist',
                                                        'Specialist or senior Physiotherapist / Sports '
                                                        'Physiotherapist after required training and '
                                                        'experience'],
                                              'indicative_salary_india': 'Healthcare hiring and pay vary '
                                                                         'strongly by qualification, '
                                                                         'specialisation, public/private '
                                                                         'employer and location.',
                                              'education_cost_india': 'Course costs vary widely between '
                                                                      'government and private institutions; '
                                                                      'include tuition, examinations, '
                                                                      'clinical materials and living costs.',
                                              'future_outlook': 'For Physiotherapist / Sports '
                                                                'Physiotherapist, assess current demand '
                                                                'using recent India-based job listings, '
                                                                'official recruitment notices and relevant '
                                                                'industry reports; outlook is not '
                                                                'guaranteed.',
                                              'recommended_next_steps': ['Read current official '
                                                                         'qualification and eligibility '
                                                                         'rules for Physiotherapist / Sports '
                                                                         'Physiotherapist.',
                                                                         'Compare at least three recognised '
                                                                         'training routes for '
                                                                         'Physiotherapist / Sports '
                                                                         'Physiotherapist, including total '
                                                                         'fees and duration.',
                                                                         'Complete one relevant project, '
                                                                         'portfolio piece, field exercise or '
                                                                         'supervised placement for '
                                                                         'Physiotherapist / Sports '
                                                                         'Physiotherapist.',
                                                                         'Speak to a working professional '
                                                                         'and review recent vacancies before '
                                                                         'committing to a course.'],
                                              'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                              'research_note': 'Role-specific starter guidance generated '
                                                               'from the career catalogue category. Verify '
                                                               'licensing, eligibility, salaries, course '
                                                               'fees and outlook with official/current '
                                                               'sources.'},
 'Fitness Trainer / Yoga Instructor': {'field': 'Sports, Fitness and Performance',
                                       'summary': 'Fitness Trainer / Yoga Instructor: Develops physical '
                                                  'performance, teaches movement, supports safe training or '
                                                  'competes in a sport.',
                                       'skills': ['Sport-specific technique and physical conditioning',
                                                  'Training design and performance tracking',
                                                  'Injury prevention and safety awareness',
                                                  'Motivation, communication and discipline'],
                                       'technologies': ['Tools and methods used in Fitness Trainer / Yoga '
                                                        'Instructor',
                                                        'Spreadsheets, digital research and clear '
                                                        'documentation where relevant',
                                                        'Role-specific platforms confirmed from current job '
                                                        'descriptions'],
                                       'projects': ['Complete a beginner project or practical exercise '
                                                    'related to Fitness Trainer / Yoga Instructor',
                                                    'Create a portfolio, case study or documented practical '
                                                    'assignment for Fitness Trainer / Yoga Instructor',
                                                    'Analyse a real-world challenge relevant to Fitness '
                                                    'Trainer / Yoga Instructor and present a safe, '
                                                    'evidence-based solution'],
                                       'pathways': ['Choose a sport or fitness specialisation and understand '
                                                    'its recognised coaching/certification route.',
                                                    'Train consistently with qualified supervision and '
                                                    'maintain a performance record.',
                                                    'Complete relevant first-aid/safety and coaching '
                                                    'qualifications where appropriate.',
                                                    'Build experience through clubs, academies, schools or '
                                                    'supervised fitness settings.'],
                                       'roles': ['Fitness Trainer / Yoga Instructor',
                                                 'Junior / Trainee Fitness Trainer / Yoga Instructor',
                                                 'Specialist or senior Fitness Trainer / Yoga Instructor '
                                                 'after required training and experience'],
                                       'indicative_salary_india': 'Income ranges from variable '
                                                                  'competition/prize earnings to salaried '
                                                                  'coaching and fitness roles.',
                                       'education_cost_india': 'Costs may include coaching qualifications, '
                                                               'equipment, facilities, travel, competition '
                                                               'fees and ongoing training.',
                                       'future_outlook': 'For Fitness Trainer / Yoga Instructor, assess '
                                                         'current demand using recent India-based job '
                                                         'listings, official recruitment notices and '
                                                         'relevant industry reports; outlook is not '
                                                         'guaranteed.',
                                       'recommended_next_steps': ['Read current official qualification and '
                                                                  'eligibility rules for Fitness Trainer / '
                                                                  'Yoga Instructor.',
                                                                  'Compare at least three recognised '
                                                                  'training routes for Fitness Trainer / '
                                                                  'Yoga Instructor, including total fees and '
                                                                  'duration.',
                                                                  'Complete one relevant project, portfolio '
                                                                  'piece, field exercise or supervised '
                                                                  'placement for Fitness Trainer / Yoga '
                                                                  'Instructor.',
                                                                  'Speak to a working professional and '
                                                                  'review recent vacancies before committing '
                                                                  'to a course.'],
                                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                       'research_note': 'Role-specific starter guidance generated from the '
                                                        'career catalogue category. Verify licensing, '
                                                        'eligibility, salaries, course fees and outlook with '
                                                        'official/current sources.'},
 'Army / Navy / Air Force Officer': {'field': 'Public Service, Defence and Social Impact',
                                     'summary': 'Army / Navy / Air Force Officer: Serves communities or '
                                                'public institutions through administration, protection, '
                                                'policy, development or disciplined operational work.',
                                     'skills': ['Communication and public-service orientation',
                                                'Ethical judgement and accountability',
                                                'Role-specific general knowledge, fitness or subject '
                                                'preparation',
                                                'Planning, teamwork and decision-making'],
                                     'technologies': ['Tools and methods used in Army / Navy / Air Force '
                                                      'Officer',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to Army / Navy / Air Force Officer',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for Army / Navy / Air Force Officer',
                                                  'Analyse a real-world challenge relevant to Army / Navy / '
                                                  'Air Force Officer and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Read the latest official eligibility, age, education, '
                                                  'medical and selection criteria for the exact post.',
                                                  'Plan degree choices and exam preparation around the '
                                                  'official recruitment route.',
                                                  'For uniformed services, assess physical and medical '
                                                  'standards early.',
                                                  'Use official notifications for dates, syllabus, selection '
                                                  'stages and pay details.'],
                                     'roles': ['Army / Navy / Air Force Officer',
                                               'Junior / Trainee Army / Navy / Air Force Officer',
                                               'Specialist or senior Army / Navy / Air Force Officer after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Vacancies and pay depend on official '
                                                                'recruitment cycles, rank, cadre, allowances '
                                                                'and service rules.',
                                     'education_cost_india': 'Preparation expenses vary; include exam fees, '
                                                             'study materials, coaching if chosen, travel '
                                                             'and medical/fitness preparation.',
                                     'future_outlook': 'For Army / Navy / Air Force Officer, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for Army / Navy / Air '
                                                                'Force Officer.',
                                                                'Compare at least three recognised training '
                                                                'routes for Army / Navy / Air Force Officer, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for Army / Navy / Air Force '
                                                                'Officer.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'Professional Sportsperson': {'field': 'Sports, Fitness and Performance',
                               'summary': 'Professional Sportsperson: Develops physical performance, teaches '
                                          'movement, supports safe training or competes in a sport.',
                               'skills': ['Sport-specific technique and physical conditioning',
                                          'Training design and performance tracking',
                                          'Injury prevention and safety awareness',
                                          'Motivation, communication and discipline'],
                               'technologies': ['Tools and methods used in Professional Sportsperson',
                                                'Spreadsheets, digital research and clear documentation '
                                                'where relevant',
                                                'Role-specific platforms confirmed from current job '
                                                'descriptions'],
                               'projects': ['Complete a beginner project or practical exercise related to '
                                            'Professional Sportsperson',
                                            'Create a portfolio, case study or documented practical '
                                            'assignment for Professional Sportsperson',
                                            'Analyse a real-world challenge relevant to Professional '
                                            'Sportsperson and present a safe, evidence-based solution'],
                               'pathways': ['Choose a sport or fitness specialisation and understand its '
                                            'recognised coaching/certification route.',
                                            'Train consistently with qualified supervision and maintain a '
                                            'performance record.',
                                            'Complete relevant first-aid/safety and coaching qualifications '
                                            'where appropriate.',
                                            'Build experience through clubs, academies, schools or '
                                            'supervised fitness settings.'],
                               'roles': ['Professional Sportsperson',
                                         'Junior / Trainee Professional Sportsperson',
                                         'Specialist or senior Professional Sportsperson after required '
                                         'training and experience'],
                               'indicative_salary_india': 'Income ranges from variable competition/prize '
                                                          'earnings to salaried coaching and fitness roles.',
                               'education_cost_india': 'Costs may include coaching qualifications, '
                                                       'equipment, facilities, travel, competition fees and '
                                                       'ongoing training.',
                               'future_outlook': 'For Professional Sportsperson, assess current demand using '
                                                 'recent India-based job listings, official recruitment '
                                                 'notices and relevant industry reports; outlook is not '
                                                 'guaranteed.',
                               'recommended_next_steps': ['Read current official qualification and '
                                                          'eligibility rules for Professional Sportsperson.',
                                                          'Compare at least three recognised training routes '
                                                          'for Professional Sportsperson, including total '
                                                          'fees and duration.',
                                                          'Complete one relevant project, portfolio piece, '
                                                          'field exercise or supervised placement for '
                                                          'Professional Sportsperson.',
                                                          'Speak to a working professional and review recent '
                                                          'vacancies before committing to a course.'],
                               'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                               'research_note': 'Role-specific starter guidance generated from the career '
                                                'catalogue category. Verify licensing, eligibility, '
                                                'salaries, course fees and outlook with official/current '
                                                'sources.'},
 'Dancer / Choreographer': {'field': 'Creative Media, Communication and Design',
                            'summary': 'Dancer / Choreographer: Creates stories, experiences, visuals, '
                                       'performances or communication materials for a defined audience.',
                            'skills': ['Creative development and audience awareness',
                                       'Portfolio-building and revision from feedback',
                                       'Communication, collaboration and deadlines',
                                       'Relevant production, design, language or editing tools'],
                            'technologies': ['Tools and methods used in Dancer / Choreographer',
                                             'Spreadsheets, digital research and clear documentation where '
                                             'relevant',
                                             'Role-specific platforms confirmed from current job '
                                             'descriptions'],
                            'projects': ['Complete a beginner project or practical exercise related to '
                                         'Dancer / Choreographer',
                                         'Create a portfolio, case study or documented practical assignment '
                                         'for Dancer / Choreographer',
                                         'Analyse a real-world challenge relevant to Dancer / Choreographer '
                                         'and present a safe, evidence-based solution'],
                            'pathways': ['Study the craft through a suitable course, mentorship or '
                                         'structured self-learning route.',
                                         'Build a portfolio/showreel with original work relevant to the '
                                         'target role.',
                                         'Practise with realistic briefs and document your creative process.',
                                         'Seek internships, auditions, commissions or entry-level projects; '
                                         'check contract and copyright basics.'],
                            'roles': ['Dancer / Choreographer',
                                      'Junior / Trainee Dancer / Choreographer',
                                      'Specialist or senior Dancer / Choreographer after required training '
                                      'and experience'],
                            'indicative_salary_india': 'Income may be project-based or variable; results '
                                                       'depend on portfolio quality, network, niche and '
                                                       'experience.',
                            'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                    'formal design/media programmes; budget for software, '
                                                    'equipment, materials and production.',
                            'future_outlook': 'For Dancer / Choreographer, assess current demand using '
                                              'recent India-based job listings, official recruitment notices '
                                              'and relevant industry reports; outlook is not guaranteed.',
                            'recommended_next_steps': ['Read current official qualification and eligibility '
                                                       'rules for Dancer / Choreographer.',
                                                       'Compare at least three recognised training routes '
                                                       'for Dancer / Choreographer, including total fees and '
                                                       'duration.',
                                                       'Complete one relevant project, portfolio piece, '
                                                       'field exercise or supervised placement for Dancer / '
                                                       'Choreographer.',
                                                       'Speak to a working professional and review recent '
                                                       'vacancies before committing to a course.'],
                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                            'research_note': 'Role-specific starter guidance generated from the career '
                                             'catalogue category. Verify licensing, eligibility, salaries, '
                                             'course fees and outlook with official/current sources.'},
 'Surgeon / Orthopedic Specialist': {'field': 'Healthcare and Life Sciences',
                                     'summary': 'Surgeon / Orthopedic Specialist: Patient care, clinical '
                                                'knowledge, evidence-based practice, ethical judgement and '
                                                'clear communication.',
                                     'skills': ['Biology and health-science foundations',
                                                'Careful observation and documentation',
                                                'Communication with patients or teams',
                                                'Ethics, safety and evidence-based decision-making'],
                                     'technologies': ['Tools and methods used in Surgeon / Orthopedic '
                                                      'Specialist',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to Surgeon / Orthopedic Specialist',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for Surgeon / Orthopedic Specialist',
                                                  'Analyse a real-world challenge relevant to Surgeon / '
                                                  'Orthopedic Specialist and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Investigate the recognised health-science route and '
                                                  'entrance requirements for this exact profession.',
                                                  'Complete the required accredited degree and supervised '
                                                  'clinical training.',
                                                  'Check registration/licensing rules with the relevant '
                                                  'Indian regulator or council.',
                                                  'Build experience through approved clinical placements and '
                                                  'continuing education.'],
                                     'roles': ['Surgeon / Orthopedic Specialist',
                                               'Junior / Trainee Surgeon / Orthopedic Specialist',
                                               'Specialist or senior Surgeon / Orthopedic Specialist after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Healthcare hiring and pay vary strongly by '
                                                                'qualification, specialisation, '
                                                                'public/private employer and location.',
                                     'education_cost_india': 'Course costs vary widely between government '
                                                             'and private institutions; include tuition, '
                                                             'examinations, clinical materials and living '
                                                             'costs.',
                                     'future_outlook': 'For Surgeon / Orthopedic Specialist, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for Surgeon / Orthopedic '
                                                                'Specialist.',
                                                                'Compare at least three recognised training '
                                                                'routes for Surgeon / Orthopedic Specialist, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for Surgeon / Orthopedic '
                                                                'Specialist.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'Cabin Crew / Air Hostess': {'field': 'Specialised Professional Careers',
                              'summary': 'Cabin Crew / Air Hostess: Cabin Crew / Air Hostess is a distinct '
                                         'career path requiring role-specific knowledge, practical '
                                         'experience and an understanding of its professional standards.',
                              'skills': ['Core subject knowledge relevant to the role',
                                         'Problem-solving and professional communication',
                                         'Ethical conduct and accurate documentation',
                                         'Practical skills using tools or methods specific to the '
                                         'occupation'],
                              'technologies': ['Tools and methods used in Cabin Crew / Air Hostess',
                                               'Spreadsheets, digital research and clear documentation where '
                                               'relevant',
                                               'Role-specific platforms confirmed from current job '
                                               'descriptions'],
                              'projects': ['Complete a beginner project or practical exercise related to '
                                           'Cabin Crew / Air Hostess',
                                           'Create a portfolio, case study or documented practical '
                                           'assignment for Cabin Crew / Air Hostess',
                                           'Analyse a real-world challenge relevant to Cabin Crew / Air '
                                           'Hostess and present a safe, evidence-based solution'],
                              'pathways': ['Research the day-to-day duties and official eligibility '
                                           'requirements for Cabin Crew / Air Hostess.',
                                           'Compare recognised courses, entry routes, duration and total '
                                           'cost before enrolling.',
                                           'Build role-relevant experience through projects, supervised '
                                           'practice, internships or a portfolio.',
                                           'Review current job advertisements and consult a qualified '
                                           'professional in this field.'],
                              'roles': ['Cabin Crew / Air Hostess',
                                        'Junior / Trainee Cabin Crew / Air Hostess',
                                        'Specialist or senior Cabin Crew / Air Hostess after required '
                                        'training and experience'],
                              'indicative_salary_india': 'Salary and demand should be checked against '
                                                         'current India-specific sources for the exact role '
                                                         'and experience level.',
                              'education_cost_india': 'Confirm official course fees and include exams, '
                                                      'materials, equipment, travel and living costs.',
                              'future_outlook': 'For Cabin Crew / Air Hostess, assess current demand using '
                                                'recent India-based job listings, official recruitment '
                                                'notices and relevant industry reports; outlook is not '
                                                'guaranteed.',
                              'recommended_next_steps': ['Read current official qualification and '
                                                         'eligibility rules for Cabin Crew / Air Hostess.',
                                                         'Compare at least three recognised training routes '
                                                         'for Cabin Crew / Air Hostess, including total fees '
                                                         'and duration.',
                                                         'Complete one relevant project, portfolio piece, '
                                                         'field exercise or supervised placement for Cabin '
                                                         'Crew / Air Hostess.',
                                                         'Speak to a working professional and review recent '
                                                         'vacancies before committing to a course.'],
                              'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                              'research_note': 'Role-specific starter guidance generated from the career '
                                               'catalogue category. Verify licensing, eligibility, salaries, '
                                               'course fees and outlook with official/current sources.'},
 'Journalist / Reporter / News Anchor': {'field': 'Creative Media, Communication and Design',
                                         'summary': 'Journalist / Reporter / News Anchor: Creates stories, '
                                                    'experiences, visuals, performances or communication '
                                                    'materials for a defined audience.',
                                         'skills': ['Creative development and audience awareness',
                                                    'Portfolio-building and revision from feedback',
                                                    'Communication, collaboration and deadlines',
                                                    'Relevant production, design, language or editing tools'],
                                         'technologies': ['Tools and methods used in Journalist / Reporter / '
                                                          'News Anchor',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Journalist / Reporter / News Anchor',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Journalist / Reporter / News '
                                                      'Anchor',
                                                      'Analyse a real-world challenge relevant to Journalist '
                                                      '/ Reporter / News Anchor and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Study the craft through a suitable course, mentorship '
                                                      'or structured self-learning route.',
                                                      'Build a portfolio/showreel with original work '
                                                      'relevant to the target role.',
                                                      'Practise with realistic briefs and document your '
                                                      'creative process.',
                                                      'Seek internships, auditions, commissions or '
                                                      'entry-level projects; check contract and copyright '
                                                      'basics.'],
                                         'roles': ['Journalist / Reporter / News Anchor',
                                                   'Junior / Trainee Journalist / Reporter / News Anchor',
                                                   'Specialist or senior Journalist / Reporter / News Anchor '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Income may be project-based or '
                                                                    'variable; results depend on portfolio '
                                                                    'quality, network, niche and experience.',
                                         'education_cost_india': 'Course costs range from low-cost '
                                                                 'self-learning to formal design/media '
                                                                 'programmes; budget for software, '
                                                                 'equipment, materials and production.',
                                         'future_outlook': 'For Journalist / Reporter / News Anchor, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Journalist / '
                                                                    'Reporter / News Anchor.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Journalist / '
                                                                    'Reporter / News Anchor, including total '
                                                                    'fees and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Journalist / '
                                                                    'Reporter / News Anchor.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Lawyer / Advocate / Corporate Lawyer': {'field': 'Specialised Professional Careers',
                                          'summary': 'Lawyer / Advocate / Corporate Lawyer: Lawyer / '
                                                     'Advocate / Corporate Lawyer is a distinct career path '
                                                     'requiring role-specific knowledge, practical '
                                                     'experience and an understanding of its professional '
                                                     'standards.',
                                          'skills': ['Core subject knowledge relevant to the role',
                                                     'Problem-solving and professional communication',
                                                     'Ethical conduct and accurate documentation',
                                                     'Practical skills using tools or methods specific to '
                                                     'the occupation'],
                                          'technologies': ['Tools and methods used in Lawyer / Advocate / '
                                                           'Corporate Lawyer',
                                                           'Spreadsheets, digital research and clear '
                                                           'documentation where relevant',
                                                           'Role-specific platforms confirmed from current '
                                                           'job descriptions'],
                                          'projects': ['Complete a beginner project or practical exercise '
                                                       'related to Lawyer / Advocate / Corporate Lawyer',
                                                       'Create a portfolio, case study or documented '
                                                       'practical assignment for Lawyer / Advocate / '
                                                       'Corporate Lawyer',
                                                       'Analyse a real-world challenge relevant to Lawyer / '
                                                       'Advocate / Corporate Lawyer and present a safe, '
                                                       'evidence-based solution'],
                                          'pathways': ['Research the day-to-day duties and official '
                                                       'eligibility requirements for Lawyer / Advocate / '
                                                       'Corporate Lawyer.',
                                                       'Compare recognised courses, entry routes, duration '
                                                       'and total cost before enrolling.',
                                                       'Build role-relevant experience through projects, '
                                                       'supervised practice, internships or a portfolio.',
                                                       'Review current job advertisements and consult a '
                                                       'qualified professional in this field.'],
                                          'roles': ['Lawyer / Advocate / Corporate Lawyer',
                                                    'Junior / Trainee Lawyer / Advocate / Corporate Lawyer',
                                                    'Specialist or senior Lawyer / Advocate / Corporate '
                                                    'Lawyer after required training and experience'],
                                          'indicative_salary_india': 'Salary and demand should be checked '
                                                                     'against current India-specific sources '
                                                                     'for the exact role and experience '
                                                                     'level.',
                                          'education_cost_india': 'Confirm official course fees and include '
                                                                  'exams, materials, equipment, travel and '
                                                                  'living costs.',
                                          'future_outlook': 'For Lawyer / Advocate / Corporate Lawyer, '
                                                            'assess current demand using recent India-based '
                                                            'job listings, official recruitment notices and '
                                                            'relevant industry reports; outlook is not '
                                                            'guaranteed.',
                                          'recommended_next_steps': ['Read current official qualification '
                                                                     'and eligibility rules for Lawyer / '
                                                                     'Advocate / Corporate Lawyer.',
                                                                     'Compare at least three recognised '
                                                                     'training routes for Lawyer / Advocate '
                                                                     '/ Corporate Lawyer, including total '
                                                                     'fees and duration.',
                                                                     'Complete one relevant project, '
                                                                     'portfolio piece, field exercise or '
                                                                     'supervised placement for Lawyer / '
                                                                     'Advocate / Corporate Lawyer.',
                                                                     'Speak to a working professional and '
                                                                     'review recent vacancies before '
                                                                     'committing to a course.'],
                                          'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                          'research_note': 'Role-specific starter guidance generated from '
                                                           'the career catalogue category. Verify licensing, '
                                                           'eligibility, salaries, course fees and outlook '
                                                           'with official/current sources.'},
 'Content Writer / Copywriter': {'field': 'Creative Media, Communication and Design',
                                 'summary': 'Content Writer / Copywriter: Creates stories, experiences, '
                                            'visuals, performances or communication materials for a defined '
                                            'audience.',
                                 'skills': ['Creative development and audience awareness',
                                            'Portfolio-building and revision from feedback',
                                            'Communication, collaboration and deadlines',
                                            'Relevant production, design, language or editing tools'],
                                 'technologies': ['Tools and methods used in Content Writer / Copywriter',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Content Writer / Copywriter',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Content Writer / Copywriter',
                                              'Analyse a real-world challenge relevant to Content Writer / '
                                              'Copywriter and present a safe, evidence-based solution'],
                                 'pathways': ['Study the craft through a suitable course, mentorship or '
                                              'structured self-learning route.',
                                              'Build a portfolio/showreel with original work relevant to the '
                                              'target role.',
                                              'Practise with realistic briefs and document your creative '
                                              'process.',
                                              'Seek internships, auditions, commissions or entry-level '
                                              'projects; check contract and copyright basics.'],
                                 'roles': ['Content Writer / Copywriter',
                                           'Junior / Trainee Content Writer / Copywriter',
                                           'Specialist or senior Content Writer / Copywriter after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Income may be project-based or variable; '
                                                            'results depend on portfolio quality, network, '
                                                            'niche and experience.',
                                 'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                         'formal design/media programmes; budget for '
                                                         'software, equipment, materials and production.',
                                 'future_outlook': 'For Content Writer / Copywriter, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Content Writer / '
                                                            'Copywriter.',
                                                            'Compare at least three recognised training '
                                                            'routes for Content Writer / Copywriter, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Content Writer / Copywriter.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'IAS / IPS / Civil Services Officer (UPSC)': {'field': 'Public Service, Defence and Social Impact',
                                               'summary': 'IAS / IPS / Civil Services Officer (UPSC): Serves '
                                                          'communities or public institutions through '
                                                          'administration, protection, policy, development '
                                                          'or disciplined operational work.',
                                               'skills': ['Communication and public-service orientation',
                                                          'Ethical judgement and accountability',
                                                          'Role-specific general knowledge, fitness or '
                                                          'subject preparation',
                                                          'Planning, teamwork and decision-making'],
                                               'technologies': ['Tools and methods used in IAS / IPS / Civil '
                                                                'Services Officer (UPSC)',
                                                                'Spreadsheets, digital research and clear '
                                                                'documentation where relevant',
                                                                'Role-specific platforms confirmed from '
                                                                'current job descriptions'],
                                               'projects': ['Complete a beginner project or practical '
                                                            'exercise related to IAS / IPS / Civil Services '
                                                            'Officer (UPSC)',
                                                            'Create a portfolio, case study or documented '
                                                            'practical assignment for IAS / IPS / Civil '
                                                            'Services Officer (UPSC)',
                                                            'Analyse a real-world challenge relevant to IAS '
                                                            '/ IPS / Civil Services Officer (UPSC) and '
                                                            'present a safe, evidence-based solution'],
                                               'pathways': ['Read the latest official eligibility, age, '
                                                            'education, medical and selection criteria for '
                                                            'the exact post.',
                                                            'Plan degree choices and exam preparation around '
                                                            'the official recruitment route.',
                                                            'For uniformed services, assess physical and '
                                                            'medical standards early.',
                                                            'Use official notifications for dates, syllabus, '
                                                            'selection stages and pay details.'],
                                               'roles': ['IAS / IPS / Civil Services Officer (UPSC)',
                                                         'Junior / Trainee IAS / IPS / Civil Services '
                                                         'Officer (UPSC)',
                                                         'Specialist or senior IAS / IPS / Civil Services '
                                                         'Officer (UPSC) after required training and '
                                                         'experience'],
                                               'indicative_salary_india': 'Vacancies and pay depend on '
                                                                          'official recruitment cycles, '
                                                                          'rank, cadre, allowances and '
                                                                          'service rules.',
                                               'education_cost_india': 'Preparation expenses vary; include '
                                                                       'exam fees, study materials, coaching '
                                                                       'if chosen, travel and '
                                                                       'medical/fitness preparation.',
                                               'future_outlook': 'For IAS / IPS / Civil Services Officer '
                                                                 '(UPSC), assess current demand using recent '
                                                                 'India-based job listings, official '
                                                                 'recruitment notices and relevant industry '
                                                                 'reports; outlook is not guaranteed.',
                                               'recommended_next_steps': ['Read current official '
                                                                          'qualification and eligibility '
                                                                          'rules for IAS / IPS / Civil '
                                                                          'Services Officer (UPSC).',
                                                                          'Compare at least three recognised '
                                                                          'training routes for IAS / IPS / '
                                                                          'Civil Services Officer (UPSC), '
                                                                          'including total fees and '
                                                                          'duration.',
                                                                          'Complete one relevant project, '
                                                                          'portfolio piece, field exercise '
                                                                          'or supervised placement for IAS / '
                                                                          'IPS / Civil Services Officer '
                                                                          '(UPSC).',
                                                                          'Speak to a working professional '
                                                                          'and review recent vacancies '
                                                                          'before committing to a course.'],
                                               'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                               'research_note': 'Role-specific starter guidance generated '
                                                                'from the career catalogue category. Verify '
                                                                'licensing, eligibility, salaries, course '
                                                                'fees and outlook with official/current '
                                                                'sources.'},
 'Author / Novelist / Content Creator': {'field': 'Creative Media, Communication and Design',
                                         'summary': 'Author / Novelist / Content Creator: Creates stories, '
                                                    'experiences, visuals, performances or communication '
                                                    'materials for a defined audience.',
                                         'skills': ['Creative development and audience awareness',
                                                    'Portfolio-building and revision from feedback',
                                                    'Communication, collaboration and deadlines',
                                                    'Relevant production, design, language or editing tools'],
                                         'technologies': ['Tools and methods used in Author / Novelist / '
                                                          'Content Creator',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Author / Novelist / Content Creator',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Author / Novelist / Content '
                                                      'Creator',
                                                      'Analyse a real-world challenge relevant to Author / '
                                                      'Novelist / Content Creator and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Study the craft through a suitable course, mentorship '
                                                      'or structured self-learning route.',
                                                      'Build a portfolio/showreel with original work '
                                                      'relevant to the target role.',
                                                      'Practise with realistic briefs and document your '
                                                      'creative process.',
                                                      'Seek internships, auditions, commissions or '
                                                      'entry-level projects; check contract and copyright '
                                                      'basics.'],
                                         'roles': ['Author / Novelist / Content Creator',
                                                   'Junior / Trainee Author / Novelist / Content Creator',
                                                   'Specialist or senior Author / Novelist / Content Creator '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Income may be project-based or '
                                                                    'variable; results depend on portfolio '
                                                                    'quality, network, niche and experience.',
                                         'education_cost_india': 'Course costs range from low-cost '
                                                                 'self-learning to formal design/media '
                                                                 'programmes; budget for software, '
                                                                 'equipment, materials and production.',
                                         'future_outlook': 'For Author / Novelist / Content Creator, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Author / Novelist '
                                                                    '/ Content Creator.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Author / Novelist / '
                                                                    'Content Creator, including total fees '
                                                                    'and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Author / '
                                                                    'Novelist / Content Creator.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Public Relations Manager': {'field': 'Creative Media, Communication and Design',
                              'summary': 'Public Relations Manager: Creates stories, experiences, visuals, '
                                         'performances or communication materials for a defined audience.',
                              'skills': ['Creative development and audience awareness',
                                         'Portfolio-building and revision from feedback',
                                         'Communication, collaboration and deadlines',
                                         'Relevant production, design, language or editing tools'],
                              'technologies': ['Tools and methods used in Public Relations Manager',
                                               'Spreadsheets, digital research and clear documentation where '
                                               'relevant',
                                               'Role-specific platforms confirmed from current job '
                                               'descriptions'],
                              'projects': ['Complete a beginner project or practical exercise related to '
                                           'Public Relations Manager',
                                           'Create a portfolio, case study or documented practical '
                                           'assignment for Public Relations Manager',
                                           'Analyse a real-world challenge relevant to Public Relations '
                                           'Manager and present a safe, evidence-based solution'],
                              'pathways': ['Study the craft through a suitable course, mentorship or '
                                           'structured self-learning route.',
                                           'Build a portfolio/showreel with original work relevant to the '
                                           'target role.',
                                           'Practise with realistic briefs and document your creative '
                                           'process.',
                                           'Seek internships, auditions, commissions or entry-level '
                                           'projects; check contract and copyright basics.'],
                              'roles': ['Public Relations Manager',
                                        'Junior / Trainee Public Relations Manager',
                                        'Specialist or senior Public Relations Manager after required '
                                        'training and experience'],
                              'indicative_salary_india': 'Income may be project-based or variable; results '
                                                         'depend on portfolio quality, network, niche and '
                                                         'experience.',
                              'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                      'formal design/media programmes; budget for software, '
                                                      'equipment, materials and production.',
                              'future_outlook': 'For Public Relations Manager, assess current demand using '
                                                'recent India-based job listings, official recruitment '
                                                'notices and relevant industry reports; outlook is not '
                                                'guaranteed.',
                              'recommended_next_steps': ['Read current official qualification and '
                                                         'eligibility rules for Public Relations Manager.',
                                                         'Compare at least three recognised training routes '
                                                         'for Public Relations Manager, including total fees '
                                                         'and duration.',
                                                         'Complete one relevant project, portfolio piece, '
                                                         'field exercise or supervised placement for Public '
                                                         'Relations Manager.',
                                                         'Speak to a working professional and review recent '
                                                         'vacancies before committing to a course.'],
                              'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                              'research_note': 'Role-specific starter guidance generated from the career '
                                               'catalogue category. Verify licensing, eligibility, salaries, '
                                               'course fees and outlook with official/current sources.'},
 'Translator / Interpreter': {'field': 'Creative Media, Communication and Design',
                              'summary': 'Translator / Interpreter: Creates stories, experiences, visuals, '
                                         'performances or communication materials for a defined audience.',
                              'skills': ['Creative development and audience awareness',
                                         'Portfolio-building and revision from feedback',
                                         'Communication, collaboration and deadlines',
                                         'Relevant production, design, language or editing tools'],
                              'technologies': ['Tools and methods used in Translator / Interpreter',
                                               'Spreadsheets, digital research and clear documentation where '
                                               'relevant',
                                               'Role-specific platforms confirmed from current job '
                                               'descriptions'],
                              'projects': ['Complete a beginner project or practical exercise related to '
                                           'Translator / Interpreter',
                                           'Create a portfolio, case study or documented practical '
                                           'assignment for Translator / Interpreter',
                                           'Analyse a real-world challenge relevant to Translator / '
                                           'Interpreter and present a safe, evidence-based solution'],
                              'pathways': ['Study the craft through a suitable course, mentorship or '
                                           'structured self-learning route.',
                                           'Build a portfolio/showreel with original work relevant to the '
                                           'target role.',
                                           'Practise with realistic briefs and document your creative '
                                           'process.',
                                           'Seek internships, auditions, commissions or entry-level '
                                           'projects; check contract and copyright basics.'],
                              'roles': ['Translator / Interpreter',
                                        'Junior / Trainee Translator / Interpreter',
                                        'Specialist or senior Translator / Interpreter after required '
                                        'training and experience'],
                              'indicative_salary_india': 'Income may be project-based or variable; results '
                                                         'depend on portfolio quality, network, niche and '
                                                         'experience.',
                              'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                      'formal design/media programmes; budget for software, '
                                                      'equipment, materials and production.',
                              'future_outlook': 'For Translator / Interpreter, assess current demand using '
                                                'recent India-based job listings, official recruitment '
                                                'notices and relevant industry reports; outlook is not '
                                                'guaranteed.',
                              'recommended_next_steps': ['Read current official qualification and '
                                                         'eligibility rules for Translator / Interpreter.',
                                                         'Compare at least three recognised training routes '
                                                         'for Translator / Interpreter, including total fees '
                                                         'and duration.',
                                                         'Complete one relevant project, portfolio piece, '
                                                         'field exercise or supervised placement for '
                                                         'Translator / Interpreter.',
                                                         'Speak to a working professional and review recent '
                                                         'vacancies before committing to a course.'],
                              'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                              'research_note': 'Role-specific starter guidance generated from the career '
                                               'catalogue category. Verify licensing, eligibility, salaries, '
                                               'course fees and outlook with official/current sources.'},
 'RJ / Podcast Host': {'field': 'Creative Media, Communication and Design',
                       'summary': 'RJ / Podcast Host: Creates stories, experiences, visuals, performances or '
                                  'communication materials for a defined audience.',
                       'skills': ['Creative development and audience awareness',
                                  'Portfolio-building and revision from feedback',
                                  'Communication, collaboration and deadlines',
                                  'Relevant production, design, language or editing tools'],
                       'technologies': ['Tools and methods used in RJ / Podcast Host',
                                        'Spreadsheets, digital research and clear documentation where '
                                        'relevant',
                                        'Role-specific platforms confirmed from current job descriptions'],
                       'projects': ['Complete a beginner project or practical exercise related to RJ / '
                                    'Podcast Host',
                                    'Create a portfolio, case study or documented practical assignment for '
                                    'RJ / Podcast Host',
                                    'Analyse a real-world challenge relevant to RJ / Podcast Host and '
                                    'present a safe, evidence-based solution'],
                       'pathways': ['Study the craft through a suitable course, mentorship or structured '
                                    'self-learning route.',
                                    'Build a portfolio/showreel with original work relevant to the target '
                                    'role.',
                                    'Practise with realistic briefs and document your creative process.',
                                    'Seek internships, auditions, commissions or entry-level projects; check '
                                    'contract and copyright basics.'],
                       'roles': ['RJ / Podcast Host',
                                 'Junior / Trainee RJ / Podcast Host',
                                 'Specialist or senior RJ / Podcast Host after required training and '
                                 'experience'],
                       'indicative_salary_india': 'Income may be project-based or variable; results depend '
                                                  'on portfolio quality, network, niche and experience.',
                       'education_cost_india': 'Course costs range from low-cost self-learning to formal '
                                               'design/media programmes; budget for software, equipment, '
                                               'materials and production.',
                       'future_outlook': 'For RJ / Podcast Host, assess current demand using recent '
                                         'India-based job listings, official recruitment notices and '
                                         'relevant industry reports; outlook is not guaranteed.',
                       'recommended_next_steps': ['Read current official qualification and eligibility rules '
                                                  'for RJ / Podcast Host.',
                                                  'Compare at least three recognised training routes for RJ '
                                                  '/ Podcast Host, including total fees and duration.',
                                                  'Complete one relevant project, portfolio piece, field '
                                                  'exercise or supervised placement for RJ / Podcast Host.',
                                                  'Speak to a working professional and review recent '
                                                  'vacancies before committing to a course.'],
                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                       'research_note': 'Role-specific starter guidance generated from the career catalogue '
                                        'category. Verify licensing, eligibility, salaries, course fees and '
                                        'outlook with official/current sources.'},
 'Playback Singer / Music Artist': {'field': 'Creative Media, Communication and Design',
                                    'summary': 'Playback Singer / Music Artist: Creates stories, '
                                               'experiences, visuals, performances or communication '
                                               'materials for a defined audience.',
                                    'skills': ['Creative development and audience awareness',
                                               'Portfolio-building and revision from feedback',
                                               'Communication, collaboration and deadlines',
                                               'Relevant production, design, language or editing tools'],
                                    'technologies': ['Tools and methods used in Playback Singer / Music '
                                                     'Artist',
                                                     'Spreadsheets, digital research and clear documentation '
                                                     'where relevant',
                                                     'Role-specific platforms confirmed from current job '
                                                     'descriptions'],
                                    'projects': ['Complete a beginner project or practical exercise related '
                                                 'to Playback Singer / Music Artist',
                                                 'Create a portfolio, case study or documented practical '
                                                 'assignment for Playback Singer / Music Artist',
                                                 'Analyse a real-world challenge relevant to Playback Singer '
                                                 '/ Music Artist and present a safe, evidence-based '
                                                 'solution'],
                                    'pathways': ['Study the craft through a suitable course, mentorship or '
                                                 'structured self-learning route.',
                                                 'Build a portfolio/showreel with original work relevant to '
                                                 'the target role.',
                                                 'Practise with realistic briefs and document your creative '
                                                 'process.',
                                                 'Seek internships, auditions, commissions or entry-level '
                                                 'projects; check contract and copyright basics.'],
                                    'roles': ['Playback Singer / Music Artist',
                                              'Junior / Trainee Playback Singer / Music Artist',
                                              'Specialist or senior Playback Singer / Music Artist after '
                                              'required training and experience'],
                                    'indicative_salary_india': 'Income may be project-based or variable; '
                                                               'results depend on portfolio quality, '
                                                               'network, niche and experience.',
                                    'education_cost_india': 'Course costs range from low-cost self-learning '
                                                            'to formal design/media programmes; budget for '
                                                            'software, equipment, materials and production.',
                                    'future_outlook': 'For Playback Singer / Music Artist, assess current '
                                                      'demand using recent India-based job listings, '
                                                      'official recruitment notices and relevant industry '
                                                      'reports; outlook is not guaranteed.',
                                    'recommended_next_steps': ['Read current official qualification and '
                                                               'eligibility rules for Playback Singer / '
                                                               'Music Artist.',
                                                               'Compare at least three recognised training '
                                                               'routes for Playback Singer / Music Artist, '
                                                               'including total fees and duration.',
                                                               'Complete one relevant project, portfolio '
                                                               'piece, field exercise or supervised '
                                                               'placement for Playback Singer / Music '
                                                               'Artist.',
                                                               'Speak to a working professional and review '
                                                               'recent vacancies before committing to a '
                                                               'course.'],
                                    'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                    'research_note': 'Role-specific starter guidance generated from the '
                                                     'career catalogue category. Verify licensing, '
                                                     'eligibility, salaries, course fees and outlook with '
                                                     'official/current sources.'},
 'Film Score Composer': {'field': 'Specialised Professional Careers',
                         'summary': 'Film Score Composer: Film Score Composer is a distinct career path '
                                    'requiring role-specific knowledge, practical experience and an '
                                    'understanding of its professional standards.',
                         'skills': ['Core subject knowledge relevant to the role',
                                    'Problem-solving and professional communication',
                                    'Ethical conduct and accurate documentation',
                                    'Practical skills using tools or methods specific to the occupation'],
                         'technologies': ['Tools and methods used in Film Score Composer',
                                          'Spreadsheets, digital research and clear documentation where '
                                          'relevant',
                                          'Role-specific platforms confirmed from current job descriptions'],
                         'projects': ['Complete a beginner project or practical exercise related to Film '
                                      'Score Composer',
                                      'Create a portfolio, case study or documented practical assignment for '
                                      'Film Score Composer',
                                      'Analyse a real-world challenge relevant to Film Score Composer and '
                                      'present a safe, evidence-based solution'],
                         'pathways': ['Research the day-to-day duties and official eligibility requirements '
                                      'for Film Score Composer.',
                                      'Compare recognised courses, entry routes, duration and total cost '
                                      'before enrolling.',
                                      'Build role-relevant experience through projects, supervised practice, '
                                      'internships or a portfolio.',
                                      'Review current job advertisements and consult a qualified '
                                      'professional in this field.'],
                         'roles': ['Film Score Composer',
                                   'Junior / Trainee Film Score Composer',
                                   'Specialist or senior Film Score Composer after required training and '
                                   'experience'],
                         'indicative_salary_india': 'Salary and demand should be checked against current '
                                                    'India-specific sources for the exact role and '
                                                    'experience level.',
                         'education_cost_india': 'Confirm official course fees and include exams, materials, '
                                                 'equipment, travel and living costs.',
                         'future_outlook': 'For Film Score Composer, assess current demand using recent '
                                           'India-based job listings, official recruitment notices and '
                                           'relevant industry reports; outlook is not guaranteed.',
                         'recommended_next_steps': ['Read current official qualification and eligibility '
                                                    'rules for Film Score Composer.',
                                                    'Compare at least three recognised training routes for '
                                                    'Film Score Composer, including total fees and duration.',
                                                    'Complete one relevant project, portfolio piece, field '
                                                    'exercise or supervised placement for Film Score '
                                                    'Composer.',
                                                    'Speak to a working professional and review recent '
                                                    'vacancies before committing to a course.'],
                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                         'research_note': 'Role-specific starter guidance generated from the career '
                                          'catalogue category. Verify licensing, eligibility, salaries, '
                                          'course fees and outlook with official/current sources.'},
 'Music Teacher / Music Therapist': {'field': 'Healthcare and Life Sciences',
                                     'summary': 'Music Teacher / Music Therapist: Patient care, clinical '
                                                'knowledge, evidence-based practice, ethical judgement and '
                                                'clear communication.',
                                     'skills': ['Biology and health-science foundations',
                                                'Careful observation and documentation',
                                                'Communication with patients or teams',
                                                'Ethics, safety and evidence-based decision-making'],
                                     'technologies': ['Tools and methods used in Music Teacher / Music '
                                                      'Therapist',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to Music Teacher / Music Therapist',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for Music Teacher / Music Therapist',
                                                  'Analyse a real-world challenge relevant to Music Teacher '
                                                  '/ Music Therapist and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Investigate the recognised health-science route and '
                                                  'entrance requirements for this exact profession.',
                                                  'Complete the required accredited degree and supervised '
                                                  'clinical training.',
                                                  'Check registration/licensing rules with the relevant '
                                                  'Indian regulator or council.',
                                                  'Build experience through approved clinical placements and '
                                                  'continuing education.'],
                                     'roles': ['Music Teacher / Music Therapist',
                                               'Junior / Trainee Music Teacher / Music Therapist',
                                               'Specialist or senior Music Teacher / Music Therapist after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Healthcare hiring and pay vary strongly by '
                                                                'qualification, specialisation, '
                                                                'public/private employer and location.',
                                     'education_cost_india': 'Course costs vary widely between government '
                                                             'and private institutions; include tuition, '
                                                             'examinations, clinical materials and living '
                                                             'costs.',
                                     'future_outlook': 'For Music Teacher / Music Therapist, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for Music Teacher / Music '
                                                                'Therapist.',
                                                                'Compare at least three recognised training '
                                                                'routes for Music Teacher / Music Therapist, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for Music Teacher / Music '
                                                                'Therapist.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'DJ / Electronic Music Producer': {'field': 'Creative Media, Communication and Design',
                                    'summary': 'DJ / Electronic Music Producer: Creates stories, '
                                               'experiences, visuals, performances or communication '
                                               'materials for a defined audience.',
                                    'skills': ['Creative development and audience awareness',
                                               'Portfolio-building and revision from feedback',
                                               'Communication, collaboration and deadlines',
                                               'Relevant production, design, language or editing tools'],
                                    'technologies': ['Tools and methods used in DJ / Electronic Music '
                                                     'Producer',
                                                     'Spreadsheets, digital research and clear documentation '
                                                     'where relevant',
                                                     'Role-specific platforms confirmed from current job '
                                                     'descriptions'],
                                    'projects': ['Complete a beginner project or practical exercise related '
                                                 'to DJ / Electronic Music Producer',
                                                 'Create a portfolio, case study or documented practical '
                                                 'assignment for DJ / Electronic Music Producer',
                                                 'Analyse a real-world challenge relevant to DJ / Electronic '
                                                 'Music Producer and present a safe, evidence-based '
                                                 'solution'],
                                    'pathways': ['Study the craft through a suitable course, mentorship or '
                                                 'structured self-learning route.',
                                                 'Build a portfolio/showreel with original work relevant to '
                                                 'the target role.',
                                                 'Practise with realistic briefs and document your creative '
                                                 'process.',
                                                 'Seek internships, auditions, commissions or entry-level '
                                                 'projects; check contract and copyright basics.'],
                                    'roles': ['DJ / Electronic Music Producer',
                                              'Junior / Trainee DJ / Electronic Music Producer',
                                              'Specialist or senior DJ / Electronic Music Producer after '
                                              'required training and experience'],
                                    'indicative_salary_india': 'Income may be project-based or variable; '
                                                               'results depend on portfolio quality, '
                                                               'network, niche and experience.',
                                    'education_cost_india': 'Course costs range from low-cost self-learning '
                                                            'to formal design/media programmes; budget for '
                                                            'software, equipment, materials and production.',
                                    'future_outlook': 'For DJ / Electronic Music Producer, assess current '
                                                      'demand using recent India-based job listings, '
                                                      'official recruitment notices and relevant industry '
                                                      'reports; outlook is not guaranteed.',
                                    'recommended_next_steps': ['Read current official qualification and '
                                                               'eligibility rules for DJ / Electronic Music '
                                                               'Producer.',
                                                               'Compare at least three recognised training '
                                                               'routes for DJ / Electronic Music Producer, '
                                                               'including total fees and duration.',
                                                               'Complete one relevant project, portfolio '
                                                               'piece, field exercise or supervised '
                                                               'placement for DJ / Electronic Music '
                                                               'Producer.',
                                                               'Speak to a working professional and review '
                                                               'recent vacancies before committing to a '
                                                               'course.'],
                                    'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                    'research_note': 'Role-specific starter guidance generated from the '
                                                     'career catalogue category. Verify licensing, '
                                                     'eligibility, salaries, course fees and outlook with '
                                                     'official/current sources.'},
 'Actor / Theatre Artist': {'field': 'Creative Media, Communication and Design',
                            'summary': 'Actor / Theatre Artist: Creates stories, experiences, visuals, '
                                       'performances or communication materials for a defined audience.',
                            'skills': ['Creative development and audience awareness',
                                       'Portfolio-building and revision from feedback',
                                       'Communication, collaboration and deadlines',
                                       'Relevant production, design, language or editing tools'],
                            'technologies': ['Tools and methods used in Actor / Theatre Artist',
                                             'Spreadsheets, digital research and clear documentation where '
                                             'relevant',
                                             'Role-specific platforms confirmed from current job '
                                             'descriptions'],
                            'projects': ['Complete a beginner project or practical exercise related to Actor '
                                         '/ Theatre Artist',
                                         'Create a portfolio, case study or documented practical assignment '
                                         'for Actor / Theatre Artist',
                                         'Analyse a real-world challenge relevant to Actor / Theatre Artist '
                                         'and present a safe, evidence-based solution'],
                            'pathways': ['Study the craft through a suitable course, mentorship or '
                                         'structured self-learning route.',
                                         'Build a portfolio/showreel with original work relevant to the '
                                         'target role.',
                                         'Practise with realistic briefs and document your creative process.',
                                         'Seek internships, auditions, commissions or entry-level projects; '
                                         'check contract and copyright basics.'],
                            'roles': ['Actor / Theatre Artist',
                                      'Junior / Trainee Actor / Theatre Artist',
                                      'Specialist or senior Actor / Theatre Artist after required training '
                                      'and experience'],
                            'indicative_salary_india': 'Income may be project-based or variable; results '
                                                       'depend on portfolio quality, network, niche and '
                                                       'experience.',
                            'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                    'formal design/media programmes; budget for software, '
                                                    'equipment, materials and production.',
                            'future_outlook': 'For Actor / Theatre Artist, assess current demand using '
                                              'recent India-based job listings, official recruitment notices '
                                              'and relevant industry reports; outlook is not guaranteed.',
                            'recommended_next_steps': ['Read current official qualification and eligibility '
                                                       'rules for Actor / Theatre Artist.',
                                                       'Compare at least three recognised training routes '
                                                       'for Actor / Theatre Artist, including total fees and '
                                                       'duration.',
                                                       'Complete one relevant project, portfolio piece, '
                                                       'field exercise or supervised placement for Actor / '
                                                       'Theatre Artist.',
                                                       'Speak to a working professional and review recent '
                                                       'vacancies before committing to a course.'],
                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                            'research_note': 'Role-specific starter guidance generated from the career '
                                             'catalogue category. Verify licensing, eligibility, salaries, '
                                             'course fees and outlook with official/current sources.'},
 'Environmental / ESG Analyst': {'field': 'Environment, Agriculture and Scientific Research',
                                 'summary': 'Environmental / ESG Analyst: Uses scientific methods, '
                                            'fieldwork, laboratory work or evidence analysis to understand '
                                            'natural systems and solve specialised problems.',
                                 'skills': ['Biology, chemistry, physics or earth-science foundations as '
                                            'relevant',
                                            'Data collection, observation and analysis',
                                            'Laboratory/field safety and accurate records',
                                            'Scientific writing and evidence evaluation'],
                                 'technologies': ['Tools and methods used in Environmental / ESG Analyst',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Environmental / ESG Analyst',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Environmental / ESG Analyst',
                                              'Analyse a real-world challenge relevant to Environmental / '
                                              'ESG Analyst and present a safe, evidence-based solution'],
                                 'pathways': ['Identify the exact specialisation and required science '
                                              'subjects.',
                                              'Choose a recognised relevant degree and check whether '
                                              'postgraduate study is expected.',
                                              'Build field, lab, data-analysis or research experience under '
                                              'appropriate supervision.',
                                              'Check government recruitment, research fellowship and '
                                              'professional registration requirements where applicable.'],
                                 'roles': ['Environmental / ESG Analyst',
                                           'Junior / Trainee Environmental / ESG Analyst',
                                           'Specialist or senior Environmental / ESG Analyst after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                            'research funding, government recruitment and '
                                                            'location.',
                                 'education_cost_india': 'Budget for tuition, lab/fieldwork, equipment, '
                                                         'travel and postgraduate study; use official '
                                                         'institution fee schedules.',
                                 'future_outlook': 'For Environmental / ESG Analyst, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Environmental / ESG '
                                                            'Analyst.',
                                                            'Compare at least three recognised training '
                                                            'routes for Environmental / ESG Analyst, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Environmental / ESG Analyst.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Forest Officer (IFS)': {'field': 'Environment, Agriculture and Scientific Research',
                          'summary': 'Forest Officer (IFS): Uses scientific methods, fieldwork, laboratory '
                                     'work or evidence analysis to understand natural systems and solve '
                                     'specialised problems.',
                          'skills': ['Biology, chemistry, physics or earth-science foundations as relevant',
                                     'Data collection, observation and analysis',
                                     'Laboratory/field safety and accurate records',
                                     'Scientific writing and evidence evaluation'],
                          'technologies': ['Tools and methods used in Forest Officer (IFS)',
                                           'Spreadsheets, digital research and clear documentation where '
                                           'relevant',
                                           'Role-specific platforms confirmed from current job descriptions'],
                          'projects': ['Complete a beginner project or practical exercise related to Forest '
                                       'Officer (IFS)',
                                       'Create a portfolio, case study or documented practical assignment '
                                       'for Forest Officer (IFS)',
                                       'Analyse a real-world challenge relevant to Forest Officer (IFS) and '
                                       'present a safe, evidence-based solution'],
                          'pathways': ['Identify the exact specialisation and required science subjects.',
                                       'Choose a recognised relevant degree and check whether postgraduate '
                                       'study is expected.',
                                       'Build field, lab, data-analysis or research experience under '
                                       'appropriate supervision.',
                                       'Check government recruitment, research fellowship and professional '
                                       'registration requirements where applicable.'],
                          'roles': ['Forest Officer (IFS)',
                                    'Junior / Trainee Forest Officer (IFS)',
                                    'Specialist or senior Forest Officer (IFS) after required training and '
                                    'experience'],
                          'indicative_salary_india': 'Opportunities depend on specialisation, research '
                                                     'funding, government recruitment and location.',
                          'education_cost_india': 'Budget for tuition, lab/fieldwork, equipment, travel and '
                                                  'postgraduate study; use official institution fee '
                                                  'schedules.',
                          'future_outlook': 'For Forest Officer (IFS), assess current demand using recent '
                                            'India-based job listings, official recruitment notices and '
                                            'relevant industry reports; outlook is not guaranteed.',
                          'recommended_next_steps': ['Read current official qualification and eligibility '
                                                     'rules for Forest Officer (IFS).',
                                                     'Compare at least three recognised training routes for '
                                                     'Forest Officer (IFS), including total fees and '
                                                     'duration.',
                                                     'Complete one relevant project, portfolio piece, field '
                                                     'exercise or supervised placement for Forest Officer '
                                                     '(IFS).',
                                                     'Speak to a working professional and review recent '
                                                     'vacancies before committing to a course.'],
                          'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                          'research_note': 'Role-specific starter guidance generated from the career '
                                           'catalogue category. Verify licensing, eligibility, salaries, '
                                           'course fees and outlook with official/current sources.'},
 'Agricultural Scientist / Agronomist': {'field': 'Environment, Agriculture and Scientific Research',
                                         'summary': 'Agricultural Scientist / Agronomist: Uses scientific '
                                                    'methods, fieldwork, laboratory work or evidence '
                                                    'analysis to understand natural systems and solve '
                                                    'specialised problems.',
                                         'skills': ['Biology, chemistry, physics or earth-science '
                                                    'foundations as relevant',
                                                    'Data collection, observation and analysis',
                                                    'Laboratory/field safety and accurate records',
                                                    'Scientific writing and evidence evaluation'],
                                         'technologies': ['Tools and methods used in Agricultural Scientist '
                                                          '/ Agronomist',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Agricultural Scientist / Agronomist',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Agricultural Scientist / '
                                                      'Agronomist',
                                                      'Analyse a real-world challenge relevant to '
                                                      'Agricultural Scientist / Agronomist and present a '
                                                      'safe, evidence-based solution'],
                                         'pathways': ['Identify the exact specialisation and required '
                                                      'science subjects.',
                                                      'Choose a recognised relevant degree and check whether '
                                                      'postgraduate study is expected.',
                                                      'Build field, lab, data-analysis or research '
                                                      'experience under appropriate supervision.',
                                                      'Check government recruitment, research fellowship and '
                                                      'professional registration requirements where '
                                                      'applicable.'],
                                         'roles': ['Agricultural Scientist / Agronomist',
                                                   'Junior / Trainee Agricultural Scientist / Agronomist',
                                                   'Specialist or senior Agricultural Scientist / Agronomist '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                                    'research funding, government '
                                                                    'recruitment and location.',
                                         'education_cost_india': 'Budget for tuition, lab/fieldwork, '
                                                                 'equipment, travel and postgraduate study; '
                                                                 'use official institution fee schedules.',
                                         'future_outlook': 'For Agricultural Scientist / Agronomist, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Agricultural '
                                                                    'Scientist / Agronomist.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Agricultural '
                                                                    'Scientist / Agronomist, including total '
                                                                    'fees and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Agricultural '
                                                                    'Scientist / Agronomist.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Marine Biologist / Oceanographer': {'field': 'Environment, Agriculture and Scientific Research',
                                      'summary': 'Marine Biologist / Oceanographer: Uses scientific methods, '
                                                 'fieldwork, laboratory work or evidence analysis to '
                                                 'understand natural systems and solve specialised problems.',
                                      'skills': ['Biology, chemistry, physics or earth-science foundations '
                                                 'as relevant',
                                                 'Data collection, observation and analysis',
                                                 'Laboratory/field safety and accurate records',
                                                 'Scientific writing and evidence evaluation'],
                                      'technologies': ['Tools and methods used in Marine Biologist / '
                                                       'Oceanographer',
                                                       'Spreadsheets, digital research and clear '
                                                       'documentation where relevant',
                                                       'Role-specific platforms confirmed from current job '
                                                       'descriptions'],
                                      'projects': ['Complete a beginner project or practical exercise '
                                                   'related to Marine Biologist / Oceanographer',
                                                   'Create a portfolio, case study or documented practical '
                                                   'assignment for Marine Biologist / Oceanographer',
                                                   'Analyse a real-world challenge relevant to Marine '
                                                   'Biologist / Oceanographer and present a safe, '
                                                   'evidence-based solution'],
                                      'pathways': ['Identify the exact specialisation and required science '
                                                   'subjects.',
                                                   'Choose a recognised relevant degree and check whether '
                                                   'postgraduate study is expected.',
                                                   'Build field, lab, data-analysis or research experience '
                                                   'under appropriate supervision.',
                                                   'Check government recruitment, research fellowship and '
                                                   'professional registration requirements where '
                                                   'applicable.'],
                                      'roles': ['Marine Biologist / Oceanographer',
                                                'Junior / Trainee Marine Biologist / Oceanographer',
                                                'Specialist or senior Marine Biologist / Oceanographer after '
                                                'required training and experience'],
                                      'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                                 'research funding, government recruitment '
                                                                 'and location.',
                                      'education_cost_india': 'Budget for tuition, lab/fieldwork, equipment, '
                                                              'travel and postgraduate study; use official '
                                                              'institution fee schedules.',
                                      'future_outlook': 'For Marine Biologist / Oceanographer, assess '
                                                        'current demand using recent India-based job '
                                                        'listings, official recruitment notices and relevant '
                                                        'industry reports; outlook is not guaranteed.',
                                      'recommended_next_steps': ['Read current official qualification and '
                                                                 'eligibility rules for Marine Biologist / '
                                                                 'Oceanographer.',
                                                                 'Compare at least three recognised training '
                                                                 'routes for Marine Biologist / '
                                                                 'Oceanographer, including total fees and '
                                                                 'duration.',
                                                                 'Complete one relevant project, portfolio '
                                                                 'piece, field exercise or supervised '
                                                                 'placement for Marine Biologist / '
                                                                 'Oceanographer.',
                                                                 'Speak to a working professional and review '
                                                                 'recent vacancies before committing to a '
                                                                 'course.'],
                                      'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                      'research_note': 'Role-specific starter guidance generated from the '
                                                       'career catalogue category. Verify licensing, '
                                                       'eligibility, salaries, course fees and outlook with '
                                                       'official/current sources.'},
 'Wildlife Photographer': {'field': 'Creative Media, Communication and Design',
                           'summary': 'Wildlife Photographer: Creates stories, experiences, visuals, '
                                      'performances or communication materials for a defined audience.',
                           'skills': ['Creative development and audience awareness',
                                      'Portfolio-building and revision from feedback',
                                      'Communication, collaboration and deadlines',
                                      'Relevant production, design, language or editing tools'],
                           'technologies': ['Tools and methods used in Wildlife Photographer',
                                            'Spreadsheets, digital research and clear documentation where '
                                            'relevant',
                                            'Role-specific platforms confirmed from current job '
                                            'descriptions'],
                           'projects': ['Complete a beginner project or practical exercise related to '
                                        'Wildlife Photographer',
                                        'Create a portfolio, case study or documented practical assignment '
                                        'for Wildlife Photographer',
                                        'Analyse a real-world challenge relevant to Wildlife Photographer '
                                        'and present a safe, evidence-based solution'],
                           'pathways': ['Study the craft through a suitable course, mentorship or structured '
                                        'self-learning route.',
                                        'Build a portfolio/showreel with original work relevant to the '
                                        'target role.',
                                        'Practise with realistic briefs and document your creative process.',
                                        'Seek internships, auditions, commissions or entry-level projects; '
                                        'check contract and copyright basics.'],
                           'roles': ['Wildlife Photographer',
                                     'Junior / Trainee Wildlife Photographer',
                                     'Specialist or senior Wildlife Photographer after required training and '
                                     'experience'],
                           'indicative_salary_india': 'Income may be project-based or variable; results '
                                                      'depend on portfolio quality, network, niche and '
                                                      'experience.',
                           'education_cost_india': 'Course costs range from low-cost self-learning to formal '
                                                   'design/media programmes; budget for software, equipment, '
                                                   'materials and production.',
                           'future_outlook': 'For Wildlife Photographer, assess current demand using recent '
                                             'India-based job listings, official recruitment notices and '
                                             'relevant industry reports; outlook is not guaranteed.',
                           'recommended_next_steps': ['Read current official qualification and eligibility '
                                                      'rules for Wildlife Photographer.',
                                                      'Compare at least three recognised training routes for '
                                                      'Wildlife Photographer, including total fees and '
                                                      'duration.',
                                                      'Complete one relevant project, portfolio piece, field '
                                                      'exercise or supervised placement for Wildlife '
                                                      'Photographer.',
                                                      'Speak to a working professional and review recent '
                                                      'vacancies before committing to a course.'],
                           'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                           'research_note': 'Role-specific starter guidance generated from the career '
                                            'catalogue category. Verify licensing, eligibility, salaries, '
                                            'course fees and outlook with official/current sources.'},
 'Horticulturist / Landscape Designer': {'field': 'Environment, Agriculture and Scientific Research',
                                         'summary': 'Horticulturist / Landscape Designer: Uses scientific '
                                                    'methods, fieldwork, laboratory work or evidence '
                                                    'analysis to understand natural systems and solve '
                                                    'specialised problems.',
                                         'skills': ['Biology, chemistry, physics or earth-science '
                                                    'foundations as relevant',
                                                    'Data collection, observation and analysis',
                                                    'Laboratory/field safety and accurate records',
                                                    'Scientific writing and evidence evaluation'],
                                         'technologies': ['Tools and methods used in Horticulturist / '
                                                          'Landscape Designer',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Horticulturist / Landscape Designer',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Horticulturist / Landscape '
                                                      'Designer',
                                                      'Analyse a real-world challenge relevant to '
                                                      'Horticulturist / Landscape Designer and present a '
                                                      'safe, evidence-based solution'],
                                         'pathways': ['Identify the exact specialisation and required '
                                                      'science subjects.',
                                                      'Choose a recognised relevant degree and check whether '
                                                      'postgraduate study is expected.',
                                                      'Build field, lab, data-analysis or research '
                                                      'experience under appropriate supervision.',
                                                      'Check government recruitment, research fellowship and '
                                                      'professional registration requirements where '
                                                      'applicable.'],
                                         'roles': ['Horticulturist / Landscape Designer',
                                                   'Junior / Trainee Horticulturist / Landscape Designer',
                                                   'Specialist or senior Horticulturist / Landscape Designer '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                                    'research funding, government '
                                                                    'recruitment and location.',
                                         'education_cost_india': 'Budget for tuition, lab/fieldwork, '
                                                                 'equipment, travel and postgraduate study; '
                                                                 'use official institution fee schedules.',
                                         'future_outlook': 'For Horticulturist / Landscape Designer, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Horticulturist / '
                                                                    'Landscape Designer.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Horticulturist / '
                                                                    'Landscape Designer, including total '
                                                                    'fees and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Horticulturist '
                                                                    '/ Landscape Designer.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Geologist / Earth Scientist': {'field': 'Environment, Agriculture and Scientific Research',
                                 'summary': 'Geologist / Earth Scientist: Uses scientific methods, '
                                            'fieldwork, laboratory work or evidence analysis to understand '
                                            'natural systems and solve specialised problems.',
                                 'skills': ['Biology, chemistry, physics or earth-science foundations as '
                                            'relevant',
                                            'Data collection, observation and analysis',
                                            'Laboratory/field safety and accurate records',
                                            'Scientific writing and evidence evaluation'],
                                 'technologies': ['Tools and methods used in Geologist / Earth Scientist',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Geologist / Earth Scientist',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Geologist / Earth Scientist',
                                              'Analyse a real-world challenge relevant to Geologist / Earth '
                                              'Scientist and present a safe, evidence-based solution'],
                                 'pathways': ['Identify the exact specialisation and required science '
                                              'subjects.',
                                              'Choose a recognised relevant degree and check whether '
                                              'postgraduate study is expected.',
                                              'Build field, lab, data-analysis or research experience under '
                                              'appropriate supervision.',
                                              'Check government recruitment, research fellowship and '
                                              'professional registration requirements where applicable.'],
                                 'roles': ['Geologist / Earth Scientist',
                                           'Junior / Trainee Geologist / Earth Scientist',
                                           'Specialist or senior Geologist / Earth Scientist after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                            'research funding, government recruitment and '
                                                            'location.',
                                 'education_cost_india': 'Budget for tuition, lab/fieldwork, equipment, '
                                                         'travel and postgraduate study; use official '
                                                         'institution fee schedules.',
                                 'future_outlook': 'For Geologist / Earth Scientist, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Geologist / Earth '
                                                            'Scientist.',
                                                            'Compare at least three recognised training '
                                                            'routes for Geologist / Earth Scientist, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Geologist / Earth Scientist.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Graphic Designer / UI Designer': {'field': 'Creative Media, Communication and Design',
                                    'summary': 'Graphic Designer / UI Designer: Creates stories, '
                                               'experiences, visuals, performances or communication '
                                               'materials for a defined audience.',
                                    'skills': ['Creative development and audience awareness',
                                               'Portfolio-building and revision from feedback',
                                               'Communication, collaboration and deadlines',
                                               'Relevant production, design, language or editing tools'],
                                    'technologies': ['Tools and methods used in Graphic Designer / UI '
                                                     'Designer',
                                                     'Spreadsheets, digital research and clear documentation '
                                                     'where relevant',
                                                     'Role-specific platforms confirmed from current job '
                                                     'descriptions'],
                                    'projects': ['Complete a beginner project or practical exercise related '
                                                 'to Graphic Designer / UI Designer',
                                                 'Create a portfolio, case study or documented practical '
                                                 'assignment for Graphic Designer / UI Designer',
                                                 'Analyse a real-world challenge relevant to Graphic '
                                                 'Designer / UI Designer and present a safe, evidence-based '
                                                 'solution'],
                                    'pathways': ['Study the craft through a suitable course, mentorship or '
                                                 'structured self-learning route.',
                                                 'Build a portfolio/showreel with original work relevant to '
                                                 'the target role.',
                                                 'Practise with realistic briefs and document your creative '
                                                 'process.',
                                                 'Seek internships, auditions, commissions or entry-level '
                                                 'projects; check contract and copyright basics.'],
                                    'roles': ['Graphic Designer / UI Designer',
                                              'Junior / Trainee Graphic Designer / UI Designer',
                                              'Specialist or senior Graphic Designer / UI Designer after '
                                              'required training and experience'],
                                    'indicative_salary_india': 'Income may be project-based or variable; '
                                                               'results depend on portfolio quality, '
                                                               'network, niche and experience.',
                                    'education_cost_india': 'Course costs range from low-cost self-learning '
                                                            'to formal design/media programmes; budget for '
                                                            'software, equipment, materials and production.',
                                    'future_outlook': 'For Graphic Designer / UI Designer, assess current '
                                                      'demand using recent India-based job listings, '
                                                      'official recruitment notices and relevant industry '
                                                      'reports; outlook is not guaranteed.',
                                    'recommended_next_steps': ['Read current official qualification and '
                                                               'eligibility rules for Graphic Designer / UI '
                                                               'Designer.',
                                                               'Compare at least three recognised training '
                                                               'routes for Graphic Designer / UI Designer, '
                                                               'including total fees and duration.',
                                                               'Complete one relevant project, portfolio '
                                                               'piece, field exercise or supervised '
                                                               'placement for Graphic Designer / UI '
                                                               'Designer.',
                                                               'Speak to a working professional and review '
                                                               'recent vacancies before committing to a '
                                                               'course.'],
                                    'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                    'research_note': 'Role-specific starter guidance generated from the '
                                                     'career catalogue category. Verify licensing, '
                                                     'eligibility, salaries, course fees and outlook with '
                                                     'official/current sources.'},
 'Interior Designer': {'field': 'Creative Media, Communication and Design',
                       'summary': 'Interior Designer: Creates stories, experiences, visuals, performances or '
                                  'communication materials for a defined audience.',
                       'skills': ['Creative development and audience awareness',
                                  'Portfolio-building and revision from feedback',
                                  'Communication, collaboration and deadlines',
                                  'Relevant production, design, language or editing tools'],
                       'technologies': ['Tools and methods used in Interior Designer',
                                        'Spreadsheets, digital research and clear documentation where '
                                        'relevant',
                                        'Role-specific platforms confirmed from current job descriptions'],
                       'projects': ['Complete a beginner project or practical exercise related to Interior '
                                    'Designer',
                                    'Create a portfolio, case study or documented practical assignment for '
                                    'Interior Designer',
                                    'Analyse a real-world challenge relevant to Interior Designer and '
                                    'present a safe, evidence-based solution'],
                       'pathways': ['Study the craft through a suitable course, mentorship or structured '
                                    'self-learning route.',
                                    'Build a portfolio/showreel with original work relevant to the target '
                                    'role.',
                                    'Practise with realistic briefs and document your creative process.',
                                    'Seek internships, auditions, commissions or entry-level projects; check '
                                    'contract and copyright basics.'],
                       'roles': ['Interior Designer',
                                 'Junior / Trainee Interior Designer',
                                 'Specialist or senior Interior Designer after required training and '
                                 'experience'],
                       'indicative_salary_india': 'Income may be project-based or variable; results depend '
                                                  'on portfolio quality, network, niche and experience.',
                       'education_cost_india': 'Course costs range from low-cost self-learning to formal '
                                               'design/media programmes; budget for software, equipment, '
                                               'materials and production.',
                       'future_outlook': 'For Interior Designer, assess current demand using recent '
                                         'India-based job listings, official recruitment notices and '
                                         'relevant industry reports; outlook is not guaranteed.',
                       'recommended_next_steps': ['Read current official qualification and eligibility rules '
                                                  'for Interior Designer.',
                                                  'Compare at least three recognised training routes for '
                                                  'Interior Designer, including total fees and duration.',
                                                  'Complete one relevant project, portfolio piece, field '
                                                  'exercise or supervised placement for Interior Designer.',
                                                  'Speak to a working professional and review recent '
                                                  'vacancies before committing to a course.'],
                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                       'research_note': 'Role-specific starter guidance generated from the career catalogue '
                                        'category. Verify licensing, eligibility, salaries, course fees and '
                                        'outlook with official/current sources.'},
 'UX Researcher / UX-UI Designer': {'field': 'Creative Media, Communication and Design',
                                    'summary': 'UX Researcher / UX-UI Designer: Creates stories, '
                                               'experiences, visuals, performances or communication '
                                               'materials for a defined audience.',
                                    'skills': ['Creative development and audience awareness',
                                               'Portfolio-building and revision from feedback',
                                               'Communication, collaboration and deadlines',
                                               'Relevant production, design, language or editing tools'],
                                    'technologies': ['Tools and methods used in UX Researcher / UX-UI '
                                                     'Designer',
                                                     'Spreadsheets, digital research and clear documentation '
                                                     'where relevant',
                                                     'Role-specific platforms confirmed from current job '
                                                     'descriptions'],
                                    'projects': ['Complete a beginner project or practical exercise related '
                                                 'to UX Researcher / UX-UI Designer',
                                                 'Create a portfolio, case study or documented practical '
                                                 'assignment for UX Researcher / UX-UI Designer',
                                                 'Analyse a real-world challenge relevant to UX Researcher / '
                                                 'UX-UI Designer and present a safe, evidence-based '
                                                 'solution'],
                                    'pathways': ['Study the craft through a suitable course, mentorship or '
                                                 'structured self-learning route.',
                                                 'Build a portfolio/showreel with original work relevant to '
                                                 'the target role.',
                                                 'Practise with realistic briefs and document your creative '
                                                 'process.',
                                                 'Seek internships, auditions, commissions or entry-level '
                                                 'projects; check contract and copyright basics.'],
                                    'roles': ['UX Researcher / UX-UI Designer',
                                              'Junior / Trainee UX Researcher / UX-UI Designer',
                                              'Specialist or senior UX Researcher / UX-UI Designer after '
                                              'required training and experience'],
                                    'indicative_salary_india': 'Income may be project-based or variable; '
                                                               'results depend on portfolio quality, '
                                                               'network, niche and experience.',
                                    'education_cost_india': 'Course costs range from low-cost self-learning '
                                                            'to formal design/media programmes; budget for '
                                                            'software, equipment, materials and production.',
                                    'future_outlook': 'For UX Researcher / UX-UI Designer, assess current '
                                                      'demand using recent India-based job listings, '
                                                      'official recruitment notices and relevant industry '
                                                      'reports; outlook is not guaranteed.',
                                    'recommended_next_steps': ['Read current official qualification and '
                                                               'eligibility rules for UX Researcher / UX-UI '
                                                               'Designer.',
                                                               'Compare at least three recognised training '
                                                               'routes for UX Researcher / UX-UI Designer, '
                                                               'including total fees and duration.',
                                                               'Complete one relevant project, portfolio '
                                                               'piece, field exercise or supervised '
                                                               'placement for UX Researcher / UX-UI '
                                                               'Designer.',
                                                               'Speak to a working professional and review '
                                                               'recent vacancies before committing to a '
                                                               'course.'],
                                    'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                    'research_note': 'Role-specific starter guidance generated from the '
                                                     'career catalogue category. Verify licensing, '
                                                     'eligibility, salaries, course fees and outlook with '
                                                     'official/current sources.'},
 'Animator / VFX Artist / Game Artist': {'field': 'Creative Media, Communication and Design',
                                         'summary': 'Animator / VFX Artist / Game Artist: Creates stories, '
                                                    'experiences, visuals, performances or communication '
                                                    'materials for a defined audience.',
                                         'skills': ['Creative development and audience awareness',
                                                    'Portfolio-building and revision from feedback',
                                                    'Communication, collaboration and deadlines',
                                                    'Relevant production, design, language or editing tools'],
                                         'technologies': ['Tools and methods used in Animator / VFX Artist / '
                                                          'Game Artist',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Animator / VFX Artist / Game Artist',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Animator / VFX Artist / Game '
                                                      'Artist',
                                                      'Analyse a real-world challenge relevant to Animator / '
                                                      'VFX Artist / Game Artist and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Study the craft through a suitable course, mentorship '
                                                      'or structured self-learning route.',
                                                      'Build a portfolio/showreel with original work '
                                                      'relevant to the target role.',
                                                      'Practise with realistic briefs and document your '
                                                      'creative process.',
                                                      'Seek internships, auditions, commissions or '
                                                      'entry-level projects; check contract and copyright '
                                                      'basics.'],
                                         'roles': ['Animator / VFX Artist / Game Artist',
                                                   'Junior / Trainee Animator / VFX Artist / Game Artist',
                                                   'Specialist or senior Animator / VFX Artist / Game Artist '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Income may be project-based or '
                                                                    'variable; results depend on portfolio '
                                                                    'quality, network, niche and experience.',
                                         'education_cost_india': 'Course costs range from low-cost '
                                                                 'self-learning to formal design/media '
                                                                 'programmes; budget for software, '
                                                                 'equipment, materials and production.',
                                         'future_outlook': 'For Animator / VFX Artist / Game Artist, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Animator / VFX '
                                                                    'Artist / Game Artist.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Animator / VFX '
                                                                    'Artist / Game Artist, including total '
                                                                    'fees and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Animator / VFX '
                                                                    'Artist / Game Artist.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Fashion Designer / Textile Designer': {'field': 'Creative Media, Communication and Design',
                                         'summary': 'Fashion Designer / Textile Designer: Creates stories, '
                                                    'experiences, visuals, performances or communication '
                                                    'materials for a defined audience.',
                                         'skills': ['Creative development and audience awareness',
                                                    'Portfolio-building and revision from feedback',
                                                    'Communication, collaboration and deadlines',
                                                    'Relevant production, design, language or editing tools'],
                                         'technologies': ['Tools and methods used in Fashion Designer / '
                                                          'Textile Designer',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Fashion Designer / Textile Designer',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Fashion Designer / Textile '
                                                      'Designer',
                                                      'Analyse a real-world challenge relevant to Fashion '
                                                      'Designer / Textile Designer and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Study the craft through a suitable course, mentorship '
                                                      'or structured self-learning route.',
                                                      'Build a portfolio/showreel with original work '
                                                      'relevant to the target role.',
                                                      'Practise with realistic briefs and document your '
                                                      'creative process.',
                                                      'Seek internships, auditions, commissions or '
                                                      'entry-level projects; check contract and copyright '
                                                      'basics.'],
                                         'roles': ['Fashion Designer / Textile Designer',
                                                   'Junior / Trainee Fashion Designer / Textile Designer',
                                                   'Specialist or senior Fashion Designer / Textile Designer '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Income may be project-based or '
                                                                    'variable; results depend on portfolio '
                                                                    'quality, network, niche and experience.',
                                         'education_cost_india': 'Course costs range from low-cost '
                                                                 'self-learning to formal design/media '
                                                                 'programmes; budget for software, '
                                                                 'equipment, materials and production.',
                                         'future_outlook': 'For Fashion Designer / Textile Designer, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Fashion Designer '
                                                                    '/ Textile Designer.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Fashion Designer / '
                                                                    'Textile Designer, including total fees '
                                                                    'and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Fashion '
                                                                    'Designer / Textile Designer.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Photographer / Videographer': {'field': 'Creative Media, Communication and Design',
                                 'summary': 'Photographer / Videographer: Creates stories, experiences, '
                                            'visuals, performances or communication materials for a defined '
                                            'audience.',
                                 'skills': ['Creative development and audience awareness',
                                            'Portfolio-building and revision from feedback',
                                            'Communication, collaboration and deadlines',
                                            'Relevant production, design, language or editing tools'],
                                 'technologies': ['Tools and methods used in Photographer / Videographer',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Photographer / Videographer',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Photographer / Videographer',
                                              'Analyse a real-world challenge relevant to Photographer / '
                                              'Videographer and present a safe, evidence-based solution'],
                                 'pathways': ['Study the craft through a suitable course, mentorship or '
                                              'structured self-learning route.',
                                              'Build a portfolio/showreel with original work relevant to the '
                                              'target role.',
                                              'Practise with realistic briefs and document your creative '
                                              'process.',
                                              'Seek internships, auditions, commissions or entry-level '
                                              'projects; check contract and copyright basics.'],
                                 'roles': ['Photographer / Videographer',
                                           'Junior / Trainee Photographer / Videographer',
                                           'Specialist or senior Photographer / Videographer after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Income may be project-based or variable; '
                                                            'results depend on portfolio quality, network, '
                                                            'niche and experience.',
                                 'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                         'formal design/media programmes; budget for '
                                                         'software, equipment, materials and production.',
                                 'future_outlook': 'For Photographer / Videographer, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Photographer / '
                                                            'Videographer.',
                                                            'Compare at least three recognised training '
                                                            'routes for Photographer / Videographer, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Photographer / Videographer.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Illustrator / Cartoonist': {'field': 'Creative Media, Communication and Design',
                              'summary': 'Illustrator / Cartoonist: Creates stories, experiences, visuals, '
                                         'performances or communication materials for a defined audience.',
                              'skills': ['Creative development and audience awareness',
                                         'Portfolio-building and revision from feedback',
                                         'Communication, collaboration and deadlines',
                                         'Relevant production, design, language or editing tools'],
                              'technologies': ['Tools and methods used in Illustrator / Cartoonist',
                                               'Spreadsheets, digital research and clear documentation where '
                                               'relevant',
                                               'Role-specific platforms confirmed from current job '
                                               'descriptions'],
                              'projects': ['Complete a beginner project or practical exercise related to '
                                           'Illustrator / Cartoonist',
                                           'Create a portfolio, case study or documented practical '
                                           'assignment for Illustrator / Cartoonist',
                                           'Analyse a real-world challenge relevant to Illustrator / '
                                           'Cartoonist and present a safe, evidence-based solution'],
                              'pathways': ['Study the craft through a suitable course, mentorship or '
                                           'structured self-learning route.',
                                           'Build a portfolio/showreel with original work relevant to the '
                                           'target role.',
                                           'Practise with realistic briefs and document your creative '
                                           'process.',
                                           'Seek internships, auditions, commissions or entry-level '
                                           'projects; check contract and copyright basics.'],
                              'roles': ['Illustrator / Cartoonist',
                                        'Junior / Trainee Illustrator / Cartoonist',
                                        'Specialist or senior Illustrator / Cartoonist after required '
                                        'training and experience'],
                              'indicative_salary_india': 'Income may be project-based or variable; results '
                                                         'depend on portfolio quality, network, niche and '
                                                         'experience.',
                              'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                      'formal design/media programmes; budget for software, '
                                                      'equipment, materials and production.',
                              'future_outlook': 'For Illustrator / Cartoonist, assess current demand using '
                                                'recent India-based job listings, official recruitment '
                                                'notices and relevant industry reports; outlook is not '
                                                'guaranteed.',
                              'recommended_next_steps': ['Read current official qualification and '
                                                         'eligibility rules for Illustrator / Cartoonist.',
                                                         'Compare at least three recognised training routes '
                                                         'for Illustrator / Cartoonist, including total fees '
                                                         'and duration.',
                                                         'Complete one relevant project, portfolio piece, '
                                                         'field exercise or supervised placement for '
                                                         'Illustrator / Cartoonist.',
                                                         'Speak to a working professional and review recent '
                                                         'vacancies before committing to a course.'],
                              'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                              'research_note': 'Role-specific starter guidance generated from the career '
                                               'catalogue category. Verify licensing, eligibility, salaries, '
                                               'course fees and outlook with official/current sources.'},
 'Clinical Psychologist / Counseling Psychologist': {'field': 'Psychology, Counselling and Community Support',
                                                     'summary': 'Clinical Psychologist / Counseling '
                                                                'Psychologist: Supports people through '
                                                                'evidence-informed guidance, assessment, '
                                                                'education or community services within '
                                                                'professional boundaries.',
                                                     'skills': ['Active listening and respectful '
                                                                'communication',
                                                                'Ethics, confidentiality and boundaries',
                                                                'Research literacy and accurate '
                                                                'documentation',
                                                                'Cultural awareness and reflective practice'],
                                                     'technologies': ['Tools and methods used in Clinical '
                                                                      'Psychologist / Counseling '
                                                                      'Psychologist',
                                                                      'Spreadsheets, digital research and '
                                                                      'clear documentation where relevant',
                                                                      'Role-specific platforms confirmed '
                                                                      'from current job descriptions'],
                                                     'projects': ['Complete a beginner project or practical '
                                                                  'exercise related to Clinical Psychologist '
                                                                  '/ Counseling Psychologist',
                                                                  'Create a portfolio, case study or '
                                                                  'documented practical assignment for '
                                                                  'Clinical Psychologist / Counseling '
                                                                  'Psychologist',
                                                                  'Analyse a real-world challenge relevant '
                                                                  'to Clinical Psychologist / Counseling '
                                                                  'Psychologist and present a safe, '
                                                                  'evidence-based solution'],
                                                     'pathways': ['Check the exact role title and '
                                                                  'qualification rules; clinical practice '
                                                                  'may require specific recognised training '
                                                                  'and registration.',
                                                                  'Choose an accredited psychology, '
                                                                  'counselling or social-work route suited '
                                                                  'to the intended scope.',
                                                                  'Gain supervised practice only within the '
                                                                  'permitted training framework.',
                                                                  'Do not present short courses as '
                                                                  'substitutes for regulated qualifications; '
                                                                  'verify current rules.'],
                                                     'roles': ['Clinical Psychologist / Counseling '
                                                               'Psychologist',
                                                               'Junior / Trainee Clinical Psychologist / '
                                                               'Counseling Psychologist',
                                                               'Specialist or senior Clinical Psychologist / '
                                                               'Counseling Psychologist after required '
                                                               'training and experience'],
                                                     'indicative_salary_india': 'Earnings vary by '
                                                                                'credentials, setting, '
                                                                                'caseload, city and '
                                                                                'experience; private '
                                                                                'practice income is not '
                                                                                'guaranteed.',
                                                     'education_cost_india': 'Include degree/postgraduate '
                                                                             'fees, supervised training, '
                                                                             'registration where required '
                                                                             'and continuing professional '
                                                                             'development.',
                                                     'future_outlook': 'For Clinical Psychologist / '
                                                                       'Counseling Psychologist, assess '
                                                                       'current demand using recent '
                                                                       'India-based job listings, official '
                                                                       'recruitment notices and relevant '
                                                                       'industry reports; outlook is not '
                                                                       'guaranteed.',
                                                     'recommended_next_steps': ['Read current official '
                                                                                'qualification and '
                                                                                'eligibility rules for '
                                                                                'Clinical Psychologist / '
                                                                                'Counseling Psychologist.',
                                                                                'Compare at least three '
                                                                                'recognised training routes '
                                                                                'for Clinical Psychologist / '
                                                                                'Counseling Psychologist, '
                                                                                'including total fees and '
                                                                                'duration.',
                                                                                'Complete one relevant '
                                                                                'project, portfolio piece, '
                                                                                'field exercise or '
                                                                                'supervised placement for '
                                                                                'Clinical Psychologist / '
                                                                                'Counseling Psychologist.',
                                                                                'Speak to a working '
                                                                                'professional and review '
                                                                                'recent vacancies before '
                                                                                'committing to a course.'],
                                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                                     'research_note': 'Role-specific starter guidance '
                                                                      'generated from the career catalogue '
                                                                      'category. Verify licensing, '
                                                                      'eligibility, salaries, course fees '
                                                                      'and outlook with official/current '
                                                                      'sources.'},
 'Life Coach / Mental Health Coach': {'field': 'Psychology, Counselling and Community Support',
                                      'summary': 'Life Coach / Mental Health Coach: Supports people through '
                                                 'evidence-informed guidance, assessment, education or '
                                                 'community services within professional boundaries.',
                                      'skills': ['Active listening and respectful communication',
                                                 'Ethics, confidentiality and boundaries',
                                                 'Research literacy and accurate documentation',
                                                 'Cultural awareness and reflective practice'],
                                      'technologies': ['Tools and methods used in Life Coach / Mental Health '
                                                       'Coach',
                                                       'Spreadsheets, digital research and clear '
                                                       'documentation where relevant',
                                                       'Role-specific platforms confirmed from current job '
                                                       'descriptions'],
                                      'projects': ['Complete a beginner project or practical exercise '
                                                   'related to Life Coach / Mental Health Coach',
                                                   'Create a portfolio, case study or documented practical '
                                                   'assignment for Life Coach / Mental Health Coach',
                                                   'Analyse a real-world challenge relevant to Life Coach / '
                                                   'Mental Health Coach and present a safe, evidence-based '
                                                   'solution'],
                                      'pathways': ['Check the exact role title and qualification rules; '
                                                   'clinical practice may require specific recognised '
                                                   'training and registration.',
                                                   'Choose an accredited psychology, counselling or '
                                                   'social-work route suited to the intended scope.',
                                                   'Gain supervised practice only within the permitted '
                                                   'training framework.',
                                                   'Do not present short courses as substitutes for '
                                                   'regulated qualifications; verify current rules.'],
                                      'roles': ['Life Coach / Mental Health Coach',
                                                'Junior / Trainee Life Coach / Mental Health Coach',
                                                'Specialist or senior Life Coach / Mental Health Coach after '
                                                'required training and experience'],
                                      'indicative_salary_india': 'Earnings vary by credentials, setting, '
                                                                 'caseload, city and experience; private '
                                                                 'practice income is not guaranteed.',
                                      'education_cost_india': 'Include degree/postgraduate fees, supervised '
                                                              'training, registration where required and '
                                                              'continuing professional development.',
                                      'future_outlook': 'For Life Coach / Mental Health Coach, assess '
                                                        'current demand using recent India-based job '
                                                        'listings, official recruitment notices and relevant '
                                                        'industry reports; outlook is not guaranteed.',
                                      'recommended_next_steps': ['Read current official qualification and '
                                                                 'eligibility rules for Life Coach / Mental '
                                                                 'Health Coach.',
                                                                 'Compare at least three recognised training '
                                                                 'routes for Life Coach / Mental Health '
                                                                 'Coach, including total fees and duration.',
                                                                 'Complete one relevant project, portfolio '
                                                                 'piece, field exercise or supervised '
                                                                 'placement for Life Coach / Mental Health '
                                                                 'Coach.',
                                                                 'Speak to a working professional and review '
                                                                 'recent vacancies before committing to a '
                                                                 'course.'],
                                      'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                      'research_note': 'Role-specific starter guidance generated from the '
                                                       'career catalogue category. Verify licensing, '
                                                       'eligibility, salaries, course fees and outlook with '
                                                       'official/current sources.'},
 'Research Scholar / PhD Academic': {'field': 'Education, Training and Research',
                                     'summary': 'Research Scholar / PhD Academic: Supports learning, '
                                                'assessment, research or professional development through '
                                                'subject expertise and structured communication.',
                                     'skills': ['Subject knowledge and clear explanation',
                                                'Lesson, training or research planning',
                                                'Feedback, assessment and learner support',
                                                'Digital learning tools and professional ethics'],
                                     'technologies': ['Tools and methods used in Research Scholar / PhD '
                                                      'Academic',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to Research Scholar / PhD Academic',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for Research Scholar / PhD Academic',
                                                  'Analyse a real-world challenge relevant to Research '
                                                  'Scholar / PhD Academic and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Choose the subject and age/group you want to work with.',
                                                  'Check recognised teacher-training, postgraduate, '
                                                  'eligibility-test or research requirements for the target '
                                                  'role.',
                                                  'Create sample lessons, training materials, research work '
                                                  'or a teaching portfolio.',
                                                  'Gain supervised teaching/training experience and check '
                                                  'current recruitment criteria.'],
                                     'roles': ['Research Scholar / PhD Academic',
                                               'Junior / Trainee Research Scholar / PhD Academic',
                                               'Specialist or senior Research Scholar / PhD Academic after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Opportunities depend on subject, '
                                                                'institution, qualifications, location and '
                                                                'public/private recruitment cycles.',
                                     'education_cost_india': 'Costs depend on degree, teacher-training '
                                                             'qualification, eligibility tests, research '
                                                             'fees and institution; confirm official fee '
                                                             'schedules.',
                                     'future_outlook': 'For Research Scholar / PhD Academic, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for Research Scholar / '
                                                                'PhD Academic.',
                                                                'Compare at least three recognised training '
                                                                'routes for Research Scholar / PhD Academic, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for Research Scholar / PhD '
                                                                'Academic.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'Career Counselor / School Counselor': {'field': 'Education, Training and Research',
                                         'summary': 'Career Counselor / School Counselor: Supports learning, '
                                                    'assessment, research or professional development '
                                                    'through subject expertise and structured communication.',
                                         'skills': ['Subject knowledge and clear explanation',
                                                    'Lesson, training or research planning',
                                                    'Feedback, assessment and learner support',
                                                    'Digital learning tools and professional ethics'],
                                         'technologies': ['Tools and methods used in Career Counselor / '
                                                          'School Counselor',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Career Counselor / School Counselor',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Career Counselor / School '
                                                      'Counselor',
                                                      'Analyse a real-world challenge relevant to Career '
                                                      'Counselor / School Counselor and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Choose the subject and age/group you want to work '
                                                      'with.',
                                                      'Check recognised teacher-training, postgraduate, '
                                                      'eligibility-test or research requirements for the '
                                                      'target role.',
                                                      'Create sample lessons, training materials, research '
                                                      'work or a teaching portfolio.',
                                                      'Gain supervised teaching/training experience and '
                                                      'check current recruitment criteria.'],
                                         'roles': ['Career Counselor / School Counselor',
                                                   'Junior / Trainee Career Counselor / School Counselor',
                                                   'Specialist or senior Career Counselor / School Counselor '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Opportunities depend on subject, '
                                                                    'institution, qualifications, location '
                                                                    'and public/private recruitment cycles.',
                                         'education_cost_india': 'Costs depend on degree, teacher-training '
                                                                 'qualification, eligibility tests, research '
                                                                 'fees and institution; confirm official fee '
                                                                 'schedules.',
                                         'future_outlook': 'For Career Counselor / School Counselor, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Career Counselor '
                                                                    '/ School Counselor.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Career Counselor / '
                                                                    'School Counselor, including total fees '
                                                                    'and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Career '
                                                                    'Counselor / School Counselor.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Instructional Designer': {'field': 'Education, Training and Research',
                            'summary': 'Instructional Designer: Supports learning, assessment, research or '
                                       'professional development through subject expertise and structured '
                                       'communication.',
                            'skills': ['Subject knowledge and clear explanation',
                                       'Lesson, training or research planning',
                                       'Feedback, assessment and learner support',
                                       'Digital learning tools and professional ethics'],
                            'technologies': ['Tools and methods used in Instructional Designer',
                                             'Spreadsheets, digital research and clear documentation where '
                                             'relevant',
                                             'Role-specific platforms confirmed from current job '
                                             'descriptions'],
                            'projects': ['Complete a beginner project or practical exercise related to '
                                         'Instructional Designer',
                                         'Create a portfolio, case study or documented practical assignment '
                                         'for Instructional Designer',
                                         'Analyse a real-world challenge relevant to Instructional Designer '
                                         'and present a safe, evidence-based solution'],
                            'pathways': ['Choose the subject and age/group you want to work with.',
                                         'Check recognised teacher-training, postgraduate, eligibility-test '
                                         'or research requirements for the target role.',
                                         'Create sample lessons, training materials, research work or a '
                                         'teaching portfolio.',
                                         'Gain supervised teaching/training experience and check current '
                                         'recruitment criteria.'],
                            'roles': ['Instructional Designer',
                                      'Junior / Trainee Instructional Designer',
                                      'Specialist or senior Instructional Designer after required training '
                                      'and experience'],
                            'indicative_salary_india': 'Opportunities depend on subject, institution, '
                                                       'qualifications, location and public/private '
                                                       'recruitment cycles.',
                            'education_cost_india': 'Costs depend on degree, teacher-training qualification, '
                                                    'eligibility tests, research fees and institution; '
                                                    'confirm official fee schedules.',
                            'future_outlook': 'For Instructional Designer, assess current demand using '
                                              'recent India-based job listings, official recruitment notices '
                                              'and relevant industry reports; outlook is not guaranteed.',
                            'recommended_next_steps': ['Read current official qualification and eligibility '
                                                       'rules for Instructional Designer.',
                                                       'Compare at least three recognised training routes '
                                                       'for Instructional Designer, including total fees and '
                                                       'duration.',
                                                       'Complete one relevant project, portfolio piece, '
                                                       'field exercise or supervised placement for '
                                                       'Instructional Designer.',
                                                       'Speak to a working professional and review recent '
                                                       'vacancies before committing to a course.'],
                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                            'research_note': 'Role-specific starter guidance generated from the career '
                                             'catalogue category. Verify licensing, eligibility, salaries, '
                                             'course fees and outlook with official/current sources.'},
 'Public Policy Analyst': {'field': 'Finance, Accounting and Governance',
                           'summary': 'Public Policy Analyst: Works with financial records, analysis, risk, '
                                      'regulation, markets or organisational decisions.',
                           'skills': ['Numeracy and analytical reasoning',
                                      'Excel/spreadsheets and data interpretation',
                                      'Accuracy, confidentiality and professional ethics',
                                      'Financial reporting, regulation or research relevant to the role'],
                           'technologies': ['Tools and methods used in Public Policy Analyst',
                                            'Spreadsheets, digital research and clear documentation where '
                                            'relevant',
                                            'Role-specific platforms confirmed from current job '
                                            'descriptions'],
                           'projects': ['Complete a beginner project or practical exercise related to Public '
                                        'Policy Analyst',
                                        'Create a portfolio, case study or documented practical assignment '
                                        'for Public Policy Analyst',
                                        'Analyse a real-world challenge relevant to Public Policy Analyst '
                                        'and present a safe, evidence-based solution'],
                           'pathways': ['Check the official qualification or recruitment route (for example, '
                                        'professional-body exams or public recruitment notices).',
                                        'Build accounting, finance, economics, spreadsheet and analytical '
                                        'foundations as appropriate.',
                                        'Practise with case studies, financial models or compliant sample '
                                        'reports.',
                                        'Verify current exam rules, eligibility, registration and '
                                        'role-specific certifications from official sources.'],
                           'roles': ['Public Policy Analyst',
                                     'Junior / Trainee Public Policy Analyst',
                                     'Specialist or senior Public Policy Analyst after required training and '
                                     'experience'],
                           'indicative_salary_india': 'Compensation varies by qualification, employer, city, '
                                                      'performance and experience; public-sector pay follows '
                                                      'official notices.',
                           'education_cost_india': 'Include professional-body registration, exam attempts, '
                                                   'coaching if chosen, study materials and degree tuition; '
                                                   'official fees change.',
                           'future_outlook': 'For Public Policy Analyst, assess current demand using recent '
                                             'India-based job listings, official recruitment notices and '
                                             'relevant industry reports; outlook is not guaranteed.',
                           'recommended_next_steps': ['Read current official qualification and eligibility '
                                                      'rules for Public Policy Analyst.',
                                                      'Compare at least three recognised training routes for '
                                                      'Public Policy Analyst, including total fees and '
                                                      'duration.',
                                                      'Complete one relevant project, portfolio piece, field '
                                                      'exercise or supervised placement for Public Policy '
                                                      'Analyst.',
                                                      'Speak to a working professional and review recent '
                                                      'vacancies before committing to a course.'],
                           'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                           'research_note': 'Role-specific starter guidance generated from the career '
                                            'catalogue category. Verify licensing, eligibility, salaries, '
                                            'course fees and outlook with official/current sources.'},
 'Social Entrepreneur / Consultant': {'field': 'Public Service, Defence and Social Impact',
                                      'summary': 'Social Entrepreneur / Consultant: Serves communities or '
                                                 'public institutions through administration, protection, '
                                                 'policy, development or disciplined operational work.',
                                      'skills': ['Communication and public-service orientation',
                                                 'Ethical judgement and accountability',
                                                 'Role-specific general knowledge, fitness or subject '
                                                 'preparation',
                                                 'Planning, teamwork and decision-making'],
                                      'technologies': ['Tools and methods used in Social Entrepreneur / '
                                                       'Consultant',
                                                       'Spreadsheets, digital research and clear '
                                                       'documentation where relevant',
                                                       'Role-specific platforms confirmed from current job '
                                                       'descriptions'],
                                      'projects': ['Complete a beginner project or practical exercise '
                                                   'related to Social Entrepreneur / Consultant',
                                                   'Create a portfolio, case study or documented practical '
                                                   'assignment for Social Entrepreneur / Consultant',
                                                   'Analyse a real-world challenge relevant to Social '
                                                   'Entrepreneur / Consultant and present a safe, '
                                                   'evidence-based solution'],
                                      'pathways': ['Read the latest official eligibility, age, education, '
                                                   'medical and selection criteria for the exact post.',
                                                   'Plan degree choices and exam preparation around the '
                                                   'official recruitment route.',
                                                   'For uniformed services, assess physical and medical '
                                                   'standards early.',
                                                   'Use official notifications for dates, syllabus, '
                                                   'selection stages and pay details.'],
                                      'roles': ['Social Entrepreneur / Consultant',
                                                'Junior / Trainee Social Entrepreneur / Consultant',
                                                'Specialist or senior Social Entrepreneur / Consultant after '
                                                'required training and experience'],
                                      'indicative_salary_india': 'Vacancies and pay depend on official '
                                                                 'recruitment cycles, rank, cadre, '
                                                                 'allowances and service rules.',
                                      'education_cost_india': 'Preparation expenses vary; include exam fees, '
                                                              'study materials, coaching if chosen, travel '
                                                              'and medical/fitness preparation.',
                                      'future_outlook': 'For Social Entrepreneur / Consultant, assess '
                                                        'current demand using recent India-based job '
                                                        'listings, official recruitment notices and relevant '
                                                        'industry reports; outlook is not guaranteed.',
                                      'recommended_next_steps': ['Read current official qualification and '
                                                                 'eligibility rules for Social Entrepreneur '
                                                                 '/ Consultant.',
                                                                 'Compare at least three recognised training '
                                                                 'routes for Social Entrepreneur / '
                                                                 'Consultant, including total fees and '
                                                                 'duration.',
                                                                 'Complete one relevant project, portfolio '
                                                                 'piece, field exercise or supervised '
                                                                 'placement for Social Entrepreneur / '
                                                                 'Consultant.',
                                                                 'Speak to a working professional and review '
                                                                 'recent vacancies before committing to a '
                                                                 'course.'],
                                      'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                      'research_note': 'Role-specific starter guidance generated from the '
                                                       'career catalogue category. Verify licensing, '
                                                       'eligibility, salaries, course fees and outlook with '
                                                       'official/current sources.'},
 'MBBS Doctor / General Physician': {'field': 'Healthcare and Life Sciences',
                                     'summary': 'MBBS Doctor / General Physician: Patient care, clinical '
                                                'knowledge, evidence-based practice, ethical judgement and '
                                                'clear communication.',
                                     'skills': ['Biology and health-science foundations',
                                                'Careful observation and documentation',
                                                'Communication with patients or teams',
                                                'Ethics, safety and evidence-based decision-making'],
                                     'technologies': ['Tools and methods used in MBBS Doctor / General '
                                                      'Physician',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to MBBS Doctor / General Physician',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for MBBS Doctor / General Physician',
                                                  'Analyse a real-world challenge relevant to MBBS Doctor / '
                                                  'General Physician and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Investigate the recognised health-science route and '
                                                  'entrance requirements for this exact profession.',
                                                  'Complete the required accredited degree and supervised '
                                                  'clinical training.',
                                                  'Check registration/licensing rules with the relevant '
                                                  'Indian regulator or council.',
                                                  'Build experience through approved clinical placements and '
                                                  'continuing education.'],
                                     'roles': ['MBBS Doctor / General Physician',
                                               'Junior / Trainee MBBS Doctor / General Physician',
                                               'Specialist or senior MBBS Doctor / General Physician after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Healthcare hiring and pay vary strongly by '
                                                                'qualification, specialisation, '
                                                                'public/private employer and location.',
                                     'education_cost_india': 'Course costs vary widely between government '
                                                             'and private institutions; include tuition, '
                                                             'examinations, clinical materials and living '
                                                             'costs.',
                                     'future_outlook': 'For MBBS Doctor / General Physician, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for MBBS Doctor / General '
                                                                'Physician.',
                                                                'Compare at least three recognised training '
                                                                'routes for MBBS Doctor / General Physician, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for MBBS Doctor / General '
                                                                'Physician.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'Nurse / Staff Nurse': {'field': 'Healthcare and Life Sciences',
                         'summary': 'Nurse / Staff Nurse: Patient care, clinical knowledge, evidence-based '
                                    'practice, ethical judgement and clear communication.',
                         'skills': ['Biology and health-science foundations',
                                    'Careful observation and documentation',
                                    'Communication with patients or teams',
                                    'Ethics, safety and evidence-based decision-making'],
                         'technologies': ['Tools and methods used in Nurse / Staff Nurse',
                                          'Spreadsheets, digital research and clear documentation where '
                                          'relevant',
                                          'Role-specific platforms confirmed from current job descriptions'],
                         'projects': ['Complete a beginner project or practical exercise related to Nurse / '
                                      'Staff Nurse',
                                      'Create a portfolio, case study or documented practical assignment for '
                                      'Nurse / Staff Nurse',
                                      'Analyse a real-world challenge relevant to Nurse / Staff Nurse and '
                                      'present a safe, evidence-based solution'],
                         'pathways': ['Investigate the recognised health-science route and entrance '
                                      'requirements for this exact profession.',
                                      'Complete the required accredited degree and supervised clinical '
                                      'training.',
                                      'Check registration/licensing rules with the relevant Indian regulator '
                                      'or council.',
                                      'Build experience through approved clinical placements and continuing '
                                      'education.'],
                         'roles': ['Nurse / Staff Nurse',
                                   'Junior / Trainee Nurse / Staff Nurse',
                                   'Specialist or senior Nurse / Staff Nurse after required training and '
                                   'experience'],
                         'indicative_salary_india': 'Healthcare hiring and pay vary strongly by '
                                                    'qualification, specialisation, public/private employer '
                                                    'and location.',
                         'education_cost_india': 'Course costs vary widely between government and private '
                                                 'institutions; include tuition, examinations, clinical '
                                                 'materials and living costs.',
                         'future_outlook': 'For Nurse / Staff Nurse, assess current demand using recent '
                                           'India-based job listings, official recruitment notices and '
                                           'relevant industry reports; outlook is not guaranteed.',
                         'recommended_next_steps': ['Read current official qualification and eligibility '
                                                    'rules for Nurse / Staff Nurse.',
                                                    'Compare at least three recognised training routes for '
                                                    'Nurse / Staff Nurse, including total fees and duration.',
                                                    'Complete one relevant project, portfolio piece, field '
                                                    'exercise or supervised placement for Nurse / Staff '
                                                    'Nurse.',
                                                    'Speak to a working professional and review recent '
                                                    'vacancies before committing to a course.'],
                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                         'research_note': 'Role-specific starter guidance generated from the career '
                                          'catalogue category. Verify licensing, eligibility, salaries, '
                                          'course fees and outlook with official/current sources.'},
 'School Teacher / College Professor': {'field': 'Education, Training and Research',
                                        'summary': 'School Teacher / College Professor: Supports learning, '
                                                   'assessment, research or professional development through '
                                                   'subject expertise and structured communication.',
                                        'skills': ['Subject knowledge and clear explanation',
                                                   'Lesson, training or research planning',
                                                   'Feedback, assessment and learner support',
                                                   'Digital learning tools and professional ethics'],
                                        'technologies': ['Tools and methods used in School Teacher / College '
                                                         'Professor',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to School Teacher / College Professor',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for School Teacher / College Professor',
                                                     'Analyse a real-world challenge relevant to School '
                                                     'Teacher / College Professor and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Choose the subject and age/group you want to work '
                                                     'with.',
                                                     'Check recognised teacher-training, postgraduate, '
                                                     'eligibility-test or research requirements for the '
                                                     'target role.',
                                                     'Create sample lessons, training materials, research '
                                                     'work or a teaching portfolio.',
                                                     'Gain supervised teaching/training experience and check '
                                                     'current recruitment criteria.'],
                                        'roles': ['School Teacher / College Professor',
                                                  'Junior / Trainee School Teacher / College Professor',
                                                  'Specialist or senior School Teacher / College Professor '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Opportunities depend on subject, '
                                                                   'institution, qualifications, location '
                                                                   'and public/private recruitment cycles.',
                                        'education_cost_india': 'Costs depend on degree, teacher-training '
                                                                'qualification, eligibility tests, research '
                                                                'fees and institution; confirm official fee '
                                                                'schedules.',
                                        'future_outlook': 'For School Teacher / College Professor, assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for School Teacher / '
                                                                   'College Professor.',
                                                                   'Compare at least three recognised '
                                                                   'training routes for School Teacher / '
                                                                   'College Professor, including total fees '
                                                                   'and duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for School Teacher / College '
                                                                   'Professor.',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'Social Worker / Community Development Officer': {'field': 'Public Service, Defence and Social Impact',
                                                   'summary': 'Social Worker / Community Development '
                                                              'Officer: Serves communities or public '
                                                              'institutions through administration, '
                                                              'protection, policy, development or '
                                                              'disciplined operational work.',
                                                   'skills': ['Communication and public-service orientation',
                                                              'Ethical judgement and accountability',
                                                              'Role-specific general knowledge, fitness or '
                                                              'subject preparation',
                                                              'Planning, teamwork and decision-making'],
                                                   'technologies': ['Tools and methods used in Social Worker '
                                                                    '/ Community Development Officer',
                                                                    'Spreadsheets, digital research and '
                                                                    'clear documentation where relevant',
                                                                    'Role-specific platforms confirmed from '
                                                                    'current job descriptions'],
                                                   'projects': ['Complete a beginner project or practical '
                                                                'exercise related to Social Worker / '
                                                                'Community Development Officer',
                                                                'Create a portfolio, case study or '
                                                                'documented practical assignment for Social '
                                                                'Worker / Community Development Officer',
                                                                'Analyse a real-world challenge relevant to '
                                                                'Social Worker / Community Development '
                                                                'Officer and present a safe, evidence-based '
                                                                'solution'],
                                                   'pathways': ['Read the latest official eligibility, age, '
                                                                'education, medical and selection criteria '
                                                                'for the exact post.',
                                                                'Plan degree choices and exam preparation '
                                                                'around the official recruitment route.',
                                                                'For uniformed services, assess physical and '
                                                                'medical standards early.',
                                                                'Use official notifications for dates, '
                                                                'syllabus, selection stages and pay '
                                                                'details.'],
                                                   'roles': ['Social Worker / Community Development Officer',
                                                             'Junior / Trainee Social Worker / Community '
                                                             'Development Officer',
                                                             'Specialist or senior Social Worker / Community '
                                                             'Development Officer after required training '
                                                             'and experience'],
                                                   'indicative_salary_india': 'Vacancies and pay depend on '
                                                                              'official recruitment cycles, '
                                                                              'rank, cadre, allowances and '
                                                                              'service rules.',
                                                   'education_cost_india': 'Preparation expenses vary; '
                                                                           'include exam fees, study '
                                                                           'materials, coaching if chosen, '
                                                                           'travel and medical/fitness '
                                                                           'preparation.',
                                                   'future_outlook': 'For Social Worker / Community '
                                                                     'Development Officer, assess current '
                                                                     'demand using recent India-based job '
                                                                     'listings, official recruitment notices '
                                                                     'and relevant industry reports; outlook '
                                                                     'is not guaranteed.',
                                                   'recommended_next_steps': ['Read current official '
                                                                              'qualification and eligibility '
                                                                              'rules for Social Worker / '
                                                                              'Community Development '
                                                                              'Officer.',
                                                                              'Compare at least three '
                                                                              'recognised training routes '
                                                                              'for Social Worker / Community '
                                                                              'Development Officer, '
                                                                              'including total fees and '
                                                                              'duration.',
                                                                              'Complete one relevant '
                                                                              'project, portfolio piece, '
                                                                              'field exercise or supervised '
                                                                              'placement for Social Worker / '
                                                                              'Community Development '
                                                                              'Officer.',
                                                                              'Speak to a working '
                                                                              'professional and review '
                                                                              'recent vacancies before '
                                                                              'committing to a course.'],
                                                   'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                                   'research_note': 'Role-specific starter guidance '
                                                                    'generated from the career catalogue '
                                                                    'category. Verify licensing, '
                                                                    'eligibility, salaries, course fees and '
                                                                    'outlook with official/current sources.'},
 'NGO Professional / CSR Executive': {'field': 'Public Service, Defence and Social Impact',
                                      'summary': 'NGO Professional / CSR Executive: Serves communities or '
                                                 'public institutions through administration, protection, '
                                                 'policy, development or disciplined operational work.',
                                      'skills': ['Communication and public-service orientation',
                                                 'Ethical judgement and accountability',
                                                 'Role-specific general knowledge, fitness or subject '
                                                 'preparation',
                                                 'Planning, teamwork and decision-making'],
                                      'technologies': ['Tools and methods used in NGO Professional / CSR '
                                                       'Executive',
                                                       'Spreadsheets, digital research and clear '
                                                       'documentation where relevant',
                                                       'Role-specific platforms confirmed from current job '
                                                       'descriptions'],
                                      'projects': ['Complete a beginner project or practical exercise '
                                                   'related to NGO Professional / CSR Executive',
                                                   'Create a portfolio, case study or documented practical '
                                                   'assignment for NGO Professional / CSR Executive',
                                                   'Analyse a real-world challenge relevant to NGO '
                                                   'Professional / CSR Executive and present a safe, '
                                                   'evidence-based solution'],
                                      'pathways': ['Read the latest official eligibility, age, education, '
                                                   'medical and selection criteria for the exact post.',
                                                   'Plan degree choices and exam preparation around the '
                                                   'official recruitment route.',
                                                   'For uniformed services, assess physical and medical '
                                                   'standards early.',
                                                   'Use official notifications for dates, syllabus, '
                                                   'selection stages and pay details.'],
                                      'roles': ['NGO Professional / CSR Executive',
                                                'Junior / Trainee NGO Professional / CSR Executive',
                                                'Specialist or senior NGO Professional / CSR Executive after '
                                                'required training and experience'],
                                      'indicative_salary_india': 'Vacancies and pay depend on official '
                                                                 'recruitment cycles, rank, cadre, '
                                                                 'allowances and service rules.',
                                      'education_cost_india': 'Preparation expenses vary; include exam fees, '
                                                              'study materials, coaching if chosen, travel '
                                                              'and medical/fitness preparation.',
                                      'future_outlook': 'For NGO Professional / CSR Executive, assess '
                                                        'current demand using recent India-based job '
                                                        'listings, official recruitment notices and relevant '
                                                        'industry reports; outlook is not guaranteed.',
                                      'recommended_next_steps': ['Read current official qualification and '
                                                                 'eligibility rules for NGO Professional / '
                                                                 'CSR Executive.',
                                                                 'Compare at least three recognised training '
                                                                 'routes for NGO Professional / CSR '
                                                                 'Executive, including total fees and '
                                                                 'duration.',
                                                                 'Complete one relevant project, portfolio '
                                                                 'piece, field exercise or supervised '
                                                                 'placement for NGO Professional / CSR '
                                                                 'Executive.',
                                                                 'Speak to a working professional and review '
                                                                 'recent vacancies before committing to a '
                                                                 'course.'],
                                      'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                      'research_note': 'Role-specific starter guidance generated from the '
                                                       'career catalogue category. Verify licensing, '
                                                       'eligibility, salaries, course fees and outlook with '
                                                       'official/current sources.'},
 'Pediatrician / Child Specialist': {'field': 'Healthcare and Life Sciences',
                                     'summary': 'Pediatrician / Child Specialist: Patient care, clinical '
                                                'knowledge, evidence-based practice, ethical judgement and '
                                                'clear communication.',
                                     'skills': ['Biology and health-science foundations',
                                                'Careful observation and documentation',
                                                'Communication with patients or teams',
                                                'Ethics, safety and evidence-based decision-making'],
                                     'technologies': ['Tools and methods used in Pediatrician / Child '
                                                      'Specialist',
                                                      'Spreadsheets, digital research and clear '
                                                      'documentation where relevant',
                                                      'Role-specific platforms confirmed from current job '
                                                      'descriptions'],
                                     'projects': ['Complete a beginner project or practical exercise related '
                                                  'to Pediatrician / Child Specialist',
                                                  'Create a portfolio, case study or documented practical '
                                                  'assignment for Pediatrician / Child Specialist',
                                                  'Analyse a real-world challenge relevant to Pediatrician / '
                                                  'Child Specialist and present a safe, evidence-based '
                                                  'solution'],
                                     'pathways': ['Investigate the recognised health-science route and '
                                                  'entrance requirements for this exact profession.',
                                                  'Complete the required accredited degree and supervised '
                                                  'clinical training.',
                                                  'Check registration/licensing rules with the relevant '
                                                  'Indian regulator or council.',
                                                  'Build experience through approved clinical placements and '
                                                  'continuing education.'],
                                     'roles': ['Pediatrician / Child Specialist',
                                               'Junior / Trainee Pediatrician / Child Specialist',
                                               'Specialist or senior Pediatrician / Child Specialist after '
                                               'required training and experience'],
                                     'indicative_salary_india': 'Healthcare hiring and pay vary strongly by '
                                                                'qualification, specialisation, '
                                                                'public/private employer and location.',
                                     'education_cost_india': 'Course costs vary widely between government '
                                                             'and private institutions; include tuition, '
                                                             'examinations, clinical materials and living '
                                                             'costs.',
                                     'future_outlook': 'For Pediatrician / Child Specialist, assess current '
                                                       'demand using recent India-based job listings, '
                                                       'official recruitment notices and relevant industry '
                                                       'reports; outlook is not guaranteed.',
                                     'recommended_next_steps': ['Read current official qualification and '
                                                                'eligibility rules for Pediatrician / Child '
                                                                'Specialist.',
                                                                'Compare at least three recognised training '
                                                                'routes for Pediatrician / Child Specialist, '
                                                                'including total fees and duration.',
                                                                'Complete one relevant project, portfolio '
                                                                'piece, field exercise or supervised '
                                                                'placement for Pediatrician / Child '
                                                                'Specialist.',
                                                                'Speak to a working professional and review '
                                                                'recent vacancies before committing to a '
                                                                'course.'],
                                     'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                     'research_note': 'Role-specific starter guidance generated from the '
                                                      'career catalogue category. Verify licensing, '
                                                      'eligibility, salaries, course fees and outlook with '
                                                      'official/current sources.'},
 'Welfare Officer / Government Social Worker': {'field': 'Public Service, Defence and Social Impact',
                                                'summary': 'Welfare Officer / Government Social Worker: '
                                                           'Serves communities or public institutions '
                                                           'through administration, protection, policy, '
                                                           'development or disciplined operational work.',
                                                'skills': ['Communication and public-service orientation',
                                                           'Ethical judgement and accountability',
                                                           'Role-specific general knowledge, fitness or '
                                                           'subject preparation',
                                                           'Planning, teamwork and decision-making'],
                                                'technologies': ['Tools and methods used in Welfare Officer '
                                                                 '/ Government Social Worker',
                                                                 'Spreadsheets, digital research and clear '
                                                                 'documentation where relevant',
                                                                 'Role-specific platforms confirmed from '
                                                                 'current job descriptions'],
                                                'projects': ['Complete a beginner project or practical '
                                                             'exercise related to Welfare Officer / '
                                                             'Government Social Worker',
                                                             'Create a portfolio, case study or documented '
                                                             'practical assignment for Welfare Officer / '
                                                             'Government Social Worker',
                                                             'Analyse a real-world challenge relevant to '
                                                             'Welfare Officer / Government Social Worker and '
                                                             'present a safe, evidence-based solution'],
                                                'pathways': ['Read the latest official eligibility, age, '
                                                             'education, medical and selection criteria for '
                                                             'the exact post.',
                                                             'Plan degree choices and exam preparation '
                                                             'around the official recruitment route.',
                                                             'For uniformed services, assess physical and '
                                                             'medical standards early.',
                                                             'Use official notifications for dates, '
                                                             'syllabus, selection stages and pay details.'],
                                                'roles': ['Welfare Officer / Government Social Worker',
                                                          'Junior / Trainee Welfare Officer / Government '
                                                          'Social Worker',
                                                          'Specialist or senior Welfare Officer / Government '
                                                          'Social Worker after required training and '
                                                          'experience'],
                                                'indicative_salary_india': 'Vacancies and pay depend on '
                                                                           'official recruitment cycles, '
                                                                           'rank, cadre, allowances and '
                                                                           'service rules.',
                                                'education_cost_india': 'Preparation expenses vary; include '
                                                                        'exam fees, study materials, '
                                                                        'coaching if chosen, travel and '
                                                                        'medical/fitness preparation.',
                                                'future_outlook': 'For Welfare Officer / Government Social '
                                                                  'Worker, assess current demand using '
                                                                  'recent India-based job listings, official '
                                                                  'recruitment notices and relevant industry '
                                                                  'reports; outlook is not guaranteed.',
                                                'recommended_next_steps': ['Read current official '
                                                                           'qualification and eligibility '
                                                                           'rules for Welfare Officer / '
                                                                           'Government Social Worker.',
                                                                           'Compare at least three '
                                                                           'recognised training routes for '
                                                                           'Welfare Officer / Government '
                                                                           'Social Worker, including total '
                                                                           'fees and duration.',
                                                                           'Complete one relevant project, '
                                                                           'portfolio piece, field exercise '
                                                                           'or supervised placement for '
                                                                           'Welfare Officer / Government '
                                                                           'Social Worker.',
                                                                           'Speak to a working professional '
                                                                           'and review recent vacancies '
                                                                           'before committing to a course.'],
                                                'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                                'research_note': 'Role-specific starter guidance generated '
                                                                 'from the career catalogue category. Verify '
                                                                 'licensing, eligibility, salaries, course '
                                                                 'fees and outlook with official/current '
                                                                 'sources.'},
 'Management Consultant (MBA)': {'field': 'Business, Management and Entrepreneurship',
                                 'summary': 'Management Consultant (MBA): Coordinates people, customers, '
                                            'services, operations or business growth using commercial '
                                            'judgement and measurable goals.',
                                 'skills': ['Communication, negotiation and teamwork',
                                            'Planning, budgeting and data-informed decisions',
                                            'Customer or stakeholder understanding',
                                            'Digital tools and professional ethics'],
                                 'technologies': ['Tools and methods used in Management Consultant (MBA)',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Management Consultant (MBA)',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Management Consultant (MBA)',
                                              'Analyse a real-world challenge relevant to Management '
                                              'Consultant (MBA) and present a safe, evidence-based solution'],
                                 'pathways': ['Learn the industry and target role through a relevant degree, '
                                              'diploma or practical experience.',
                                              'Build evidence through internships, sales/service projects or '
                                              'a small validated business experiment.',
                                              'Practise spreadsheets, presentations, customer research and '
                                              'project planning.',
                                              'Review entry-level job descriptions and speak with '
                                              'practitioners in the target sector.'],
                                 'roles': ['Management Consultant (MBA)',
                                           'Junior / Trainee Management Consultant (MBA)',
                                           'Specialist or senior Management Consultant (MBA) after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Pay varies widely by industry, location, '
                                                            'seniority, targets and whether income is '
                                                            'salaried or entrepreneurial.',
                                 'education_cost_india': 'Costs depend on degree/course choice; '
                                                         'entrepreneurship also requires a separate business '
                                                         'budget and risk planning.',
                                 'future_outlook': 'For Management Consultant (MBA), assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Management Consultant '
                                                            '(MBA).',
                                                            'Compare at least three recognised training '
                                                            'routes for Management Consultant (MBA), '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Management Consultant (MBA).',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Sales Director / Business Development Manager': {'field': 'Business, Management and Entrepreneurship',
                                                   'summary': 'Sales Director / Business Development '
                                                              'Manager: Coordinates people, customers, '
                                                              'services, operations or business growth using '
                                                              'commercial judgement and measurable goals.',
                                                   'skills': ['Communication, negotiation and teamwork',
                                                              'Planning, budgeting and data-informed '
                                                              'decisions',
                                                              'Customer or stakeholder understanding',
                                                              'Digital tools and professional ethics'],
                                                   'technologies': ['Tools and methods used in Sales '
                                                                    'Director / Business Development Manager',
                                                                    'Spreadsheets, digital research and '
                                                                    'clear documentation where relevant',
                                                                    'Role-specific platforms confirmed from '
                                                                    'current job descriptions'],
                                                   'projects': ['Complete a beginner project or practical '
                                                                'exercise related to Sales Director / '
                                                                'Business Development Manager',
                                                                'Create a portfolio, case study or '
                                                                'documented practical assignment for Sales '
                                                                'Director / Business Development Manager',
                                                                'Analyse a real-world challenge relevant to '
                                                                'Sales Director / Business Development '
                                                                'Manager and present a safe, evidence-based '
                                                                'solution'],
                                                   'pathways': ['Learn the industry and target role through '
                                                                'a relevant degree, diploma or practical '
                                                                'experience.',
                                                                'Build evidence through internships, '
                                                                'sales/service projects or a small validated '
                                                                'business experiment.',
                                                                'Practise spreadsheets, presentations, '
                                                                'customer research and project planning.',
                                                                'Review entry-level job descriptions and '
                                                                'speak with practitioners in the target '
                                                                'sector.'],
                                                   'roles': ['Sales Director / Business Development Manager',
                                                             'Junior / Trainee Sales Director / Business '
                                                             'Development Manager',
                                                             'Specialist or senior Sales Director / Business '
                                                             'Development Manager after required training '
                                                             'and experience'],
                                                   'indicative_salary_india': 'Pay varies widely by '
                                                                              'industry, location, '
                                                                              'seniority, targets and '
                                                                              'whether income is salaried or '
                                                                              'entrepreneurial.',
                                                   'education_cost_india': 'Costs depend on degree/course '
                                                                           'choice; entrepreneurship also '
                                                                           'requires a separate business '
                                                                           'budget and risk planning.',
                                                   'future_outlook': 'For Sales Director / Business '
                                                                     'Development Manager, assess current '
                                                                     'demand using recent India-based job '
                                                                     'listings, official recruitment notices '
                                                                     'and relevant industry reports; outlook '
                                                                     'is not guaranteed.',
                                                   'recommended_next_steps': ['Read current official '
                                                                              'qualification and eligibility '
                                                                              'rules for Sales Director / '
                                                                              'Business Development Manager.',
                                                                              'Compare at least three '
                                                                              'recognised training routes '
                                                                              'for Sales Director / Business '
                                                                              'Development Manager, '
                                                                              'including total fees and '
                                                                              'duration.',
                                                                              'Complete one relevant '
                                                                              'project, portfolio piece, '
                                                                              'field exercise or supervised '
                                                                              'placement for Sales Director '
                                                                              '/ Business Development '
                                                                              'Manager.',
                                                                              'Speak to a working '
                                                                              'professional and review '
                                                                              'recent vacancies before '
                                                                              'committing to a course.'],
                                                   'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                                   'research_note': 'Role-specific starter guidance '
                                                                    'generated from the career catalogue '
                                                                    'category. Verify licensing, '
                                                                    'eligibility, salaries, course fees and '
                                                                    'outlook with official/current sources.'},
 'CEO / Managing Director': {'field': 'Business, Management and Entrepreneurship',
                             'summary': 'CEO / Managing Director: Coordinates people, customers, services, '
                                        'operations or business growth using commercial judgement and '
                                        'measurable goals.',
                             'skills': ['Communication, negotiation and teamwork',
                                        'Planning, budgeting and data-informed decisions',
                                        'Customer or stakeholder understanding',
                                        'Digital tools and professional ethics'],
                             'technologies': ['Tools and methods used in CEO / Managing Director',
                                              'Spreadsheets, digital research and clear documentation where '
                                              'relevant',
                                              'Role-specific platforms confirmed from current job '
                                              'descriptions'],
                             'projects': ['Complete a beginner project or practical exercise related to CEO '
                                          '/ Managing Director',
                                          'Create a portfolio, case study or documented practical assignment '
                                          'for CEO / Managing Director',
                                          'Analyse a real-world challenge relevant to CEO / Managing '
                                          'Director and present a safe, evidence-based solution'],
                             'pathways': ['Learn the industry and target role through a relevant degree, '
                                          'diploma or practical experience.',
                                          'Build evidence through internships, sales/service projects or a '
                                          'small validated business experiment.',
                                          'Practise spreadsheets, presentations, customer research and '
                                          'project planning.',
                                          'Review entry-level job descriptions and speak with practitioners '
                                          'in the target sector.'],
                             'roles': ['CEO / Managing Director',
                                       'Junior / Trainee CEO / Managing Director',
                                       'Specialist or senior CEO / Managing Director after required training '
                                       'and experience'],
                             'indicative_salary_india': 'Pay varies widely by industry, location, seniority, '
                                                        'targets and whether income is salaried or '
                                                        'entrepreneurial.',
                             'education_cost_india': 'Costs depend on degree/course choice; entrepreneurship '
                                                     'also requires a separate business budget and risk '
                                                     'planning.',
                             'future_outlook': 'For CEO / Managing Director, assess current demand using '
                                               'recent India-based job listings, official recruitment '
                                               'notices and relevant industry reports; outlook is not '
                                               'guaranteed.',
                             'recommended_next_steps': ['Read current official qualification and eligibility '
                                                        'rules for CEO / Managing Director.',
                                                        'Compare at least three recognised training routes '
                                                        'for CEO / Managing Director, including total fees '
                                                        'and duration.',
                                                        'Complete one relevant project, portfolio piece, '
                                                        'field exercise or supervised placement for CEO / '
                                                        'Managing Director.',
                                                        'Speak to a working professional and review recent '
                                                        'vacancies before committing to a course.'],
                             'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                             'research_note': 'Role-specific starter guidance generated from the career '
                                              'catalogue category. Verify licensing, eligibility, salaries, '
                                              'course fees and outlook with official/current sources.'},
 'Stock Broker / Investment Advisor': {'field': 'Finance, Accounting and Governance',
                                       'summary': 'Stock Broker / Investment Advisor: Works with financial '
                                                  'records, analysis, risk, regulation, markets or '
                                                  'organisational decisions.',
                                       'skills': ['Numeracy and analytical reasoning',
                                                  'Excel/spreadsheets and data interpretation',
                                                  'Accuracy, confidentiality and professional ethics',
                                                  'Financial reporting, regulation or research relevant to '
                                                  'the role'],
                                       'technologies': ['Tools and methods used in Stock Broker / Investment '
                                                        'Advisor',
                                                        'Spreadsheets, digital research and clear '
                                                        'documentation where relevant',
                                                        'Role-specific platforms confirmed from current job '
                                                        'descriptions'],
                                       'projects': ['Complete a beginner project or practical exercise '
                                                    'related to Stock Broker / Investment Advisor',
                                                    'Create a portfolio, case study or documented practical '
                                                    'assignment for Stock Broker / Investment Advisor',
                                                    'Analyse a real-world challenge relevant to Stock Broker '
                                                    '/ Investment Advisor and present a safe, evidence-based '
                                                    'solution'],
                                       'pathways': ['Check the official qualification or recruitment route '
                                                    '(for example, professional-body exams or public '
                                                    'recruitment notices).',
                                                    'Build accounting, finance, economics, spreadsheet and '
                                                    'analytical foundations as appropriate.',
                                                    'Practise with case studies, financial models or '
                                                    'compliant sample reports.',
                                                    'Verify current exam rules, eligibility, registration '
                                                    'and role-specific certifications from official '
                                                    'sources.'],
                                       'roles': ['Stock Broker / Investment Advisor',
                                                 'Junior / Trainee Stock Broker / Investment Advisor',
                                                 'Specialist or senior Stock Broker / Investment Advisor '
                                                 'after required training and experience'],
                                       'indicative_salary_india': 'Compensation varies by qualification, '
                                                                  'employer, city, performance and '
                                                                  'experience; public-sector pay follows '
                                                                  'official notices.',
                                       'education_cost_india': 'Include professional-body registration, exam '
                                                               'attempts, coaching if chosen, study '
                                                               'materials and degree tuition; official fees '
                                                               'change.',
                                       'future_outlook': 'For Stock Broker / Investment Advisor, assess '
                                                         'current demand using recent India-based job '
                                                         'listings, official recruitment notices and '
                                                         'relevant industry reports; outlook is not '
                                                         'guaranteed.',
                                       'recommended_next_steps': ['Read current official qualification and '
                                                                  'eligibility rules for Stock Broker / '
                                                                  'Investment Advisor.',
                                                                  'Compare at least three recognised '
                                                                  'training routes for Stock Broker / '
                                                                  'Investment Advisor, including total fees '
                                                                  'and duration.',
                                                                  'Complete one relevant project, portfolio '
                                                                  'piece, field exercise or supervised '
                                                                  'placement for Stock Broker / Investment '
                                                                  'Advisor.',
                                                                  'Speak to a working professional and '
                                                                  'review recent vacancies before committing '
                                                                  'to a course.'],
                                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                       'research_note': 'Role-specific starter guidance generated from the '
                                                        'career catalogue category. Verify licensing, '
                                                        'eligibility, salaries, course fees and outlook with '
                                                        'official/current sources.'},
 'Real Estate Developer': {'field': 'Business, Management and Entrepreneurship',
                           'summary': 'Real Estate Developer: Coordinates people, customers, services, '
                                      'operations or business growth using commercial judgement and '
                                      'measurable goals.',
                           'skills': ['Communication, negotiation and teamwork',
                                      'Planning, budgeting and data-informed decisions',
                                      'Customer or stakeholder understanding',
                                      'Digital tools and professional ethics'],
                           'technologies': ['Tools and methods used in Real Estate Developer',
                                            'Spreadsheets, digital research and clear documentation where '
                                            'relevant',
                                            'Role-specific platforms confirmed from current job '
                                            'descriptions'],
                           'projects': ['Complete a beginner project or practical exercise related to Real '
                                        'Estate Developer',
                                        'Create a portfolio, case study or documented practical assignment '
                                        'for Real Estate Developer',
                                        'Analyse a real-world challenge relevant to Real Estate Developer '
                                        'and present a safe, evidence-based solution'],
                           'pathways': ['Learn the industry and target role through a relevant degree, '
                                        'diploma or practical experience.',
                                        'Build evidence through internships, sales/service projects or a '
                                        'small validated business experiment.',
                                        'Practise spreadsheets, presentations, customer research and project '
                                        'planning.',
                                        'Review entry-level job descriptions and speak with practitioners in '
                                        'the target sector.'],
                           'roles': ['Real Estate Developer',
                                     'Junior / Trainee Real Estate Developer',
                                     'Specialist or senior Real Estate Developer after required training and '
                                     'experience'],
                           'indicative_salary_india': 'Pay varies widely by industry, location, seniority, '
                                                      'targets and whether income is salaried or '
                                                      'entrepreneurial.',
                           'education_cost_india': 'Costs depend on degree/course choice; entrepreneurship '
                                                   'also requires a separate business budget and risk '
                                                   'planning.',
                           'future_outlook': 'For Real Estate Developer, assess current demand using recent '
                                             'India-based job listings, official recruitment notices and '
                                             'relevant industry reports; outlook is not guaranteed.',
                           'recommended_next_steps': ['Read current official qualification and eligibility '
                                                      'rules for Real Estate Developer.',
                                                      'Compare at least three recognised training routes for '
                                                      'Real Estate Developer, including total fees and '
                                                      'duration.',
                                                      'Complete one relevant project, portfolio piece, field '
                                                      'exercise or supervised placement for Real Estate '
                                                      'Developer.',
                                                      'Speak to a working professional and review recent '
                                                      'vacancies before committing to a course.'],
                           'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                           'research_note': 'Role-specific starter guidance generated from the career '
                                            'catalogue category. Verify licensing, eligibility, salaries, '
                                            'course fees and outlook with official/current sources.'},
 'IAS / IPS / Civil Services Officer': {'field': 'Public Service, Defence and Social Impact',
                                        'summary': 'IAS / IPS / Civil Services Officer: Serves communities '
                                                   'or public institutions through administration, '
                                                   'protection, policy, development or disciplined '
                                                   'operational work.',
                                        'skills': ['Communication and public-service orientation',
                                                   'Ethical judgement and accountability',
                                                   'Role-specific general knowledge, fitness or subject '
                                                   'preparation',
                                                   'Planning, teamwork and decision-making'],
                                        'technologies': ['Tools and methods used in IAS / IPS / Civil '
                                                         'Services Officer',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to IAS / IPS / Civil Services Officer',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for IAS / IPS / Civil Services Officer',
                                                     'Analyse a real-world challenge relevant to IAS / IPS / '
                                                     'Civil Services Officer and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Read the latest official eligibility, age, education, '
                                                     'medical and selection criteria for the exact post.',
                                                     'Plan degree choices and exam preparation around the '
                                                     'official recruitment route.',
                                                     'For uniformed services, assess physical and medical '
                                                     'standards early.',
                                                     'Use official notifications for dates, syllabus, '
                                                     'selection stages and pay details.'],
                                        'roles': ['IAS / IPS / Civil Services Officer',
                                                  'Junior / Trainee IAS / IPS / Civil Services Officer',
                                                  'Specialist or senior IAS / IPS / Civil Services Officer '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Vacancies and pay depend on official '
                                                                   'recruitment cycles, rank, cadre, '
                                                                   'allowances and service rules.',
                                        'education_cost_india': 'Preparation expenses vary; include exam '
                                                                'fees, study materials, coaching if chosen, '
                                                                'travel and medical/fitness preparation.',
                                        'future_outlook': 'For IAS / IPS / Civil Services Officer, assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for IAS / IPS / Civil '
                                                                   'Services Officer.',
                                                                   'Compare at least three recognised '
                                                                   'training routes for IAS / IPS / Civil '
                                                                   'Services Officer, including total fees '
                                                                   'and duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for IAS / IPS / Civil Services '
                                                                   'Officer.',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'E-Commerce Entrepreneur': {'field': 'Business, Management and Entrepreneurship',
                             'summary': 'E-Commerce Entrepreneur: Coordinates people, customers, services, '
                                        'operations or business growth using commercial judgement and '
                                        'measurable goals.',
                             'skills': ['Communication, negotiation and teamwork',
                                        'Planning, budgeting and data-informed decisions',
                                        'Customer or stakeholder understanding',
                                        'Digital tools and professional ethics'],
                             'technologies': ['Tools and methods used in E-Commerce Entrepreneur',
                                              'Spreadsheets, digital research and clear documentation where '
                                              'relevant',
                                              'Role-specific platforms confirmed from current job '
                                              'descriptions'],
                             'projects': ['Complete a beginner project or practical exercise related to '
                                          'E-Commerce Entrepreneur',
                                          'Create a portfolio, case study or documented practical assignment '
                                          'for E-Commerce Entrepreneur',
                                          'Analyse a real-world challenge relevant to E-Commerce '
                                          'Entrepreneur and present a safe, evidence-based solution'],
                             'pathways': ['Learn the industry and target role through a relevant degree, '
                                          'diploma or practical experience.',
                                          'Build evidence through internships, sales/service projects or a '
                                          'small validated business experiment.',
                                          'Practise spreadsheets, presentations, customer research and '
                                          'project planning.',
                                          'Review entry-level job descriptions and speak with practitioners '
                                          'in the target sector.'],
                             'roles': ['E-Commerce Entrepreneur',
                                       'Junior / Trainee E-Commerce Entrepreneur',
                                       'Specialist or senior E-Commerce Entrepreneur after required training '
                                       'and experience'],
                             'indicative_salary_india': 'Pay varies widely by industry, location, seniority, '
                                                        'targets and whether income is salaried or '
                                                        'entrepreneurial.',
                             'education_cost_india': 'Costs depend on degree/course choice; entrepreneurship '
                                                     'also requires a separate business budget and risk '
                                                     'planning.',
                             'future_outlook': 'For E-Commerce Entrepreneur, assess current demand using '
                                               'recent India-based job listings, official recruitment '
                                               'notices and relevant industry reports; outlook is not '
                                               'guaranteed.',
                             'recommended_next_steps': ['Read current official qualification and eligibility '
                                                        'rules for E-Commerce Entrepreneur.',
                                                        'Compare at least three recognised training routes '
                                                        'for E-Commerce Entrepreneur, including total fees '
                                                        'and duration.',
                                                        'Complete one relevant project, portfolio piece, '
                                                        'field exercise or supervised placement for '
                                                        'E-Commerce Entrepreneur.',
                                                        'Speak to a working professional and review recent '
                                                        'vacancies before committing to a course.'],
                             'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                             'research_note': 'Role-specific starter guidance generated from the career '
                                              'catalogue category. Verify licensing, eligibility, salaries, '
                                              'course fees and outlook with official/current sources.'},
 'Research Scientist / PhD Researcher': {'field': 'Environment, Agriculture and Scientific Research',
                                         'summary': 'Research Scientist / PhD Researcher: Uses scientific '
                                                    'methods, fieldwork, laboratory work or evidence '
                                                    'analysis to understand natural systems and solve '
                                                    'specialised problems.',
                                         'skills': ['Biology, chemistry, physics or earth-science '
                                                    'foundations as relevant',
                                                    'Data collection, observation and analysis',
                                                    'Laboratory/field safety and accurate records',
                                                    'Scientific writing and evidence evaluation'],
                                         'technologies': ['Tools and methods used in Research Scientist / '
                                                          'PhD Researcher',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Research Scientist / PhD Researcher',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Research Scientist / PhD '
                                                      'Researcher',
                                                      'Analyse a real-world challenge relevant to Research '
                                                      'Scientist / PhD Researcher and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Identify the exact specialisation and required '
                                                      'science subjects.',
                                                      'Choose a recognised relevant degree and check whether '
                                                      'postgraduate study is expected.',
                                                      'Build field, lab, data-analysis or research '
                                                      'experience under appropriate supervision.',
                                                      'Check government recruitment, research fellowship and '
                                                      'professional registration requirements where '
                                                      'applicable.'],
                                         'roles': ['Research Scientist / PhD Researcher',
                                                   'Junior / Trainee Research Scientist / PhD Researcher',
                                                   'Specialist or senior Research Scientist / PhD Researcher '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                                    'research funding, government '
                                                                    'recruitment and location.',
                                         'education_cost_india': 'Budget for tuition, lab/fieldwork, '
                                                                 'equipment, travel and postgraduate study; '
                                                                 'use official institution fee schedules.',
                                         'future_outlook': 'For Research Scientist / PhD Researcher, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Research '
                                                                    'Scientist / PhD Researcher.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Research Scientist '
                                                                    '/ PhD Researcher, including total fees '
                                                                    'and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Research '
                                                                    'Scientist / PhD Researcher.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Cybersecurity Analyst / Ethical Hacker': {'field': 'Engineering, Technology and Applied Science',
                                            'summary': 'Cybersecurity Analyst / Ethical Hacker: Applies '
                                                       'technical knowledge to design, build, analyse, '
                                                       'secure or operate systems and solve practical '
                                                       'problems.',
                                            'skills': ['Mathematics and technical fundamentals',
                                                       'Structured problem-solving and troubleshooting',
                                                       'Role-specific software, tools or laboratory practice',
                                                       'Project documentation, teamwork and safety'],
                                            'technologies': ['Tools and methods used in Cybersecurity '
                                                             'Analyst / Ethical Hacker',
                                                             'Spreadsheets, digital research and clear '
                                                             'documentation where relevant',
                                                             'Role-specific platforms confirmed from current '
                                                             'job descriptions'],
                                            'projects': ['Complete a beginner project or practical exercise '
                                                         'related to Cybersecurity Analyst / Ethical Hacker',
                                                         'Create a portfolio, case study or documented '
                                                         'practical assignment for Cybersecurity Analyst / '
                                                         'Ethical Hacker',
                                                         'Analyse a real-world challenge relevant to '
                                                         'Cybersecurity Analyst / Ethical Hacker and present '
                                                         'a safe, evidence-based solution'],
                                            'pathways': ['Compare accredited degree, diploma and approved '
                                                         'alternative routes for the exact specialisation.',
                                                         'Build foundations in mathematics, science and the '
                                                         'relevant technical tools.',
                                                         'Complete documented practical projects or '
                                                         'supervised lab work.',
                                                         'Check role-specific licences, certifications and '
                                                         'current job descriptions before applying.'],
                                            'roles': ['Cybersecurity Analyst / Ethical Hacker',
                                                      'Junior / Trainee Cybersecurity Analyst / Ethical '
                                                      'Hacker',
                                                      'Specialist or senior Cybersecurity Analyst / Ethical '
                                                      'Hacker after required training and experience'],
                                            'indicative_salary_india': 'Demand and pay differ by '
                                                                       'specialisation, skills, city and '
                                                                       'industry; check current job postings '
                                                                       'and salary surveys.',
                                            'education_cost_india': 'Costs depend on institution, equipment, '
                                                                    'software, lab access, certification and '
                                                                    'whether a licence or flight/sea '
                                                                    'training is required.',
                                            'future_outlook': 'For Cybersecurity Analyst / Ethical Hacker, '
                                                              'assess current demand using recent '
                                                              'India-based job listings, official '
                                                              'recruitment notices and relevant industry '
                                                              'reports; outlook is not guaranteed.',
                                            'recommended_next_steps': ['Read current official qualification '
                                                                       'and eligibility rules for '
                                                                       'Cybersecurity Analyst / Ethical '
                                                                       'Hacker.',
                                                                       'Compare at least three recognised '
                                                                       'training routes for Cybersecurity '
                                                                       'Analyst / Ethical Hacker, including '
                                                                       'total fees and duration.',
                                                                       'Complete one relevant project, '
                                                                       'portfolio piece, field exercise or '
                                                                       'supervised placement for '
                                                                       'Cybersecurity Analyst / Ethical '
                                                                       'Hacker.',
                                                                       'Speak to a working professional and '
                                                                       'review recent vacancies before '
                                                                       'committing to a course.'],
                                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                            'research_note': 'Role-specific starter guidance generated from '
                                                             'the career catalogue category. Verify '
                                                             'licensing, eligibility, salaries, course fees '
                                                             'and outlook with official/current sources.'},
 'Forensic Scientist / Crime Analyst': {'field': 'Environment, Agriculture and Scientific Research',
                                        'summary': 'Forensic Scientist / Crime Analyst: Uses scientific '
                                                   'methods, fieldwork, laboratory work or evidence analysis '
                                                   'to understand natural systems and solve specialised '
                                                   'problems.',
                                        'skills': ['Biology, chemistry, physics or earth-science foundations '
                                                   'as relevant',
                                                   'Data collection, observation and analysis',
                                                   'Laboratory/field safety and accurate records',
                                                   'Scientific writing and evidence evaluation'],
                                        'technologies': ['Tools and methods used in Forensic Scientist / '
                                                         'Crime Analyst',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to Forensic Scientist / Crime Analyst',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for Forensic Scientist / Crime Analyst',
                                                     'Analyse a real-world challenge relevant to Forensic '
                                                     'Scientist / Crime Analyst and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Identify the exact specialisation and required science '
                                                     'subjects.',
                                                     'Choose a recognised relevant degree and check whether '
                                                     'postgraduate study is expected.',
                                                     'Build field, lab, data-analysis or research experience '
                                                     'under appropriate supervision.',
                                                     'Check government recruitment, research fellowship and '
                                                     'professional registration requirements where '
                                                     'applicable.'],
                                        'roles': ['Forensic Scientist / Crime Analyst',
                                                  'Junior / Trainee Forensic Scientist / Crime Analyst',
                                                  'Specialist or senior Forensic Scientist / Crime Analyst '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Opportunities depend on specialisation, '
                                                                   'research funding, government recruitment '
                                                                   'and location.',
                                        'education_cost_india': 'Budget for tuition, lab/fieldwork, '
                                                                'equipment, travel and postgraduate study; '
                                                                'use official institution fee schedules.',
                                        'future_outlook': 'For Forensic Scientist / Crime Analyst, assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for Forensic Scientist '
                                                                   '/ Crime Analyst.',
                                                                   'Compare at least three recognised '
                                                                   'training routes for Forensic Scientist / '
                                                                   'Crime Analyst, including total fees and '
                                                                   'duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for Forensic Scientist / Crime '
                                                                   'Analyst.',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'Biotechnologist / Genetic Engineer': {'field': 'Engineering, Technology and Applied Science',
                                        'summary': 'Biotechnologist / Genetic Engineer: Applies technical '
                                                   'knowledge to design, build, analyse, secure or operate '
                                                   'systems and solve practical problems.',
                                        'skills': ['Mathematics and technical fundamentals',
                                                   'Structured problem-solving and troubleshooting',
                                                   'Role-specific software, tools or laboratory practice',
                                                   'Project documentation, teamwork and safety'],
                                        'technologies': ['Tools and methods used in Biotechnologist / '
                                                         'Genetic Engineer',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to Biotechnologist / Genetic Engineer',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for Biotechnologist / Genetic Engineer',
                                                     'Analyse a real-world challenge relevant to '
                                                     'Biotechnologist / Genetic Engineer and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Compare accredited degree, diploma and approved '
                                                     'alternative routes for the exact specialisation.',
                                                     'Build foundations in mathematics, science and the '
                                                     'relevant technical tools.',
                                                     'Complete documented practical projects or supervised '
                                                     'lab work.',
                                                     'Check role-specific licences, certifications and '
                                                     'current job descriptions before applying.'],
                                        'roles': ['Biotechnologist / Genetic Engineer',
                                                  'Junior / Trainee Biotechnologist / Genetic Engineer',
                                                  'Specialist or senior Biotechnologist / Genetic Engineer '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Demand and pay differ by specialisation, '
                                                                   'skills, city and industry; check current '
                                                                   'job postings and salary surveys.',
                                        'education_cost_india': 'Costs depend on institution, equipment, '
                                                                'software, lab access, certification and '
                                                                'whether a licence or flight/sea training is '
                                                                'required.',
                                        'future_outlook': 'For Biotechnologist / Genetic Engineer, assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for Biotechnologist / '
                                                                   'Genetic Engineer.',
                                                                   'Compare at least three recognised '
                                                                   'training routes for Biotechnologist / '
                                                                   'Genetic Engineer, including total fees '
                                                                   'and duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for Biotechnologist / Genetic '
                                                                   'Engineer.',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'Pharmacist / Clinical Researcher': {'field': 'Healthcare and Life Sciences',
                                      'summary': 'Pharmacist / Clinical Researcher: Patient care, clinical '
                                                 'knowledge, evidence-based practice, ethical judgement and '
                                                 'clear communication.',
                                      'skills': ['Biology and health-science foundations',
                                                 'Careful observation and documentation',
                                                 'Communication with patients or teams',
                                                 'Ethics, safety and evidence-based decision-making'],
                                      'technologies': ['Tools and methods used in Pharmacist / Clinical '
                                                       'Researcher',
                                                       'Spreadsheets, digital research and clear '
                                                       'documentation where relevant',
                                                       'Role-specific platforms confirmed from current job '
                                                       'descriptions'],
                                      'projects': ['Complete a beginner project or practical exercise '
                                                   'related to Pharmacist / Clinical Researcher',
                                                   'Create a portfolio, case study or documented practical '
                                                   'assignment for Pharmacist / Clinical Researcher',
                                                   'Analyse a real-world challenge relevant to Pharmacist / '
                                                   'Clinical Researcher and present a safe, evidence-based '
                                                   'solution'],
                                      'pathways': ['Investigate the recognised health-science route and '
                                                   'entrance requirements for this exact profession.',
                                                   'Complete the required accredited degree and supervised '
                                                   'clinical training.',
                                                   'Check registration/licensing rules with the relevant '
                                                   'Indian regulator or council.',
                                                   'Build experience through approved clinical placements '
                                                   'and continuing education.'],
                                      'roles': ['Pharmacist / Clinical Researcher',
                                                'Junior / Trainee Pharmacist / Clinical Researcher',
                                                'Specialist or senior Pharmacist / Clinical Researcher after '
                                                'required training and experience'],
                                      'indicative_salary_india': 'Healthcare hiring and pay vary strongly by '
                                                                 'qualification, specialisation, '
                                                                 'public/private employer and location.',
                                      'education_cost_india': 'Course costs vary widely between government '
                                                              'and private institutions; include tuition, '
                                                              'examinations, clinical materials and living '
                                                              'costs.',
                                      'future_outlook': 'For Pharmacist / Clinical Researcher, assess '
                                                        'current demand using recent India-based job '
                                                        'listings, official recruitment notices and relevant '
                                                        'industry reports; outlook is not guaranteed.',
                                      'recommended_next_steps': ['Read current official qualification and '
                                                                 'eligibility rules for Pharmacist / '
                                                                 'Clinical Researcher.',
                                                                 'Compare at least three recognised training '
                                                                 'routes for Pharmacist / Clinical '
                                                                 'Researcher, including total fees and '
                                                                 'duration.',
                                                                 'Complete one relevant project, portfolio '
                                                                 'piece, field exercise or supervised '
                                                                 'placement for Pharmacist / Clinical '
                                                                 'Researcher.',
                                                                 'Speak to a working professional and review '
                                                                 'recent vacancies before committing to a '
                                                                 'course.'],
                                      'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                      'research_note': 'Role-specific starter guidance generated from the '
                                                       'career catalogue category. Verify licensing, '
                                                       'eligibility, salaries, course fees and outlook with '
                                                       'official/current sources.'},
 'AI & ML Specialist': {'field': 'Engineering, Technology and Applied Science',
                        'summary': 'AI & ML Specialist: Applies technical knowledge to design, build, '
                                   'analyse, secure or operate systems and solve practical problems.',
                        'skills': ['Mathematics and technical fundamentals',
                                   'Structured problem-solving and troubleshooting',
                                   'Role-specific software, tools or laboratory practice',
                                   'Project documentation, teamwork and safety'],
                        'technologies': ['Tools and methods used in AI & ML Specialist',
                                         'Spreadsheets, digital research and clear documentation where '
                                         'relevant',
                                         'Role-specific platforms confirmed from current job descriptions'],
                        'projects': ['Complete a beginner project or practical exercise related to AI & ML '
                                     'Specialist',
                                     'Create a portfolio, case study or documented practical assignment for '
                                     'AI & ML Specialist',
                                     'Analyse a real-world challenge relevant to AI & ML Specialist and '
                                     'present a safe, evidence-based solution'],
                        'pathways': ['Compare accredited degree, diploma and approved alternative routes for '
                                     'the exact specialisation.',
                                     'Build foundations in mathematics, science and the relevant technical '
                                     'tools.',
                                     'Complete documented practical projects or supervised lab work.',
                                     'Check role-specific licences, certifications and current job '
                                     'descriptions before applying.'],
                        'roles': ['AI & ML Specialist',
                                  'Junior / Trainee AI & ML Specialist',
                                  'Specialist or senior AI & ML Specialist after required training and '
                                  'experience'],
                        'indicative_salary_india': 'Demand and pay differ by specialisation, skills, city '
                                                   'and industry; check current job postings and salary '
                                                   'surveys.',
                        'education_cost_india': 'Costs depend on institution, equipment, software, lab '
                                                'access, certification and whether a licence or flight/sea '
                                                'training is required.',
                        'future_outlook': 'For AI & ML Specialist, assess current demand using recent '
                                          'India-based job listings, official recruitment notices and '
                                          'relevant industry reports; outlook is not guaranteed.',
                        'recommended_next_steps': ['Read current official qualification and eligibility '
                                                   'rules for AI & ML Specialist.',
                                                   'Compare at least three recognised training routes for AI '
                                                   '& ML Specialist, including total fees and duration.',
                                                   'Complete one relevant project, portfolio piece, field '
                                                   'exercise or supervised placement for AI & ML Specialist.',
                                                   'Speak to a working professional and review recent '
                                                   'vacancies before committing to a course.'],
                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                        'research_note': 'Role-specific starter guidance generated from the career catalogue '
                                         'category. Verify licensing, eligibility, salaries, course fees and '
                                         'outlook with official/current sources.'},
 'Civil / Mechanical / Electrical Engineer': {'field': 'Engineering, Technology and Applied Science',
                                              'summary': 'Civil / Mechanical / Electrical Engineer: Applies '
                                                         'technical knowledge to design, build, analyse, '
                                                         'secure or operate systems and solve practical '
                                                         'problems.',
                                              'skills': ['Mathematics and technical fundamentals',
                                                         'Structured problem-solving and troubleshooting',
                                                         'Role-specific software, tools or laboratory '
                                                         'practice',
                                                         'Project documentation, teamwork and safety'],
                                              'technologies': ['Tools and methods used in Civil / Mechanical '
                                                               '/ Electrical Engineer',
                                                               'Spreadsheets, digital research and clear '
                                                               'documentation where relevant',
                                                               'Role-specific platforms confirmed from '
                                                               'current job descriptions'],
                                              'projects': ['Complete a beginner project or practical '
                                                           'exercise related to Civil / Mechanical / '
                                                           'Electrical Engineer',
                                                           'Create a portfolio, case study or documented '
                                                           'practical assignment for Civil / Mechanical / '
                                                           'Electrical Engineer',
                                                           'Analyse a real-world challenge relevant to Civil '
                                                           '/ Mechanical / Electrical Engineer and present a '
                                                           'safe, evidence-based solution'],
                                              'pathways': ['Compare accredited degree, diploma and approved '
                                                           'alternative routes for the exact specialisation.',
                                                           'Build foundations in mathematics, science and '
                                                           'the relevant technical tools.',
                                                           'Complete documented practical projects or '
                                                           'supervised lab work.',
                                                           'Check role-specific licences, certifications and '
                                                           'current job descriptions before applying.'],
                                              'roles': ['Civil / Mechanical / Electrical Engineer',
                                                        'Junior / Trainee Civil / Mechanical / Electrical '
                                                        'Engineer',
                                                        'Specialist or senior Civil / Mechanical / '
                                                        'Electrical Engineer after required training and '
                                                        'experience'],
                                              'indicative_salary_india': 'Demand and pay differ by '
                                                                         'specialisation, skills, city and '
                                                                         'industry; check current job '
                                                                         'postings and salary surveys.',
                                              'education_cost_india': 'Costs depend on institution, '
                                                                      'equipment, software, lab access, '
                                                                      'certification and whether a licence '
                                                                      'or flight/sea training is required.',
                                              'future_outlook': 'For Civil / Mechanical / Electrical '
                                                                'Engineer, assess current demand using '
                                                                'recent India-based job listings, official '
                                                                'recruitment notices and relevant industry '
                                                                'reports; outlook is not guaranteed.',
                                              'recommended_next_steps': ['Read current official '
                                                                         'qualification and eligibility '
                                                                         'rules for Civil / Mechanical / '
                                                                         'Electrical Engineer.',
                                                                         'Compare at least three recognised '
                                                                         'training routes for Civil / '
                                                                         'Mechanical / Electrical Engineer, '
                                                                         'including total fees and duration.',
                                                                         'Complete one relevant project, '
                                                                         'portfolio piece, field exercise or '
                                                                         'supervised placement for Civil / '
                                                                         'Mechanical / Electrical Engineer.',
                                                                         'Speak to a working professional '
                                                                         'and review recent vacancies before '
                                                                         'committing to a course.'],
                                              'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                              'research_note': 'Role-specific starter guidance generated '
                                                               'from the career catalogue category. Verify '
                                                               'licensing, eligibility, salaries, course '
                                                               'fees and outlook with official/current '
                                                               'sources.'},
 'Commercial Pilot / Air Traffic Controller': {'field': 'Engineering, Technology and Applied Science',
                                               'summary': 'Commercial Pilot / Air Traffic Controller: '
                                                          'Applies technical knowledge to design, build, '
                                                          'analyse, secure or operate systems and solve '
                                                          'practical problems.',
                                               'skills': ['Mathematics and technical fundamentals',
                                                          'Structured problem-solving and troubleshooting',
                                                          'Role-specific software, tools or laboratory '
                                                          'practice',
                                                          'Project documentation, teamwork and safety'],
                                               'technologies': ['Tools and methods used in Commercial Pilot '
                                                                '/ Air Traffic Controller',
                                                                'Spreadsheets, digital research and clear '
                                                                'documentation where relevant',
                                                                'Role-specific platforms confirmed from '
                                                                'current job descriptions'],
                                               'projects': ['Complete a beginner project or practical '
                                                            'exercise related to Commercial Pilot / Air '
                                                            'Traffic Controller',
                                                            'Create a portfolio, case study or documented '
                                                            'practical assignment for Commercial Pilot / Air '
                                                            'Traffic Controller',
                                                            'Analyse a real-world challenge relevant to '
                                                            'Commercial Pilot / Air Traffic Controller and '
                                                            'present a safe, evidence-based solution'],
                                               'pathways': ['Compare accredited degree, diploma and approved '
                                                            'alternative routes for the exact '
                                                            'specialisation.',
                                                            'Build foundations in mathematics, science and '
                                                            'the relevant technical tools.',
                                                            'Complete documented practical projects or '
                                                            'supervised lab work.',
                                                            'Check role-specific licences, certifications '
                                                            'and current job descriptions before applying.'],
                                               'roles': ['Commercial Pilot / Air Traffic Controller',
                                                         'Junior / Trainee Commercial Pilot / Air Traffic '
                                                         'Controller',
                                                         'Specialist or senior Commercial Pilot / Air '
                                                         'Traffic Controller after required training and '
                                                         'experience'],
                                               'indicative_salary_india': 'Demand and pay differ by '
                                                                          'specialisation, skills, city and '
                                                                          'industry; check current job '
                                                                          'postings and salary surveys.',
                                               'education_cost_india': 'Costs depend on institution, '
                                                                       'equipment, software, lab access, '
                                                                       'certification and whether a licence '
                                                                       'or flight/sea training is required.',
                                               'future_outlook': 'For Commercial Pilot / Air Traffic '
                                                                 'Controller, assess current demand using '
                                                                 'recent India-based job listings, official '
                                                                 'recruitment notices and relevant industry '
                                                                 'reports; outlook is not guaranteed.',
                                               'recommended_next_steps': ['Read current official '
                                                                          'qualification and eligibility '
                                                                          'rules for Commercial Pilot / Air '
                                                                          'Traffic Controller.',
                                                                          'Compare at least three recognised '
                                                                          'training routes for Commercial '
                                                                          'Pilot / Air Traffic Controller, '
                                                                          'including total fees and '
                                                                          'duration.',
                                                                          'Complete one relevant project, '
                                                                          'portfolio piece, field exercise '
                                                                          'or supervised placement for '
                                                                          'Commercial Pilot / Air Traffic '
                                                                          'Controller.',
                                                                          'Speak to a working professional '
                                                                          'and review recent vacancies '
                                                                          'before committing to a course.'],
                                               'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                               'research_note': 'Role-specific starter guidance generated '
                                                                'from the career catalogue category. Verify '
                                                                'licensing, eligibility, salaries, course '
                                                                'fees and outlook with official/current '
                                                                'sources.'},
 'Army / Defence Officer (NDA/CDS)': {'field': 'Public Service, Defence and Social Impact',
                                      'summary': 'Army / Defence Officer (NDA/CDS): Serves communities or '
                                                 'public institutions through administration, protection, '
                                                 'policy, development or disciplined operational work.',
                                      'skills': ['Communication and public-service orientation',
                                                 'Ethical judgement and accountability',
                                                 'Role-specific general knowledge, fitness or subject '
                                                 'preparation',
                                                 'Planning, teamwork and decision-making'],
                                      'technologies': ['Tools and methods used in Army / Defence Officer '
                                                       '(NDA/CDS)',
                                                       'Spreadsheets, digital research and clear '
                                                       'documentation where relevant',
                                                       'Role-specific platforms confirmed from current job '
                                                       'descriptions'],
                                      'projects': ['Complete a beginner project or practical exercise '
                                                   'related to Army / Defence Officer (NDA/CDS)',
                                                   'Create a portfolio, case study or documented practical '
                                                   'assignment for Army / Defence Officer (NDA/CDS)',
                                                   'Analyse a real-world challenge relevant to Army / '
                                                   'Defence Officer (NDA/CDS) and present a safe, '
                                                   'evidence-based solution'],
                                      'pathways': ['Read the latest official eligibility, age, education, '
                                                   'medical and selection criteria for the exact post.',
                                                   'Plan degree choices and exam preparation around the '
                                                   'official recruitment route.',
                                                   'For uniformed services, assess physical and medical '
                                                   'standards early.',
                                                   'Use official notifications for dates, syllabus, '
                                                   'selection stages and pay details.'],
                                      'roles': ['Army / Defence Officer (NDA/CDS)',
                                                'Junior / Trainee Army / Defence Officer (NDA/CDS)',
                                                'Specialist or senior Army / Defence Officer (NDA/CDS) after '
                                                'required training and experience'],
                                      'indicative_salary_india': 'Vacancies and pay depend on official '
                                                                 'recruitment cycles, rank, cadre, '
                                                                 'allowances and service rules.',
                                      'education_cost_india': 'Preparation expenses vary; include exam fees, '
                                                              'study materials, coaching if chosen, travel '
                                                              'and medical/fitness preparation.',
                                      'future_outlook': 'For Army / Defence Officer (NDA/CDS), assess '
                                                        'current demand using recent India-based job '
                                                        'listings, official recruitment notices and relevant '
                                                        'industry reports; outlook is not guaranteed.',
                                      'recommended_next_steps': ['Read current official qualification and '
                                                                 'eligibility rules for Army / Defence '
                                                                 'Officer (NDA/CDS).',
                                                                 'Compare at least three recognised training '
                                                                 'routes for Army / Defence Officer '
                                                                 '(NDA/CDS), including total fees and '
                                                                 'duration.',
                                                                 'Complete one relevant project, portfolio '
                                                                 'piece, field exercise or supervised '
                                                                 'placement for Army / Defence Officer '
                                                                 '(NDA/CDS).',
                                                                 'Speak to a working professional and review '
                                                                 'recent vacancies before committing to a '
                                                                 'course.'],
                                      'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                      'research_note': 'Role-specific starter guidance generated from the '
                                                       'career catalogue category. Verify licensing, '
                                                       'eligibility, salaries, course fees and outlook with '
                                                       'official/current sources.'},
 'Automobile Engineer / EV Specialist': {'field': 'Engineering, Technology and Applied Science',
                                         'summary': 'Automobile Engineer / EV Specialist: Applies technical '
                                                    'knowledge to design, build, analyse, secure or operate '
                                                    'systems and solve practical problems.',
                                         'skills': ['Mathematics and technical fundamentals',
                                                    'Structured problem-solving and troubleshooting',
                                                    'Role-specific software, tools or laboratory practice',
                                                    'Project documentation, teamwork and safety'],
                                         'technologies': ['Tools and methods used in Automobile Engineer / '
                                                          'EV Specialist',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Automobile Engineer / EV Specialist',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Automobile Engineer / EV '
                                                      'Specialist',
                                                      'Analyse a real-world challenge relevant to Automobile '
                                                      'Engineer / EV Specialist and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Compare accredited degree, diploma and approved '
                                                      'alternative routes for the exact specialisation.',
                                                      'Build foundations in mathematics, science and the '
                                                      'relevant technical tools.',
                                                      'Complete documented practical projects or supervised '
                                                      'lab work.',
                                                      'Check role-specific licences, certifications and '
                                                      'current job descriptions before applying.'],
                                         'roles': ['Automobile Engineer / EV Specialist',
                                                   'Junior / Trainee Automobile Engineer / EV Specialist',
                                                   'Specialist or senior Automobile Engineer / EV Specialist '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Demand and pay differ by '
                                                                    'specialisation, skills, city and '
                                                                    'industry; check current job postings '
                                                                    'and salary surveys.',
                                         'education_cost_india': 'Costs depend on institution, equipment, '
                                                                 'software, lab access, certification and '
                                                                 'whether a licence or flight/sea training '
                                                                 'is required.',
                                         'future_outlook': 'For Automobile Engineer / EV Specialist, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Automobile '
                                                                    'Engineer / EV Specialist.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Automobile Engineer '
                                                                    '/ EV Specialist, including total fees '
                                                                    'and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Automobile '
                                                                    'Engineer / EV Specialist.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Aeronautical Engineer': {'field': 'Engineering, Technology and Applied Science',
                           'summary': 'Aeronautical Engineer: Applies technical knowledge to design, build, '
                                      'analyse, secure or operate systems and solve practical problems.',
                           'skills': ['Mathematics and technical fundamentals',
                                      'Structured problem-solving and troubleshooting',
                                      'Role-specific software, tools or laboratory practice',
                                      'Project documentation, teamwork and safety'],
                           'technologies': ['Tools and methods used in Aeronautical Engineer',
                                            'Spreadsheets, digital research and clear documentation where '
                                            'relevant',
                                            'Role-specific platforms confirmed from current job '
                                            'descriptions'],
                           'projects': ['Complete a beginner project or practical exercise related to '
                                        'Aeronautical Engineer',
                                        'Create a portfolio, case study or documented practical assignment '
                                        'for Aeronautical Engineer',
                                        'Analyse a real-world challenge relevant to Aeronautical Engineer '
                                        'and present a safe, evidence-based solution'],
                           'pathways': ['Compare accredited degree, diploma and approved alternative routes '
                                        'for the exact specialisation.',
                                        'Build foundations in mathematics, science and the relevant '
                                        'technical tools.',
                                        'Complete documented practical projects or supervised lab work.',
                                        'Check role-specific licences, certifications and current job '
                                        'descriptions before applying.'],
                           'roles': ['Aeronautical Engineer',
                                     'Junior / Trainee Aeronautical Engineer',
                                     'Specialist or senior Aeronautical Engineer after required training and '
                                     'experience'],
                           'indicative_salary_india': 'Demand and pay differ by specialisation, skills, city '
                                                      'and industry; check current job postings and salary '
                                                      'surveys.',
                           'education_cost_india': 'Costs depend on institution, equipment, software, lab '
                                                   'access, certification and whether a licence or '
                                                   'flight/sea training is required.',
                           'future_outlook': 'For Aeronautical Engineer, assess current demand using recent '
                                             'India-based job listings, official recruitment notices and '
                                             'relevant industry reports; outlook is not guaranteed.',
                           'recommended_next_steps': ['Read current official qualification and eligibility '
                                                      'rules for Aeronautical Engineer.',
                                                      'Compare at least three recognised training routes for '
                                                      'Aeronautical Engineer, including total fees and '
                                                      'duration.',
                                                      'Complete one relevant project, portfolio piece, field '
                                                      'exercise or supervised placement for Aeronautical '
                                                      'Engineer.',
                                                      'Speak to a working professional and review recent '
                                                      'vacancies before committing to a course.'],
                           'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                           'research_note': 'Role-specific starter guidance generated from the career '
                                            'catalogue category. Verify licensing, eligibility, salaries, '
                                            'course fees and outlook with official/current sources.'},
 'Robotics & Automation Engineer': {'field': 'Engineering, Technology and Applied Science',
                                    'summary': 'Robotics & Automation Engineer: Applies technical knowledge '
                                               'to design, build, analyse, secure or operate systems and '
                                               'solve practical problems.',
                                    'skills': ['Mathematics and technical fundamentals',
                                               'Structured problem-solving and troubleshooting',
                                               'Role-specific software, tools or laboratory practice',
                                               'Project documentation, teamwork and safety'],
                                    'technologies': ['Tools and methods used in Robotics & Automation '
                                                     'Engineer',
                                                     'Spreadsheets, digital research and clear documentation '
                                                     'where relevant',
                                                     'Role-specific platforms confirmed from current job '
                                                     'descriptions'],
                                    'projects': ['Complete a beginner project or practical exercise related '
                                                 'to Robotics & Automation Engineer',
                                                 'Create a portfolio, case study or documented practical '
                                                 'assignment for Robotics & Automation Engineer',
                                                 'Analyse a real-world challenge relevant to Robotics & '
                                                 'Automation Engineer and present a safe, evidence-based '
                                                 'solution'],
                                    'pathways': ['Compare accredited degree, diploma and approved '
                                                 'alternative routes for the exact specialisation.',
                                                 'Build foundations in mathematics, science and the relevant '
                                                 'technical tools.',
                                                 'Complete documented practical projects or supervised lab '
                                                 'work.',
                                                 'Check role-specific licences, certifications and current '
                                                 'job descriptions before applying.'],
                                    'roles': ['Robotics & Automation Engineer',
                                              'Junior / Trainee Robotics & Automation Engineer',
                                              'Specialist or senior Robotics & Automation Engineer after '
                                              'required training and experience'],
                                    'indicative_salary_india': 'Demand and pay differ by specialisation, '
                                                               'skills, city and industry; check current job '
                                                               'postings and salary surveys.',
                                    'education_cost_india': 'Costs depend on institution, equipment, '
                                                            'software, lab access, certification and whether '
                                                            'a licence or flight/sea training is required.',
                                    'future_outlook': 'For Robotics & Automation Engineer, assess current '
                                                      'demand using recent India-based job listings, '
                                                      'official recruitment notices and relevant industry '
                                                      'reports; outlook is not guaranteed.',
                                    'recommended_next_steps': ['Read current official qualification and '
                                                               'eligibility rules for Robotics & Automation '
                                                               'Engineer.',
                                                               'Compare at least three recognised training '
                                                               'routes for Robotics & Automation Engineer, '
                                                               'including total fees and duration.',
                                                               'Complete one relevant project, portfolio '
                                                               'piece, field exercise or supervised '
                                                               'placement for Robotics & Automation '
                                                               'Engineer.',
                                                               'Speak to a working professional and review '
                                                               'recent vacancies before committing to a '
                                                               'course.'],
                                    'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                    'research_note': 'Role-specific starter guidance generated from the '
                                                     'career catalogue category. Verify licensing, '
                                                     'eligibility, salaries, course fees and outlook with '
                                                     'official/current sources.'},
 'Drone Technology Specialist': {'field': 'Engineering, Technology and Applied Science',
                                 'summary': 'Drone Technology Specialist: Applies technical knowledge to '
                                            'design, build, analyse, secure or operate systems and solve '
                                            'practical problems.',
                                 'skills': ['Mathematics and technical fundamentals',
                                            'Structured problem-solving and troubleshooting',
                                            'Role-specific software, tools or laboratory practice',
                                            'Project documentation, teamwork and safety'],
                                 'technologies': ['Tools and methods used in Drone Technology Specialist',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'Drone Technology Specialist',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for Drone Technology Specialist',
                                              'Analyse a real-world challenge relevant to Drone Technology '
                                              'Specialist and present a safe, evidence-based solution'],
                                 'pathways': ['Compare accredited degree, diploma and approved alternative '
                                              'routes for the exact specialisation.',
                                              'Build foundations in mathematics, science and the relevant '
                                              'technical tools.',
                                              'Complete documented practical projects or supervised lab '
                                              'work.',
                                              'Check role-specific licences, certifications and current job '
                                              'descriptions before applying.'],
                                 'roles': ['Drone Technology Specialist',
                                           'Junior / Trainee Drone Technology Specialist',
                                           'Specialist or senior Drone Technology Specialist after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Demand and pay differ by specialisation, '
                                                            'skills, city and industry; check current job '
                                                            'postings and salary surveys.',
                                 'education_cost_india': 'Costs depend on institution, equipment, software, '
                                                         'lab access, certification and whether a licence or '
                                                         'flight/sea training is required.',
                                 'future_outlook': 'For Drone Technology Specialist, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for Drone Technology '
                                                            'Specialist.',
                                                            'Compare at least three recognised training '
                                                            'routes for Drone Technology Specialist, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for '
                                                            'Drone Technology Specialist.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Merchant Navy / Deck Officer': {'field': 'Engineering, Technology and Applied Science',
                                  'summary': 'Merchant Navy / Deck Officer: Applies technical knowledge to '
                                             'design, build, analyse, secure or operate systems and solve '
                                             'practical problems.',
                                  'skills': ['Mathematics and technical fundamentals',
                                             'Structured problem-solving and troubleshooting',
                                             'Role-specific software, tools or laboratory practice',
                                             'Project documentation, teamwork and safety'],
                                  'technologies': ['Tools and methods used in Merchant Navy / Deck Officer',
                                                   'Spreadsheets, digital research and clear documentation '
                                                   'where relevant',
                                                   'Role-specific platforms confirmed from current job '
                                                   'descriptions'],
                                  'projects': ['Complete a beginner project or practical exercise related to '
                                               'Merchant Navy / Deck Officer',
                                               'Create a portfolio, case study or documented practical '
                                               'assignment for Merchant Navy / Deck Officer',
                                               'Analyse a real-world challenge relevant to Merchant Navy / '
                                               'Deck Officer and present a safe, evidence-based solution'],
                                  'pathways': ['Compare accredited degree, diploma and approved alternative '
                                               'routes for the exact specialisation.',
                                               'Build foundations in mathematics, science and the relevant '
                                               'technical tools.',
                                               'Complete documented practical projects or supervised lab '
                                               'work.',
                                               'Check role-specific licences, certifications and current job '
                                               'descriptions before applying.'],
                                  'roles': ['Merchant Navy / Deck Officer',
                                            'Junior / Trainee Merchant Navy / Deck Officer',
                                            'Specialist or senior Merchant Navy / Deck Officer after '
                                            'required training and experience'],
                                  'indicative_salary_india': 'Demand and pay differ by specialisation, '
                                                             'skills, city and industry; check current job '
                                                             'postings and salary surveys.',
                                  'education_cost_india': 'Costs depend on institution, equipment, software, '
                                                          'lab access, certification and whether a licence '
                                                          'or flight/sea training is required.',
                                  'future_outlook': 'For Merchant Navy / Deck Officer, assess current demand '
                                                    'using recent India-based job listings, official '
                                                    'recruitment notices and relevant industry reports; '
                                                    'outlook is not guaranteed.',
                                  'recommended_next_steps': ['Read current official qualification and '
                                                             'eligibility rules for Merchant Navy / Deck '
                                                             'Officer.',
                                                             'Compare at least three recognised training '
                                                             'routes for Merchant Navy / Deck Officer, '
                                                             'including total fees and duration.',
                                                             'Complete one relevant project, portfolio '
                                                             'piece, field exercise or supervised placement '
                                                             'for Merchant Navy / Deck Officer.',
                                                             'Speak to a working professional and review '
                                                             'recent vacancies before committing to a '
                                                             'course.'],
                                  'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                  'research_note': 'Role-specific starter guidance generated from the career '
                                                   'catalogue category. Verify licensing, eligibility, '
                                                   'salaries, course fees and outlook with official/current '
                                                   'sources.'},
 'Film Director / Assistant Director': {'field': 'Creative Media, Communication and Design',
                                        'summary': 'Film Director / Assistant Director: Creates stories, '
                                                   'experiences, visuals, performances or communication '
                                                   'materials for a defined audience.',
                                        'skills': ['Creative development and audience awareness',
                                                   'Portfolio-building and revision from feedback',
                                                   'Communication, collaboration and deadlines',
                                                   'Relevant production, design, language or editing tools'],
                                        'technologies': ['Tools and methods used in Film Director / '
                                                         'Assistant Director',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to Film Director / Assistant Director',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for Film Director / Assistant Director',
                                                     'Analyse a real-world challenge relevant to Film '
                                                     'Director / Assistant Director and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Study the craft through a suitable course, mentorship '
                                                     'or structured self-learning route.',
                                                     'Build a portfolio/showreel with original work relevant '
                                                     'to the target role.',
                                                     'Practise with realistic briefs and document your '
                                                     'creative process.',
                                                     'Seek internships, auditions, commissions or '
                                                     'entry-level projects; check contract and copyright '
                                                     'basics.'],
                                        'roles': ['Film Director / Assistant Director',
                                                  'Junior / Trainee Film Director / Assistant Director',
                                                  'Specialist or senior Film Director / Assistant Director '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Income may be project-based or variable; '
                                                                   'results depend on portfolio quality, '
                                                                   'network, niche and experience.',
                                        'education_cost_india': 'Course costs range from low-cost '
                                                                'self-learning to formal design/media '
                                                                'programmes; budget for software, equipment, '
                                                                'materials and production.',
                                        'future_outlook': 'For Film Director / Assistant Director, assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for Film Director / '
                                                                   'Assistant Director.',
                                                                   'Compare at least three recognised '
                                                                   'training routes for Film Director / '
                                                                   'Assistant Director, including total fees '
                                                                   'and duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for Film Director / Assistant '
                                                                   'Director.',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'Graphic Designer / Brand Designer': {'field': 'Creative Media, Communication and Design',
                                       'summary': 'Graphic Designer / Brand Designer: Creates stories, '
                                                  'experiences, visuals, performances or communication '
                                                  'materials for a defined audience.',
                                       'skills': ['Creative development and audience awareness',
                                                  'Portfolio-building and revision from feedback',
                                                  'Communication, collaboration and deadlines',
                                                  'Relevant production, design, language or editing tools'],
                                       'technologies': ['Tools and methods used in Graphic Designer / Brand '
                                                        'Designer',
                                                        'Spreadsheets, digital research and clear '
                                                        'documentation where relevant',
                                                        'Role-specific platforms confirmed from current job '
                                                        'descriptions'],
                                       'projects': ['Complete a beginner project or practical exercise '
                                                    'related to Graphic Designer / Brand Designer',
                                                    'Create a portfolio, case study or documented practical '
                                                    'assignment for Graphic Designer / Brand Designer',
                                                    'Analyse a real-world challenge relevant to Graphic '
                                                    'Designer / Brand Designer and present a safe, '
                                                    'evidence-based solution'],
                                       'pathways': ['Study the craft through a suitable course, mentorship '
                                                    'or structured self-learning route.',
                                                    'Build a portfolio/showreel with original work relevant '
                                                    'to the target role.',
                                                    'Practise with realistic briefs and document your '
                                                    'creative process.',
                                                    'Seek internships, auditions, commissions or entry-level '
                                                    'projects; check contract and copyright basics.'],
                                       'roles': ['Graphic Designer / Brand Designer',
                                                 'Junior / Trainee Graphic Designer / Brand Designer',
                                                 'Specialist or senior Graphic Designer / Brand Designer '
                                                 'after required training and experience'],
                                       'indicative_salary_india': 'Income may be project-based or variable; '
                                                                  'results depend on portfolio quality, '
                                                                  'network, niche and experience.',
                                       'education_cost_india': 'Course costs range from low-cost '
                                                               'self-learning to formal design/media '
                                                               'programmes; budget for software, equipment, '
                                                               'materials and production.',
                                       'future_outlook': 'For Graphic Designer / Brand Designer, assess '
                                                         'current demand using recent India-based job '
                                                         'listings, official recruitment notices and '
                                                         'relevant industry reports; outlook is not '
                                                         'guaranteed.',
                                       'recommended_next_steps': ['Read current official qualification and '
                                                                  'eligibility rules for Graphic Designer / '
                                                                  'Brand Designer.',
                                                                  'Compare at least three recognised '
                                                                  'training routes for Graphic Designer / '
                                                                  'Brand Designer, including total fees and '
                                                                  'duration.',
                                                                  'Complete one relevant project, portfolio '
                                                                  'piece, field exercise or supervised '
                                                                  'placement for Graphic Designer / Brand '
                                                                  'Designer.',
                                                                  'Speak to a working professional and '
                                                                  'review recent vacancies before committing '
                                                                  'to a course.'],
                                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                       'research_note': 'Role-specific starter guidance generated from the '
                                                        'career catalogue category. Verify licensing, '
                                                        'eligibility, salaries, course fees and outlook with '
                                                        'official/current sources.'},
 'Fashion Designer / Costume Designer': {'field': 'Creative Media, Communication and Design',
                                         'summary': 'Fashion Designer / Costume Designer: Creates stories, '
                                                    'experiences, visuals, performances or communication '
                                                    'materials for a defined audience.',
                                         'skills': ['Creative development and audience awareness',
                                                    'Portfolio-building and revision from feedback',
                                                    'Communication, collaboration and deadlines',
                                                    'Relevant production, design, language or editing tools'],
                                         'technologies': ['Tools and methods used in Fashion Designer / '
                                                          'Costume Designer',
                                                          'Spreadsheets, digital research and clear '
                                                          'documentation where relevant',
                                                          'Role-specific platforms confirmed from current '
                                                          'job descriptions'],
                                         'projects': ['Complete a beginner project or practical exercise '
                                                      'related to Fashion Designer / Costume Designer',
                                                      'Create a portfolio, case study or documented '
                                                      'practical assignment for Fashion Designer / Costume '
                                                      'Designer',
                                                      'Analyse a real-world challenge relevant to Fashion '
                                                      'Designer / Costume Designer and present a safe, '
                                                      'evidence-based solution'],
                                         'pathways': ['Study the craft through a suitable course, mentorship '
                                                      'or structured self-learning route.',
                                                      'Build a portfolio/showreel with original work '
                                                      'relevant to the target role.',
                                                      'Practise with realistic briefs and document your '
                                                      'creative process.',
                                                      'Seek internships, auditions, commissions or '
                                                      'entry-level projects; check contract and copyright '
                                                      'basics.'],
                                         'roles': ['Fashion Designer / Costume Designer',
                                                   'Junior / Trainee Fashion Designer / Costume Designer',
                                                   'Specialist or senior Fashion Designer / Costume Designer '
                                                   'after required training and experience'],
                                         'indicative_salary_india': 'Income may be project-based or '
                                                                    'variable; results depend on portfolio '
                                                                    'quality, network, niche and experience.',
                                         'education_cost_india': 'Course costs range from low-cost '
                                                                 'self-learning to formal design/media '
                                                                 'programmes; budget for software, '
                                                                 'equipment, materials and production.',
                                         'future_outlook': 'For Fashion Designer / Costume Designer, assess '
                                                           'current demand using recent India-based job '
                                                           'listings, official recruitment notices and '
                                                           'relevant industry reports; outlook is not '
                                                           'guaranteed.',
                                         'recommended_next_steps': ['Read current official qualification and '
                                                                    'eligibility rules for Fashion Designer '
                                                                    '/ Costume Designer.',
                                                                    'Compare at least three recognised '
                                                                    'training routes for Fashion Designer / '
                                                                    'Costume Designer, including total fees '
                                                                    'and duration.',
                                                                    'Complete one relevant project, '
                                                                    'portfolio piece, field exercise or '
                                                                    'supervised placement for Fashion '
                                                                    'Designer / Costume Designer.',
                                                                    'Speak to a working professional and '
                                                                    'review recent vacancies before '
                                                                    'committing to a course.'],
                                         'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                         'research_note': 'Role-specific starter guidance generated from the '
                                                          'career catalogue category. Verify licensing, '
                                                          'eligibility, salaries, course fees and outlook '
                                                          'with official/current sources.'},
 'Advertising Creative Director': {'field': 'Creative Media, Communication and Design',
                                   'summary': 'Advertising Creative Director: Creates stories, experiences, '
                                              'visuals, performances or communication materials for a '
                                              'defined audience.',
                                   'skills': ['Creative development and audience awareness',
                                              'Portfolio-building and revision from feedback',
                                              'Communication, collaboration and deadlines',
                                              'Relevant production, design, language or editing tools'],
                                   'technologies': ['Tools and methods used in Advertising Creative Director',
                                                    'Spreadsheets, digital research and clear documentation '
                                                    'where relevant',
                                                    'Role-specific platforms confirmed from current job '
                                                    'descriptions'],
                                   'projects': ['Complete a beginner project or practical exercise related '
                                                'to Advertising Creative Director',
                                                'Create a portfolio, case study or documented practical '
                                                'assignment for Advertising Creative Director',
                                                'Analyse a real-world challenge relevant to Advertising '
                                                'Creative Director and present a safe, evidence-based '
                                                'solution'],
                                   'pathways': ['Study the craft through a suitable course, mentorship or '
                                                'structured self-learning route.',
                                                'Build a portfolio/showreel with original work relevant to '
                                                'the target role.',
                                                'Practise with realistic briefs and document your creative '
                                                'process.',
                                                'Seek internships, auditions, commissions or entry-level '
                                                'projects; check contract and copyright basics.'],
                                   'roles': ['Advertising Creative Director',
                                             'Junior / Trainee Advertising Creative Director',
                                             'Specialist or senior Advertising Creative Director after '
                                             'required training and experience'],
                                   'indicative_salary_india': 'Income may be project-based or variable; '
                                                              'results depend on portfolio quality, network, '
                                                              'niche and experience.',
                                   'education_cost_india': 'Course costs range from low-cost self-learning '
                                                           'to formal design/media programmes; budget for '
                                                           'software, equipment, materials and production.',
                                   'future_outlook': 'For Advertising Creative Director, assess current '
                                                     'demand using recent India-based job listings, official '
                                                     'recruitment notices and relevant industry reports; '
                                                     'outlook is not guaranteed.',
                                   'recommended_next_steps': ['Read current official qualification and '
                                                              'eligibility rules for Advertising Creative '
                                                              'Director.',
                                                              'Compare at least three recognised training '
                                                              'routes for Advertising Creative Director, '
                                                              'including total fees and duration.',
                                                              'Complete one relevant project, portfolio '
                                                              'piece, field exercise or supervised placement '
                                                              'for Advertising Creative Director.',
                                                              'Speak to a working professional and review '
                                                              'recent vacancies before committing to a '
                                                              'course.'],
                                   'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                   'research_note': 'Role-specific starter guidance generated from the '
                                                    'career catalogue category. Verify licensing, '
                                                    'eligibility, salaries, course fees and outlook with '
                                                    'official/current sources.'},
 'UX/UI Designer / Product Designer': {'field': 'Creative Media, Communication and Design',
                                       'summary': 'UX/UI Designer / Product Designer: Creates stories, '
                                                  'experiences, visuals, performances or communication '
                                                  'materials for a defined audience.',
                                       'skills': ['Creative development and audience awareness',
                                                  'Portfolio-building and revision from feedback',
                                                  'Communication, collaboration and deadlines',
                                                  'Relevant production, design, language or editing tools'],
                                       'technologies': ['Tools and methods used in UX/UI Designer / Product '
                                                        'Designer',
                                                        'Spreadsheets, digital research and clear '
                                                        'documentation where relevant',
                                                        'Role-specific platforms confirmed from current job '
                                                        'descriptions'],
                                       'projects': ['Complete a beginner project or practical exercise '
                                                    'related to UX/UI Designer / Product Designer',
                                                    'Create a portfolio, case study or documented practical '
                                                    'assignment for UX/UI Designer / Product Designer',
                                                    'Analyse a real-world challenge relevant to UX/UI '
                                                    'Designer / Product Designer and present a safe, '
                                                    'evidence-based solution'],
                                       'pathways': ['Study the craft through a suitable course, mentorship '
                                                    'or structured self-learning route.',
                                                    'Build a portfolio/showreel with original work relevant '
                                                    'to the target role.',
                                                    'Practise with realistic briefs and document your '
                                                    'creative process.',
                                                    'Seek internships, auditions, commissions or entry-level '
                                                    'projects; check contract and copyright basics.'],
                                       'roles': ['UX/UI Designer / Product Designer',
                                                 'Junior / Trainee UX/UI Designer / Product Designer',
                                                 'Specialist or senior UX/UI Designer / Product Designer '
                                                 'after required training and experience'],
                                       'indicative_salary_india': 'Income may be project-based or variable; '
                                                                  'results depend on portfolio quality, '
                                                                  'network, niche and experience.',
                                       'education_cost_india': 'Course costs range from low-cost '
                                                               'self-learning to formal design/media '
                                                               'programmes; budget for software, equipment, '
                                                               'materials and production.',
                                       'future_outlook': 'For UX/UI Designer / Product Designer, assess '
                                                         'current demand using recent India-based job '
                                                         'listings, official recruitment notices and '
                                                         'relevant industry reports; outlook is not '
                                                         'guaranteed.',
                                       'recommended_next_steps': ['Read current official qualification and '
                                                                  'eligibility rules for UX/UI Designer / '
                                                                  'Product Designer.',
                                                                  'Compare at least three recognised '
                                                                  'training routes for UX/UI Designer / '
                                                                  'Product Designer, including total fees '
                                                                  'and duration.',
                                                                  'Complete one relevant project, portfolio '
                                                                  'piece, field exercise or supervised '
                                                                  'placement for UX/UI Designer / Product '
                                                                  'Designer.',
                                                                  'Speak to a working professional and '
                                                                  'review recent vacancies before committing '
                                                                  'to a course.'],
                                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                       'research_note': 'Role-specific starter guidance generated from the '
                                                        'career catalogue category. Verify licensing, '
                                                        'eligibility, salaries, course fees and outlook with '
                                                        'official/current sources.'},
 'Animator / VFX Artist': {'field': 'Creative Media, Communication and Design',
                           'summary': 'Animator / VFX Artist: Creates stories, experiences, visuals, '
                                      'performances or communication materials for a defined audience.',
                           'skills': ['Creative development and audience awareness',
                                      'Portfolio-building and revision from feedback',
                                      'Communication, collaboration and deadlines',
                                      'Relevant production, design, language or editing tools'],
                           'technologies': ['Tools and methods used in Animator / VFX Artist',
                                            'Spreadsheets, digital research and clear documentation where '
                                            'relevant',
                                            'Role-specific platforms confirmed from current job '
                                            'descriptions'],
                           'projects': ['Complete a beginner project or practical exercise related to '
                                        'Animator / VFX Artist',
                                        'Create a portfolio, case study or documented practical assignment '
                                        'for Animator / VFX Artist',
                                        'Analyse a real-world challenge relevant to Animator / VFX Artist '
                                        'and present a safe, evidence-based solution'],
                           'pathways': ['Study the craft through a suitable course, mentorship or structured '
                                        'self-learning route.',
                                        'Build a portfolio/showreel with original work relevant to the '
                                        'target role.',
                                        'Practise with realistic briefs and document your creative process.',
                                        'Seek internships, auditions, commissions or entry-level projects; '
                                        'check contract and copyright basics.'],
                           'roles': ['Animator / VFX Artist',
                                     'Junior / Trainee Animator / VFX Artist',
                                     'Specialist or senior Animator / VFX Artist after required training and '
                                     'experience'],
                           'indicative_salary_india': 'Income may be project-based or variable; results '
                                                      'depend on portfolio quality, network, niche and '
                                                      'experience.',
                           'education_cost_india': 'Course costs range from low-cost self-learning to formal '
                                                   'design/media programmes; budget for software, equipment, '
                                                   'materials and production.',
                           'future_outlook': 'For Animator / VFX Artist, assess current demand using recent '
                                             'India-based job listings, official recruitment notices and '
                                             'relevant industry reports; outlook is not guaranteed.',
                           'recommended_next_steps': ['Read current official qualification and eligibility '
                                                      'rules for Animator / VFX Artist.',
                                                      'Compare at least three recognised training routes for '
                                                      'Animator / VFX Artist, including total fees and '
                                                      'duration.',
                                                      'Complete one relevant project, portfolio piece, field '
                                                      'exercise or supervised placement for Animator / VFX '
                                                      'Artist.',
                                                      'Speak to a working professional and review recent '
                                                      'vacancies before committing to a course.'],
                           'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                           'research_note': 'Role-specific starter guidance generated from the career '
                                            'catalogue category. Verify licensing, eligibility, salaries, '
                                            'course fees and outlook with official/current sources.'},
 'Screenwriter / Script Writer': {'field': 'Creative Media, Communication and Design',
                                  'summary': 'Screenwriter / Script Writer: Creates stories, experiences, '
                                             'visuals, performances or communication materials for a defined '
                                             'audience.',
                                  'skills': ['Creative development and audience awareness',
                                             'Portfolio-building and revision from feedback',
                                             'Communication, collaboration and deadlines',
                                             'Relevant production, design, language or editing tools'],
                                  'technologies': ['Tools and methods used in Screenwriter / Script Writer',
                                                   'Spreadsheets, digital research and clear documentation '
                                                   'where relevant',
                                                   'Role-specific platforms confirmed from current job '
                                                   'descriptions'],
                                  'projects': ['Complete a beginner project or practical exercise related to '
                                               'Screenwriter / Script Writer',
                                               'Create a portfolio, case study or documented practical '
                                               'assignment for Screenwriter / Script Writer',
                                               'Analyse a real-world challenge relevant to Screenwriter / '
                                               'Script Writer and present a safe, evidence-based solution'],
                                  'pathways': ['Study the craft through a suitable course, mentorship or '
                                               'structured self-learning route.',
                                               'Build a portfolio/showreel with original work relevant to '
                                               'the target role.',
                                               'Practise with realistic briefs and document your creative '
                                               'process.',
                                               'Seek internships, auditions, commissions or entry-level '
                                               'projects; check contract and copyright basics.'],
                                  'roles': ['Screenwriter / Script Writer',
                                            'Junior / Trainee Screenwriter / Script Writer',
                                            'Specialist or senior Screenwriter / Script Writer after '
                                            'required training and experience'],
                                  'indicative_salary_india': 'Income may be project-based or variable; '
                                                             'results depend on portfolio quality, network, '
                                                             'niche and experience.',
                                  'education_cost_india': 'Course costs range from low-cost self-learning to '
                                                          'formal design/media programmes; budget for '
                                                          'software, equipment, materials and production.',
                                  'future_outlook': 'For Screenwriter / Script Writer, assess current demand '
                                                    'using recent India-based job listings, official '
                                                    'recruitment notices and relevant industry reports; '
                                                    'outlook is not guaranteed.',
                                  'recommended_next_steps': ['Read current official qualification and '
                                                             'eligibility rules for Screenwriter / Script '
                                                             'Writer.',
                                                             'Compare at least three recognised training '
                                                             'routes for Screenwriter / Script Writer, '
                                                             'including total fees and duration.',
                                                             'Complete one relevant project, portfolio '
                                                             'piece, field exercise or supervised placement '
                                                             'for Screenwriter / Script Writer.',
                                                             'Speak to a working professional and review '
                                                             'recent vacancies before committing to a '
                                                             'course.'],
                                  'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                  'research_note': 'Role-specific starter guidance generated from the career '
                                                   'catalogue category. Verify licensing, eligibility, '
                                                   'salaries, course fees and outlook with official/current '
                                                   'sources.'},
 'Company Secretary (CS)': {'field': 'Finance, Accounting and Governance',
                            'summary': 'Company Secretary (CS): Works with financial records, analysis, '
                                       'risk, regulation, markets or organisational decisions.',
                            'skills': ['Numeracy and analytical reasoning',
                                       'Excel/spreadsheets and data interpretation',
                                       'Accuracy, confidentiality and professional ethics',
                                       'Financial reporting, regulation or research relevant to the role'],
                            'technologies': ['Tools and methods used in Company Secretary (CS)',
                                             'Spreadsheets, digital research and clear documentation where '
                                             'relevant',
                                             'Role-specific platforms confirmed from current job '
                                             'descriptions'],
                            'projects': ['Complete a beginner project or practical exercise related to '
                                         'Company Secretary (CS)',
                                         'Create a portfolio, case study or documented practical assignment '
                                         'for Company Secretary (CS)',
                                         'Analyse a real-world challenge relevant to Company Secretary (CS) '
                                         'and present a safe, evidence-based solution'],
                            'pathways': ['Check the official qualification or recruitment route (for '
                                         'example, professional-body exams or public recruitment notices).',
                                         'Build accounting, finance, economics, spreadsheet and analytical '
                                         'foundations as appropriate.',
                                         'Practise with case studies, financial models or compliant sample '
                                         'reports.',
                                         'Verify current exam rules, eligibility, registration and '
                                         'role-specific certifications from official sources.'],
                            'roles': ['Company Secretary (CS)',
                                      'Junior / Trainee Company Secretary (CS)',
                                      'Specialist or senior Company Secretary (CS) after required training '
                                      'and experience'],
                            'indicative_salary_india': 'Compensation varies by qualification, employer, '
                                                       'city, performance and experience; public-sector pay '
                                                       'follows official notices.',
                            'education_cost_india': 'Include professional-body registration, exam attempts, '
                                                    'coaching if chosen, study materials and degree tuition; '
                                                    'official fees change.',
                            'future_outlook': 'For Company Secretary (CS), assess current demand using '
                                              'recent India-based job listings, official recruitment notices '
                                              'and relevant industry reports; outlook is not guaranteed.',
                            'recommended_next_steps': ['Read current official qualification and eligibility '
                                                       'rules for Company Secretary (CS).',
                                                       'Compare at least three recognised training routes '
                                                       'for Company Secretary (CS), including total fees and '
                                                       'duration.',
                                                       'Complete one relevant project, portfolio piece, '
                                                       'field exercise or supervised placement for Company '
                                                       'Secretary (CS).',
                                                       'Speak to a working professional and review recent '
                                                       'vacancies before committing to a course.'],
                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                            'research_note': 'Role-specific starter guidance generated from the career '
                                             'catalogue category. Verify licensing, eligibility, salaries, '
                                             'course fees and outlook with official/current sources.'},
 'Bank PO / Bank Manager': {'field': 'Finance, Accounting and Governance',
                            'summary': 'Bank PO / Bank Manager: Works with financial records, analysis, '
                                       'risk, regulation, markets or organisational decisions.',
                            'skills': ['Numeracy and analytical reasoning',
                                       'Excel/spreadsheets and data interpretation',
                                       'Accuracy, confidentiality and professional ethics',
                                       'Financial reporting, regulation or research relevant to the role'],
                            'technologies': ['Tools and methods used in Bank PO / Bank Manager',
                                             'Spreadsheets, digital research and clear documentation where '
                                             'relevant',
                                             'Role-specific platforms confirmed from current job '
                                             'descriptions'],
                            'projects': ['Complete a beginner project or practical exercise related to Bank '
                                         'PO / Bank Manager',
                                         'Create a portfolio, case study or documented practical assignment '
                                         'for Bank PO / Bank Manager',
                                         'Analyse a real-world challenge relevant to Bank PO / Bank Manager '
                                         'and present a safe, evidence-based solution'],
                            'pathways': ['Check the official qualification or recruitment route (for '
                                         'example, professional-body exams or public recruitment notices).',
                                         'Build accounting, finance, economics, spreadsheet and analytical '
                                         'foundations as appropriate.',
                                         'Practise with case studies, financial models or compliant sample '
                                         'reports.',
                                         'Verify current exam rules, eligibility, registration and '
                                         'role-specific certifications from official sources.'],
                            'roles': ['Bank PO / Bank Manager',
                                      'Junior / Trainee Bank PO / Bank Manager',
                                      'Specialist or senior Bank PO / Bank Manager after required training '
                                      'and experience'],
                            'indicative_salary_india': 'Compensation varies by qualification, employer, '
                                                       'city, performance and experience; public-sector pay '
                                                       'follows official notices.',
                            'education_cost_india': 'Include professional-body registration, exam attempts, '
                                                    'coaching if chosen, study materials and degree tuition; '
                                                    'official fees change.',
                            'future_outlook': 'For Bank PO / Bank Manager, assess current demand using '
                                              'recent India-based job listings, official recruitment notices '
                                              'and relevant industry reports; outlook is not guaranteed.',
                            'recommended_next_steps': ['Read current official qualification and eligibility '
                                                       'rules for Bank PO / Bank Manager.',
                                                       'Compare at least three recognised training routes '
                                                       'for Bank PO / Bank Manager, including total fees and '
                                                       'duration.',
                                                       'Complete one relevant project, portfolio piece, '
                                                       'field exercise or supervised placement for Bank PO / '
                                                       'Bank Manager.',
                                                       'Speak to a working professional and review recent '
                                                       'vacancies before committing to a course.'],
                            'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                            'research_note': 'Role-specific starter guidance generated from the career '
                                             'catalogue category. Verify licensing, eligibility, salaries, '
                                             'course fees and outlook with official/current sources.'},
 'Cost & Management Accountant (CMA)': {'field': 'Finance, Accounting and Governance',
                                        'summary': 'Cost & Management Accountant (CMA): Works with financial '
                                                   'records, analysis, risk, regulation, markets or '
                                                   'organisational decisions.',
                                        'skills': ['Numeracy and analytical reasoning',
                                                   'Excel/spreadsheets and data interpretation',
                                                   'Accuracy, confidentiality and professional ethics',
                                                   'Financial reporting, regulation or research relevant to '
                                                   'the role'],
                                        'technologies': ['Tools and methods used in Cost & Management '
                                                         'Accountant (CMA)',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to Cost & Management Accountant (CMA)',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for Cost & Management Accountant (CMA)',
                                                     'Analyse a real-world challenge relevant to Cost & '
                                                     'Management Accountant (CMA) and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Check the official qualification or recruitment route '
                                                     '(for example, professional-body exams or public '
                                                     'recruitment notices).',
                                                     'Build accounting, finance, economics, spreadsheet and '
                                                     'analytical foundations as appropriate.',
                                                     'Practise with case studies, financial models or '
                                                     'compliant sample reports.',
                                                     'Verify current exam rules, eligibility, registration '
                                                     'and role-specific certifications from official '
                                                     'sources.'],
                                        'roles': ['Cost & Management Accountant (CMA)',
                                                  'Junior / Trainee Cost & Management Accountant (CMA)',
                                                  'Specialist or senior Cost & Management Accountant (CMA) '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Compensation varies by qualification, '
                                                                   'employer, city, performance and '
                                                                   'experience; public-sector pay follows '
                                                                   'official notices.',
                                        'education_cost_india': 'Include professional-body registration, '
                                                                'exam attempts, coaching if chosen, study '
                                                                'materials and degree tuition; official fees '
                                                                'change.',
                                        'future_outlook': 'For Cost & Management Accountant (CMA), assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for Cost & Management '
                                                                   'Accountant (CMA).',
                                                                   'Compare at least three recognised '
                                                                   'training routes for Cost & Management '
                                                                   'Accountant (CMA), including total fees '
                                                                   'and duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for Cost & Management '
                                                                   'Accountant (CMA).',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'Tax Consultant / GST Practitioner': {'field': 'Finance, Accounting and Governance',
                                       'summary': 'Tax Consultant / GST Practitioner: Works with financial '
                                                  'records, analysis, risk, regulation, markets or '
                                                  'organisational decisions.',
                                       'skills': ['Numeracy and analytical reasoning',
                                                  'Excel/spreadsheets and data interpretation',
                                                  'Accuracy, confidentiality and professional ethics',
                                                  'Financial reporting, regulation or research relevant to '
                                                  'the role'],
                                       'technologies': ['Tools and methods used in Tax Consultant / GST '
                                                        'Practitioner',
                                                        'Spreadsheets, digital research and clear '
                                                        'documentation where relevant',
                                                        'Role-specific platforms confirmed from current job '
                                                        'descriptions'],
                                       'projects': ['Complete a beginner project or practical exercise '
                                                    'related to Tax Consultant / GST Practitioner',
                                                    'Create a portfolio, case study or documented practical '
                                                    'assignment for Tax Consultant / GST Practitioner',
                                                    'Analyse a real-world challenge relevant to Tax '
                                                    'Consultant / GST Practitioner and present a safe, '
                                                    'evidence-based solution'],
                                       'pathways': ['Check the official qualification or recruitment route '
                                                    '(for example, professional-body exams or public '
                                                    'recruitment notices).',
                                                    'Build accounting, finance, economics, spreadsheet and '
                                                    'analytical foundations as appropriate.',
                                                    'Practise with case studies, financial models or '
                                                    'compliant sample reports.',
                                                    'Verify current exam rules, eligibility, registration '
                                                    'and role-specific certifications from official '
                                                    'sources.'],
                                       'roles': ['Tax Consultant / GST Practitioner',
                                                 'Junior / Trainee Tax Consultant / GST Practitioner',
                                                 'Specialist or senior Tax Consultant / GST Practitioner '
                                                 'after required training and experience'],
                                       'indicative_salary_india': 'Compensation varies by qualification, '
                                                                  'employer, city, performance and '
                                                                  'experience; public-sector pay follows '
                                                                  'official notices.',
                                       'education_cost_india': 'Include professional-body registration, exam '
                                                               'attempts, coaching if chosen, study '
                                                               'materials and degree tuition; official fees '
                                                               'change.',
                                       'future_outlook': 'For Tax Consultant / GST Practitioner, assess '
                                                         'current demand using recent India-based job '
                                                         'listings, official recruitment notices and '
                                                         'relevant industry reports; outlook is not '
                                                         'guaranteed.',
                                       'recommended_next_steps': ['Read current official qualification and '
                                                                  'eligibility rules for Tax Consultant / '
                                                                  'GST Practitioner.',
                                                                  'Compare at least three recognised '
                                                                  'training routes for Tax Consultant / GST '
                                                                  'Practitioner, including total fees and '
                                                                  'duration.',
                                                                  'Complete one relevant project, portfolio '
                                                                  'piece, field exercise or supervised '
                                                                  'placement for Tax Consultant / GST '
                                                                  'Practitioner.',
                                                                  'Speak to a working professional and '
                                                                  'review recent vacancies before committing '
                                                                  'to a course.'],
                                       'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                       'research_note': 'Role-specific starter guidance generated from the '
                                                        'career catalogue category. Verify licensing, '
                                                        'eligibility, salaries, course fees and outlook with '
                                                        'official/current sources.'},
 'Compliance Officer / Legal Advisor': {'field': 'Finance, Accounting and Governance',
                                        'summary': 'Compliance Officer / Legal Advisor: Works with financial '
                                                   'records, analysis, risk, regulation, markets or '
                                                   'organisational decisions.',
                                        'skills': ['Numeracy and analytical reasoning',
                                                   'Excel/spreadsheets and data interpretation',
                                                   'Accuracy, confidentiality and professional ethics',
                                                   'Financial reporting, regulation or research relevant to '
                                                   'the role'],
                                        'technologies': ['Tools and methods used in Compliance Officer / '
                                                         'Legal Advisor',
                                                         'Spreadsheets, digital research and clear '
                                                         'documentation where relevant',
                                                         'Role-specific platforms confirmed from current job '
                                                         'descriptions'],
                                        'projects': ['Complete a beginner project or practical exercise '
                                                     'related to Compliance Officer / Legal Advisor',
                                                     'Create a portfolio, case study or documented practical '
                                                     'assignment for Compliance Officer / Legal Advisor',
                                                     'Analyse a real-world challenge relevant to Compliance '
                                                     'Officer / Legal Advisor and present a safe, '
                                                     'evidence-based solution'],
                                        'pathways': ['Check the official qualification or recruitment route '
                                                     '(for example, professional-body exams or public '
                                                     'recruitment notices).',
                                                     'Build accounting, finance, economics, spreadsheet and '
                                                     'analytical foundations as appropriate.',
                                                     'Practise with case studies, financial models or '
                                                     'compliant sample reports.',
                                                     'Verify current exam rules, eligibility, registration '
                                                     'and role-specific certifications from official '
                                                     'sources.'],
                                        'roles': ['Compliance Officer / Legal Advisor',
                                                  'Junior / Trainee Compliance Officer / Legal Advisor',
                                                  'Specialist or senior Compliance Officer / Legal Advisor '
                                                  'after required training and experience'],
                                        'indicative_salary_india': 'Compensation varies by qualification, '
                                                                   'employer, city, performance and '
                                                                   'experience; public-sector pay follows '
                                                                   'official notices.',
                                        'education_cost_india': 'Include professional-body registration, '
                                                                'exam attempts, coaching if chosen, study '
                                                                'materials and degree tuition; official fees '
                                                                'change.',
                                        'future_outlook': 'For Compliance Officer / Legal Advisor, assess '
                                                          'current demand using recent India-based job '
                                                          'listings, official recruitment notices and '
                                                          'relevant industry reports; outlook is not '
                                                          'guaranteed.',
                                        'recommended_next_steps': ['Read current official qualification and '
                                                                   'eligibility rules for Compliance Officer '
                                                                   '/ Legal Advisor.',
                                                                   'Compare at least three recognised '
                                                                   'training routes for Compliance Officer / '
                                                                   'Legal Advisor, including total fees and '
                                                                   'duration.',
                                                                   'Complete one relevant project, portfolio '
                                                                   'piece, field exercise or supervised '
                                                                   'placement for Compliance Officer / Legal '
                                                                   'Advisor.',
                                                                   'Speak to a working professional and '
                                                                   'review recent vacancies before '
                                                                   'committing to a course.'],
                                        'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                        'research_note': 'Role-specific starter guidance generated from the '
                                                         'career catalogue category. Verify licensing, '
                                                         'eligibility, salaries, course fees and outlook '
                                                         'with official/current sources.'},
 'RBI / SEBI / NABARD Officer': {'field': 'Finance, Accounting and Governance',
                                 'summary': 'RBI / SEBI / NABARD Officer: Works with financial records, '
                                            'analysis, risk, regulation, markets or organisational '
                                            'decisions.',
                                 'skills': ['Numeracy and analytical reasoning',
                                            'Excel/spreadsheets and data interpretation',
                                            'Accuracy, confidentiality and professional ethics',
                                            'Financial reporting, regulation or research relevant to the '
                                            'role'],
                                 'technologies': ['Tools and methods used in RBI / SEBI / NABARD Officer',
                                                  'Spreadsheets, digital research and clear documentation '
                                                  'where relevant',
                                                  'Role-specific platforms confirmed from current job '
                                                  'descriptions'],
                                 'projects': ['Complete a beginner project or practical exercise related to '
                                              'RBI / SEBI / NABARD Officer',
                                              'Create a portfolio, case study or documented practical '
                                              'assignment for RBI / SEBI / NABARD Officer',
                                              'Analyse a real-world challenge relevant to RBI / SEBI / '
                                              'NABARD Officer and present a safe, evidence-based solution'],
                                 'pathways': ['Check the official qualification or recruitment route (for '
                                              'example, professional-body exams or public recruitment '
                                              'notices).',
                                              'Build accounting, finance, economics, spreadsheet and '
                                              'analytical foundations as appropriate.',
                                              'Practise with case studies, financial models or compliant '
                                              'sample reports.',
                                              'Verify current exam rules, eligibility, registration and '
                                              'role-specific certifications from official sources.'],
                                 'roles': ['RBI / SEBI / NABARD Officer',
                                           'Junior / Trainee RBI / SEBI / NABARD Officer',
                                           'Specialist or senior RBI / SEBI / NABARD Officer after required '
                                           'training and experience'],
                                 'indicative_salary_india': 'Compensation varies by qualification, employer, '
                                                            'city, performance and experience; public-sector '
                                                            'pay follows official notices.',
                                 'education_cost_india': 'Include professional-body registration, exam '
                                                         'attempts, coaching if chosen, study materials and '
                                                         'degree tuition; official fees change.',
                                 'future_outlook': 'For RBI / SEBI / NABARD Officer, assess current demand '
                                                   'using recent India-based job listings, official '
                                                   'recruitment notices and relevant industry reports; '
                                                   'outlook is not guaranteed.',
                                 'recommended_next_steps': ['Read current official qualification and '
                                                            'eligibility rules for RBI / SEBI / NABARD '
                                                            'Officer.',
                                                            'Compare at least three recognised training '
                                                            'routes for RBI / SEBI / NABARD Officer, '
                                                            'including total fees and duration.',
                                                            'Complete one relevant project, portfolio piece, '
                                                            'field exercise or supervised placement for RBI '
                                                            '/ SEBI / NABARD Officer.',
                                                            'Speak to a working professional and review '
                                                            'recent vacancies before committing to a '
                                                            'course.'],
                                 'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                 'research_note': 'Role-specific starter guidance generated from the career '
                                                  'catalogue category. Verify licensing, eligibility, '
                                                  'salaries, course fees and outlook with official/current '
                                                  'sources.'},
 'Government Clerk / Administrative Officer': {'field': 'Public Service, Defence and Social Impact',
                                               'summary': 'Government Clerk / Administrative Officer: Serves '
                                                          'communities or public institutions through '
                                                          'administration, protection, policy, development '
                                                          'or disciplined operational work.',
                                               'skills': ['Communication and public-service orientation',
                                                          'Ethical judgement and accountability',
                                                          'Role-specific general knowledge, fitness or '
                                                          'subject preparation',
                                                          'Planning, teamwork and decision-making'],
                                               'technologies': ['Tools and methods used in Government Clerk '
                                                                '/ Administrative Officer',
                                                                'Spreadsheets, digital research and clear '
                                                                'documentation where relevant',
                                                                'Role-specific platforms confirmed from '
                                                                'current job descriptions'],
                                               'projects': ['Complete a beginner project or practical '
                                                            'exercise related to Government Clerk / '
                                                            'Administrative Officer',
                                                            'Create a portfolio, case study or documented '
                                                            'practical assignment for Government Clerk / '
                                                            'Administrative Officer',
                                                            'Analyse a real-world challenge relevant to '
                                                            'Government Clerk / Administrative Officer and '
                                                            'present a safe, evidence-based solution'],
                                               'pathways': ['Read the latest official eligibility, age, '
                                                            'education, medical and selection criteria for '
                                                            'the exact post.',
                                                            'Plan degree choices and exam preparation around '
                                                            'the official recruitment route.',
                                                            'For uniformed services, assess physical and '
                                                            'medical standards early.',
                                                            'Use official notifications for dates, syllabus, '
                                                            'selection stages and pay details.'],
                                               'roles': ['Government Clerk / Administrative Officer',
                                                         'Junior / Trainee Government Clerk / Administrative '
                                                         'Officer',
                                                         'Specialist or senior Government Clerk / '
                                                         'Administrative Officer after required training and '
                                                         'experience'],
                                               'indicative_salary_india': 'Vacancies and pay depend on '
                                                                          'official recruitment cycles, '
                                                                          'rank, cadre, allowances and '
                                                                          'service rules.',
                                               'education_cost_india': 'Preparation expenses vary; include '
                                                                       'exam fees, study materials, coaching '
                                                                       'if chosen, travel and '
                                                                       'medical/fitness preparation.',
                                               'future_outlook': 'For Government Clerk / Administrative '
                                                                 'Officer, assess current demand using '
                                                                 'recent India-based job listings, official '
                                                                 'recruitment notices and relevant industry '
                                                                 'reports; outlook is not guaranteed.',
                                               'recommended_next_steps': ['Read current official '
                                                                          'qualification and eligibility '
                                                                          'rules for Government Clerk / '
                                                                          'Administrative Officer.',
                                                                          'Compare at least three recognised '
                                                                          'training routes for Government '
                                                                          'Clerk / Administrative Officer, '
                                                                          'including total fees and '
                                                                          'duration.',
                                                                          'Complete one relevant project, '
                                                                          'portfolio piece, field exercise '
                                                                          'or supervised placement for '
                                                                          'Government Clerk / Administrative '
                                                                          'Officer.',
                                                                          'Speak to a working professional '
                                                                          'and review recent vacancies '
                                                                          'before committing to a course.'],
                                               'catalogue_status': 'domain_specific_profile_needs_current_source_verification',
                                               'research_note': 'Role-specific starter guidance generated '
                                                                'from the career catalogue category. Verify '
                                                                'licensing, eligibility, salaries, course '
                                                                'fees and outlook with official/current '
                                                                'sources.'}})

CAREER_PLANNING_NOTES = {
    "salary": "Use current India-specific salary research for the exact role, city, employer and experience level; figures are indicative, never guaranteed.",
    "cost": "Compare official tuition, exam fees, materials, equipment, accommodation and living costs for each shortlisted route.",
    "outlook": "Future demand varies by region, industry, regulation and technology; revisit current job postings and official sources.",
}

def _enrich_profile(profile, career_title):
    result = dict(profile)
    result.setdefault("career_domain", result.get("field", "Career Exploration"))
    result.setdefault("indicative_salary_india", CAREER_PLANNING_NOTES["salary"])
    result.setdefault("education_cost_india", CAREER_PLANNING_NOTES["cost"])
    result.setdefault("future_outlook", CAREER_PLANNING_NOTES["outlook"])
    result.setdefault("recommended_next_steps", [
        "Compare recognised courses, eligibility, duration and total cost.",
        "Review recent job descriptions for the skills commonly requested.",
        "Complete a relevant project or supervised practical experience and document the result.",
        "Speak with a qualified practitioner or course adviser before committing to major expenses.",
    ])
    result["cost_salary_disclaimer"] = "Guidance is exploratory. Verify current fees, salaries, accreditation, licensing and eligibility with official sources."
    result["career_title"] = career_title
    return result


def get_career_guidance(career_title):
    """Return career-specific guidance or a domain-matched starter profile."""
    if not career_title:
        return _enrich_profile(_make_general_guidance("Career exploration"), "Career exploration")

    requested = _normalise_title(career_title)

    for known_title, profile in CAREER_GUIDANCE.items():
        if _normalise_title(known_title) == requested:
            result = dict(profile)
            result["catalogue_status"] = "starter_profile"
            result["research_note"] = (
                "Review current official course, eligibility and employment "
                "requirements before making an education or career decision."
            )
            return _enrich_profile(result, career_title)

    return _enrich_profile(_make_general_guidance(career_title), career_title)
