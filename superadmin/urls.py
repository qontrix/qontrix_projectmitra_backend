from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.AdminProjectListView.as_view()),
    path('projects/<int:pk>/approve/', views.ApproveProjectView.as_view()),
    path('projects/<int:pk>/reject/', views.RejectProjectView.as_view()),
    path('projects/<int:pk>/toggle-featured/', views.ToggleFeaturedView.as_view()),
    path('projects/<int:pk>/', views.EditProjectView.as_view()),
    path('dashboard/metrics/', views.AdminDashboardMetricsView.as_view()),
]
