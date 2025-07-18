from rest_framework import serializers
from projects.models import Project  # replace with actual model import

class ProjectEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
