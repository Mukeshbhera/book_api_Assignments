from django.shortcuts import render

from django.conf import settings
# Create your views here.
from django.http import JsonResponse
from .decorators import require_api_key
from rest_framework import viewsets, permissions, status
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, permissions
from django.core.files.uploadedfile import UploadedFile
from rest_framework.parsers import MultiPartParser

# from django.contrib.auth.models import User

# User.objects.filter(username='mukesh').exists()


@require_api_key
def protected_view(request):
    return JsonResponse({"message": "This is a protected endpoint"})

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'uploadcover']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def upload_cover(self, request, pk=None):
        book = self.get_object()

        if 'cover' not in request.FILES:
            return Response({'error': 'No cover file provided'}, status=status.HTTP_400_BAD_REQUEST)

        cover_file = request.FILES['cover']
     
        if cover_file.size > settings.MAX_UPLOAD_SIZE:
            return Response({'error': 'File size exceeds 2MB limit'}, status=status.HTTP_400_BAD_REQUEST)

        if cover_file.content_type not in settings.ALLOWED_CONTENT_TYPES:
            return Response({'error': 'Invalid file type. Allowed types: jpg, png, webp'},
                            status=status.HTTP_400_BAD_REQUEST)

        book.image = cover_file
        book.save()

        return Response({
            'message': 'Cover uploaded successfully',
            'cover_url': request.build_absolute_uri(book.image.url)
        }, status=status.HTTP_200_OK)
            

