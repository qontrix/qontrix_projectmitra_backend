from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics

#from projectmitra.utils.email_utils import send_custom_email
from .models import Project, Purchase, Comment, Wishlist
from .serializers import ProjectSerializer, PurchaseSerializer, CommentSerializer, MyProjectsSerializer, WishlistSerializer, MyPurchaseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from projects.permissions import IsSeller, IsBuyer









class BuyerProjectListView(generics.ListAPIView):
    queryset = Project.objects.filter(status='approved')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsBuyer]




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
    
class MyProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ✅ Only allow sellers
        if user.role != 'seller':
            print(user.role)
            return Response({"error": "Only sellers can access this endpoint."}, status=status.HTTP_403_FORBIDDEN)

        # ✅ Filter base query by logged-in user
        projects = Project.objects.filter(seller=user)

        # ✅ Apply optional query params (e.g., status=Pending)
        status_param = request.query_params.get('status')
        if status_param:
            projects = projects.filter(status=status_param)

        edit_pending = request.query_params.get('edit_pending')
        if edit_pending is not None:
            if edit_pending.lower() == 'true':
                projects = projects.filter(is_edit_pending=True)
            elif edit_pending.lower() == 'false':
                projects = projects.filter(is_edit_pending=False)

        # ✅ Serialize and return
        serializer = MyProjectsSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PurchaseViewSet(viewsets.ReadOnlyModelViewSet): # for admin
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
    
class MyPurchasesView(APIView):    #buyer checking purchased projects
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        purchases = Purchase.objects.filter(buyer=request.user).select_related('project')
        serializer = MyPurchaseSerializer(purchases, many=True)
        return Response(serializer.data)    


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(project__id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_id'])
        serializer.save(user=self.request.user, project=project)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.user != request.user:
            return Response({"error": "You can delete only your own comments."}, status=403)
        return super().destroy(request, *args, **kwargs)





class WishlistViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        try:
            project = Project.objects.get(pk=pk)
            Wishlist.objects.get_or_create(user=request.user, project=project)
            return Response({"message": "Added to wishlist"}, status=status.HTTP_201_CREATED)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, project_id=pk)
            wishlist_item.delete()
            return Response({"message": "Removed from wishlist"}, status=status.HTTP_204_NO_CONTENT)
        except Wishlist.DoesNotExist:
            return Response({"error": "Item not in wishlist"}, status=status.HTTP_404_NOT_FOUND)
    
    
    
   

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
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        project.status = 'approved'
        project.save()

        """# Optional: Notify seller
        send_custom_email(
            subject="Project Approved ✅",
            message=f"Your project '{project.title}' has been approved by the admin.",
            recipient_list=[project.seller.email]
        )"""

        return Response({"message": "Project approved successfully"}, status=200)


class RejectProjectEditView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)

        project.status = 'rejected'
        project.save()

        # Optional: Notify seller
        """send_custom_email(
            subject="Project Rejected ❌",
            message=f"Your project '{project.title}' has been rejected by the admin.",
            recipient_list=[project.seller.email]
        )"""

        return Response({"message": "Project rejected successfully"}, status=200)
