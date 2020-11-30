from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.http import Http404
from django.dispatch import receiver
from tinymce.models import HTMLField

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.user',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    caption = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return f'{self.author} Post'

    class Meta:
        db_table = 'post'
        ordering = ['-created_date']

    def addlikes(self):
        self.likes.count()

    def save_post(self):
        self.save()

    def delete_post(self):
        self.delete()

    @classmethod
    def search_by_author(cls,search_term):
        image = cls.objects.filter(author__username__icontains=search_term)
        return image

    @classmethod
    def get_post(cls,id):
        try:
            post = Post.objects.get(pk=id)
        except ObjectDoesNotExist:
            raise Http404()
        return post

class Profile(models.Model):


    bio = models.TextField(max_length=200, null=True, blank=True, default="bio")
    image = models.ImageField(upload_to='picture/', null=True, blank=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE, blank=True, related_name="profile")
    followers = models.ManyToManyField(User, related_name="followers", blank=True)
    following = models.ManyToManyField(User, related_name="following", blank=True)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def follow_user(self, follower):
        return self.following.add(follower)

    def unfollow_user(self, to_unfollow):
        return self.following.remove(to_unfollow)

    def is_following(self, checkuser):
        return checkuser in self.following.all()

    def get_number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        else:
            return 0

    def get_number_of_following(self):
        if self.following.count():
            return self.following.count()
        else:
            return 0

    @classmethod
    def search_users(cls, search_term):
        profiles = cls.objects.filter(user__username__icontains=search_term)
        return profiles

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.post.author}, {self.user.username}'

    class Meta:
        db_table = 'comment'

    def save_comment(self):
        self.save()