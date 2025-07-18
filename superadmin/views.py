#1️⃣ View All Projects
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from superadmin.permissions import IsSuperAdmin
from projects.models import Project
from superadmin.serializers import ProjectEditSerializer

class AdminProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectEditSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]


#2️⃣ Approve Project
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ApproveProjectView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.status = 'approved'
            project.save()
            return Response({'message': 'Project approved'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


#3️⃣ Reject Project
class RejectProjectView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.status = 'rejected'
            project.save()
            return Response({'message': 'Project rejected'}, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


#4️⃣ Toggle Featured
class ToggleFeaturedView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
            project.is_featured = not project.is_featured
            project.save()
            return Response({'message': 'Toggled featured', 'is_featured': project.is_featured})
        except Project.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


#5️⃣ Edit Any Project (Full Update)
from rest_framework.generics import UpdateAPIView

class EditProjectView(UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectEditSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]


#6️⃣ Admin Dashboard Metrics
from rest_framework.views import APIView

class AdminDashboardMetricsView(APIView):
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = User.objects.count()
        sellers = User.objects.filter(role='seller').count()  # change to your role field
        projects = Project.objects.all()

        data = {
            'total_users': users,
            'total_sellers': sellers,
            'projects': {
                'approved': projects.filter(status='approved').count(),
                'pending': projects.filter(status='pending').count(),
                'rejected': projects.filter(status='rejected').count(),
            },
            'total_revenue': sum([p.price for p in projects if p.status == 'approved']),
            'top_projects': [
                {
                    'title': p.title,
                    'downloads': p.total_downloads
                }
                for p in projects.order_by('-total_downloads')[:3]
            ]
        }
        return Response(data)

