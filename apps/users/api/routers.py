from rest_framework.routers import DefaultRouter

from apps.users.api.api import UserViewSet, GroupViewSet, UserGroupViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename="users")
router.register('groups', GroupViewSet, basename="groups")
router.register('user-groups', UserGroupViewSet, basename="user-groups")


urlpatterns = router.urls