from django.db import models

# Create your models here.

class Wishlist(models.Model):
    user = models.CharField(max_length=255, unique=True)  # Firebase UID
    email = models.EmailField(blank=True, null=True)  # Email for easier lookup
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wishlists'

    def __str__(self):
        return f"Wishlist for {self.user}"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    reference = models.URLField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'wishlist_items'
        ordering = ['created_at']

    def __str__(self):
        return self.title
