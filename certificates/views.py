from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from accounts.decorators import role_required
from .models import Certificate
from .services import sync_student_certificates


@role_required('student')
def certificate_list(request):
    sync_student_certificates(request.user)
    return render(request, 'certificates/list.html', {
        'certificates': Certificate.objects.filter(
            student=request.user
        ).select_related('topic__subject'),
    })


def certificate_verify(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related('student', 'topic__subject'),
        certificate_id=certificate_id,
    )
    return render(
        request,
        'certificates/verify.html',
        {'certificate': certificate},
    )


def centered_text(pdf, text, y, font, size, color, width=842):
    pdf.setFillColor(color)
    pdf.setFont(font, size)
    pdf.drawCentredString(width / 2, y, text)


def fitted_size(text, font, preferred, maximum_width, minimum=9):
    size = preferred
    while size > minimum and stringWidth(text, font, size) > maximum_width:
        size -= 0.5
    return size


def draw_graduation_cap(pdf, x, y, scale, color):
    """Draw a simple graduation cap without external image files."""
    pdf.saveState()
    pdf.translate(x, y)
    pdf.scale(scale, scale)
    pdf.setFillColor(color)
    pdf.setStrokeColor(color)

    cap = pdf.beginPath()
    cap.moveTo(-75, 0)
    cap.lineTo(0, 34)
    cap.lineTo(75, 0)
    cap.lineTo(0, -34)
    cap.close()
    pdf.drawPath(cap, fill=1, stroke=0)

    base = pdf.beginPath()
    base.moveTo(-43, -18)
    base.lineTo(-43, -52)
    base.curveTo(-18, -70, 18, -70, 43, -52)
    base.lineTo(43, -18)
    base.lineTo(0, -39)
    base.close()
    pdf.drawPath(base, fill=1, stroke=0)

    pdf.setLineWidth(2)
    pdf.line(59, -7, 59, -53)
    pdf.circle(59, -55, 3, fill=1, stroke=0)
    pdf.restoreState()


def draw_qr(pdf, url, x, y, size=70):
    qr = QrCodeWidget(url)
    x1, y1, x2, y2 = qr.getBounds()

    drawing = Drawing(
        size,
        size,
        transform=[
            size / (x2 - x1),
            0,
            0,
            size / (y2 - y1),
            0,
            0,
        ],
    )
    drawing.add(qr)
    renderPDF.draw(drawing, pdf, x, y)


@role_required('student')
def certificate_pdf(request, certificate_id):
    certificate = get_object_or_404(
        Certificate.objects.select_related('student', 'topic__subject'),
        certificate_id=certificate_id,
        student=request.user,
    )

    buffer = BytesIO()
    width, height = 842, 595

    pdf = canvas.Canvas(buffer, pagesize=(width, height))

    black = HexColor('#201D1A')
    gold = HexColor('#B9893F')
    light_gold = HexColor('#E6C98D')
    cream = HexColor('#FFFCF5')
    pale_gold = HexColor('#FFF3DB')
    muted = HexColor('#65594C')

    # Background
    pdf.setFillColor(cream)
    pdf.rect(0, 0, width, height, fill=1, stroke=0)

    # Header: PrepX branding
    logo = Path(settings.BASE_DIR) / 'static' / 'images' / 'prepx-logo.png'

    if logo.is_file():
        pdf.drawImage(
            ImageReader(str(logo)),
            47, 519, 44, 44,
            preserveAspectRatio=True,
            mask='auto',
        )

    pdf.setFillColor(black)
    pdf.setFont('Times-Bold', 27)
    pdf.drawString(101, 535, 'Prep')

    pdf.setFillColor(gold)
    pdf.drawString(157, 535, 'X')

    pdf.setFillColor(muted)
    pdf.setFont('Helvetica', 7)
    pdf.drawString(102, 521, 'EXAM & LEARNING WORKSPACE')

    pdf.setFillColor(black)
    pdf.setFont('Helvetica', 8)
    pdf.drawRightString(
        795, 546,
        'PRACTICE  |  LEARN  |  IMPROVE  |  ACHIEVE',
    )

    # Faint graduation-cap watermark
    pdf.saveState()
    watermark_color = HexColor('#F7EEDC')
    draw_graduation_cap(
        pdf, 126, 299, 1.15, watermark_color
    )
    pdf.restoreState()

    # Small academic symbol above heading
    draw_graduation_cap(pdf, width / 2, 487, 0.27, gold)

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(0.7)
    pdf.line(314, 486, 387, 486)
    pdf.line(455, 486, 528, 486)

    # Main heading
    centered_text(
        pdf, 'CERTIFICATE', 440,
        'Times-Bold', 37, black
    )
    centered_text(
        pdf, 'OF COMPLETION', 399,
        'Times-Bold', 36, gold
    )

    pdf.setStrokeColor(gold)
    pdf.setLineWidth(0.7)
    pdf.line(290, 383, 552, 383)

    centered_text(
        pdf, 'T H I S   I S   P R O U D L Y   P R E S E N T E D   T O',
        364, 'Helvetica', 8.5, muted
    )

    # Student name
    name = (
        certificate.student.get_full_name().strip()
        or certificate.student.username
    )[:75]

    name_size = fitted_size(
        name, 'Times-Bold', 34, 570, minimum=12
    )

    centered_text(
        pdf, name, 325,
        'Times-Bold', name_size, black
    )

    centered_text(
        pdf,
        'for successfully completing all ten practice tests in the topic',
        294, 'Times-Roman', 12, black
    )

    # Topic highlight
    pdf.setFillColor(pale_gold)
    pdf.setStrokeColor(light_gold)
    pdf.setLineWidth(0.9)
    pdf.roundRect(
        258, 246, 326, 37,
        5, fill=1, stroke=1
    )

    topic_name = certificate.topic.name[:85]
    topic_size = fitted_size(
        topic_name, 'Times-Bold', 23, 305, minimum=10
    )

    centered_text(
        pdf, topic_name, 257,
        'Times-Bold', topic_size, black
    )

    subject_text = (
        'Subject: ' + certificate.topic.subject.name
    )[:100]

    subject_size = fitted_size(
        subject_text, 'Times-Bold', 13, 550, minimum=9
    )

    centered_text(
        pdf, subject_text, 226,
        'Times-Bold', subject_size, black
    )

    centered_text(
        pdf,
        'This certificate recognizes your consistent effort and',
        205, 'Times-Roman', 11, muted
    )
    centered_text(
        pdf,
        'commitment to improving your skills with PrepX.',
        189, 'Times-Roman', 11, muted
    )

    # Bottom information
    pdf.setStrokeColor(light_gold)
    pdf.setLineWidth(0.7)
    pdf.line(244, 85, 244, 148)
    pdf.line(550, 85, 550, 148)

    completed_date = timezone.localtime(
        certificate.completed_at
    ).strftime('%d %B %Y')

    pdf.setFillColor(gold)
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(48, 137, 'COMPLETED ON')

    pdf.setFillColor(black)
    pdf.setFont('Times-Roman', 12)
    pdf.drawString(48, 118, completed_date)

    pdf.setFillColor(gold)
    pdf.setFont('Helvetica-Bold', 9)
    pdf.drawString(260, 137, 'CERTIFICATE ID')

    certificate_code = str(
        certificate.certificate_id
    ).upper()

    id_size = fitted_size(
        certificate_code, 'Helvetica', 9, 278, minimum=7
    )

    pdf.setFillColor(black)
    pdf.setFont('Helvetica', id_size)
    pdf.drawString(260, 118, certificate_code)

    # Real verification URL and scannable QR
    verify_url = request.build_absolute_uri(
        reverse(
            'certificate_verify',
            args=[certificate.certificate_id],
        )
    )

    pdf.setFillColor(black)
    pdf.setFont('Times-Bold', 12)
    pdf.drawString(562, 141, 'Verify Certificate')

    pdf.setFillColor(muted)
    pdf.setFont('Helvetica', 8)
    pdf.drawString(562, 127, 'Scan QR or visit:')

    pdf.setFillColor(gold)
    pdf.setFont('Helvetica', 7.5)

    host = request.get_host()
    pdf.drawString(562, 114, host)
    pdf.drawString(562, 103, '/certificates/verify/')
    pdf.setFont('Helvetica', 6.5)
    pdf.drawString(562, 92, str(certificate.certificate_id))

    draw_qr(pdf, verify_url, 731, 89, 68)

    # Footer motto
    pdf.setStrokeColor(gold)
    pdf.line(302, 54, 388, 54)
    pdf.line(454, 54, 540, 54)

    centered_text(
        pdf,
        'K N O W L E D G E   T O D A Y'
        '    •    '
        'B R I G H T E R   T O M O R R O W',
        35, 'Helvetica', 7, muted
    )

    pdf.setTitle('PrepX Certificate of Completion')
    pdf.setAuthor('PrepX')
    pdf.showPage()
    pdf.save()

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/pdf',
    )
    response['Content-Disposition'] = (
        f'attachment; filename="PrepX-Certificate-'
        f'{certificate.certificate_id}.pdf"'
    )
    return response
