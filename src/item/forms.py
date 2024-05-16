from django import forms
from item.models import Item, Category
from owners.models import Branch


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "image", "category", "branch"]

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full bg-neutral border-dark"}
        ),
        label="Nombre",
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "textarea textarea-bordered w-full bg-neutral border-dark"}
        ),
        label="Descripción",
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={"class": "file-input file-input-bordered w-full border-1"}
        ),
        label="Imagen",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={"class": "select select-bordered w-full bg-neutral border-dark"}
        ),
        label="Categoría",
    )
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        # help_text="Selecciona la sucursal en la que desea realizar el trueque.",
        widget=forms.Select(
            attrs={"class": "select select-bordered w-full bg-neutral border-dark"}
        ),
        label="Sucursal",
    )

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return self.instance.image
        try:
            if hasattr(image, "content_type"):
                try:
                    main, sub = image.content_type.split("/")
                    if not (
                        main == "image"
                        and sub
                        in ["jpeg", "pjpeg", "gif", "png", "webp", "aviff", "aviff2"]
                    ):
                        raise forms.ValidationError(
                            "Por favor, utilice un formato de imagen conocido (e.g JPG, JPEG, WEBP, AVIFF)."
                        )
                except Exception as e:
                    raise forms.ValidationError(f"Imagen invalida: {e}")
        except Exception as e:
            raise forms.ValidationError(f"Imagen invalida: {e}")

        return image
