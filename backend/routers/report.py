
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import Result, User
from auth_utils import get_current_user

from io import BytesIO
from xml.sax.saxutils import escape
import json
import os

from services.career_guidance import (
    get_career_guidance,
    get_strengths,
)

router = APIRouter(prefix="/report", tags=["Report"])


# ---------------------------------------------------------
# GET: CURRENT STUDENT'S ASSESSMENT RESULT
# ---------------------------------------------------------
@router.get("/my-result")
def get_my_result(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No result found. Please complete the test first.",
        )

    top_5 = result.top_5_careers or []

    if isinstance(top_5, str):
        try:
            top_5 = json.loads(top_5)
        except (ValueError, TypeError):
            top_5 = []

    if not isinstance(top_5, list):
        top_5 = []

    return {
        "user": {
            "name": current_user.name,
            "email": current_user.email,
            "school": current_user.school,
            "student_class": current_user.student_class,
            "father_name": current_user.father_name,
            "mother_name": current_user.mother_name,
        },
        "intelligence": {
            "logical_mathematical": round(
                result.logical_mathematical or 0, 2
            ),
            "interpersonal": round(
                result.interpersonal or 0, 2
            ),
            "bodily_kinesthetic": round(
                result.bodily_kinesthetic or 0, 2
            ),
            "verbal_linguistic": round(
                result.verbal_linguistic or 0, 2
            ),
            "musical": round(result.musical or 0, 2),
            "naturalist": round(result.naturalist or 0, 2),
            "spatial_visual": round(
                result.spatial_visual or 0, 2
            ),
            "intrapersonal": round(
                result.intrapersonal or 0, 2
            ),
        },
        "riasec": {
            "realistic": round(
                result.riasec_realistic or 0, 2
            ),
            "investigative": round(
                result.riasec_investigative or 0, 2
            ),
            "artistic": round(
                result.riasec_artistic or 0, 2
            ),
            "social": round(result.riasec_social or 0, 2),
            "enterprising": round(
                result.riasec_enterprising or 0, 2
            ),
            "conventional": round(
                result.riasec_conventional or 0, 2
            ),
        },
        "top_career": result.top_career,
        "top_5_careers": top_5,
        "personality_clarity": (
            result.personality_clarity or "Moderately Defined"
        ),
        "trait_variance": result.trait_variance or 0,
        "completed_at": (
            str(result.completed_at)
            if result.completed_at
            else ""
        ),
    }


# ---------------------------------------------------------
# GET: CHECK WHETHER THE STUDENT HAS A RESULT
# ---------------------------------------------------------
@router.get("/has-result")
def has_result(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .first()
    )

    return {"has_result": result is not None}


# ---------------------------------------------------------
# DOWNLOAD PERSONALIZED PDF REPORT
# ---------------------------------------------------------
@router.get("/download-pdf")
def download_pdf(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = (
        db.query(Result)
        .filter(Result.user_id == current_user.id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="No result found. Please complete the test first.",
        )

    # Safely normalize top-five career data.
    top_5 = result.top_5_careers or []

    if isinstance(top_5, str):
        try:
            top_5 = json.loads(top_5)
        except (ValueError, TypeError):
            top_5 = []

    if not isinstance(top_5, list):
        top_5 = []

    # ReportLab imports.
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            HRFlowable,
            PageBreak,
            Image as RLImage,
        )
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_CENTER, TA_RIGHT
        from reportlab.graphics.shapes import Drawing
        from reportlab.graphics.charts.barcharts import HorizontalBarChart

    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="ReportLab is not installed. Install it using pip install reportlab.",
        )

    # -----------------------------------------------------
    # PDF CONFIGURATION
    # -----------------------------------------------------
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
        title="Personalized Psychometric Assessment Report",
        author="Knowletive",
    )

    PRIMARY = colors.HexColor("#2855D9")       # Knowletive blue
    SECONDARY = colors.HexColor("#0F9F91")     # Teal accent
    DARK = colors.HexColor("#18243A")
    GRAY = colors.HexColor("#5F6F86")
    LGRAY = colors.HexColor("#F4F7FC")
    WHITE = colors.white
    GREEN = colors.HexColor("#0E9F6E")
    ORANGE = colors.HexColor("#D97706")
    RED = colors.HexColor("#DC4C4C")
    BLUE = colors.HexColor("#4285F4")
    BORDER = colors.HexColor("#E1E7F0")

    # Use a clean modern font when available, with portable PDF-safe fallback.
    FONT = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        font_candidates = [
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "KnowletiveSans"),
            ("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf", "KnowletiveSans"),
        ]
        bold_candidates = [
            ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "KnowletiveSansBold"),
            ("/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf", "KnowletiveSansBold"),
        ]
        regular_path = next((path for path, _ in font_candidates if os.path.exists(path)), None)
        bold_path = next((path for path, _ in bold_candidates if os.path.exists(path)), None)
        if regular_path and bold_path:
            pdfmetrics.registerFont(TTFont("KnowletiveSans", regular_path))
            pdfmetrics.registerFont(TTFont("KnowletiveSansBold", bold_path))
            FONT, FONT_BOLD = "KnowletiveSans", "KnowletiveSansBold"
    except Exception:
        pass

    title_s = ParagraphStyle(
        "ReportTitle",
        fontSize=18,
        fontName=FONT_BOLD,
        textColor=DARK,
        alignment=TA_CENTER,
        leading=22,
    )

    sub_s = ParagraphStyle(
        "ReportSubtitle",
        fontSize=9,
        fontName=FONT,
        textColor=GRAY,
        alignment=TA_CENTER,
        leading=12,
    )

    sec_s = ParagraphStyle(
        "SectionHeading",
        fontSize=13,
        fontName=FONT_BOLD,
        textColor=DARK,
        spaceBefore=8,
        spaceAfter=6,
        leading=17,
        borderColor=PRIMARY,
        borderWidth=0,
    )

    lbl_s = ParagraphStyle(
        "Label",
        fontSize=9,
        fontName=FONT_BOLD,
        textColor=DARK,
        leading=12,
    )

    val_s = ParagraphStyle(
        "Value",
        fontSize=9,
        fontName=FONT,
        textColor=GRAY,
        leading=13,
    )

    sm_s = ParagraphStyle(
        "SmallText",
        fontSize=8,
        fontName=FONT,
        textColor=GRAY,
        leading=11,
    )

    car_s = ParagraphStyle(
        "CareerBanner",
        fontSize=17,
        fontName=FONT_BOLD,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        leading=21,
    )

    rt_s = ParagraphStyle(
        "RightAligned",
        fontSize=9,
        fontName=FONT_BOLD,
        textColor=DARK,
        alignment=TA_RIGHT,
    )

    story = []
    W = A4[0] - 40 * mm

    # -----------------------------------------------------
    # HEADER AND KNOWLETIVE BRANDING
    # -----------------------------------------------------
    logo_candidates = [
        os.getenv("KNOWLETIVE_LOGO_PATH", ""),
        os.path.join(os.path.dirname(__file__), "..", "static", "logo.png"),
        os.path.join(os.path.dirname(__file__), "..", "static", "knowletive-logo.png"),
        os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public", "logo.png"),
        os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "public", "knowletive-logo.png"),
    ]
    logo_path = next((os.path.abspath(path) for path in logo_candidates if path and os.path.exists(path)), "")

    if os.path.exists(logo_path):
        logo = RLImage(
            logo_path,
            width=30 * mm,
            height=16 * mm,
            kind="proportional",
        )

        header = Table(
            [[
                logo,
                Paragraph(
                    "Psychometric Assessment<br/>Career Guidance Report",
                    title_s,
                ),
            ]],
            colWidths=[38 * mm, W - 38 * mm],
        )
    else:
        header = Table(
            [[
                Paragraph("Knowletive", title_s),
                Paragraph(
                    "Psychometric Assessment<br/>Career Guidance Report",
                    title_s,
                ),
            ]],
            colWidths=[W / 2, W / 2],
        )

    header.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
            ("LINEBELOW", (0, 0), (-1, -1), 2, PRIMARY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(header)

    tagline = Table(
        [[
            Paragraph(
                "Knowletive | Training Minds, Placing Talents",
                sub_s,
            )
        ]],
        colWidths=[W],
    )

    tagline.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EFF4FF")),
            ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ])
    )

    story.append(tagline)
    story.append(Spacer(1, 7 * mm))

    # -----------------------------------------------------
    # STUDENT INFORMATION
    # -----------------------------------------------------
    story.append(Paragraph("Student Information", sec_s))
    story.append(
        HRFlowable(
            width=W,
            thickness=1,
            color=PRIMARY,
            spaceAfter=5,
        )
    )

    completed_str = (
        result.completed_at.strftime("%d %B %Y")
        if result.completed_at
        else "Not available"
    )

    def safe_text(value):
        """Escape user/database text before placing it in a Paragraph."""
        return escape(str(value)) if value not in (None, "") else "—"

    info_rows = [
        [
            Paragraph("<b>Name</b>", lbl_s),
            Paragraph(safe_text(current_user.name), val_s),
            Paragraph("<b>Email</b>", lbl_s),
            Paragraph(safe_text(current_user.email), val_s),
        ],
        [
            Paragraph("<b>School</b>", lbl_s),
            Paragraph(safe_text(current_user.school), val_s),
            Paragraph("<b>Class</b>", lbl_s),
            Paragraph(safe_text(current_user.student_class), val_s),
        ],
        [
            Paragraph("<b>Father's Name</b>", lbl_s),
            Paragraph(safe_text(current_user.father_name), val_s),
            Paragraph("<b>Mother's Name</b>", lbl_s),
            Paragraph(safe_text(current_user.mother_name), val_s),
        ],
        [
            Paragraph("<b>Completed On</b>", lbl_s),
            Paragraph(safe_text(completed_str), val_s),
            "",
            "",
        ],
    ]

    info_table = Table(
        info_rows,
        colWidths=[32 * mm, 53 * mm, 32 * mm, 53 * mm],
    )

    info_table.setStyle(
        TableStyle([
            ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, LGRAY]),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.3,
                BORDER,
            ),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )

    story.append(info_table)
    story.append(Spacer(1, 7 * mm))

    # -----------------------------------------------------
    # RECOMMENDED CAREER BANNER
    # -----------------------------------------------------
    top_career = safe_text(result.top_career)

    career_rows = [
        [Paragraph("RECOMMENDED CAREER TO EXPLORE", sub_s)],
        [Paragraph(top_career, car_s)],
        [
            Paragraph(
                "Personality profile: "
                + safe_text(
                    result.personality_clarity
                    or "Moderately Defined"
                ),
                sub_s,
            )
        ],
    ]

    career_table = Table(career_rows, colWidths=[W])

    career_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F6FF")),
            ("BOX", (0, 0), (-1, -1), 0.8, BORDER),
            ("LINEBEFORE", (0, 0), (-1, -1), 3, PRIMARY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(career_table)
    story.append(Spacer(1, 6 * mm))

    # -----------------------------------------------------
    # TOP FIVE CAREER MATCHES
    # -----------------------------------------------------
    if top_5:
        story.append(
            Paragraph(
                "Top 5 Career Matches — Relative Match Scores",
                sec_s,
            )
        )
        story.append(
            HRFlowable(
                width=W,
                thickness=1,
                color=PRIMARY,
                spaceAfter=5,
            )
        )

        score_rows = [[
            Paragraph("<b>Rank</b>", lbl_s),
            Paragraph("<b>Career</b>", lbl_s),
            Paragraph("<b>Relative Score</b>", rt_s),
        ]]

        for index, career in enumerate(top_5, start=1):
            if isinstance(career, dict):
                title = (
                    career.get("title")
                    or career.get("career")
                    or career.get("name")
                    or "Career option"
                )

                try:
                    score = float(career.get("confidence", 0) or 0)
                except (ValueError, TypeError):
                    score = 0.0
            else:
                title = str(career)
                score = 0.0

            score_rows.append([
                Paragraph(f"#{index}", val_s),
                Paragraph(safe_text(title), val_s),
                Paragraph(f"<b>{score:.1f}</b>", rt_s),
            ])

        # -------------------------------------------------
        # VISUAL CAREER-MATCH COMPARISON GRAPH
        # Scores are relative ranking values, not probabilities.
        # -------------------------------------------------
        graph_titles = []
        graph_scores = []

        for career in top_5[:5]:
            if isinstance(career, dict):
                graph_title = (
                    career.get("title")
                    or career.get("career")
                    or career.get("name")
                    or "Career option"
                )
                raw_score = career.get("confidence", 0)
            else:
                graph_title = str(career)
                raw_score = 0

            try:
                graph_score = float(raw_score or 0)
            except (ValueError, TypeError):
                graph_score = 0.0

            graph_titles.append(str(graph_title)[:30])
            graph_scores.append(max(0.0, min(100.0, graph_score)))

        if graph_scores:
            graph_height = max(55 * mm, len(graph_scores) * 13 * mm)
            drawing = Drawing(W, graph_height)

            chart = HorizontalBarChart()
            chart.x = 58 * mm
            chart.y = 7 * mm
            chart.width = W - 65 * mm
            chart.height = graph_height - 14 * mm
            chart.categoryAxis.categoryNames = list(reversed(graph_titles))
            chart.data = [list(reversed(graph_scores))]
            chart.categoryAxis.labels.fontName = FONT
            chart.categoryAxis.labels.fontSize = 7
            chart.categoryAxis.labels.boxAnchor = "e"
            chart.valueAxis.valueMin = 0
            chart.valueAxis.valueMax = 100
            chart.valueAxis.valueStep = 20
            chart.valueAxis.labels.fontName = FONT
            chart.valueAxis.labels.fontSize = 7
            chart.bars[0].fillColor = PRIMARY
            chart.barWidth = 7
            chart.groupSpacing = 5
            drawing.add(chart)

            story.append(Paragraph("Career Match Comparison", lbl_s))
            story.append(drawing)
            story.append(Spacer(1, 4 * mm))

        score_table = Table(
            score_rows,
            colWidths=[18 * mm, 105 * mm, 47 * mm],
            repeatRows=1,
        )

        score_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [WHITE, LGRAY],
                ),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    BORDER,
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )

        story.append(score_table)
        story.append(Spacer(1, 3 * mm))
        story.append(
            Paragraph(
                "Interpretation: Relative scores show the ranking "
                "produced by this assessment's scoring method. "
                "They are not probabilities of career success, "
                "admission, employment, or future performance.",
                sm_s,
            )
        )
        story.append(Spacer(1, 5 * mm))

    # -----------------------------------------------------
    # MULTIPLE INTELLIGENCE SCORES
    # -----------------------------------------------------
    story.append(
        Paragraph(
            "Multiple Intelligence Dimensions",
            sec_s,
        )
    )
    story.append(
        HRFlowable(
            width=W,
            thickness=1,
            color=PRIMARY,
            spaceAfter=5,
        )
    )

    intel_items = [
        ("Logical-Mathematical", result.logical_mathematical or 0),
        ("Interpersonal", result.interpersonal or 0),
        ("Bodily-Kinesthetic", result.bodily_kinesthetic or 0),
        ("Verbal-Linguistic", result.verbal_linguistic or 0),
        ("Musical", result.musical or 0),
        ("Naturalist", result.naturalist or 0),
        ("Spatial-Visual", result.spatial_visual or 0),
        ("Intrapersonal", result.intrapersonal or 0),
    ]

    intel_items.sort(key=lambda item: item[1], reverse=True)

    def get_intelligence_status(score):
        if score >= 75:
            return "Higher relative score", GREEN
        if score >= 60:
            return "Moderately higher", BLUE
        if score >= 45:
            return "Middle range", ORANGE
        return "Lower relative score", RED

    def make_score_bar(score):
        score = max(0, min(100, float(score)))
        filled = max(0.1, score)
        remaining = max(0.1, 100 - score)

        bar = Table(
            [["", ""]],
            colWidths=[
                filled * 0.65 * mm,
                remaining * 0.65 * mm,
            ],
            rowHeights=[4 * mm],
        )

        bar.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (0, 0), PRIMARY),
                ("BACKGROUND", (1, 0), (1, 0), LGRAY),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ])
        )

        return bar

    intel_rows = [[
        Paragraph("<b>Dimension</b>", lbl_s),
        Paragraph("<b>Score Bar</b>", lbl_s),
        Paragraph("<b>Score</b>", rt_s),
        Paragraph("<b>Relative Band</b>", lbl_s),
    ]]

    for name, score in intel_items:
        score = float(score)
        status, status_color = get_intelligence_status(score)

        status_style = ParagraphStyle(
            "IntelligenceStatus",
            fontSize=7.5,
            fontName=FONT_BOLD,
            textColor=status_color,
            leading=10,
        )

        intel_rows.append([
            Paragraph(safe_text(name), val_s),
            make_score_bar(score),
            Paragraph(f"<b>{score:.1f}</b>", rt_s),
            Paragraph(safe_text(status), status_style),
        ])

    intel_table = Table(
        intel_rows,
        colWidths=[43 * mm, 60 * mm, 20 * mm, 47 * mm],
        repeatRows=1,
    )

    intel_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [WHITE, LGRAY],
            ),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.3,
                BORDER,
            ),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )

    story.append(intel_table)
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "These scores describe responses within this assessment. "
            "They should not be treated as a clinical diagnosis or "
            "a complete measurement of a student's ability.",
            sm_s,
        )
    )

    # -----------------------------------------------------
    # RIASEC PERSONALITY / INTEREST PROFILE
    # -----------------------------------------------------
    story.append(Spacer(1, 5 * mm))
    story.append(
        Paragraph(
            "RIASEC Career Interest Profile",
            sec_s,
        )
    )
    story.append(
        HRFlowable(
            width=W,
            thickness=1,
            color=SECONDARY,
            spaceAfter=5,
        )
    )

    riasec_items = [
        ("Realistic", "The Doers", result.riasec_realistic or 0),
        (
            "Investigative",
            "The Thinkers",
            result.riasec_investigative or 0,
        ),
        ("Artistic", "The Creators", result.riasec_artistic or 0),
        ("Social", "The Helpers", result.riasec_social or 0),
        (
            "Enterprising",
            "The Persuaders",
            result.riasec_enterprising or 0,
        ),
        (
            "Conventional",
            "The Organizers",
            result.riasec_conventional or 0,
        ),
    ]

    riasec_items.sort(key=lambda item: item[2], reverse=True)

    def get_riasec_status(score):
        if score > 80:
            return "Higher relative score", colors.HexColor("#be185d")
        if score > 60:
            return "Moderately higher", GREEN
        if score > 40:
            return "Middle range", ORANGE
        return "Lower relative score", GRAY

    riasec_rows = [[
        Paragraph("<b>Interest Type</b>", lbl_s),
        Paragraph("<b>Description</b>", lbl_s),
        Paragraph("<b>Score</b>", rt_s),
        Paragraph("<b>Relative Band</b>", lbl_s),
    ]]

    for name, description, score in riasec_items:
        score = float(score)
        status, status_color = get_riasec_status(score)

        status_style = ParagraphStyle(
            "RIASECStatus",
            fontSize=7.5,
            fontName=FONT_BOLD,
            textColor=status_color,
            leading=10,
        )

        riasec_rows.append([
            Paragraph(f"<b>{safe_text(name)}</b>", lbl_s),
            Paragraph(safe_text(description), val_s),
            Paragraph(f"<b>{score:.1f}</b>", rt_s),
            Paragraph(safe_text(status), status_style),
        ])

    riasec_table = Table(
        riasec_rows,
        colWidths=[37 * mm, 48 * mm, 25 * mm, 60 * mm],
        repeatRows=1,
    )

    riasec_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), SECONDARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [WHITE, LGRAY],
            ),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.3,
                BORDER,
            ),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )

    story.append(riasec_table)
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "RIASEC describes broad work-interest themes. A high "
            "score indicates a stronger relative interest in this "
            "profile within the assessment; it does not determine "
            "which career a student must choose.",
            sm_s,
        )
    )

    # -----------------------------------------------------
    # PERSONALIZED STRENGTHS SUMMARY
    # -----------------------------------------------------
    intelligence_data = {
        "logical_mathematical": result.logical_mathematical or 0,
        "interpersonal": result.interpersonal or 0,
        "bodily_kinesthetic": result.bodily_kinesthetic or 0,
        "verbal_linguistic": result.verbal_linguistic or 0,
        "musical": result.musical or 0,
        "naturalist": result.naturalist or 0,
        "spatial_visual": result.spatial_visual or 0,
        "intrapersonal": result.intrapersonal or 0,
    }

    riasec_data = {
        "realistic": result.riasec_realistic or 0,
        "investigative": result.riasec_investigative or 0,
        "artistic": result.riasec_artistic or 0,
        "social": result.riasec_social or 0,
        "enterprising": result.riasec_enterprising or 0,
        "conventional": result.riasec_conventional or 0,
    }

    strengths = get_strengths(
        intelligence_data,
        riasec_data,
    )

    story.append(PageBreak())
    story.append(
        Paragraph(
            "Personalized Strengths Summary",
            sec_s,
        )
    )

    story.append(
        Paragraph(
            "The dimensions below received the highest scores in "
            "this student's assessment. Use them as starting points "
            "for reflection, skill development, and career exploration. "
            "They are not fixed limits on ability.",
            val_s,
        )
    )
    story.append(Spacer(1, 4 * mm))

    for section_title, key in [
        (
            "Leading Intelligence Dimensions",
            "leading_intelligence_dimensions",
        ),
        (
            "Leading RIASEC Interests",
            "leading_riasec_dimensions",
        ),
    ]:
        story.append(Paragraph(section_title, sec_s))

        items = strengths.get(key, [])

        if not items:
            story.append(
                Paragraph(
                    "No scores are available for this section.",
                    val_s,
                )
            )
        else:
            for item in items:
                name = safe_text(item.get("name"))
                score = float(item.get("score", 0) or 0)

                story.append(
                    Paragraph(
                        f"• <b>{name}</b> — score: {score:.1f}",
                        val_s,
                    )
                )

        story.append(Spacer(1, 4 * mm))

    # -----------------------------------------------------
    # PERSONALIZED CAREER EXPLORATION GUIDE
    # -----------------------------------------------------
    story.append(PageBreak())
    story.append(
        Paragraph(
            "Personalized Career Exploration Guide",
            sec_s,
        )
    )

    story.append(
        Paragraph(
            "The career options below are drawn from this student's "
            "assessment results. Review the day-to-day work, required "
            "qualifications, personal interests, and practical "
            "opportunities before choosing a pathway. The assessment "
            "is one source of guidance, not a final decision.",
            val_s,
        )
    )
    story.append(Spacer(1, 5 * mm))

    # Support dictionary and string representations of career matches.
    career_titles = []

    for career in top_5:
        if isinstance(career, dict):
            title = (
                career.get("title")
                or career.get("career")
                or career.get("name")
                or ""
            )
        else:
            title = str(career)

        title = str(title).strip()

        if title and title not in career_titles:
            career_titles.append(title)

    # Ensure the primary career is included.
    if result.top_career:
        primary_career = str(result.top_career).strip()

        if primary_career and primary_career not in career_titles:
            career_titles.insert(0, primary_career)

    # Generate a section for each of the student's top career matches.
    for index, career_title in enumerate(career_titles[:5], start=1):
        guidance = get_career_guidance(career_title)

        story.append(Spacer(1, 3 * mm))
        career_heading = Table(
            [[Paragraph(
                f"<font color='#2855D9'>CAREER {index:02d}</font><br/>"
                f"{safe_text(guidance.get('career_title') or guidance.get('title') or career_title)}",
                ParagraphStyle(
                    f"CareerHeading{index}", parent=sec_s,
                    fontName=FONT_BOLD, fontSize=15, leading=19,
                    textColor=DARK, spaceBefore=0, spaceAfter=0,
                ),
            )]],
            colWidths=[W],
        )
        career_heading.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F6FF")),
            ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
            ("LINEBEFORE", (0, 0), (-1, -1), 3, PRIMARY),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ]))
        story.append(career_heading)

        story.append(
            Paragraph(
                f"<b>Career field:</b> "
                f"{safe_text(guidance.get('field'))}",
                val_s,
            )
        )

        story.append(Spacer(1, 2 * mm))

        story.append(
            Paragraph(
                safe_text(guidance.get("summary")),
                val_s,
            )
        )
        story.append(Spacer(1, 3 * mm))

        # Visual career roadmap: use this career's own pathway items where available.
        roadmap_items = guidance.get("pathways", []) or []
        if isinstance(roadmap_items, str):
            roadmap_items = [roadmap_items]
        roadmap_items = [str(item).strip() for item in roadmap_items if str(item).strip()][:3]
        if roadmap_items:
            roadmap_cells = []
            for step_index, roadmap_item in enumerate(roadmap_items, start=1):
                roadmap_cells.append(Paragraph(
                    f"<font color='#2855D9'><b>STEP {step_index}</b></font><br/>{safe_text(roadmap_item)}",
                    ParagraphStyle(
                        f"RoadmapStep{index}_{step_index}", parent=val_s,
                        fontName=FONT, fontSize=7.5, leading=10,
                        textColor=GRAY,
                    ),
                ))
            roadmap_table = Table([roadmap_cells], colWidths=[W / len(roadmap_cells)] * len(roadmap_cells))
            roadmap_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F6FF")),
                ("BOX", (0, 0), (-1, -1), 0.6, BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            story.append(Paragraph("CAREER ROADMAP", lbl_s))
            story.append(roadmap_table)
            story.append(Spacer(1, 3 * mm))

        guidance_sections = [
            ("Skills to Develop", "skills"),
            ("Technologies and Tools", "technologies"),
            ("Portfolio Project Ideas", "projects"),
            ("Suggested Learning Pathway", "pathways"),
            ("Possible Related Roles", "roles"),
            ("India Salary Guidance", "indicative_salary_india"),
            ("Education and Training Cost Guidance", "education_cost_india"),
            ("Future Outlook", "future_outlook"),
            ("Recommended Next Steps", "recommended_next_steps"),
        ]

        for label, key in guidance_sections:
            items = guidance.get(key, [])

            if isinstance(items, str):
                items = [items]
            elif items is None:
                items = []

            if not items:
                continue

            story.append(
                Paragraph(f"<b>{label}</b>", lbl_s)
            )

            for item in items:
                story.append(
                    Paragraph(
                        f"<font color='#2855D9'>●</font>  {safe_text(item)}",
                        val_s,
                    )
                )

            story.append(Spacer(1, 2 * mm))

        if guidance.get("catalogue_status") in {
            "needs_career_specific_research",
            "domain_specific_profile_needs_current_source_verification",
        }:
            story.append(
                Paragraph(
                    "<i>This is exploratory career guidance, not a guarantee. "
                    "Verify current eligibility, accreditation, licensing, fees, "
                    "salary data and recruitment rules with official or current sources.</i>",
                    sm_s,
                )
            )

        # Separate career options to make the report easier to read.
        if index < min(len(career_titles), 5):
            story.append(PageBreak())

    if not career_titles:
        story.append(
            Paragraph(
                "No career matches are currently available. "
                "Please complete the assessment again or contact "
                "the administrator to review the saved result.",
                val_s,
            )
        )

    # -----------------------------------------------------
    # FINAL GUIDANCE AND DISCLAIMER
    # -----------------------------------------------------
    story.append(PageBreak())
    story.append(
        Paragraph(
            "How to Use This Report",
            sec_s,
        )
    )

    next_steps = [
        "Reflect on which suggested careers genuinely interest you.",
        "Research the qualifications and entrance requirements for "
        "each career you are considering.",
        "Compare course duration, curriculum, total fees, and "
        "available financial support directly with recognised "
        "institutions.",
        "Try a beginner project, workshop, club, internship, or "
        "conversation with a professional in the field.",
        "Discuss major education and career decisions with trusted "
        "parents, teachers, mentors, or qualified career counsellors.",
        "Revisit your plan as your interests, skills, and circumstances "
        "change.",
    ]

    for step_number, step in enumerate(next_steps, start=1):
        story.append(
            Paragraph(
                f"{step_number}. {safe_text(step)}",
                val_s,
            )
        )
        story.append(Spacer(1, 2 * mm))

    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Important Disclaimer",
            sec_s,
        )
    )

    story.append(
        Paragraph(
            "This report provides educational career-exploration "
            "guidance based on recorded assessment scores. It is not "
            "a clinical or psychological diagnosis, an IQ certificate, "
            "an admission prediction, or a guarantee of employment "
            "or career success. Relative match scores are outputs of "
            "the application's scoring method and should not be "
            "interpreted as probabilities. Course fees, qualifications, "
            "and employment requirements can change and must be verified "
            "with the relevant institutions or official sources.",
            sm_s,
        )
    )

    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------
    story.append(Spacer(1, 8 * mm))

    footer = Table(
        [[
            Paragraph(
                "© Knowletive — Training Minds, Placing Talents",
                sm_s,
            ),
            Paragraph(
                "Confidential Student Report",
                ParagraphStyle(
                    "FooterRight",
                    fontSize=8,
                    fontName=FONT,
                    textColor=GRAY,
                    alignment=TA_RIGHT,
                ),
            ),
        ]],
        colWidths=[W / 2, W / 2],
    )

    footer.setStyle(
        TableStyle([
            (
                "LINEABOVE",
                (0, 0),
                (-1, -1),
                0.5,
                BORDER,
            ),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )

    story.append(footer)

    # -----------------------------------------------------
    # PAGE DESIGN: WATERMARK, RUNNING HEADER AND PAGE FOOTER
    # -----------------------------------------------------
    def draw_page(canvas, document):
        """Draw a subtle Knowletive watermark and consistent page footer."""
        canvas.saveState()

        # Light diagonal watermark behind the page content.
        canvas.setFillColor(colors.HexColor("#F7F9FD"))
        canvas.translate(A4[0] / 2, A4[1] / 2)
        canvas.rotate(35)
        canvas.setFont(FONT_BOLD, 38)
        canvas.drawCentredString(0, 0, "KNOWLETIVE")
        canvas.restoreState()

        # Footer line, company label and page number.
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#DCE3EF"))
        canvas.setLineWidth(0.8)
        canvas.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
        canvas.setStrokeColor(PRIMARY)
        canvas.setLineWidth(2)
        canvas.line(20 * mm, 14 * mm, 42 * mm, 14 * mm)
        canvas.setFillColor(GRAY)
        canvas.setFont(FONT, 7)
        canvas.drawString(20 * mm, 9 * mm, "Knowletive | Career Guidance")
        canvas.drawRightString(A4[0] - 20 * mm, 9 * mm, f"Page {document.page}")
        canvas.restoreState()

    # -----------------------------------------------------
    # BUILD PDF AND RETURN DOWNLOAD
    # -----------------------------------------------------
    try:
        doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)
    except Exception as exc:
        # Log the full error in the backend terminal.
        import logging
        logging.exception("Failed to generate the psychometric PDF")

        raise HTTPException(
            status_code=500,
            detail="The PDF could not be generated. Check the backend logs.",
        ) from exc

    buffer.seek(0)

    safe_filename = "".join(
        character
        if character.isalnum() or character in ("-", "_")
        else "_"
        for character in (current_user.name or "student")
    )

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": (
                f'attachment; filename="psychometric_report_'
                f'{safe_filename}.pdf"'
            )
        },
    )
