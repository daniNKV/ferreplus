from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from user.forms import UserEditForm
from .forms import ProfileEditForm
from django.forms import inlineformset_factory

from .models import Profile


@login_required
def profile_view(request, user_id):
    user_model = get_user_model()
    user = get_object_or_404(user_model, pk=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    return render(request, "profiles/profile_detail.html", {"profile": profile})


@login_required
def profile_edit(request, user_id):
    user_model = get_user_model()
    user = get_object_or_404(user_model, pk=user_id)

    if request.user.id != user.id:
        return HttpResponseForbidden()

    ProfileFormSet = inlineformset_factory(user_model, Profile, form=ProfileEditForm, extra=0, can_delete=False)

    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=user)
        profile_formset = ProfileFormSet(request.POST, request.FILES, instance=user)
        if user_form.is_valid() and profile_formset.is_valid():
            user_form.save()
            profile_formset.save()
            # return redirect("profile_view", user_id=request.user.pk)
    else:
        user_form = UserEditForm(instance=user)
        profile_formset = ProfileFormSet(instance=user)

    return render(
        request,
        "profiles/profile_edit.html",
        {"user_form": user_form, "profile_formset": profile_formset},)  