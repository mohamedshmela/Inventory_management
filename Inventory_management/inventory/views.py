from rest_framework import generics, filters 
from django_filters.rest_framework import DjangoFilterBackend
from .models import InventoryItem, InventoryChangeLog
from .serializers import InventoryChangeLogSerializer, InventoryItemSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class InventoryItemListCreate(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    # Add filter backends for filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields to filter by (e.g., category, price)
    filterset_fields = ['category', 'price']

    # Fields that can be searched (e.g., name, description)
    search_fields = ['name', 'description']

    # Fields that can be used for ordering (e.g., name, quantity, price)
    ordering_fields = ['name', 'quantity', 'price', 'date_added']

    def get_queryset(self):

        # Get inventory items belonging to the authenticated user
        queryset = InventoryItem.objects.filter(user=self.request.user)

        # Additional filtering based on query parameters
        low_stock_threshold = self.request.query_params.get('low_stock', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

         # Filter by price range
        if min_price is not None and max_price is not None:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        elif min_price is not None:
            queryset = queryset.filter(price__gte=min_price)
        elif max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        # Filter for low stock items (quantity below a specified threshold)
        if low_stock_threshold is not None:
            queryset = queryset.filter(quantity__lt=low_stock_threshold)

         # Default ordering by 'name' unless specified otherwise
        ordering = self.request.query_params.get('ordering', 'name')
        return queryset.order_by(ordering)

    # def perform_create(self, serializer):
    #     inventory_item = serializer.save(user=self.request.user)
    #     # Log the initial inventory quantity
    #     InventoryChangeLog.objects.create(
    #         inventory_item=inventory_item,
    #         user=self.request.user,
    #         quantity_change=inventory_item.quantity  # Log initial quantity
    #     )

    
    # def perform_update(self, serializer):
    #      # Retrieve the current instance from the database
    #     instance = InventoryItem.objects.get(pk=instance.pk)
    #     previous_quantity = instance.quantity # Store previous quantity
    #     updated_instance = serializer.save()
    #     # Calculate quantity difference (new - old)

    #     # previous_quantity = InventoryItem.objects.get(pk=instance.pk).quantity
    #     quantity_difference = updated_instance.quantity - previous_quantity
        
    #     if quantity_difference != 0:
    #         # Log the change in quantity
    #         InventoryChangeLog.objects.create(
    #             inventory_item=instance,
    #             user=self.request.user,
    #             quantity_change=quantity_difference
    #         )

class InventoryItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        old_quantity = instance.quantity #getting the old quantity of the item before performing update
        # print(f"old quantity for {self.get_object()} is {old_quantity}")

        instance = serializer.save() #performing update
        new_quantity = instance.quantity #getting the new quantity of the same item after updating
        # print(f"new quantity for {self.get_object()} is {new_quantity}")

        quantity_change = new_quantity - old_quantity
        # print(f"quantity change for {self.get_object()} is {quantity_change}")

        if quantity_change != 0:
            InventoryChangeLog.objects.create(
                inventory_item=instance,
                user=self.request.user,  
                quantity_change=quantity_change
            )
        return instance
    
    # def update(self, request, *args, **kwargs):
    #     # Get the instance (inventory item) to be updated
    #     instance = self.get_object()
    #     old_quantity = instance.quantity  # Store the old quantity

    #     # Call the superclass update method
    #     response = super().update(request, *args, **kwargs)

    #     # Calculate the quantity change
    #     new_quantity = instance.quantity  # This is updated after calling super().update
    #     quantity_change = new_quantity - old_quantity

    #     # Log the change if the quantity has changed
    #     if quantity_change != 0:
    #         InventoryChangeLog.objects.create(
    #             inventory_item=instance,
    #             user=request.user.username,  # or request.user if you want the full User object
    #             quantity_change=quantity_change
    #         )

    #     return response
    

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)  # Only allow access to the logged-in user's data



class InventoryChangeLogList(generics.ListAPIView):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        inventory_item_id = self.kwargs['item_id']
        # print(InventoryChangeLog.objects.all())
        return InventoryChangeLog.objects.filter(inventory_item__id=inventory_item_id).order_by('-timestamp')
    

