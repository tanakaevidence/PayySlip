import pandas as pd
from fpdf import FPDF
import yagmail
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve email credentials from the environment variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Step 1: Simulated Employee Data
employee_data = {
    'Name': ['Evidence Murima', 'Wayne Benhure', 'Vincent Mugondora'],
    'Employee ID': ['E123', 'E124', 'E125'],
    'Email': ['evidencetanakamurima40@gmail.com', 'wayn@uncommon.com', 'vincent@uncommon.org'],
    'Basic Salary': [5000, 6000, 5500],
    'Allowances': [500, 600, 450],
    'Deductions': [200, 250, 300],
}

# Calculate Net Salary
employee_data['Net Salary'] = [
    employee_data['Basic Salary'][i] + employee_data['Allowances'][i] - employee_data['Deductions'][i]
    for i in range(len(employee_data['Name']))
]
employees_df = pd.DataFrame(employee_data)

# Step 2: Generate Payslip PDF
def generate_payslip_pdf(employee):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f"Payslip for {employee['Name']}", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Name        : {employee['Name']}", ln=True)
    pdf.cell(200, 10, f"Employee ID : {employee['Employee ID']}", ln=True)
    pdf.cell(200, 10, f"Email       : {employee['Email']}", ln=True)
    pdf.cell(200, 10, f"Basic Salary: ${employee['Basic Salary']:.2f}", ln=True)
    pdf.cell(200, 10, f"Allowances  : ${employee['Allowances']:.2f}", ln=True)
    pdf.cell(200, 10, f"Deductions  : ${employee['Deductions']:.2f}", ln=True)
    pdf.cell(200, 10, f"Net Salary  : ${employee['Net Salary']:.2f}", ln=True)

    filename = f"Payslip_{employee['Name'].replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

# Step 3: Send Email Using Yagmail
def send_email(receiver_email, name, attachment):
    yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASS)

    subject = "Your End of Month Payslip"
    body = f"Hello {name},\n\nPlease find your attached payslip for the month.\n\nRegards,\nHR Team"

    yag.send(
        to=receiver_email,
        subject=subject,
        contents=body,
        attachments=attachment
    )

    print(f"✅ Email sent to {name} ({receiver_email})")

# Step 4: Loop Through Each Employee
for index, row in employees_df.iterrows():
    employee = row.to_dict()
    payslip_filename = generate_payslip_pdf(employee)
    print(f"📄 Payslip PDF generated: {payslip_filename}")
    send_email(employee['Email'], employee['Name'], payslip_filename)

