from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    ProjectViewSet,
    PurchaseViewSet,
    CommentViewSet,
    WishlistRequestViewSet,
    SellerEditProjectView,
    ApproveProjectEditView,
    RejectProjectEditView
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'wishlist', WishlistRequestViewSet, basename='wishlist')

urlpatterns = router.urls + [
    # Seller edit API
    path("seller/projects/<int:pk>/edit/", SellerEditProjectView.as_view(), name="seller-edit-project"),

    # Admin approval/rejection APIs
    path("admin/projects/<int:pk>/approve/", ApproveProjectEditView.as_view(), name="approve-project"),
    path("admin/projects/<int:pk>/reject/", RejectProjectEditView.as_view(), name="reject-project"),
]
