from allauth.account.adapter import DefaultAccountAdapter


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

    # TODO: Agregar logica de redireccion segun el usuario
    def get_signup_redirect_url(self, request):
        path = "/"
        return path

    def get_login_redirect_url(self, request):
        path = "/"
        return path
