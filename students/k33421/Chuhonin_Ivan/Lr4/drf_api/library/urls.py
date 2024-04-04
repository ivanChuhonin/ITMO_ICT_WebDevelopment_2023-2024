from django.urls import include, path
from rest_framework import routers

from library.views import UserViewSet, ReaderViewSet, HallViewSet, LibraryCardViewSet, BookViewSet, \
    BookCopyViewSet, OperationViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
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
]
