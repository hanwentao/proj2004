from .models import get_linked_classes


class LinkedClassesMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            user.linked_classes = get_linked_classes(user)
        response = self.get_response(request)
        return response
