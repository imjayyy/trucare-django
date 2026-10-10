from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from intake.models import Condition, PatientIntake
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from accounts.models import AccountProfile
from intake.models import Condition, PatientIntake
from rest_framework.views import APIView

from .models import PrescribeAbleItem, Script, ScriptClientRelationship, ScriptIntakeRelationship, ScriptItem
from .serializers import (
	ConditionSerializer,
	OrganizationProfileSearchSerializer,
	PrescribeAbleItemSerializer,
	ScriptCategoryItemsSerializer,
	ScriptAssignmentReadSerializer,
	ScriptAssignmentWriteSerializer,
	ScriptItemReadSerializer,
	ScriptItemWriteSerializer,
	ScriptSerializer,
)


@extend_schema_view(
	list=extend_schema(
		summary="List prescribeable items",
		description="Retrieve a paginated list of prescribeable items with search and ordering support.",
		tags=["Script Builder"],
		parameters=[
			OpenApiParameter(
				name="search",
				description="Search by name, generic name, strength, dosage form, sig, description, or category name.",
				required=False,
				type=str,
			),
			OpenApiParameter(
				name="ordering",
				description="Order results by one of: name, category__name, item_type, active.",
				required=False,
				type=str,
			),
			OpenApiParameter(
				name="category_id",
				description="Optional condition category ID filter.",
				required=False,
				type=int,
			),
			OpenApiParameter(name="page", description="Page number.", required=False, type=int),
			OpenApiParameter(name="page_size", description="Items per page (max 100).", required=False, type=int),
		],
		responses={
			200: PrescribeAbleItemSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	retrieve=extend_schema(
		summary="Retrieve a prescribeable item",
		description="Retrieve a single prescribeable item by ID.",
		tags=["Script Builder"],
		responses={
			200: PrescribeAbleItemSerializer,
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			404: OpenApiResponse(description="Prescribeable item not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	create=extend_schema(
		summary="Create a prescribeable item",
		description="Create a new prescribeable item.",
		tags=["Script Builder"],
		request=PrescribeAbleItemSerializer,
		responses={
			201: PrescribeAbleItemSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			500: OpenApiResponse(description="Internal server error."),
		},
		examples=[
			OpenApiExample(
				"Create Medication",
				request_only=True,
				value={
					"category": 18,
					"item_type": "medication",
					"name": "Diclofenac Sodium 3% Topical Gel",
					"generic_name": "Diclofenac Sodium",
					"strength": "3%",
					"dosage_form": "Gel",
					"usual_sig": "Apply 1-2 grams to affected area(s) up to 4 times daily as needed for pain.",
					"quantity": "200",
					"refills": 0,
					"duration": "30 days",
					"description": "NDC: 71085-0003-00",
					"active": True,
				},
			)
		],
	),
	update=extend_schema(
		summary="Replace a prescribeable item",
		description="Replace all writable fields on an existing prescribeable item.",
		tags=["Script Builder"],
		request=PrescribeAbleItemSerializer,
		responses={
			200: PrescribeAbleItemSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			404: OpenApiResponse(description="Prescribeable item not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	partial_update=extend_schema(
		summary="Partially update a prescribeable item",
		description="Update one or more fields on an existing prescribeable item.",
		tags=["Script Builder"],
		request=PrescribeAbleItemSerializer,
		responses={
			200: PrescribeAbleItemSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			404: OpenApiResponse(description="Prescribeable item not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	destroy=extend_schema(
		summary="Delete a prescribeable item",
		description="Delete an existing prescribeable item by ID.",
		tags=["Script Builder"],
		responses={
			204: OpenApiResponse(description="Deleted successfully."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			404: OpenApiResponse(description="Prescribeable item not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
)
class PrescribeAbleItemViewSet(viewsets.ModelViewSet):
	queryset = PrescribeAbleItem.objects.select_related("category").all()
	serializer_class = PrescribeAbleItemSerializer
	permission_classes = [permissions.IsAuthenticated]
	search_fields = [
		"name",
		"generic_name",
		"strength",
		"dosage_form",
		"usual_sig",
		"description",
		"category__name",
	]
	ordering_fields = ["name", "category__name", "item_type", "active"]
	ordering = ["category__name", "name"]
	filter_backends = [SearchFilter, OrderingFilter]

	def get_queryset(self):
		queryset = super().get_queryset()
		category_id = self.request.query_params.get("category_id")
		if category_id:
			queryset = queryset.filter(category_id=category_id)
		return queryset


@extend_schema_view(
	list=extend_schema(
		summary="List scripts",
		description="Retrieve paginated scripts. Supports text search by script name.",
		tags=["Script Builder"],
		parameters=[
			OpenApiParameter(name="search", description="Search by script name.", required=False, type=str),
			OpenApiParameter(name="ordering", description="Order by name or id.", required=False, type=str),
			OpenApiParameter(name="page", description="Page number.", required=False, type=int),
			OpenApiParameter(name="page_size", description="Items per page (max 100).", required=False, type=int),
		],
		responses={
			200: ScriptSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
		},
	),
	create=extend_schema(
		summary="Create script",
		description="Create a script that can later be assigned to organization profiles.",
		tags=["Script Builder"],
		request=ScriptSerializer,
		responses={
			201: ScriptSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
		},
		examples=[
			OpenApiExample(
				"Create Script",
				request_only=True,
				value={"name": "Pain Starter Script"},
			)
		],
	),
	retrieve=extend_schema(
		summary="Retrieve script",
		description="Retrieve script by ID.",
		tags=["Script Builder"],
		responses={
			200: ScriptSerializer,
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
		},
	),
	update=extend_schema(
		summary="Update script",
		description="Replace script fields.",
		tags=["Script Builder"],
		request=ScriptSerializer,
		responses={
			200: ScriptSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
		},
	),
	partial_update=extend_schema(
		summary="Partially update script",
		description="Update one or more script fields.",
		tags=["Script Builder"],
		request=ScriptSerializer,
		responses={
			200: ScriptSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
		},
	),
	destroy=extend_schema(
		summary="Delete script",
		description="Delete script by ID.",
		tags=["Script Builder"],
		responses={
			204: OpenApiResponse(description="Deleted successfully."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
		},
	),
)
class ScriptViewSet(viewsets.ModelViewSet):
	queryset = Script.objects.all()
	serializer_class = ScriptSerializer
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["name"]
	ordering_fields = ["id", "name"]
	ordering = ["name"]

	@extend_schema(
		summary="List script drugs grouped by category",
		description="Retrieve all drugs/prescribeable items assigned to a script, grouped by condition category.",
		tags=["Script Builder"],
		responses={
			200: ScriptCategoryItemsSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
		examples=[
			OpenApiExample(
				"Category Grouped Script Items",
				response_only=True,
				value=[
					{
						"category_id": 18,
						"category_name": "Pain",
						"items": [
							{
								"id": 5,
								"script": 2,
								"script_name": "Pain Starter Script",
								"prescribeable_item": 31,
								"prescribeable_item_name": "Diclofenac Sodium 3% Topical Gel",
								"category": 18,
								"category_name": "Pain",
								"item_type": "medication",
								"generic_name": "Diclofenac Sodium",
								"strength": "3%",
								"dosage_form": "Gel",
								"usual_sig": "Apply 1-2 grams to affected area(s) up to 4 times daily as needed for pain.",
								"quantity": "200",
								"refills": 0,
								"duration": "30 days",
								"description": "NDC: 71085-0003-00",
								"active": True,
							}
						],
					}
				],
			),
		],
	)
	@action(detail=True, methods=["get"], url_path="drugs-by-category")
	def drugs_by_category(self, request, *args, **kwargs):
		script = self.get_object()
		script_items = (
			ScriptItem.objects.select_related("script", "prescribeable_item__category")
			.filter(script=script)
			.order_by("prescribeable_item__category__name", "prescribeable_item__name")
		)
		grouped = {}
		for script_item in script_items:
			category = script_item.prescribeable_item.category
			if category.id not in grouped:
				grouped[category.id] = {
					"category_id": category.id,
					"category_name": category.name,
					"items": [],
				}
			grouped[category.id]["items"].append(script_item)

		response_payload = []
		for data in grouped.values():
			response_payload.append(
				{
					"category_id": data["category_id"],
					"category_name": data["category_name"],
					"items": ScriptItemReadSerializer(data["items"], many=True).data,
				}
			)

		return Response(response_payload, status=status.HTTP_200_OK)


@extend_schema_view(
	list=extend_schema(
		summary="List all categories",
		description="Retrieve all condition categories available for prescribeable item grouping.",
		tags=["Script Builder"],
		parameters=[
			OpenApiParameter(name="search", description="Search category by name, code, or ICD code.", required=False, type=str),
			OpenApiParameter(name="ordering", description="Order by name, code, or id.", required=False, type=str),
		],
		responses={
			200: ConditionSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	retrieve=extend_schema(
		summary="Retrieve category",
		description="Retrieve a single condition category by ID.",
		tags=["Script Builder"],
		responses={
			200: ConditionSerializer,
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Category not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
)
class ConditionViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Condition.objects.all()
	serializer_class = ConditionSerializer
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["name", "code", "icd_code"]
	ordering_fields = ["id", "name", "code"]
	ordering = ["name"]


@extend_schema_view(
	list=extend_schema(
		summary="Search organization profiles",
		description="List organization account profiles for frontend assignment search. Authentication: JWT Bearer.",
		tags=["Script Builder"],
		parameters=[
			OpenApiParameter(
				name="search",
				description="Search by username, email, first name, last name, or organization type.",
				required=False,
				type=str,
			),
			OpenApiParameter(name="ordering", description="Order by username, email, or id.", required=False, type=str),
			OpenApiParameter(name="page", description="Page number.", required=False, type=int),
			OpenApiParameter(name="page_size", description="Items per page (max 100).", required=False, type=int),
		],
		responses={
			200: OrganizationProfileSearchSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
		},
	),
	retrieve=extend_schema(
		summary="Retrieve organization profile",
		description="Retrieve a single organization account profile.",
		tags=["Script Builder"],
		responses={
			200: OrganizationProfileSearchSerializer,
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Profile not found."),
		},
	),
)
class OrganizationProfileViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = AccountProfile.objects.select_related("user").filter(role=AccountProfile.ROLE_ORGANIZATION)
	serializer_class = OrganizationProfileSearchSerializer
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["user__username", "user__email", "user__first_name", "user__last_name", "organization_type"]
	ordering_fields = ["id", "user__username", "user__email"]
	ordering = ["user__username"]


@extend_schema_view(
	list=extend_schema(
		summary="List script assignments",
		description="List paginated script-to-organization assignments with search.",
		tags=["Script Builder"],
		parameters=[
			OpenApiParameter(
				name="search",
				description="Search by script name, client username, client email, or organization type.",
				required=False,
				type=str,
			),
			OpenApiParameter(name="ordering", description="Order by id, script name, or client username.", required=False, type=str),
			OpenApiParameter(name="page", description="Page number.", required=False, type=int),
			OpenApiParameter(name="page_size", description="Items per page (max 100).", required=False, type=int),
		],
		responses={
			200: ScriptAssignmentReadSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
		},
	),
	create=extend_schema(
		summary="Assign script to organization",
		description="Create a script assignment. Client must be an AccountProfile with role ORGANIZATION.",
		tags=["Script Builder"],
		request=ScriptAssignmentWriteSerializer,
		responses={
			201: ScriptAssignmentReadSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
		},
		examples=[
			OpenApiExample(
				"Assign Script",
				request_only=True,
				value={"script": 3, "client": 12},
			)
		],
	),
	retrieve=extend_schema(
		summary="Retrieve script assignment",
		description="Retrieve a script assignment by ID.",
		tags=["Script Builder"],
		responses={
			200: ScriptAssignmentReadSerializer,
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Assignment not found."),
		},
	),
	destroy=extend_schema(
		summary="Delete script assignment",
		description="Delete an existing script assignment.",
		tags=["Script Builder"],
		responses={
			204: OpenApiResponse(description="Deleted successfully."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Assignment not found."),
		},
	),
)
class ScriptAssignmentViewSet(
	mixins.ListModelMixin,
	mixins.CreateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet,
):
	queryset = ScriptClientRelationship.objects.select_related("script", "client__user").all()
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["script__name", "client__user__username", "client__user__email", "client__organization_type"]
	ordering_fields = ["id", "script__name", "client__user__username"]
	ordering = ["-id"]

	def get_serializer_class(self):
		if self.action == "create":
			print("Request data:", self.request.data)
			ScriptClientRelationship.objects.filter(client=self.request.data.get("client")).delete()
			return ScriptAssignmentWriteSerializer
		return ScriptAssignmentReadSerializer

	
@extend_schema_view(
	list=extend_schema(
		summary="List script item assignments",
		description="List drugs/prescribeable items assigned to scripts.",
		tags=["Script Builder"],
		parameters=[
			OpenApiParameter(name="search", description="Search by script name, drug name, or category name.", required=False, type=str),
			OpenApiParameter(name="ordering", description="Order by id, script name, category name, or drug name.", required=False, type=str),
			OpenApiParameter(name="script", description="Optional script ID filter.", required=False, type=int),
			OpenApiParameter(name="category_id", description="Optional category ID filter.", required=False, type=int),
			OpenApiParameter(name="page", description="Page number.", required=False, type=int),
			OpenApiParameter(name="page_size", description="Items per page (max 100).", required=False, type=int),
		],
		responses={
			200: ScriptItemReadSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	create=extend_schema(
		summary="Assign drug to script",
		description="Create a ScriptItem assignment that links a prescribeable item to a script.",
		tags=["Script Builder"],
		request=ScriptItemWriteSerializer,
		responses={
			201: ScriptItemReadSerializer,
			400: OpenApiResponse(description="Validation error in request body."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			500: OpenApiResponse(description="Internal server error."),
		},
		examples=[
			OpenApiExample(
				"Assign Drug",
				request_only=True,
				value={"script": 2, "prescribeable_item": 31},
			)
		],
	),
	retrieve=extend_schema(
		summary="Retrieve script item assignment",
		description="Retrieve a single script-to-drug assignment by ID.",
		tags=["Script Builder"],
		responses={
			200: ScriptItemReadSerializer,
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script item assignment not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
	destroy=extend_schema(
		summary="Delete script item assignment",
		description="Delete an existing script-to-drug assignment.",
		tags=["Script Builder"],
		responses={
			204: OpenApiResponse(description="Deleted successfully."),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script item assignment not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
	),
)
class ScriptItemAssignmentViewSet(
	mixins.ListModelMixin,
	mixins.CreateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	viewsets.GenericViewSet,
):
	queryset = ScriptItem.objects.select_related("script", "prescribeable_item__category").all()
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ["script__name", "prescribeable_item__name", "prescribeable_item__category__name"]
	ordering_fields = ["id", "script__name", "prescribeable_item__category__name", "prescribeable_item__name"]
	ordering = ["-id"]

	def get_queryset(self):
		queryset = super().get_queryset()
		script_id = self.request.query_params.get("script")
		category_id = self.request.query_params.get("category_id")
		if script_id:
			queryset = queryset.filter(script_id=script_id)
		if category_id:
			queryset = queryset.filter(prescribeable_item__category_id=category_id)
		return queryset

	def get_serializer_class(self):
		if self.action == "create":
			return ScriptItemWriteSerializer
		return ScriptItemReadSerializer

	def create(self, request, *args, **kwargs):
		write_serializer = self.get_serializer(data=request.data, many=True)
		write_serializer.is_valid(raise_exception=True)
		script_items = write_serializer.save()
		read_serializer = ScriptItemReadSerializer(script_items, context=self.get_serializer_context(), many=True)
		headers = self.get_success_headers(read_serializer.data)
		return Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)




def get_drugs_of_script_by_category(script_id):
	script_items = (
		ScriptItem.objects.select_related("script", "prescribeable_item__category")
		.filter(script_id=script_id)
		.order_by("prescribeable_item__category__name", "prescribeable_item__name")
	)
	grouped = {}
	for script_item in script_items:
		category = script_item.prescribeable_item.category
		if category.id not in grouped:
			grouped[category.id] = {
				"category_id": category.id,
				"category_name": category.name,
				"items": [],
			}
		grouped[category.id]["items"].append(script_item)

	response_payload = []
	for data in grouped.values():
		response_payload.append(
			{
				"category_id": data["category_id"],
				"category_name": data["category_name"],
				"items": ScriptItemReadSerializer(data["items"], many=True).data,
			}
		)

	return response_payload


class ScriptItemsByCategoryView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@extend_schema(
		summary="List script drugs grouped by category",
		description="Retrieve all drugs/prescribeable items assigned to a script, grouped by condition category.",
		tags=["Script Builder"],
		responses={
			200: ScriptCategoryItemsSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
		examples=[
			OpenApiExample(
				"Category Grouped Script Items",
				response_only=True,
				value=[	
					{
						"category_id": 18,
						"category_name": "Pain",
						"items": [
							{
								"id": 5,
								"script": 2,
								"script_name": "Pain Starter Script",
								"prescribeable_item": 31,
								"prescribeable_item_name": "Diclofenac Sodium 3% Topical Gel",
								"category": 18,
								"category_name": "Pain",
								"item_type": "medication",
								"generic_name": "Diclofenac Sodium",
								"strength": "3%",
								"dosage_form": "Gel",
								"usual_sig": "Apply 1-2 grams to affected area(s) up to 4 times daily as needed for pain.",
								"quantity": "200",
								"refills": 0,
								"duration": "30 days",
								"description": "NDC: 71085-0003-00",
								"active": True,
							}
						],
					}
				],
			),
		],
	)
	def get(self, request):
		script_id = self.request.query_params.get("script_id")
		if not script_id:
			return Response({"detail": "script_id is required."}, status=status.HTTP_400_BAD_REQUEST)
		script = get_object_or_404(Script, id=script_id)
		grouped_items = get_drugs_of_script_by_category(script.id)
		return Response(grouped_items, status=status.HTTP_200_OK)

class ScriptForIntakeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	@extend_schema(
		summary="List script drugs grouped by category",
		description="Retrieve all drugs/prescribeable items assigned to a script, grouped by condition category.",
		tags=["Script Builder"],
		responses={
			200: ScriptCategoryItemsSerializer(many=True),
			401: OpenApiResponse(description="Authentication credentials were not provided or are invalid."),
			403: OpenApiResponse(description="You do not have permission to perform this action."),
			404: OpenApiResponse(description="Script not found."),
			500: OpenApiResponse(description="Internal server error."),
		},
		examples=[
			OpenApiExample(
				"Category Grouped Script Items",
				response_only=True,
				value=[	
					{
						"category_id": 18,
						"category_name": "Pain",
						"items": [
							{
								"id": 5,
								"script": 2,
								"script_name": "Pain Starter Script",
								"prescribeable_item": 31,
								"prescribeable_item_name": "Diclofenac Sodium 3% Topical Gel",
								"category": 18,
								"category_name": "Pain",
								"item_type": "medication",
								"generic_name": "Diclofenac Sodium",
								"strength": "3%",
								"dosage_form": "Gel",
								"usual_sig": "Apply 1-2 grams to affected area(s) up to 4 times daily as needed for pain.",
								"quantity": "200",
								"refills": 0,
								"duration": "30 days",
								"description": "NDC: 71085-0003-00",
								"active": True,
							}
						],
					}
				],
			),
		],
	)
	def get(self, request):
		intake_id = self.request.query_params.get("intake_id")
		if not intake_id:
			return Response({"detail": "intake_id is required."}, status=status.HTTP_400_BAD_REQUEST)


		script = ScriptIntakeRelationship.objects.filter(intake=intake_id).select_related("script").first()
		if not script:
			client = get_object_or_404(PatientIntake, id=intake_id).client
			if not client:
				return Response({"detail": "Client not found for the given intake_id."}, status=status.HTTP_404_NOT_FOUND)
			account_profile = get_object_or_404(AccountProfile, user=client) if client else None
			script = ScriptClientRelationship.objects.filter(client=account_profile).select_related("script").first()
		else:
			return Response({"detail": "Script not found for the given intake_id."}, status=status.HTTP_404_NOT_FOUND)


		# script_data = ScriptSerializer(script.script).data if script else None
		script_data = get_drugs_of_script_by_category(script.script.id) if script else None

		return Response({"script": script_data}, status=status.HTTP_200_OK)




class ScriptInfoOrganizationView(APIView):

	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		user = request.user
		profile = get_object_or_404(AccountProfile, user=user)

		if profile.role != "ORGANIZATION":
			return Response({"detail": "You do not have permission to view this information."}, status=status.HTTP_403_FORBIDDEN)

		organization_scripts = ScriptClientRelationship.objects.filter(client=profile).select_related("script")
		script = organization_scripts.first().script if organization_scripts.exists() else None

		drugs = get_drugs_of_script_by_category(script.id)
		script_name = script.name if script else None
		return Response({"script_name": script_name, "drugs": drugs}, status=status.HTTP_200_OK)








class AssignScriptToIntakeView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		user = request.user
		profile = get_object_or_404(AccountProfile, user=user)
		if profile is None:
			return Response({"detail": "Account profile not found for the user."}, status=status.HTTP_404_NOT_FOUND)
		if profile.role != "ADMIN":
			return Response({"detail": "You do not have permission to assign scripts to intake."}, status=status.HTTP_403_FORBIDDEN)
		intake_id = request.data.get("intake_id")
		script_id = request.data.get("script_id")
		

		if not intake_id or not script_id:
			return Response({"detail": "intake_id and script_id are required."}, status=status.HTTP_400_BAD_REQUEST)

		intake = get_object_or_404(PatientIntake, id=intake_id)
		script = get_object_or_404(Script, id=script_id)

		relationship = ScriptIntakeRelationship.objects.filter(intake=intake).first()
		if relationship:
			relationship.script = script
			relationship.save()

		if not relationship:
			relationship, created = ScriptIntakeRelationship.objects.get_or_create(			
				intake=intake, script=script
			)
		else:
			created = False

		if created:
			message = "Script assigned to intake successfully."
		else:
			message = "Script was already assigned to this intake."
		return Response(
			{
				"message": message,
			},
			status=status.HTTP_200_OK
		)

	def get(self, request):
		intake_id = request.query_params.get("intake_id")
		if not intake_id:
			return Response({"detail": "intake_id is required."}, status=status.HTTP_400_BAD_REQUEST)
		script = None
		intake = get_object_or_404(PatientIntake, id=intake_id)
		
		relationships = ScriptIntakeRelationship.objects.filter(intake=intake).select_related("script").first()
		if relationships:
			script = relationships.script
		else:
			client = AccountProfile.objects.filter(id=intake.client.id).first()			
			script = ScriptClientRelationship.objects.filter(client=client).select_related("script").first().script
			print(script)
		if script is not None:
			script = ScriptSerializer(script).data

		return Response({"script": script}, status=status.HTTP_200_OK)
