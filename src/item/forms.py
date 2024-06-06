from django import forms
from item.models import Item, Category
from owners.models import Branch


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "image", "category", "branch"]

    name = forms.CharField(
        label="Nombre",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "input input-bordered w-full bg-neutral border-dark"}
        ),
    )
    description = forms.CharField(
        label="Descripción",
        max_length=500,
        widget=forms.Textarea(
            attrs={"class": "textarea textarea-bordered w-full bg-neutral border-dark"}
        ),
    )
    image = forms.ImageField(
        label="Imagen",
        widget=forms.ClearableFileInput(
            attrs={"class": "file-input file-input-bordered w-full border-1"}
        ),
    )
    category = forms.ModelChoiceField(
        label="Categoría",
        queryset=Category.objects.all(),
        widget=forms.Select(
            attrs={"class": "select select-bordered w-full bg-neutral border-dark"}
        ),
    )
    branch = forms.ModelChoiceField(
        label="Sucursal",
        queryset=Branch.objects.all(),
        # help_text="Selecciona la sucursal en la que desea realizar el trueque.",
        widget=forms.Select(
            attrs={"class": "select select-bordered w-full bg-neutral border-dark"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            if cleaned_data.get('category') != instance.category:
                self.add_error('category', 'No se puede cambiar la categoria de un item.')
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

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 500:
            raise forms.ValidationError('La descripcion debe ser de 500 caracteres o menos')
        return description
