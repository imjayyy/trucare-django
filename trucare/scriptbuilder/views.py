from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from accounts.models import AccountProfile

from .models import PrescribeAbleItem, Script, ScriptClientRelationship
from .serializers import (
	OrganizationProfileSearchSerializer,
	PrescribeAbleItemSerializer,
	ScriptAssignmentReadSerializer,
	ScriptAssignmentWriteSerializer,
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
			return ScriptAssignmentWriteSerializer
		return ScriptAssignmentReadSerializer



