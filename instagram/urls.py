from django.urls import path,re_path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/', views.home, name='home'),
    path('posts/', views.post, name='posts'),
    path('create_post/', views.create_post, name='createpost'),
    path('comment/<post_id>', views.comment, name='comment'),
    path('add_comment/<post_id>', views.add_comment, name='add_comment'),
    path('profile/', views.profile, name='profile'),
    path('likes/<post_id>', views.likes, name="likes"),
    path('search/', views.search_user, name="search"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', views.registration, name='register'),
    path('', auth_views.LogoutView.as_view(template_name='logout.html'), name='home')

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
