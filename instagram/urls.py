from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf import settings


urlpatterns = [
    path('posts/', views.post, name='posts'),
    path('post_create/', views.post_create, name="createpost"),
    path('profile/', views.profile, name='profile'),
    path('comment/<post_id>/', views.comment, name="comment"),
    path('commenting/<post_id>', views.commenting, name="commenting"),
    path('likes/<post_id>', views.likes, name="likes"),
    path('search/', views.search_user, name="search"),
    re_path(r'^follow/(?P<operation>.+)/(?P<pk>\d+)/$', views.follow, name="follow" ),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', views.registration, name='register'),
    path('', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='home')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)