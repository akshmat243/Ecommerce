import uuid
from django.db import models
from django.utils.text import slugify
from accounts.models import User
from catalog.models import Product


class ProductReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin moderation
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        unique_together = ("product", "user")

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.product.slug}-{self.user.email}-review")
            slug = base_slug
            counter = 1
            while ProductReview.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review by {self.user.email} on {self.product.name}"

class ReviewComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_comments")

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.email} on Review {self.review.id}"

class ProductQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="questions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")

    question = models.TextField()
    is_answered = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.question[:50]}..."

class ProductAnswer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(ProductQuestion, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")

    answer = models.TextField()
    is_accepted = models.BooleanField(default=False)  # Mark best answer

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"A by {self.user.email} on Q {self.question.id}"

class ContentEngagement(models.Model):
    ENGAGEMENT_TYPES = [
        ("like", "Like"),
        ("dislike", "Dislike"),
        ("helpful", "Helpful"),
        ("report", "Report"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="engagements")

    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, null=True, blank=True, related_name="engagements")
    comment = models.ForeignKey(ReviewComment, on_delete=models.CASCADE, null=True, blank=True, related_name="engagements")
    answer = models.ForeignKey(ProductAnswer, on_delete=models.CASCADE, null=True, blank=True, related_name="engagements")

    engagement_type = models.CharField(max_length=20, choices=ENGAGEMENT_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Content Engagement"
        verbose_name_plural = "Content Engagements"

    def __str__(self):
        target = self.review or self.comment or self.answer
        return f"{self.user.email} {self.engagement_type} {target}"
