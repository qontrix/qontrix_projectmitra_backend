from rest_framework import serializers
from .models import Project, Purchase, Comment, WishlistRequest

class ProjectSerializer(serializers.ModelSerializer):
    thumbnail = serializers.URLField(required=False, allow_null=True)
    project_zip = serializers.URLField(required=False, allow_null=True)
    documentation = serializers.URLField(required=False, allow_null=True)

    class Meta:
        model = Project
        exclude = ['seller', 'upload_date', 'total_downloads', 'status', 'is_featured']

    def validate_price(self, value):
        if self.initial_data.get('project_type') == 'Paid' and value < 1:
            raise serializers.ValidationError("Paid projects must have price > 0")
        return value

    def validate_gallery_images(self, value):
        if not isinstance(value, list) or len(value) < 1:
            raise serializers.ValidationError("At least 1 gallery image is required.")
        return value




class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']



class WishlistRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistRequest
        fields = '__all__'
        read_only_fields = ['user', 'status']
