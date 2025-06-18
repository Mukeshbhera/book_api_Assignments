from rest_framework import serializers
from .models import Book
from datetime import date

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_isbn(self, value):
        if len(value) != 13:
            raise serializers.ValidationError("ISBN must be exactly 13 characters.")
        return value

    def validate_page_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Page count must be at least 1.")
        return value

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Published date cannot be in the future.")
        return value

    def validate_image(self, value):
        # Validate file type
        valid_types = ['image/jpeg', 'image/png', 'image/webp']
        if value.content_type not in valid_types:
            raise serializers.ValidationError("Invalid file type. Only JPEG, PNG, or WEBP are allowed.")
        
        # Validate file size
        max_size = 2 * 1024 * 1024  # 2MB
        if value.size > max_size:
            raise serializers.ValidationError("Cover image size cannot exceed 2MB.")
        
        return value
