from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = "sample-condition-report.pdf"


BRAND = colors.HexColor("#126F68")
ORANGE = colors.HexColor("#D86032")
INK = colors.HexColor("#17202A")
MUTED = colors.HexColor("#687381")
LINE = colors.HexColor("#DDE3EA")
SOFT = colors.HexColor("#F5F7FA")
PALE_GREEN = colors.HexColor("#EDF5F4")
PALE_ORANGE = colors.HexColor("#FFF0E9")
BLUE = colors.HexColor("#326FD1")


class PhotoPlaceholder(Flowable):
    def __init__(self, width, height, label, detail, fill):
        super().__init__()
        self.width = width
        self.height = height
        self.label = label
        self.detail = detail
        self.fill = fill

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFillColor(self.fill)
        canvas.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)
        canvas.setStrokeColor(colors.white)
        canvas.setLineWidth(1.5)
        canvas.line(12, 18, self.width - 12, self.height - 20)
        canvas.line(22, 42, 70, 72)
        canvas.line(70, 72, 112, 38)
        canvas.setFillColor(colors.white)
        canvas.circle(self.width - 28, self.height - 28, 10, fill=1, stroke=0)
        canvas.setFillColor(INK)
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(12, 10, self.label)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawRightString(self.width - 12, 10, self.detail)
        canvas.restoreState()


def make_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=27,
            leading=31,
            textColor=INK,
            alignment=TA_LEFT,
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=MUTED,
            spaceAfter=12,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=INK,
            spaceBefore=10,
            spaceAfter=8,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=INK,
            spaceBefore=5,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=colors.HexColor("#2F3A46"),
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=MUTED,
        ),
        "badge": ParagraphStyle(
            "Badge",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,
            textColor=ORANGE,
            alignment=TA_CENTER,
        ),
        "center": ParagraphStyle(
            "Center",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=MUTED,
            alignment=TA_CENTER,
        ),
    }


def badge(text, style):
    table = Table([[Paragraph(text, style["badge"])]], colWidths=[28 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_ORANGE),
                ("BOX", (0, 0), (-1, -1), 0.25, colors.HexColor("#F4D0C2")),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def section_box(title, text, source, confidence, style, accent=BRAND):
    content = [
        [
            Paragraph(f"<b>{title}</b>", style["body"]),
            badge("AI FILLED", style),
        ],
        [Paragraph(text, style["body"]), ""],
        [
            Paragraph(source, style["small"]),
            Paragraph(confidence, style["small"]),
        ],
    ]
    table = Table(content, colWidths=[128 * mm, 32 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("LINEBEFORE", (0, 0), (0, -1), 3, accent),
                ("SPAN", (0, 1), (1, 1)),
                ("BACKGROUND", (0, 2), (-1, 2), SOFT),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 16 * mm, 192 * mm, 16 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 10 * mm, "Generated by SurveyAI Report Demo")
    canvas.drawRightString(192 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    style = make_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=20 * mm,
        title="Sample Residential Condition Report",
        author="SurveyAI Report Demo",
    )

    story = []

    header = Table(
        [
            [
                Paragraph("SurveyAI", ParagraphStyle("Logo", fontName="Helvetica-Bold", fontSize=16, textColor=BRAND)),
                Paragraph("Sample report", style["small"]),
            ]
        ],
        colWidths=[120 * mm, 50 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(header)
    story.append(Paragraph("Residential Condition Report", style["title"]))
    story.append(
        Paragraph(
            "AI-populated draft created from a recorded property walkthrough, live transcript, site notes and photo evidence. Prepared for customer demonstration purposes.",
            style["subtitle"],
        )
    )

    project_info = [
        ["Property", "42 Park Lane, London"],
        ["Report type", "Residential Condition Report"],
        ["Survey date", "5 June 2026"],
        ["Prepared for", "Acme Property Services"],
        ["Surveyor", "Zain Malik"],
        ["AI input sources", "Audio transcript, room notes, photo evidence"],
    ]
    table = Table(project_info, colWidths=[42 * mm, 118 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
                ("BACKGROUND", (0, 0), (0, -1), PALE_GREEN),
                ("TEXTCOLOR", (0, 0), (0, -1), BRAND),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEADING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 8 * mm))

    story.append(
        section_box(
            "Executive summary",
            "The property is generally well presented internally. No significant structural cracking was observed from the recorded walkthrough. Minor maintenance items were identified in the kitchen and bathroom, both suitable for routine follow-up rather than immediate urgent action.",
            "Sources: 4 transcript excerpts",
            "High confidence",
            style,
        )
    )
    story.append(Spacer(1, 4 * mm))
    story.append(
        section_box(
            "Key defects and maintenance",
            "Kitchen: minor staining near the rear window reveal, likely condensation. Bathroom: extractor fan is noisy and should be checked. Living room and bedrooms appear in good decorative order from the available notes.",
            "Sources: audio + photo slots",
            "Needs photo check",
            style,
            accent=ORANGE,
        )
    )

    story.append(Paragraph("Room-by-room findings", style["h2"]))
    room_rows = [
        ["Room", "Observed condition", "AI action"],
        ["Kitchen", "Minor staining near rear window reveal. No further kitchen defects recorded.", "Monitor and add photo evidence."],
        ["Bathroom", "Extractor fan reported as noisy during survey recording.", "Recommend service check."],
        ["Living room", "Generally well presented. No significant visible cracking mentioned.", "No action."],
        ["Bedrooms", "Good decorative order from walkthrough notes.", "No action."],
    ]
    room_table = Table(room_rows, colWidths=[30 * mm, 90 * mm, 40 * mm])
    room_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.4),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT]),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(room_table)

    story.append(Paragraph("Evidence gallery", style["h2"]))
    photos = Table(
        [
            [
                PhotoPlaceholder(50 * mm, 36 * mm, "Kitchen window", "Photo slot 01", colors.HexColor("#DCE7E6")),
                PhotoPlaceholder(50 * mm, 36 * mm, "Bathroom fan", "Photo slot 02", colors.HexColor("#E8E0D8")),
                PhotoPlaceholder(50 * mm, 36 * mm, "Living room", "Photo slot 03", colors.HexColor("#DDE5F2")),
            ]
        ],
        colWidths=[53 * mm, 53 * mm, 53 * mm],
    )
    photos.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(photos)
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "Photo placeholders demonstrate where captured site images would be automatically linked to the relevant room and defect sections.",
            style["small"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("AI audit trail", style["title"]))
    story.append(
        Paragraph(
            "The report keeps the surveyor in control by showing what the AI used, what it inferred, and what still needs review before issue to the client.",
            style["subtitle"],
        )
    )

    audit_rows = [
        ["Template block", "AI instruction", "Status"],
        ["Executive summary", "Summarise overall condition in professional surveyor tone.", "Accepted draft"],
        ["Room findings", "Extract room names, condition, defects and urgency from audio.", "Review required"],
        ["Defects list", "Prioritise observed defects and recommend next actions.", "Needs photo"],
        ["Evidence gallery", "Attach photos to matching issues and rooms.", "Pending images"],
    ]
    audit = Table(audit_rows, colWidths=[38 * mm, 88 * mm, 34 * mm])
    audit.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BRAND),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("GRID", (0, 0), (-1, -1), 0.25, LINE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, SOFT]),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(audit)
    story.append(Spacer(1, 8 * mm))

    transcript = [
        "Kitchen has minor staining near the rear window, likely condensation rather than penetrating damp.",
        "Bathroom extractor fan is noisy and should be checked during routine maintenance.",
        "Living room and bedrooms are generally well presented with no significant visible cracking.",
        "Recommend monitoring the kitchen window reveal and adding photographic evidence to the defects section.",
    ]
    story.append(Paragraph("Transcript excerpts used", style["h2"]))
    for item in transcript:
        excerpt = Table([[Paragraph(item, style["body"])]], colWidths=[160 * mm])
        excerpt.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.white),
                    ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                    ("LINEBEFORE", (0, 0), (0, -1), 3, BLUE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )
        story.append(excerpt)
        story.append(Spacer(1, 2.2 * mm))

    story.append(Spacer(1, 5 * mm))
    signoff = Table(
        [
            [Paragraph("<b>Surveyor approval</b>", style["body"]), Paragraph("<b>Client issue</b>", style["body"])],
            [Paragraph("Reviewed and approved by: ____________________", style["small"]), Paragraph("Issued to: ____________________", style["small"])],
            [Paragraph("Date: ____________________", style["small"]), Paragraph("Date: ____________________", style["small"])],
        ],
        colWidths=[80 * mm, 80 * mm],
    )
    signoff.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, LINE),
                ("BACKGROUND", (0, 0), (-1, 0), PALE_GREEN),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    story.append(signoff)

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_pdf()
