from django.urls import include, path
from rest_framework import routers

from Library.views import UserViewSet, GroupViewSet, ReaderViewSet, HallViewSet, LibraryCardViewSet, BookViewSet, \
    BookCopyViewSet, OperationViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'readers', ReaderViewSet)
router.register(r'halls', HallViewSet)
router.register(r'librarycards', LibraryCardViewSet)
router.register(r'books', BookViewSet)
router.register(r'bookcopies', BookCopyViewSet)
router.register(r'operations', OperationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
