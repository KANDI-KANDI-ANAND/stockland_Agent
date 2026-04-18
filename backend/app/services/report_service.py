import os
import uuid

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor


class ReportService:

    @staticmethod
    def generate_pdf(report_text):

        os.makedirs("reports", exist_ok=True)

        filename = f"reports/report_{uuid.uuid4()}.pdf"

        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=1*inch,
            leftMargin=1*inch,
            topMargin=1*inch,
            bottomMargin=1*inch
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "Title",
            parent=styles["Title"],
            textColor=HexColor("#1F4E79"),
            spaceAfter=20
        )

        heading_style = ParagraphStyle(
            "Heading",
            parent=styles["Heading2"],
            textColor=HexColor("#2E74B5"),
            spaceAfter=10
        )

        body_style = ParagraphStyle(
            "Body",
            parent=styles["BodyText"],
            fontSize=11,
            leading=16,
            spaceAfter=8
        )

        elements = []

        lines = report_text.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if line.startswith("**") and line.endswith("**"):

                clean = line.replace("**", "")
                elements.append(Paragraph(clean, heading_style))
                elements.append(Spacer(1, 12))

            elif line.startswith("Community Report"):

                elements.append(Paragraph(line, title_style))
                elements.append(Spacer(1, 20))

            else:
                elements.append(Paragraph(line, body_style))

        doc.build(elements)

        return filename