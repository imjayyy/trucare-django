
import json
import os
import requests
from pathlib import Path
from typing import Dict, Optional
from django.conf import settings

from intake.get_intake import GetIntakeInfo
from .intake_cleaner import IntakeCleaner
# Configure OpenRouter API
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
MODEL_NAME = 'google/gemini-2.5-flash-lite'  # Correct model name for OpenRouter


def load_sample_data(sample_file: str = 'sample_intake.json') -> Dict:
    """Load sample intake JSON data from file."""
    file_path = Path(__file__).parent / sample_file
    if not file_path.exists():
        raise FileNotFoundError(f"Sample data file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return json.load(f)


def format_patient_data(intake_data: Dict) -> str:
    """Format patient data into a readable string for the prompt."""
    info = intake_data.get('intake_info', {})
    patient = info.get('patient_info', {})
    intake = info.get('patient_intake', {})
    history = info.get('medical_history', [{}])[0] if info.get('medical_history') else {}
    family = info.get('family_history', [{}])[0] if info.get('family_history') else {}
    intake_cleaner = IntakeCleaner(intake)
    cleaned_intake = intake_cleaner.clean()
    return f'PATIENT INFORMATION:{str(cleaned_intake)}'


def generate_soap_prompt(patient_data: str) -> str:
    """Generate a structured prompt for Gemini to create SOAP notes."""
    return f"""Generate a comprehensive SOAP note based on the following patient information.

{patient_data}

INSTRUCTIONS:
1. Create a detailed SOAP note with clear sections
2. Be professional and medically appropriate, NO ASSUMPTIONS, STRICTLY BASED ON PROVIDED DATA
3. Return response as valid JSON with exactly these keys:
   - "subjective": Patient's symptoms, complaints, and medical history from their perspective
   - "objective": Measurable findings, vital signs, and clinical observations
   - "assessment": Clinical diagnosis and evaluation based on findings
   - "plan": Treatment recommendations, medications, follow-up care

IMPORTANT: Return ONLY valid JSON, no additional text or markdown."""


def generate_soap_notes(patient_intake_id: int, use_sample: bool = True) -> Optional[Dict]:
    """
    Generate SOAP notes for a patient intake using OpenRouter Gemini Flash.
    
    Args:
        patient_intake_id: ID of the patient intake
        use_sample: Use sample data for testing (default: True)
    
    Returns:
        Dictionary with SOAP note sections or None if failed
    """
    try:
        # Load and format patient data
        intake_data = GetIntakeInfo(patient_intake_id).get_intake_info()
        
        if not intake_data:
            raise ValueError("No patient data available")

        patient_text = format_patient_data(intake_data)
        prompt = generate_soap_prompt(str(patient_text))
        print( "PROMPT GENERATED:", prompt)
        # Call OpenRouter API
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://trucare.local',
            'X-Title': 'TruCare SOAP Notes Generator'
        }
        
        payload = {
            'model': MODEL_NAME,
            'messages': [
                {'role': 'user', 'content': str(prompt)}
            ],
            'temperature': 0.7,
            'max_tokens': 2000
        }
        
        response = requests.post(
            f'{OPENROUTER_BASE_URL}/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            error_msg = f"OpenRouter API Error {response.status_code}: {response.text}"
            print(error_msg)
            print(f"Request URL: {response.url}")
            print(f"Request Headers: {headers}")
            print(f"Request Payload Model: {payload.get('model')}")
            raise requests.exceptions.HTTPError(error_msg)
        
        response_data = response.json()
        
        if 'choices' not in response_data or len(response_data['choices']) == 0:
            raise ValueError(f"Unexpected API response: {response_data}")
        
        response_text = response_data['choices'][0]['message']['content'].strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        soap_data = json.loads(response_text)
        
        return soap_data
    
    except json.JSONDecodeError as e:
        print(f"Error parsing OpenRouter response: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter API: {e}")
        return None
    except Exception as e:
        print(f"Error generating SOAP notes: {e}")
        return None


def save_soap_notes_to_db(patient_intake_id: int, soap_data: Dict) -> bool:
    """
    Save generated SOAP notes to database.
    
    Args:
        patient_intake_id: ID of the patient intake
        soap_data: Dictionary with SOAP note sections
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from intake.models import PatientIntake
        from prescription.models import Soap_notes
        
        patient_intake = PatientIntake.objects.get(id=patient_intake_id)

        soap_note = Soap_notes.objects.update_or_create(patient_intake=patient_intake, defaults={
            'subjective': soap_data.get('subjective', ''),
            'objective': soap_data.get('objective', ''),
            'assessment': soap_data.get('assessment', ''),
            'plan': soap_data.get('plan', '')
        })

        if len(soap_note) > 0:
            # print(f"SOAP notes updated successfully for patient intake {patient_intake_id}")
            return True

        else:
            return False
        # soap_note = Soap_notes.objects.create(
        #     patient_intake=patient_intake,
        #     subjective=soap_data.get('subjective', ''),
        #     objective=soap_data.get('objective', ''),
        #     assessment=soap_data.get('assessment', ''),
        #     plan=soap_data.get('plan', '')
        # )
        
        # print(f"SOAP notes saved successfully for patient intake {patient_intake_id}")
        # return True
    
    except PatientIntake.DoesNotExist:
        print(f"Patient intake with ID {patient_intake_id} not found")
        return False
    except Exception as e:
        print(f"Error saving SOAP notes to database: {e}")
        return False