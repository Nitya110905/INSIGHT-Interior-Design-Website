from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    contact=models.BigIntegerField()
    password = models.CharField(max_length=20)
    usertype = models.CharField(max_length=26, default="Dreamer")
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
    

class vendor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = (
        ('residence', 'residence'),
        ('corporate', 'corporate'),
    )
    ccategory = models.CharField(max_length=30, choices=category)
    ptitle = models.CharField(max_length=30)
    pprice = models.IntegerField()
    summary = models.TextField()
    pimage = models.ImageField(upload_to='interior')

    def __str__(self):
        return f"{self.ptitle}"
