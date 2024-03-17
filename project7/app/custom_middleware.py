from django.http import Http404, HttpResponseRedirect
from django.urls import resolve


class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path.startswith('/admin/'):
            if not request.user.is_staff:  # Check if the user is not an admin
                return HttpResponseRedirect('/404/')# Redirect to a 404 page
        response = self.get_response(request)
        return response


class InvalidUrlMiddleWare:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            resolve(request.path_info)
        except Http404:
            return HttpResponseRedirect('/404/')
        return response
