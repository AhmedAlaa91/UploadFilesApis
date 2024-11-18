from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedFile
from .serializer import UploadedFileSerializer
from mimetypes import guess_type

class FileUploadView(APIView):
    """
    post:
    Upload a file.

    Validation:
    - Max file size: 5 MB
    - Allowed extensions: .jpg, .jpeg, .png, .gif, .pdf
    """
    
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileListView(APIView):
    """
    get:
    Retrieve all uploaded files or filter them by type.

    Query Parameters:
    - `type`: Filter files by type (e.g., "image", "pdf").
    """
     
    def get(self, request, *args, **kwargs):
        file_type = request.query_params.get('type')  
        files = UploadedFile.objects.all()

        if file_type:
            mime_types = {
                'image': ['image/jpeg', 'image/png', 'image/gif'],
                'pdf': ['application/pdf'],
            }
            allowed_mime_types = mime_types.get(file_type.lower(), [])
            files = [f for f in files if guess_type(f.file.url)[0] in allowed_mime_types]

        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)

class FileRetrieveView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            file = UploadedFile.objects.get(pk=pk)
            serializer = UploadedFileSerializer(file)
            return Response(serializer.data)
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
