from django.shortcuts import render, redirect
from .models import NSSVolunteer, Donor
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from io import BytesIO

# Home page where NSS Volunteers can select their name
def home(request):
    volunteers = NSSVolunteer.objects.all()
    if request.method == 'POST':
        selected_volunteer = request.POST.get('volunteer')
        return redirect('submit_donor', volunteer_id=selected_volunteer)
    return render(request, 'donor/home.html', {'volunteers': volunteers})

# Donor submission page
def submit_donor(request, volunteer_id):
    volunteer = NSSVolunteer.objects.get(id=volunteer_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        blood_group = request.POST.get('blood_group')
        donor = Donor.objects.create(
            volunteer=volunteer,
            name=name,
            address=address,
            phone_number=phone_number,
            blood_group=blood_group
        )
        donor.save()
        return redirect('home')
    return render(request, 'donor/submit_donor.html', {'volunteer': volunteer})

# Final report generation
def generate_report(request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph("Donor List", styles['Title'])
    elements.append(title)

    # Spacer between the title and the table
    elements.append(Spacer(1, 20))

    # Data for the table with Serial Number
    donors = Donor.objects.all()
    data = [["Sl. No.", "Name", "Address", "Phone Number", "Blood Group"]]  # Table headers

    # Populate the table rows with donor data
    for idx, donor in enumerate(donors, start=1):
        data.append([idx, donor.name, donor.address, donor.phone_number, donor.blood_group])

    # Adjust column widths to allow room for long names and addresses
    col_widths = [40, 120, 200, 100, 80]  # Adjusted widths for better fitting

    # Create the table with the adjusted column widths
    table = Table(data, colWidths=col_widths)

    # Define the table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # No background color for header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # Thin grid lines
        ('SIZE', (0, 0), (-1, -1), 10),  # Font size adjustment
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Vertical alignment
    ])

    # Set the style for the table
    table.setStyle(style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    doc.build(elements)

    # Move to the beginning of the buffer and return the PDF as an HTTP response
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
