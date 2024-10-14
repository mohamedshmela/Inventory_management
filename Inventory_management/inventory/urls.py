from django.urls import path
from .views import InventoryItemListCreate, InventoryItemDetail, UserListCreateView, UserRetrieveUpdateDestroyView, InventoryChangeLogList, InventoryItemQuantity, InventoryItemQuantityDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('items/', InventoryItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', InventoryItemDetail.as_view(), name='item-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('items/<int:item_id>/changes/', InventoryChangeLogList.as_view(), name='inventory-change-log'),
    path('items/quantity/', InventoryItemQuantity.as_view(), name="Items-quantity"),
    path('items/<int:pk>/quantity/', InventoryItemQuantityDetailView.as_view(), name="inventory-item-quantity")
]
