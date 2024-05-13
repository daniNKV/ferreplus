from allauth.account.adapter import DefaultAccountAdapter
from rolepermissions.checkers import has_role
from .roles import Owner

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
        self.populate_username(request, user)
        user.save()
        return user

    def get_signup_redirect_url(self, request):
        path = "/"
        return path

    def get_password_change_redirect_url(self, request):
        path = "/"
        return path
    
    def get_login_redirect_url(self, request):
        if has_role(request.user, Owner) or request.user.is_superuser:  # Replace with your condition for checking the user's role
            path = "/admin"  # Replace with your admin panel URL
        else:
            path = "/"  # Replace with your user panel URL
        return path
