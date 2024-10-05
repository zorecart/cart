

# middleware.py
"""from django.utils import timezone
from .models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is authenticated before accessing request.user
        if request.user.is_authenticated:
            # Log user activity
            UserActivity.objects.create(
                user=request.user,
                action=f"Visited {request.path}",
                timestamp=timezone.now()
            )
        return response


"""

