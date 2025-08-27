import uuid
from django.db import models
from django.utils.text import slugify
from accounts.models import User
from catalog.models import Product


class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
        unique_together = ("user", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user.email}-{self.name}")
            slug = base_slug
            counter = 1
            while Wishlist.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

class WishlistItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
        unique_together = ("wishlist", "product")

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.name}"

class CompareList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="compare_list")
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compare List"
        verbose_name_plural = "Compare Lists"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user.email}-compare")
            slug = base_slug
            counter = 1
            while CompareList.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compare List of {self.user.email}"

class CompareItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    compare_list = models.ForeignKey(CompareList, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="compare_items")

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compare Item"
        verbose_name_plural = "Compare Items"
        unique_together = ("compare_list", "product")

    def __str__(self):
        return f"{self.product.name} in Compare List of {self.compare_list.user.email}"
