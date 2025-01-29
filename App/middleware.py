from django.shortcuts import redirect
from django.urls import reverse

class RedirectLoggedInUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == reverse('login'):
            return redirect('home')
        if request.user.is_authenticated and request.path == reverse('register'):
            return redirect('home')
        if request.user.is_authenticated and request.path == reverse('job_seeker_register'):
            return redirect('home')
        if request.user.is_authenticated and request.path == reverse('hirer_register'):
            return redirect('home')
        if request.user.is_authenticated and request.path == reverse('landingPage'):
            return redirect('home')
        
        response = self.get_response(request)
        return response
