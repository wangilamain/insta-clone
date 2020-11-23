from django.test import TestCase
from .models import *
from django.contrib.auth.models import User

class PostTest(TestCase):
    def setUp(self):
        self.post = Post('image',caption='caption',created_date='created_date')

    def test_instance(self):
        self.assertTrue(isinstance(self.post,Post))

class ProfileTest(TestCase):
    def setUp(self):
        self.user = User(username='user', email='email')
        self.user.save()
        self.profile = Profile(image='image', bio='bio', user=self.user)
    def test_instance(self):
        self.assertTrue(isinstance(self.profile, Profile))

    def test_save(self):
        self.profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)

class CommentTest(TestCase):
    def setUp(self):
        self.comment = Comment(comment='This is a good comment', create_date='created_date')

    def test_instance(self):
        self.assertTrue(isinstance(self.comment, Comment))

    def test_save(self):
        self.comment.save_comment()
        comment = Comment.objects.all()
        self.assertTrue(len(comment)>0)