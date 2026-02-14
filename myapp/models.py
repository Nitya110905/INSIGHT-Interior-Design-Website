from django.db import models
from django.utils.text import slugify

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    contact=models.BigIntegerField()
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=26)
    uprofile = models.ImageField(upload_to='user_profiles/', null=True, blank=True)

    @property
    def image_url(self):
        if self.uprofile and hasattr(self.uprofile, 'url'):
            return self.uprofile.url
        else:
            # Return your default Google URL here
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

    def __str__(self):
        return f"{self.dname}"
    
    @property
    def project_code(self):
        return f"ARC-{self.id:04d}"
    
    class Meta:
        unique_together = [['user', 'dname']]

        verbose_name = "Interior Project"
        verbose_name_plural = "Interior Projects"
