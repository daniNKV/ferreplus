from django import forms
from .models import Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        label = "Perfil de usuario"
        fields = ("avatar",)
        widgets = {
            "avatar": forms.ClearableFileInput(
                attrs={
                    "class": "file-input file-input-bordered w-full",
                    "required": False,
                }
            )
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if not avatar:
            return self.instance.avatar
        try:
            if hasattr(avatar, "content_type"):
                try:
                    main, sub = avatar.content_type.split("/")
                    if not (
                        main == "image"
                        and sub in ["jpeg", "pjpeg", "gif", "png", "webp", "aviff", "aviff2"]
                    ):
                        raise forms.ValidationError(
                            "Por favor, utilice un formato de imagen conocido (e.g JPG, JPEG, WEBP, AVIFF)."
                        )
                except Exception as e:
                    raise forms.ValidationError(f"Imagen invalida: {e}")
        except Exception as e:
            raise forms.ValidationError(f"Imagen invalida: {e}")

        return avatar
