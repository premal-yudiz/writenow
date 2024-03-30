from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that should not require login
        exclude_urls = [reverse('login'), reverse('register'), '/admin/' ,'/social-auth/']

        # Check if the requested URL is in the exclude list
        if not request.user.is_authenticated and not any(request.path.startswith(url) for url in exclude_urls):
            return redirect('login')  # Redirect to login page if user is not authenticated
        response = self.get_response(request)
        return response


class LoginExistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that should redirect authenticated users
        redirect_urls = [reverse('login'), reverse('register')]

        if request.user.is_authenticated and request.path in redirect_urls:
            return redirect(reverse('index'))
        response = self.get_response(request)
        return response

