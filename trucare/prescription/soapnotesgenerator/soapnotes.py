
import json
import os
import requests
from pathlib import Path
from typing import Dict, Optional
from django.conf import settings

from intake.get_intake import GetIntakeInfo
from .intake_cleaner import IntakeCleaner
# Configure OpenRouter API
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
OPENROUTER_BASE_URL = 'https://openrouter.ai/api/v1'
MODEL_NAME = 'google/gemini-2.5-flash-lite'  # Correct model name for OpenRouter

# Configure OpenAI API
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')


def load_sample_data(sample_file: str = 'sample_intake.json') -> Dict:
    """Load sample intake JSON data from file."""
    file_path = Path(__file__).parent / sample_file
    if not file_path.exists():
        raise FileNotFoundError(f"Sample data file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return json.load(f)


def format_patient_data(intake_data: Dict) -> str:
    # print("intake_dataaaa:", intake_data)
    """Format patient data into a readable string for the prompt."""
    patient = intake_data.get('patient_info', {})
    intake = intake_data.get('patient_intake', {})
    history = intake_data.get('medical_history', [{}])[0] if intake_data.get('medical_history') else {}
    family = intake_data.get('family_history', [{}])[0] if intake_data.get('family_history') else {}
    intake_cleaner = IntakeCleaner(intake_data)
    cleaned_intake = intake_cleaner.clean().__str__()
    return f'PATIENT INFORMATION:{str(cleaned_intake)}'


def generate_soap_prompt(patient_data: str) -> str:
    """Generate a structured prompt for Gemini to create SOAP notes."""
    return """You are a medical documentation assistant. Your task is to generate a concise, professional SOAP note from the patient intake information provided below.

The intake information consists of condition/request names, questions, and patient answers. Multiple consecutive entries may belong to the same condition/request. Carefully associate each answer with the question immediately preceding it and the relevant condition/request.

IMPORTANT RULES:

1. Use ONLY information explicitly provided in the intake data.
2. Do NOT invent, assume, diagnose, or infer medical conditions, symptoms, medications, examination findings, or treatment plans that are not explicitly stated.
3. Do not convert a patient's reported condition into a confirmed diagnosis unless the intake explicitly states that the patient has been diagnosed with it.
4. Preserve the patient's reported symptoms, answers, locations, dates, and severity accurately.
5. If information is missing, do not fill the gap. Simply omit it or state "Not reported" where appropriate.
6. Distinguish between:
   * Patient-reported history
   * Current symptoms/complaints
   * Prior treatments/interventions
   * Surgical history
   * Dates
   * Functional limitations
7. If an answer contains multiple selected choices, combine them into a readable list.
8. Do not interpret a selected choice beyond what the patient selected.
9. Do not provide medical advice.
10. Do not recommend medications, procedures, diagnoses, or treatments unless they are explicitly documented in the intake information.
11. Keep the SOAP note clinically professional, concise, and suitable for review by a healthcare professional.

SOAP STRUCTURE:

Subjective: maximum 250–350 words
Objective: maximum 200–300 words
Assessment: maximum 150–250 words
Plan: maximum 250–350 words

SUBJECTIVE:
Summarize the patient's reported complaints, symptoms, relevant medical history, conditions, 
affected body areas, pain level, functional limitations, 
prior interventions, surgeries, and other relevant patient-reported information.
Omit the information you seem unfit for soap notes, if the answer is not relevant or appropriate.
If multiple orientations are provided, like (Left Foot, Right Foot), include them accurately in the summary as Both Feet.

OBJECTIVE:
Only include objective information explicitly provided in the intake data. Do not create physical examination findings, vital signs, laboratory results, imaging results, or other objective findings.

If no objective information is provided, write:
"No objective examination findings were provided in the intake."
ASSESSMENT: Summarize the clinical issues reported by the patient without making unsupported diagnoses.

Use wording such as:

* "Patient reports..."
* "Patient indicates..."
* "History is notable for..."
* "Reported concern includes..."

Do not state a diagnosis unless it was explicitly provided in the intake.

PLAN:
Only include a plan if one is explicitly provided in the intake data.
If no treatment or management plan is provided, write:
"No treatment or management plan was provided in the intake."

IMPORTANT:
The intake may contain multiple condition/request sections. 
Keep information associated with the appropriate condition/request and do not mix unrelated conditions.

Return ONLY valid JSON in the following format:
{
'subjective': ...,
'objective': ...,
'assessment': ...,
'plan': ...
}
Do not include Markdown.
Do not wrap the JSON in ```json.
Do not include any explanation before or after the JSON.
Ensure the JSON is syntactically valid and all string values are properly escaped.
Anything outside this required JSON format will not be accepted.
Avoid using  \n  (next line) in your response.
Maximum 500 to 1500 characters for each Subjective, Objective, Assessment, and Plan section. It should provide a concise yet comprehensive summary of the intake data.
Summarize the Intake data, Human readable and written in complete sentences.
Do not divide information into different conditions/requests parts.
Write concise and clear SOAP notes based on the intake data.
PATIENT INTAKE DATA:
 """ + patient_data


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

        patient_text = str(format_patient_data(intake_data))
        # print(patient_text)
        prompt = generate_soap_prompt(patient_text)
        # print( "PROMPT GENERATED:", prompt)
        # Call OpenRouter API
        headers = {
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://localhost:8000',
            'X-Title': 'TruCare SOAP Notes Generator'
        }
        
        payload = {
            'model': MODEL_NAME,
            'messages': [
                {'role': 'user', 'content': str(prompt)}
            ],
            'temperature': 0.7,
            'max_tokens': 10000
        }
        
        response = requests.post(
            f'{OPENROUTER_BASE_URL}/chat/completions',
            headers=headers,
            json=payload,
            timeout=60
        )

        print(f"OpenRouter API Response: {response.text}")  
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