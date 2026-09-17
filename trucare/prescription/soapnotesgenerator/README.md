# SOAP Notes Generation System

## Overview
This system generates medical SOAP notes (Subjective, Objective, Assessment, Plan) for prescriptions using OpenRouter's Gemini Flash AI model. It includes a clean, maintainable codebase with minimal complexity.

## Components

### 1. Core Module: `soapnotes.py`
Located in: `prescription/soapnotesgenerator/soapnotes.py`

**Main Functions:**

- **`load_sample_data(sample_file)`**: Loads patient intake data from JSON
  - Returns: Dictionary with complete patient information

- **`format_patient_data(intake_data)`**: Formats patient data for the prompt
  - Takes: Intake data dictionary
  - Returns: Formatted string with patient information

- **`generate_soap_prompt(patient_data)`**: Creates a structured prompt for Gemini
  - Takes: Patient data string
  - Returns: Formatted prompt requesting JSON SOAP note

- **`generate_soap_notes(patient_intake_id, use_sample)`**: Main function to generate SOAP notes
  - Takes: patient_intake_id and use_sample flag
  - Returns: Dictionary with `subjective`, `objective`, `assessment`, `plan` keys
  - Calls OpenRouter Gemini Flash API and parses JSON response

- **`save_soap_notes_to_db(patient_intake_id, soap_data)`**: Saves generated notes to database
  - Takes: patient_intake_id and soap_data dictionary
  - Returns: True if successful, False otherwise
  - Creates `Soap_notes` record linked to Prescription

## Usage Methods

### Method 1: Django Management Command
```bash
# Generate SOAP notes for prescription ID 1
python manage.py generate_soap_notes 1

# With specific flags
python manage.py generate_soap_notes 1 --sample
```

### Method 2: API Endpoint (REST)
```bash
# POST request to generate SOAP notes
curl -X POST http://localhost:8000/api/prescription/1/soap-notes/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# Response (201 Created):
{
  "message": "SOAP notes generated and saved successfully",
  "data": {
    "subjective": "...",
    "objective": "...",
    "assessment": "...",
    "plan": "..."
  }
}
```

### Method 3: Direct Python Usage
```python
from prescription.soapnotesgenerator.soapnotes import (
    generate_soap_notes,
    save_soap_notes_to_db
)

# Generate SOAP notes
soap_data = generate_soap_notes(prescription_id=1, use_sample=True)

# Save to database
if soap_data:
    save_soap_notes_to_db(prescription_id=1, soap_data=soap_data)
```

## Database Model

The `Soap_notes` model stores the generated SOAP notes:
```python
class Soap_notes(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name="soap_notes")
    subjective = models.TextField(blank=True)      # Patient's symptoms and complaints
    objective = models.TextField(blank=True)       # Measurable findings and vital signs
    assessment = models.TextField(blank=True)      # Clinical diagnosis and evaluation
    plan = models.TextField(blank=True)            # Treatment recommendations
    
    def __str__(self):
        return f"SOAP notes for {self.prescription.patient}"
```

## Data Flow

```
sample_intake.json
        ↓
load_sample_data()
        ↓
format_patient_data()
        ↓
generate_soap_prompt()
        ↓
OpenRouter API (google/gemini-2.0-flash-001)
        ↓
Parse JSON Response
        ↓
save_soap_notes_to_db()
        ↓
Soap_notes Database Record
```

## Configuration

### Required Environment Variables
```bash
# Set in .env or environment
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Dependencies
```
requests>=2.28.0
```

Install with:
```bash
pip install requests
```

### API Details
- **Provider**: OpenRouter (https://openrouter.ai)
- **Model**: Google Gemini 2.0 Flash (google/gemini-2.0-flash-001)
- **Base URL**: https://openrouter.ai/api/v1
- **Features**: Fast, cost-effective, reliable

## Sample Data Format

The system expects `sample_intake.json` with this structure:
```json
{
  "intake_info": {
    "patient_info": {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "date_of_birth": "1990-01-01",
      "email": "test@example.com",
      "phone_number": "1234567890",
      "address": "Test Address",
      "state": "AL"
    },
    "patient_intake": {
      "height": "1.80",
      "weight": "75.00"
    },
    "medical_history": [...],
    "family_history": [...]
  }
}
```

## Prompt Template

The system sends a structured prompt to Gemini requesting:
1. Comprehensive SOAP note sections
2. Medical professionalism
3. JSON format response
4. Exactly these keys: `subjective`, `objective`, `assessment`, `plan`

## Error Handling

- **File Not Found**: Returns None if sample data file doesn't exist
- **JSON Parse Error**: Handles markdown code blocks in response
- **Database Errors**: Returns False if database save fails
- **API Errors**: Caught and logged with descriptive messages

## Code Quality Features

✓ Minimal dependencies  
✓ Clear function separation of concerns  
✓ Type hints for all functions  
✓ Comprehensive error handling  
✓ Easily testable architecture  
✓ Reusable across views, management commands, and scripts  

## Testing

```python
# Test in Django shell
python manage.py shell

from prescription.soapnotesgenerator.soapnotes import generate_soap_notes
soap_data = generate_soap_notes(prescription_id=1, use_sample=True)
print(soap_data)
```

## Future Enhancements

- Add async processing for large batches
- Implement caching for duplicate prescriptions
- Add audit logging for SOAP note generation
- Support multiple AI providers
- Add SOAP note versioning
