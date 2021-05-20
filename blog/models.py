from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name="url_category", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория(-ю)"
        verbose_name_plural = "Категории"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("category",kwargs = {"slug":self.slug})

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name="url_tag", unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ["title"]

    def get_absolute_url(self):
        return reverse("tag", kwargs = {"slug":self.slug})

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="url_post", unique=True)
    author = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    views = models.IntegerField(default=0, verbose_name="Кол-во просмотров")
    category = models.ForeignKey(Category, on_delete=models.PROTECT,verbose_name="Категория", related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Тэг", related_name="posts")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("post", kwargs={"slug":self.slug})

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="profile_photos/%Y/%m/%d/",default="profile_photos/default.jpg")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            output_size = (200,200)
            img.thumbnail(output_size)
            img.save(self.avatar.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано:")
    active = models.BooleanField(default=False)


    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)








