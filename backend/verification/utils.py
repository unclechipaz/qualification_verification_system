import os
import io
import qrcode
from PIL import Image as PILImage
from django.core.files.base import ContentFile
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_certificate_qr_code(certificate, request=None):
    """Generate a QR code image for a certificate pointing to the verification URL."""
    if request:
        base_url = request.build_absolute_uri('/')[:-1]
    else:
        base_url = "http://localhost:8000"
        
    verify_url = f"{base_url}/verify/?code={certificate.verification_code}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(verify_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#002B49", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    
    filename = f"qr_{certificate.certificate_number}.png"
    certificate.qr_code_image.save(filename, ContentFile(buffer.getvalue()), save=True)
    return certificate.qr_code_image.url

def generate_verification_pdf_report(verification_log, certificate=None):
    """Generate printable PDF Verification Report using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        textColor=colors.HexColor('#002B49'),
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'SubTitleStyle',
        parent=styles['Heading2'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.HexColor('#D4AF37'),
        alignment=1,
        spaceAfter=25
    )
    
    label_style = ParagraphStyle('LabelStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#002B49'))
    val_style = ParagraphStyle('ValStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.black)
    
    elements = []
    
    # Title Header
    elements.append(Paragraph("MIDLANDS STATE UNIVERSITY", title_style))
    elements.append(Paragraph("OFFICIAL QUALIFICATION VERIFICATION REPORT", subtitle_style))
    elements.append(Spacer(1, 10))
    
    status = verification_log.result_status
    status_color = colors.HexColor('#198754') if status == 'VERIFIED' else colors.HexColor('#DC3545')
    
    status_style = ParagraphStyle(
        'StatusStyle',
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=status_color,
        alignment=1
    )
    elements.append(Paragraph(f"VERIFICATION STATUS: {status}", status_style))
    elements.append(Spacer(1, 15))
    
    if certificate and certificate.student:
        student = certificate.student
        data = [
            [Paragraph("Certificate Number:", label_style), Paragraph(certificate.certificate_number, val_style)],
            [Paragraph("Verification Code:", label_style), Paragraph(certificate.verification_code, val_style)],
            [Paragraph("Student Name:", label_style), Paragraph(student.full_name, val_style)],
            [Paragraph("Student Number:", label_style), Paragraph(student.student_number, val_style)],
            [Paragraph("National ID:", label_style), Paragraph(student.national_id, val_style)],
            [Paragraph("Programme:", label_style), Paragraph(student.programme, val_style)],
            [Paragraph("Faculty:", label_style), Paragraph(student.faculty, val_style)],
            [Paragraph("Qualification Awarded:", label_style), Paragraph(student.qualification, val_style)],
            [Paragraph("Degree Classification:", label_style), Paragraph(student.degree_classification, val_style)],
            [Paragraph("Graduation Date:", label_style), Paragraph(str(student.graduation_date), val_style)],
            [Paragraph("Digital Signature Hash:", label_style), Paragraph(certificate.digital_signature_hash[:32] + "...", val_style)],
            [Paragraph("Verification Timestamp:", label_style), Paragraph(verification_log.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), val_style)],
        ]
        
        t = Table(data, colWidths=[180, 320])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8F9FA')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#DEE2E6')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph(f"No valid student qualification record matching query '{verification_log.search_query}'.", val_style))
        
    elements.append(Spacer(1, 30))
    
    footer_text = "This document is an automated, tamper-evident verification statement issued by Midlands State University Qualifications Registry."
    footer_style = ParagraphStyle('Footer', parent=styles['Italic'], fontSize=8, textColor=colors.gray, alignment=1)
    elements.append(Paragraph(footer_text, footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
