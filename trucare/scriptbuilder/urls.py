from rest_framework.routers import DefaultRouter, path

from .views import (
	ConditionViewSet,
	OrganizationProfileViewSet,
	PrescribeAbleItemViewSet,
	ScriptAssignmentViewSet,
	ScriptForIntakeView,
	ScriptInfoOrganizationView,
	ScriptItemAssignmentViewSet,
	ScriptViewSet,
	ScriptItemsByCategoryView,
	AssignScriptToIntakeView,
)


router = DefaultRouter()
router.register("prescribeable-items", PrescribeAbleItemViewSet, basename="prescribeable-item")
router.register("categories", ConditionViewSet, basename="condition-category")
router.register("scripts", ScriptViewSet, basename="script")
router.register("organization-profiles", OrganizationProfileViewSet, basename="organization-profile")
router.register("script-assignments", ScriptAssignmentViewSet, basename="script-assignment")
router.register("script-items", ScriptItemAssignmentViewSet, basename="script-item")


urlpatterns = router.urls + [
        path("script-items-by-category/", ScriptItemsByCategoryView.as_view(), name="script-items-by-category"),
		path("script-items-for-intake/", ScriptForIntakeView.as_view(), name="script-items-for-intake"),
		path("assign-script-to-intake/", AssignScriptToIntakeView.as_view(), name="assign-script-to-intake"),
        path("script-info-organization/", ScriptInfoOrganizationView.as_view(), name="script-info-organization"),
]

