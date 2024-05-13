from django.contrib import admin
from django import forms
from .models import Branch

admin.site.site_header = "Panel de Administración de Ferreplus"
admin.site.site_title = "Admin"
admin.site.index_title = "Ferreplus"


class BranchAdminForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "address", "opening_hour", "closing_hour"]

    def clean_(self):
        cleaned_data = super().clean()
        if not cleaned_data.name:
            raise forms.ValidationError("This field is required.")


class BranchAdmin(admin.ModelAdmin):
    form = BranchAdminForm
    list_display = ["name", "address", "opening_hour", "closing_hour"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model._meta.verbose_name = "Ferreteria"
        self.model._meta.verbose_name_plural = "Ferreterías"


admin.site.register(Branch, BranchAdmin)
