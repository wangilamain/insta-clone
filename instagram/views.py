from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404
# from . forms import ImageForm, ProfileForm, CommentForm
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .models import *



@login_required(login_url='/accounts/login/')
def Home(request):
    images = Image.get_all_images()
    profiles = Profile.objects.all()
    comments = Comments.objects.all()
    profile_pic = User.objects.all()
    form = CommentForm()
    id = request.user.id
    title = 'Home'
    return render(request, 'index.html', {'title':title, 'images':images, 'profile_pic':profile_pic, 'form':form, 'comments':comments, 'profiles':profiles})


@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk = image_id)
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.image = image
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()

    title = 'Home'
    return render(request, 'index.html', {'title':title})


@login_required(login_url='/accounts/login/')
def profile(request, username):
    title = 'Profile'
    profile = User.objects.get(username=username)
    comments = Comments.objects.all()
    users = User.objects.get(username=username)
    
    id = request.user.id
    form = CommentForm()

    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)

    images = Image.get_profile_pic(profile.id)
    return render(request, 'profile/profile.html', {'title':title, 'comments':comments, 'profile':profile, 'profile_details':profile_details, 'images':images, 'form':form})


@login_required(login_url='/accounts/login/')
def edit_profile(request):
    title = 'Edit Profile'
    profile = User.objects.get(username=request.user)
    try:
        profile_details = Profile.get_by_id(profile.id)
    except:
        profile_details = Profile.filter_by_id(profile.id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            
            form.save()
            return redirect('profile', username=request.user)
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'profile/edit_profile.html', {'form':form, 'profile_details':profile_details})


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username__icontains = search_term)
        message = f"{search_term}"
        profile_pic = User.objects.all()
        return render(request, 'search.html', {'message':message, 'users':searched_users, 'profile_pic':profile_pic})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {'message':message})


@login_required(login_url='/accounts/login/')
def upload_image(request):

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.profile = request.user
            upload.save()
            return redirect('index')
    else:
        form = ImageForm()
    
    return render(request, 'upload.html', {'form':form})


# add like function


def follow_unfollow(request):
    if request.method == "POST":
        profile = User.objects.get(username=request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in profile.following.all():
            profile.following.remove(obj.user)
        else:
            profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:all-profiles-view')
