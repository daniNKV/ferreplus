from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        label = "Perfil de usuario"
        fields = ("avatar",)
        widgets = {
            "avatar": forms.ClearableFileInput(
                attrs={"class": "file-input file-input-bordered w-full"}
            )
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        try:
            # validate content type
            main, sub = avatar.content_type.split("/")
            if not (main == "image" and sub in ["jpeg", "pjpeg", "gif", "png", "webp", "aviff"]):
                raise forms.ValidationError("Please use a JPEG, " "GIF or PNG image.")

        except Exception as e:
            raise forms.ValidationError(f"Invalid image: {e}")

        return avatar
