from rest_framework import serializers
from .models import Wishlist, WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = WishlistItem
        fields = ['id', 'title', 'reference', 'created_at']
        read_only_fields = ['created_at']


class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True)
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'email', 'items', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        wishlist = Wishlist.objects.create(**validated_data)
        
        for item_data in items_data:
            WishlistItem.objects.create(wishlist=wishlist, **item_data)
        
        return wishlist

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        instance.user = validated_data.get('user', instance.user)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        if items_data is not None:
            # Delete existing items and create new ones
            instance.items.all().delete()
            for item_data in items_data:
                WishlistItem.objects.create(wishlist=instance, **item_data)
        
        return instance
