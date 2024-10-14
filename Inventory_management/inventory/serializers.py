from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'quantity', 'price', 'category', 'date_added', 'last_updated']

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class InventoryChangeLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # To display the username instead of the user ID

    class Meta:
        model = InventoryChangeLog
        fields = ['inventory_item', 'user', 'quantity_change', 'timestamp']

class InventoryItemsQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['id', 'name' , 'quantity']
