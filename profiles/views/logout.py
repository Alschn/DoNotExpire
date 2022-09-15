from django.contrib.auth.views import LogoutView as BaseLogoutView


class LogoutView(BaseLogoutView):
    template_name = 'profiles/logout.html'
