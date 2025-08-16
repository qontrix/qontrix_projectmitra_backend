from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, CreateAdminUserView,UserListView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('create-admin/', CreateAdminUserView.as_view(), name='create-admin'),

     path('admin/users/', UserListView.as_view(), name='user-list'),

]