from fpdf import FPDF
import tempfile
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(SCRIPT_DIR, "DejaVuSans.ttf")

def export_quiz_to_pdf(blanks, mcqs, score=None, total=None):
    pdf = FPDF()
    pdf.add_page()

    if not os.path.isfile(FONT_PATH):
        return fallback_pdf_with_message(
            "Font file 'DejaVuSans.ttf' not found.\n"
            "Please place it in the same folder as this script to support Unicode characters."
        )

    pdf.add_font("DejaVu", "", FONT_PATH, uni=True)
    pdf.set_font("DejaVu", size=14)
    pdf.cell(0, 10, txt="Quiz Report", ln=True, align="C")
    pdf.ln(5)

    if score is not None and total is not None:
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, txt=f"Score: {score} / {total}", ln=True)
        pdf.ln(5)

    if blanks:
        pdf.set_font("DejaVu",  size=12)
        pdf.cell(0, 10, txt="Fill in the Blanks", ln=True)
        pdf.set_font("DejaVu", size=11)
        for i, item in enumerate(blanks, 1):
            if len(item) == 3:
                q, correct, user = item
                pdf.multi_cell(0, 8, txt=f"{i}. {q}")
                pdf.multi_cell(0, 8, txt=f"   Your Answer: {user}")
                pdf.multi_cell(0, 8, txt=f"   Correct Answer: {correct}")
            else:
                q, correct = item
                pdf.multi_cell(0, 8, txt=f"{i}. {q} (Answer: {correct})")
            pdf.ln(1)

    if mcqs:
        pdf.ln(5)
        pdf.set_font("DejaVu", size=12)
        pdf.cell(0, 10, txt="Multiple Choice Questions", ln=True)
        pdf.set_font("DejaVu", size=11)
        for i, item in enumerate(mcqs, 1):
            if len(item) == 4:
                q, correct, opts, user = item
            else:
                q, correct, opts = item
                user = None

            pdf.multi_cell(0, 8, txt=f"{i}. {q}")
            for label, val in opts.items():
                prefix = "✓" if val == correct else " "
                pdf.cell(0, 8, txt=f"   {label}. {val} {prefix}", ln=True)
            if user:
                pdf.multi_cell(0, 8, txt=f"   Your Answer: {user}")
                pdf.multi_cell(0, 8, txt=f"   Correct Answer: {correct}")
            else:
                pdf.cell(0, 8, txt=f"   Answer: {correct}", ln=True)
            pdf.ln(1)

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name


def fallback_pdf_with_message(message):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    safe_message = message.encode("ascii", "ignore").decode("ascii")
    pdf.multi_cell(0, 10, txt=safe_message)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name
