from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ProjectViewSet,
    BuyerProjectListView,
    PurchaseViewSet,
    CommentViewSet,
    WishlistViewSet,
    SellerEditProjectView,
    ApproveProjectEditView,
    RejectProjectEditView,
    MyProjectsView
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = router.urls + [
    # Seller edit API
    path("seller/projects/<int:pk>/edit/", SellerEditProjectView.as_view(), name="seller-edit-project"),

    # Admin approval/rejection APIs
    path("admin/projects/<int:pk>/approve/", ApproveProjectEditView.as_view(), name="approve-project"),
    path("admin/projects/<int:pk>/reject/", RejectProjectEditView.as_view(), name="reject-project"),
    
    #Seller dashboard
    path('seller/my-projects/', MyProjectsView.as_view(), name='my-projects'),
    
    #Buyer viewing all the projects
    path('buyer/projects/', BuyerProjectListView.as_view(), name='buyer-projects'),
    
    #Buyer wishlist controls
    path('buyer/wishlist/', WishlistViewSet.as_view({'get': 'list'}), name='wishlist-list'),
    path('buyer/wishlist/<int:pk>/', WishlistViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='wishlist-manage'),
]
