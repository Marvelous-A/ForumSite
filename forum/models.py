from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    birth_date = models.CharField(max_length=150)
    vip_1 = models.BooleanField(default=False)
    vip_2 = models.BooleanField(default=False)
    vip_3 = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}'
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Chapter(models.Model):
    title = models.CharField(max_length=50)
    icon_img = models.ImageField(default=False, upload_to='for_site/')
    discription = models.CharField(max_length=500)
    # topics = models.ManyToManyField('Topic')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

class Topic(models.Model):
    title = models.CharField(max_length=50)
    image = models.URLField()
    discription = models.CharField(max_length=500)
    chapter = models.ManyToManyField(Chapter)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'
    
class Chat(models.Model):
    text_question = models.CharField(max_length=70)
    topic = models.ManyToManyField(Topic)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.text_question}'

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    text = models.CharField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='messages/', blank=True)
    question = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Profile: {self.author} | {self.question} | {self.text}'

class Views(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Views: {self.user}, {self.question}'