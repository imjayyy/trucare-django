from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from financials.models import DoctorConsults, DoctorConsultCost, add_doctor_consult
from intake.models import PatientIntake
# Create your views here.
from .models import PrescriptionItem, Prescription, PrimaryDrug, SecondaryDrug
from .serializers import PrescriptionItemSerializer
from .prescription_functions import ValidatePrescription, get_patient_conditions, PrescriptionPDFData
# from .pdfbuilder.prescriptionPdf import PrescriptionPDFBuilder
from accounts.models import AccountProfile, DoctorProfile
from .pdfbuilder.prescriptionPdf import create_pdf
from .soapnotesgenerator.soapnotes import generate_soap_notes, save_soap_notes_to_db
from .pdfbuilder.billerPdf import IntakePDFBuilder
from intake.get_intake import GetIntakeInfo
from .models import Soap_notes
from django.shortcuts import get_object_or_404
from django.utils import timezone


# Alex
class PrescriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Save Prescription Data",
        description="Validate and save prescription data for a specific patient intake.",
        tags=["Prescription"],
        request=PrescriptionItemSerializer,
        responses={201: dict, 400: dict},
    )
    def post(self, request, intake_id):
        prescription_data = request.data        
        user = request.user
        
        doctor_profile = get_object_or_404(DoctorProfile, user=user)

        try:
            # 1. Safely check if the PatientIntake exists first (Prevents FK crash)
            patient_intake = get_object_or_404(PatientIntake, id=intake_id)

            # 2. Now safe to get or create the prescription
            # Note: Ensure whether your model field is named 'patient' or 'patient_id'
            prescription, created = Prescription.objects.get_or_create(
                patient=patient_intake, # Or patient_id=intake_id depending on your model definition
                doctor=doctor_profile
            )
            
            if not created:
                PrimaryDrug.objects.filter(prescription=prescription).delete()
                SecondaryDrug.objects.filter(prescription=prescription).delete()
                PrescriptionItem.objects.filter(prescription=prescription).delete()
            else:
                add_doctor_consult(doctor_profile, patient_intake)

            validator = ValidatePrescription(prescription_data, prescription, intake_id)
            validated, errors = validator.validate_and_save()
            
            if not validated:
                return Response({"errors": errors}, status=400)

            intake_data = PrescriptionPDFData(intake_id).get_pdf_data()

            create_pdf(f"prescription_{intake_id}.pdf", prescription, intake_data)
            
            PatientIntake.objects.filter(id=intake_id).update(
                status="APPROVED_BY_DOCTOR",
                updated_at=timezone.now(),
            )
            
            return Response({"message": "Prescription data validated and saved successfully."}, status=201)

        except PatientIntake.DoesNotExist:
            return Response({"error": f"Patient intake with ID {intake_id} does not exist."}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

        
class DoctorDeniedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Doctor Denied Prescription",
        description="Mark a prescription as denied by the doctor for a specific patient intake.",
        tags=["Prescription"],
        request=dict,
        responses={200: dict, 400: dict, 404: dict},
    )
    def post(self, request):
        user = request.user
        doctor_profile = get_object_or_404(DoctorProfile, user=user)
        status = request.data.get("status")
        # denied_reason = request.data.get("denied_reason", '')
        intake_id = request.data.get("intake_id")
        if not intake_id:
            return Response({"error": "intake_id is required."}, status=400)
        if not status:
            return Response({"error": "status is required."}, status=400)
        patient = PatientIntake.objects.filter(id=intake_id, doctor=doctor_profile).update(
            status=status,
            updated_at=timezone.now(),
        )
        if not patient:
            return Response({"error": "Patient intake not found or not associated with the doctor."}, status=404)
        else:
            add_doctor_consult(doctor_profile, PatientIntake.objects.get(id=intake_id))
        return Response({"message": "Prescription has been denied by the doctor."}, status=200)


class PrescriptionDataAPIView(APIView):
    permission_classes = []

    def get(self, request):
        intake_id = request.query_params.get('intake_id')
        if not intake_id:
            return Response({"error": "intake_id query parameter is required."}, status=400)

        try:
            prescription = PrescriptionPDFData(intake_id).get_pdf_data()
        except Prescription.DoesNotExist:
            return Response({"error": "Prescription not found for the given intake_id."}, status=404)


        return Response(prescription, status=200)

#Bilal
class PrescriptionPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Download Prescription PDF",
        description="Generate and download a prescription PDF for a specific intake.",
        tags=["Prescription"],
        responses={200: bytes, 400: dict, 404: dict, 500: dict},
    )
    def get(self, request):
        intake_id = request.query_params.get("intake_id")
        if not intake_id:
            return Response({"error": "intake_id query parameter is required."}, status=400)

        try:
            # Use patient_id based on your model choices
            prescription = Prescription.objects.filter(patient_id=intake_id).order_by('-created_at').first()
            
            if not prescription:
                return Response({"error": "Prescription not found for the given intake_id."}, status=404)
                
            if not prescription.pdf_file:
                return Response({"error": "PDF file has not been generated for this prescription yet."}, status=404)
            
            file = prescription.pdf_file
            response = HttpResponse(file, content_type="application/pdf")
            response["Content-Disposition"] = f'attachment; filename="prescription_{intake_id}.pdf"'
            return response
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)

#Alex
# class PrescriptionPDFAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     @extend_schema(
#         summary="Download Prescription PDF",
#         description="Generate and download a prescription PDF for a specific intake.",
#         tags=["Prescription"],
#         responses={200: bytes, 400: dict, 500: dict},
#     )
#     def get(self, request):
#         intake_id = request.query_params.get("intake_id")
#         presription = Prescription.objects.get(patient=intake_id)
#         file = presription.pdf_file if presription.pdf_file else None

#         response = HttpResponse(file, content_type="application/pdf")
#         response["Content-Disposition"] = f'attachment; filename="prescription_{intake_id}.pdf"'
#         return response


class GenerateSoapNotesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Generate SOAP Notes",
        description="Generate SOAP notes for a patient intake using Gemini AI.",
        tags=["SOAP Notes"],
        responses={201: dict, 404: dict, 500: dict},
    )
    def get(self, request):
        intake_id = request.query_params.get("intake_id")
        if not intake_id:
            return Response({"error": "intake_id query parameter is required."}, status=400)
        """Generate SOAP notes for a specific patient intake."""
        try:
            # Verify patient intake exists
            patient_intake = PatientIntake.objects.get(id=intake_id)
            soap_notes = Soap_notes.objects.filter(patient_intake_id=intake_id).first()
            if soap_notes:

                return Response(
                    {
                        "message": "SOAP already exists.",
                        "data": {
                            "subjective": soap_notes.subjective,
                            "objective": soap_notes.objective,
                            "assessment": soap_notes.assessment,
                            "plan": soap_notes.plan,
                        }
                    },
                    status=200
                )
            # Generate SOAP notes using Gemini
            soap_data = generate_soap_notes(intake_id, use_sample=False)

            if not soap_data:
                return Response(
                    {"error": "Failed to generate SOAP notes from AI"},
                    status=500
                )


            # Save to database
            if not save_soap_notes_to_db(intake_id, soap_data):
                return Response(
                    {"error": "Failed to save SOAP notes to database"},
                    status=500
                )

            return Response(
                {
                    "message": "SOAP notes generated and saved successfully",
                    "data": soap_data
                },
                status=201
            )

        except PatientIntake.DoesNotExist:
            return Response(
                {"error": f"Patient intake {intake_id} not found"},
                status=404
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=500
            )


    @extend_schema(
        summary="Save SOAP notes",
        description="Save SOAP notes for a specific patient intake. soap_data should contain the subjective, objective, assessment, and plan sections.",
        tags=["SOAP Notes"],
        request={"intake_id": int, "soap_data": dict},
        responses={201: dict, 400: dict, 500: dict},
    )
    def post(self, request):
        intake_id = request.data.get("intake_id")
        soap_data = request.data.get("soap_data")
        if not intake_id:
            return Response({"error": "intake_id is required."}, status=400)
        if not soap_data:
            return Response({"error": "soap_data is required."}, status=400)

        if not save_soap_notes_to_db(intake_id, soap_data):
            return Response(
                {"error": "Failed to save SOAP notes to database"},
                status=500
            )

        return Response(
            {
                "message": "SOAP notes saved successfully",
                "data": soap_data
            },
            status=201
        )
        


class BillerPDFAPIView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Download Biller PDF",
        description="Generate and download a biller PDF for a specific intake.",
        tags=["Biller"],
        responses={200: bytes, 400: dict, 500: dict},
    )
    def get(self, request):
        intake_id = request.query_params.get("intake_id")
        if not intake_id:
            return Response({"error": "intake_id query parameter is required."}, status=400)

        intake_data_class = GetIntakeInfo(intake_id)
        intake_data = intake_data_class.get_intake_info()
        doctor_info = intake_data_class.get_doctor_info()
        soap_notes = Soap_notes.objects.filter(patient_intake=intake_id).first()
        intake_data['soap_notes'] = {}
        intake_data['soap_notes']['subjective'] = soap_notes.subjective if soap_notes else None
        intake_data['soap_notes']['objective'] = soap_notes.objective if soap_notes else None
        intake_data['soap_notes']['assessment'] = soap_notes.assessment if soap_notes else None
        intake_data['soap_notes']['plan'] = soap_notes.plan if soap_notes else None
        intake_data['doctor_info'] = doctor_info
        pdf_bytes = IntakePDFBuilder(intake_data).generate()
        # try:
            
        # except Exception as exc:
        #     return Response({"error": str(exc)}, status=500)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="biller_{intake_id}.pdf"'
        return response






