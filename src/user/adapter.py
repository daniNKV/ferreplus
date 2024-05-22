from allauth.account.adapter import DefaultAccountAdapter
from rolepermissions.checkers import has_role
from .roles import Owner, Employee


class UsersAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.birth_date = data["birth_date"]
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        user.save()
        return user

    def get_signup_redirect_url(self, request):
        path = "/"
        return path

    def get_password_change_redirect_url(self, request):
        path = "/"
        return path

    def get_login_redirect_url(self, request):
        if has_role(request.user, Owner) or request.user.is_superuser:
            path = "/admin"
        elif has_role(request.user, Employee) or request.user.is_staff:
            path = "/accounts/employee"
        else:
            path = "/"
        return path
