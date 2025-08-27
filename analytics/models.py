import uuid
from django.db import models
from django.utils.text import slugify
from accounts.models import User
from catalog.models import Product


class SearchQuery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="search_queries")
    result_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Search Query"
        verbose_name_plural = "Search Queries"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.query}-{self.user_id or 'guest'}")
            slug = base_slug
            counter = 1
            while SearchQuery.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"'{self.query}' by {self.user.email if self.user else 'Guest'}"

class UserActivity(models.Model):
    ACTION_VIEW = "view"
    ACTION_ADD_TO_CART = "add_to_cart"
    ACTION_PURCHASE = "purchase"
    ACTION_WISHLIST = "wishlist"

    ACTION_CHOICES = [
        (ACTION_VIEW, "View"),
        (ACTION_ADD_TO_CART, "Add to Cart"),
        (ACTION_PURCHASE, "Purchase"),
        (ACTION_WISHLIST, "Wishlist"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="activities")
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.user_id or 'guest'}-{self.product_id or 'na'}-{self.action}")
            slug = base_slug
            counter = 1
            while UserActivity.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email if self.user else 'Guest'} {self.action} {self.product or ''}"

class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recommendations")
    score = models.FloatField(default=0.0)  # Confidence or relevance score
    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
        unique_together = ("user", "product")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"rec-{self.user_id or 'global'}-{self.product_id}")
            slug = base_slug
            counter = 1
            while Recommendation.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Recommendation: {self.product} → {self.user.email if self.user else 'Global'}"
