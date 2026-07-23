from rest_framework.routers import DefaultRouter

from .views import OrganizationProfileViewSet, PrescribeAbleItemViewSet, ScriptAssignmentViewSet, ScriptViewSet


router = DefaultRouter()
router.register("prescribeable-items", PrescribeAbleItemViewSet, basename="prescribeable-item")
router.register("scripts", ScriptViewSet, basename="script")
router.register("organization-profiles", OrganizationProfileViewSet, basename="organization-profile")
router.register("script-assignments", ScriptAssignmentViewSet, basename="script-assignment")

urlpatterns = router.urls
