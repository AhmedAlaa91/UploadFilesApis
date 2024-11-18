from django.urls import path
from .views import FileUploadView, FileListView, FileRetrieveView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileRetrieveView.as_view(), name='file-retrieve'),
]



