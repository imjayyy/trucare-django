


from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import json
from io import BytesIO
from .prescriptionPdf import build_soap_notes_section, generate_doctors_info_for_medication, visit_summary_section
from prescription.models import Soap_notes 

class IntakePDFBuilder:
    """Generate professional PDF from intake data with minimal, maintainable code."""
    
    def __init__(self, intake_data: dict, filename: str = None):

        
        self.intake_data = intake_data
        self.filename = filename or f"intake_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Define custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='Header1',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.black,
            background=colors.HexColor('#1f4788'),
            spaceAfter=6,
            fontName='Helvetica-Bold',
            leftIndent=5,
            rightIndent=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='Label',
            fontSize=9,
            textColor=colors.HexColor('#333333'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Value',
            fontSize=9,
            textColor=colors.HexColor('#555555'),
            fontName='Helvetica'
        ))
    
    def _build_header(self):
        """Create professional header with company info and patient details."""

        patient = self.intake_data.get('patient_info', {})
        
        # Company header
        logo_path = "./prescription/pdfbuilder/logo.jpg" 
        logo = Image(logo_path, width=2.5*inch, height=1*inch)
        header_data = [
            [logo],
            [
                Paragraph("<br/>Telemedicine Services", self.styles['Header1']),
            ]
        ]
        
        header_table = Table(header_data, colWidths=[7.5*inch])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            # ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4f8')),
            ('LINEBELOW', (0, 0), (-1, -1), 2, colors.HexColor('#1f4788')),
        ]))
        
        # Patient info strip
        patient_full_name = f"{patient.get('first_name', 'N/A')} {patient.get('last_name', 'N/A')}"
        patient_info_data = [
            [
                f"<b>Patient:</b> {patient_full_name}",
                f"<b>DOB:</b> {patient.get('date_of_birth', 'N/A')}",
                f"<b>ID:</b> {patient.get('id', 'N/A')}"
            ],
            [
                f"<b>Email:</b> {patient.get('email', 'N/A')}",
                f"<b>Phone:</b> {patient.get('phone_number', 'N/A')}",
                f"<b>State:</b> {patient.get('state', 'N/A')}"
            ],
            [
                {
                    'value': f"<b>Address:</b> {patient.get('address', 'N/A')}",
                    'colspan': 3
                }
            ]
        ]
        
        patient_table = Table(
            [[Paragraph(cell['value'] if isinstance(cell, dict) else cell, self.styles['Value']) 
              for cell in row] for row in patient_info_data],
            colWidths=[2.5*inch, 2.5*inch, 2.5*inch]
        )
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f0f7')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        
        return [header_table, Spacer(1, 0.2*inch), patient_table, Spacer(1, 0.3*inch)]
    
    def _section_to_table(self, section_title: str, data: dict) -> Table:
        """Convert a data section into a formatted table."""
        rows = [
            [Paragraph(f"<b>{key.replace('_', ' ').title()}</b>", self.styles['Label']),
             Paragraph(str(value) if value is not None else 'N/A', self.styles['Value'])]
            for key, value in data.items()
            if not key.startswith('created_at') and not key.startswith('updated_at') and not key.startswith('id')
        ]
        
        if not rows:
            rows = [[Paragraph("No data available", self.styles['Value'])]]
        
        table = Table(rows, colWidths=[2.0*inch, 5.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        
        return table


    def extract_answer_in_string(self, answer: dict) -> str:
        if not answer:
            return 'N/A'
        if answer.get('selected_choices'):
            choices = answer.get('selected_choices')
            string = ''
            for choice in choices:
                string += str(choice.get('text', '')) + ', '
            return string.rstrip(', ')
        for key in ('text_answer', 'number_answer', 'date_answer', 'boolean_answer'):
            value = answer.get(key)
            if value is not None and value != '':
                return str(value)
        return 'N/A'


    def build_condition_answers_section(self):
        answers = self.intake_data.get('condition_answers', [])
        conditions = self.intake_data.get('requested_conditions', [])
        story = []
        for condition in conditions:
            rows = []
            for answer in answers:
                condition_id = condition.get('condition_id') or condition.get('id')
                if answer.get('condition_id') == condition_id:
                    rows.append([
                        Paragraph(str(answer.get('question_text') or 'N/A'), self.styles['Value']),
                        Paragraph(self.extract_answer_in_string(answer), self.styles['Value'])
                    ])
            if not rows:
                continue

            story.append(Paragraph(condition.get('condition_name', 'N/A'), self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1*inch))
            table_rows = [[
                Paragraph('<b>Question</b>', self.styles['Label']),
                Paragraph('<b>Answer</b>', self.styles['Label'])
            ]] + rows
            table = Table(table_rows, colWidths=[2.5*inch, 5.0*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f0f7')),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9f9f9')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.extend([table, Spacer(1, 0.3*inch)])
        return story


    def _build_sections(self):
        """Build all data sections dynamically."""
        elements = []
        info = self.intake_data.get('intake_info', {})
        
        # Main sections to display
        sections = {
            'Patient Information': self.intake_data.get('patient_info', {}),
            'Patient Intake': self.intake_data.get('patient_intake', {}),
        }
        
        for section_title, section_data in sections.items():
            if section_data:
                elements.append(Paragraph(section_title, self.styles['SectionHeader']))
                elements.append(Spacer(1, 0.1*inch))
                elements.append(self._section_to_table(section_title, section_data))
                elements.append(Spacer(1, 0.3*inch))
        
        # List-based sections
        list_sections = {
            'Insurance Information': self.intake_data.get('insurances', []),
            'Medical History': self.intake_data.get('medical_history', []),
            'Family History': self.intake_data.get('family_history', []),
            'Health Records': self.intake_data.get('health_records', []),
        }
        
        for section_title, items in list_sections.items():
            if items and len(items) > 0:
                elements.append(Paragraph(section_title, self.styles['SectionHeader']))
                elements.append(Spacer(1, 0.1*inch))
                
                for idx, item in enumerate(items):
                    elements.append(self._section_to_table(f"{section_title} #{idx+1}", item))
                    if idx < len(items) - 1:
                        elements.append(Spacer(1, 0.15*inch))
                
                elements.append(Spacer(1, 0.3*inch))
        
        # Requested conditions
        conditions = self.intake_data.get('requested_conditions', [])
        if conditions:
            condition_rows = [
                [Paragraph(c.get('condition_name', 'N/A'), self.styles['Value']),
                 Paragraph('✓ Yes' if c.get('requested') else '✗ No', self.styles['Value'])]
                for c in conditions
            ]
            
            elements.append(Paragraph('Requested Conditions', self.styles['SectionHeader']))
            elements.append(Spacer(1, 0.1*inch))
            
            conditions_table = Table(condition_rows, colWidths=[5.0*inch, 2.5*inch])
            conditions_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            elements.append(conditions_table)
        condition_answers_section = self.build_condition_answers_section()
        if condition_answers_section:
            elements.extend(condition_answers_section)
        soap_notes = self.intake_data.get('soap_notes', {})

        if soap_notes != {}:
            elements.extend(build_soap_notes_section(soap_notes))

        elements.append(PageBreak())
        elements.extend(visit_summary_section(self.intake_data.get('patient_intake').get('updated_at', 'N/A')))
        elements.extend(generate_doctors_info_for_medication(None, self.intake_data.get('doctor_info', {})))
        

        return elements
    
    def _build_footer(self):
        """Add footer with generation timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        footer = Paragraph(
            f"<i>Report generated on {timestamp}</i>",
            ParagraphStyle(
                name='Footer',
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=TA_CENTER
            )
        )
        return [Spacer(1, 0.4*inch), footer]
    
    def generate(self, output_path: str = None) -> bytes:
        """Generate PDF and return bytes or save to file."""
        # Create in-memory PDF if no output path
        if output_path:
            pdf_file = output_path
        else:
            pdf_file = BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build elements
        elements = []
        elements.extend(self._build_header())
        elements.extend(self._build_sections())
        elements.extend(self._build_footer())
        
        # Build PDF
        doc.build(elements)
        
        # Return bytes if in-memory, otherwise return path
        if not output_path:
            pdf_file.seek(0)
            return pdf_file.read()
        
        return None