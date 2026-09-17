from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from intake.models import PatientIntake
# Create your views here.
from .models import PrescriptionItem, Prescription, PrimaryDrug, SecondaryDrug
from .serializers import PrescriptionItemSerializer
from .prescription_functions import ValidatePrescription, get_patient_conditions, PrescriptionPDFData
# from .pdfbuilder.prescriptionPdf import PrescriptionPDFBuilder
from accounts.models import AccountProfile
from .pdfbuilder.prescriptionPdf import create_pdf
from .soapnotesgenerator.soapnotes import generate_soap_notes, save_soap_notes_to_db
from .pdfbuilder.billerPdf import IntakePDFBuilder
from intake.get_intake import GetIntakeInfo
from .models import Soap_notes

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
        # intake_id is already passed as a parameter
        prescription_data = request.data        
        user = request.user

        # try:
        #     doctor_profile = AccountProfile.objects.get(user=user, role = "DOCTOR")
        # except Exception as e:
        #     return Response({"error": str(e)}, status=400)
        prescription, created = Prescription.objects.get_or_create(patient_id=intake_id, )
        if not created:
            # If the prescription already exists, delete the existing primary and secondary drugs
            PrimaryDrug.objects.filter(prescription=prescription).delete()
            SecondaryDrug.objects.filter(prescription=prescription).delete()
            PrescriptionItem.objects.filter(prescription=prescription).delete()

        validator = ValidatePrescription(prescription_data, prescription, intake_id)
        validated, errors = validator.validate_and_save()
        
        print("validated:", validated, "errors:", errors)
        if not validated:
            return Response({"errors": errors}, status=400)
        if validated:
            try:
                intake_data = PrescriptionPDFData(intake_id).get_pdf_data()
                create_pdf(f"prescription_{intake_id}.pdf", prescription, intake_data)
                PatientIntake.objects.filter(id=intake_id).update(status="APPROVED_BY_DOCTOR")
                return Response({"message": "Prescription data validated and saved successfully."}, status=201)
            except Exception as e:
                return Response({"error": str(e)}, status=500)




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


class PrescriptionPDFAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Download Prescription PDF",
        description="Generate and download a prescription PDF for a specific intake.",
        tags=["Prescription"],
        responses={200: bytes, 400: dict, 500: dict},
    )
    def get(self, request):
        intake_id = request.query_params.get("intake_id")
        presription = Prescription.objects.get(patient=intake_id)
        file = presription.pdf_file if presription.pdf_file else None

        response = HttpResponse(file, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="prescription_{intake_id}.pdf"'
        return response


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

        try:
            intake_data = GetIntakeInfo(intake_id).get_intake_info()
            pdf_bytes = IntakePDFBuilder(intake_data).generate()
        except Exception as exc:
            return Response({"error": str(exc)}, status=500)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="biller_{intake_id}.pdf"'
        return response