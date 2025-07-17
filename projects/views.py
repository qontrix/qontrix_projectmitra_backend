from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from .models import Project, Purchase, Comment, WishlistRequest
from .serializers import ProjectSerializer, PurchaseSerializer, CommentSerializer, WishlistRequestSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView




from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from projects.permissions import IsSeller

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsSeller]

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




class WishlistRequestViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return WishlistRequest.objects.all()
        return WishlistRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        user = request.user
        if user.role != 'admin':
            return Response({"detail": "Permission denied"}, status=403)

        request_obj = self.get_object()
        request_obj.status = 'approved'
        request_obj.save()
        return Response({"detail": "Wishlist approved"}, status=200)
    
    
    
   

class SellerEditProjectView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, seller=request.user)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        data = request.data.copy()
        allowed_fields = [
            "title", "short_description", "full_description", "category",
            "tech_stack", "tools", "project_type", "price", "tags",
            "setup_video_url", "live_demo_url"
        ]

        pending_changes = {field: data.get(field) for field in allowed_fields if data.get(field) is not None}

        
        project.pending_edits = pending_changes
        project.is_edit_pending = True
        project.save()

        return Response({"message": "Project update submitted for admin review."}, status=200)



class ApproveProjectEditView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        if not project.is_edit_pending or not project.pending_edits:
            return Response({"error": "No pending edits to approve."}, status=400)

        # Apply pending edits
        for key, value in project.pending_edits.items():
            setattr(project, key, value)

        project.is_edit_pending = False
        project.pending_edits = None
        project.save()

        return Response({"message": "Edits approved and applied."}, status=200)

class RejectProjectEditView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        project.pending_edits = None
        project.is_edit_pending = False
        project.save()

        return Response({"message": "Pending edits rejected and discarded."}, status=200)
