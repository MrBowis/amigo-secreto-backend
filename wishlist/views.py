from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def get_queryset(self):
        """Filter wishlists by user if user parameter is provided"""
        queryset = Wishlist.objects.all()
        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user=user_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """Create or update wishlist for a user"""
        user_id = request.data.get('user')
        
        if not user_id:
            return Response(
                {'error': 'El campo user es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if wishlist already exists for this user
        try:
            wishlist = Wishlist.objects.get(user=user_id)
            serializer = self.get_serializer(wishlist, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Wishlist.DoesNotExist:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
