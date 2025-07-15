from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import Project, Purchase, Comment
from .serializers import ProjectSerializer, PurchaseSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
        
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        user = request.user
        if user.role != 'admin':
            return Response({"detail": "Permission denied"}, status=403)

        project = self.get_object()
        project.status = 'approved'
        project.save()
        return Response({"detail": "Project approved"}, status=200)    
    


class PurchaseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Purchase.objects.all()
        return Purchase.objects.filter(user=user)
    
    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.all()

        # Filter by approval
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by my uploads
        my_uploads = self.request.query_params.get('my_uploads')
        if my_uploads == 'true':
            queryset = queryset.filter(seller=user)

        return queryset
    
    


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Comment.objects.filter(project__id=project_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



