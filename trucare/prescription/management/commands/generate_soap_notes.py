from django.core.management.base import BaseCommand
from prescription.soapnotesgenerator.soapnotes import (
    generate_soap_notes,
    save_soap_notes_to_db
)


class Command(BaseCommand):
    help = 'Generate SOAP notes for a patient intake using Gemini API'

    def add_arguments(self, parser):
        parser.add_argument(
            'patient_intake_id',
            type=int,
            help='ID of the patient intake to generate SOAP notes for'
        )
        parser.add_argument(
            '--sample',
            action='store_true',
            default=True,
            help='Use sample data for testing (default: True)'
        )

    def handle(self, *args, **options):
        patient_intake_id = options['patient_intake_id']
        use_sample = options['sample']

        self.stdout.write(
            self.style.SUCCESS(
                f'Generating SOAP notes for patient intake {patient_intake_id}...'
            )
        )

        # Generate SOAP notes
        soap_data = generate_soap_notes(patient_intake_id, use_sample=use_sample)

        if not soap_data:
            self.stdout.write(
                self.style.ERROR('Failed to generate SOAP notes')
            )
            return

        # Display generated SOAP notes
        self.stdout.write(self.style.SUCCESS('\n=== Generated SOAP Notes ==='))
        for section, content in soap_data.items():
            self.stdout.write(f'\n{section.upper()}:\n{content}')

        # Save to database
        if save_soap_notes_to_db(patient_intake_id, soap_data):
            self.stdout.write(
                self.style.SUCCESS(
                    '\n✓ SOAP notes saved to database successfully!'
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR('\n✗ Failed to save SOAP notes to database')
            )
