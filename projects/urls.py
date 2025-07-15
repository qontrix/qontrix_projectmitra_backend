from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, PurchaseViewSet, CommentViewSet, WishlistRequestViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'purchases', PurchaseViewSet, basename='purchases')


router.register(r'comments', CommentViewSet, basename='comments')

router.register(r'wishlist', WishlistRequestViewSet, basename='wishlist')



urlpatterns = router.urls


