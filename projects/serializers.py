from rest_framework import serializers
from .models import Project, Purchase, Comment, WishlistRequest

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['seller', 'status']


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
