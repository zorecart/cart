

# custom_context_processors.py

from .models import Feature, Category, Product, BusinessEmail, Review, Document, Notification  # Import your models

def notifications(request):
    if request.user.is_authenticated:
        user = request.user
        notifications = Notification.objects.filter(user=user)
    else:
        notifications = []
    
    # Add your models to the context dictionary
    context = {
        'notifications': notifications,
        'features': Feature.objects.all(),
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
        'business_emails': BusinessEmail.objects.all(),
        'reviews': Review.objects.all(),
        'documents': Document.objects.all(),
    }

    return context

    
