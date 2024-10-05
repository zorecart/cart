
#Grade 2

#views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import PaymentForm
from django.views.generic import DetailView
from datetime import timedelta
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required
def payment_history(request):
    # Fetch both regular payments and crypto payments for the user
    regular_payments = Payment.objects.filter(user=request.user)
    crypto_payments = CryptoPayment.objects.filter(user=request.user)
    
    # Combine the two querysets
    combined_payments = sorted(
        list(regular_payments) + list(crypto_payments),
        key=lambda x: x.date, 
        reverse=True
    )

    paginator = Paginator(combined_payments, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'giftweb/payment_history.html', {'page_obj': page_obj})

#views.py

@login_required
def make_crypto_payment(request, model_name, product_id):
    if model_name == 'product':
        model = Product
    elif model_name == 'premium_product':
        model = PremiumProduct
    else:
        return HttpResponseBadRequest("Invalid model name.")

    product = get_object_or_404(model, id=product_id)
    wallets_instance = CryptoCurrency.objects.first()

    if request.method == 'POST':
        form = CryptoPaymentForm(request.POST, request.FILES)  # Ensure the correct form class is used
        if form.is_valid():
            payment = form.save(commit=False)
            payment.product = product
            payment.status = 'PENDING'
            payment.user = request.user
            # Calculate total amount based on product price and quantity
            payment.amount = product.price * form.cleaned_data['quantity']
            payment.save()
            return redirect('giftweb:crypto_payment_success')
        else:
            print(form.errors)  # Print form errors to the console
    else:
        form = CryptoPaymentForm()

    return render(request, 'giftweb/crypto_checkout.html', {'form': form, 'wallets_instance': wallets_instance, 'product': product})


@login_required
def crypto_payment_success(request):
    payment = CryptoPayment.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'giftweb/crypto_payment_success.html', {'payment': payment})




@login_required
def make_payment(request, model_name, product_id):
    if model_name == 'product':
        model = Product
    elif model_name == 'premium_product':
        model = PremiumProduct
    else:
        return HttpResponseBadRequest("Invalid model name.")

    product = get_object_or_404(model, id=product_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.product = product
            payment.status = 'PENDING'
            payment.user = request.user
            # Calculate total amount based on product price and quantity
            payment.amount = product.price * form.cleaned_data['quantity']
            payment.save()
            return redirect('giftweb:payment_success')
    else:
        form = PaymentForm()
    
    return render(request, 'giftweb/checkout.html', {'form': form, 'product': product})




def products_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    products = category.products.all()
    categories = Category.objects.all()
    
    paginator = Paginator(products, 5)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    
    return render(request, 'giftweb/products_by_category.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'giftweb/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Add some debugging output
        print("Product ID:", product.id)
        reviews = Review.objects.filter(product=product)
        print("Number of Reviews:", reviews.count())

        # Retrieve reviews for the product using the appropriate field (e.g., 'product' if that's the field name)
        reviews = Review.objects.filter(product=product)

        if product.discount:
            discounted_price = product.price - product.discount
            context['discounted_price'] = discounted_price

        # Retrieve the features associated with the product
        features = product.features.all()  # Assuming 'features' is the related name for the ManyToManyField

        context['categories'] = Category.objects.all()
        context['reviews'] = reviews
        context['features'] = features  # Pass the features to the template

        return context




from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def home(request):
    search_query = request.GET.get('q', '')

    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(features__name__icontains=search_query) |
            Q(categories__name__icontains=search_query)
        ).distinct()
        product_count = products.count()
    else:
        products = Product.objects.all()
        product_count = 0  # No need to count when not searching

    categories = Category.objects.all()

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        my_recs = profile.get_recommended_profiles()

    for product in products:
        if product.discount:
            discounted_price = product.price - (product.price * product.discount / 100)
            product.discounted_price = discounted_price

    current_time = timezone.now()

    # Pagination
    paginator = Paginator(products, 7)  # Show 7 products per page
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'product_count': product_count,
        'paginator': paginator,
    }

    if request.user.is_authenticated:
        context['my_recs'] = my_recs

    return render(request, 'giftweb/index.html', context)


from django.shortcuts import redirect

@login_required
def payment_success(request):
    payment = Payment.objects.filter(user=request.user).order_by('-id').first()

    return render(request, 'giftweb/payment_success.html', {'payment': payment})



def policy(request):
    terms = Terms.objects.all()

    
    context = {
        'terms': terms
    }
    return render(request, 'giftweb/policy.html', context)


    
def documents_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    documents = category.products.all()
    categories = Category.objects.all()
    
    paginator = Paginator(documents, 5)
    page = request.GET.get('page')
    documents = paginator.get_page(page)
    
    context = {
        'category': category,
        'categories': categories,
        'documents': documents
    }
    
    return render(request, 'giftweb/documents_by_category.html', context)

    


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'giftweb/document_detail.html'
    context_object_name = 'document'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document = self.get_object()

        context['categories'] = Category.objects.all()

        return context

def documentHome(request):
    documents = Document.objects.all()

    context = {
        'documents': documents
    }

    return render(request, 'giftweb/document_list.html', context)


class BusinessView(DetailView):
    model = BusinessEmail
    template_name = 'giftweb/business_detail.html'
    context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.get_object()

        # Add any additional context data you want to pass to the template here

        return context

def businessHome(request):
    business = BusinessEmail.objects.all()

    context = {
        'business': business
    }

    return render(request, 'giftweb/business_list.html', context)



def premium_home(request):
    products = PremiumProduct.objects.all()

    current_time = timezone.now()
    for product in products:

        if product.discount:
            discounted_price = product.price - (product.price * product.discount / 100)
            product.discounted_price = discounted_price

    return render(request, 'giftweb/products.html', {'products': products})


def about(request):
    return render(request, 'giftweb/about.html')

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'core/index.html', {'blogs': blogs})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        subject = request.POST['subject']
        email = request.POST['email']
        message = request.POST['message']
        user_id = request.POST['user_id']
        
        contact = Contactor(name=name, subject=subject, email=email, message=message)
        contact.save()

        messages.success(request, 'Your request has been submitted. We will get back to you soon!')
        
        return redirect( 'giftweb:home')

    return render(request, 'giftweb/contact.html')



