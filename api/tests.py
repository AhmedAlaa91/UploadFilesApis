import os
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

def test_file_upload_success(db):
    """
    Test the successful upload of a valid file.
    """
    # Initialize API client
    client = APIClient()

    
    file_content = b"This is a test file content"
    sample_file = SimpleUploadedFile(
        "testfile.pdf", file_content, content_type="application/pdf"
    )

    
    response = client.post('/api/upload/', {'file': sample_file}, format='multipart')

    # Assert the response status code is 201 (Created)
    assert response.status_code == 201

   
    response_data = response.json()
    assert 'id' in response_data
    assert response_data['file'].endswith('testfile.pdf')

    
    uploaded_file_path = os.path.join('uploads/uploads', 'testfile.pdf')
    assert os.path.exists(uploaded_file_path)

    
    if os.path.exists(uploaded_file_path):
        os.remove(uploaded_file_path)
