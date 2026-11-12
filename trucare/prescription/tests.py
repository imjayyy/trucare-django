from django.test import TestCase

from prescription.pdfbuilder.prescriptionPdf import generate_doctors_attestation


class DoctorAttestationPdfTests(TestCase):
    def test_generate_doctors_attestation_includes_provider_and_attestation_text(self):
        data = {
            'doctor': {
                'user': {
                    'first_name': 'Jane',
                    'last_name': 'Doe',
                },
                'npi': '1234567890',
                'phone_number': '555-123-4567',
                'signature': None,
            }
        }

        story = generate_doctors_attestation(data)

        self.assertIsNotNone(story)
        self.assertTrue(len(story) > 0)

        texts = []
        for item in story:
            if hasattr(item, 'text'):
                texts.append(item.text)
            elif isinstance(item, str):
                texts.append(item)

        combined = ' '.join(texts)
        self.assertIn('Jane Doe', combined)
        self.assertIn('Attestation', combined)
        self.assertIn('medically necessary', combined.lower())
