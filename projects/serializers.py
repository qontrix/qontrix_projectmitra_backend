from rest_framework import serializers
from .models import Project, Purchase, Comment, Wishlist

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

class MyProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'status',
            'is_edit_pending',
            'price',
            'project_type',
            'upload_date',
            'thumbnail',  # Optional visual aid in frontend
        ]


class AdminProjectSerializer(serializers.ModelSerializer): #for admin to see project info
    class Meta:
        model = Project
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):    #for seller side
    class Meta:
        model = Purchase
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']

class MyPurchaseSerializer(serializers.ModelSerializer):   #for buyer side
    project_title = serializers.CharField(source='project.title', read_only=True)
    project_id = serializers.IntegerField(source='project.id', read_only=True)
    project_price = serializers.DecimalField(source='project.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'project_id', 'project_title', 'project_price', 'purchase_date']

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'text', 'rating', 'timestamp', 'project']
        read_only_fields = ['user_name', 'timestamp', 'project']




class WishlistSerializer(serializers.ModelSerializer):
    project_title = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = Wishlist
        fields = ['id', 'project', 'project_title', 'added_on']
