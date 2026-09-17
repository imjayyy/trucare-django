"""
Example usage of the SOAP Notes Generation System

This script demonstrates how to generate SOAP notes for a prescription
using the Gemini AI integration.
"""

import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trucare.settings')
django.setup()

from prescription.soapnotesgenerator.soapnotes import (
    load_sample_data,
    format_patient_data,
    generate_soap_prompt,
    generate_soap_notes,
    save_soap_notes_to_db
)
import json


def example_1_load_sample_data():
    """Example 1: Load sample data from JSON"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Load Sample Data")
    print("="*60)
    
    try:
        intake_data = load_sample_data()
        print(f"✓ Loaded sample data with {len(intake_data)} keys")
        print(f"  Patient: {intake_data['intake_info']['patient_info']['first_name']} "
              f"{intake_data['intake_info']['patient_info']['last_name']}")
        return intake_data
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def example_2_format_patient_data(intake_data):
    """Example 2: Format patient data for the prompt"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Format Patient Data")
    print("="*60)
    
    patient_text = format_patient_data(intake_data)
    print("Formatted Patient Data:")
    print(patient_text)
    return patient_text


def example_3_generate_prompt(patient_text):
    """Example 3: Generate the prompt for Gemini"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Generate Gemini Prompt")
    print("="*60)
    
    prompt = generate_soap_prompt(patient_text)
    print(f"Prompt (first 200 chars):\n{prompt[:200]}...")
    return prompt


def example_4_generate_soap_notes_with_gemini(prescription_id=1):
    """Example 4: Generate SOAP notes using Gemini AI"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Generate SOAP Notes with Gemini")
    print("="*60)
    
    print(f"Generating SOAP notes for prescription {prescription_id}...")
    soap_data = generate_soap_notes(prescription_id=prescription_id, use_sample=True)
    
    if soap_data:
        print("✓ SOAP notes generated successfully!")
        print("\nGenerated SOAP Note Structure:")
        for section, content in soap_data.items():
            print(f"\n{section.upper()}:")
            print(f"  {content[:100]}..." if len(content) > 100 else f"  {content}")
        return soap_data
    else:
        print("✗ Failed to generate SOAP notes")
        return None


def example_5_save_to_database(prescription_id=1, soap_data=None):
    """Example 5: Save SOAP notes to database"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Save SOAP Notes to Database")
    print("="*60)
    
    if not soap_data:
        print("✗ No SOAP data to save")
        return False
    
    print(f"Saving SOAP notes for prescription {prescription_id}...")
    success = save_soap_notes_to_db(prescription_id, soap_data)
    
    if success:
        print("✓ SOAP notes saved successfully!")
        return True
    else:
        print("✗ Failed to save SOAP notes")
        return False


def example_6_complete_workflow(prescription_id=1):
    """Example 6: Complete workflow from start to finish"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Complete Workflow")
    print("="*60)
    
    # Step 1: Load data
    print("\nStep 1: Loading sample data...")
    intake_data = load_sample_data()
    
    # Step 2: Format data
    print("Step 2: Formatting patient data...")
    patient_text = format_patient_data(intake_data)
    
    # Step 3: Generate prompt
    print("Step 3: Generating prompt...")
    prompt = generate_soap_prompt(patient_text)
    
    # Step 4: Generate SOAP notes
    print("Step 4: Generating SOAP notes with Gemini...")
    soap_data = generate_soap_notes(prescription_id=prescription_id, use_sample=True)
    
    # Step 5: Save to database
    if soap_data:
        print("Step 5: Saving to database...")
        save_soap_notes_to_db(prescription_id, soap_data)
        print("\n✓ Complete workflow executed successfully!")
    else:
        print("\n✗ Workflow failed at SOAP generation step")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("SOAP NOTES GENERATION - USAGE EXAMPLES")
    print("="*60)
    
    # Example 1: Load sample data
    intake_data = example_1_load_sample_data()
    
    if intake_data:
        # Example 2: Format patient data
        patient_text = example_2_format_patient_data(intake_data)
        
        # Example 3: Generate prompt
        prompt = example_3_generate_prompt(patient_text)
        
        # Example 4: Generate SOAP notes
        soap_data = example_4_generate_soap_notes_with_gemini(prescription_id=1)
        
        # Example 5: Save to database
        if soap_data:
            example_5_save_to_database(prescription_id=1, soap_data=soap_data)
        
        # Example 6: Complete workflow
        print("\n" + "="*60)
        print("Running complete workflow...")
        print("="*60)
        example_6_complete_workflow(prescription_id=1)
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
