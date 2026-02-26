from django.db import models
from django.utils.text import slugify
import uuid

class User(models.Model):
    name = models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    contact=models.BigIntegerField()
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=26)
    uprofile = models.ImageField(upload_to='user_profiles/', null=True, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)

    @property
    def image_url(self):
        if self.uprofile and hasattr(self.uprofile, 'url'):
            return self.uprofile.url
        else:
            return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnSSxXHLqu5lsHYkFlZkvXuo2ZamNvdqLiCg&s"

    def __str__(self):
        return f"{self.name}"
    

class Designer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = (
        ('residential', 'residential'),
        ('commercial', 'commercial'),
    )
    dcategory = models.CharField(max_length=30, choices=category)
    dname = models.CharField(max_length=30)
    dstartprice = models.IntegerField()
    dsummary = models.TextField()
    dimage = models.ImageField(upload_to='interior')
    dimage2 = models.ImageField(upload_to='interior', null=True, blank=True)
    dimage3 = models.ImageField(upload_to='interior', null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.dname}"
    
    @property
    def project_code(self):
        return f"ARC-{self.id:04d}"
    
    class Meta:
        unique_together = [['user', 'dname']]

        verbose_name = "Interior Project"
        verbose_name_plural = "Interior Projects"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.dname)
            if Designer.objects.filter(slug=base_slug).exists():
                self.slug = f"{base_slug}-{str(uuid.uuid4())[:4]}"
            else:
                self.slug = base_slug
        super().save(*args, **kwargs)


class Moodboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Designer, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['user', 'design']]

class Booking(models.Model):
    dreamer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    designer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    design = models.ForeignKey(Designer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
