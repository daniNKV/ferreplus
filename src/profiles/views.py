from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import Profile


def profile_view(request, user_id):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, "profiles/profile_detail.html", { 'profile': profile})
