from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('', include(router.urls)),
   path('books/', views.BookList.as_view(), name='book-list'),
]
