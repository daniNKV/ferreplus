from django.contrib import admin
from django import forms
from user.models import Employee
from .models import Branch
from .models import Product

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


class EmployeeInline(admin.TabularInline):  # or admin.StackedInline if you prefer
    model = Employee
    extra = 0  # Number of extra forms to display
    actions = None

    def has_change_permission(self, request, obj=None):
        return False


class BranchAdmin(admin.ModelAdmin):
    form = BranchAdminForm
    inlines = [EmployeeInline]
    list_display = ["name", "address", "opening_hour", "closing_hour"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model._meta.verbose_name = "Ferreteria"
        self.model._meta.verbose_name_plural = "Ferreterías"


admin.site.register(Branch, BranchAdmin)

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "image"]

    def clean_(self):
        cleaned_data = super().clean()
        if not cleaned_data.name:
            raise forms.ValidationError("This field is required.")

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ["title", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model._meta.verbose_name = "Producto"
        self.model._meta.verbose_name_plural = "Productos"

admin.site.register(Product, ProductAdmin)