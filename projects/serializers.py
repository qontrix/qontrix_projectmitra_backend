# projects/serializers.py

from rest_framework import serializers
from .models import Project, Purchase

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
