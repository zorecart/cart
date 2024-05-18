
#Grade 2

#models.py

from django.db import models
from datetime import datetime
import random
import string
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from cloudinary.models import CloudinaryField

from django.conf import settings
from django_countries.fields import CountryField




User = settings.AUTH_USER_MODEL


def generate_tracking_id():
    # Generate 3 random alphabets
    alphabets = ''.join(random.choice(string.ascii_letters) for _ in range(3))
    
    # Generate 6 random digits
    numbers = ''.join(random.choice(string.digits) for _ in range(6))
    
    # Combine alphabets and numbers
    tracking_id = alphabets + numbers
    
    return tracking_id

class Feature(models.Model):
    name = models.CharField(max_length=255, verbose_name='Feature Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'E- FEATURE'
        verbose_name_plural = 'E- FEATUREs'

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'

    class Meta:
        verbose_name = 'F - Categories'
        verbose_name_plural = 'F - Categories'


class Product(models.Model):

    STATUS_CHOICES = [
        ('ACTIVE', 'ACTIVE'),
        ('UNAVAILABLE', 'UNAVAILABLE')
    ]

    name = models.CharField(max_length=255)
    description = RichTextUploadingField( blank=True)
    features = models.ManyToManyField('Feature', related_name='website_products', blank=True)
    customer_reviews = models.ManyToManyField('Review', related_name='website_products', blank=True)

    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=17, default='ACTIVE')
    sold = models.IntegerField(verbose_name='copies sold', null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField("products", blank=True, default=None)
    image2 = CloudinaryField("products", null=True, blank=True)
    image3 = CloudinaryField("products", null=True, blank=True)
    image4 = CloudinaryField("products", null=True, blank=True)
    image5 = CloudinaryField("products", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'A- ITEMS'
        verbose_name_plural = 'A- ITEMS'



class CryptoCurrency(models.Model):
    bitcoin = models.CharField(max_length=500)
    ethereum = models.CharField(max_length=500)
    usdt_erc20 = models.CharField(max_length=500)
    usdt_trc20 = models.CharField(max_length=500)
    solana = models.CharField(max_length=500)

    class Meta:
        verbose_name = "B - Wallets"
        verbose_name_plural = "B - Wallets"

    def __str__(self):
        return "Crypto Wallets"



class CryptoPayment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('USDT_ERC20', 'USDT ERC20'),
        ('USDT_TRC20', 'USDT TRC20'),
        ('ETHEREUM', 'Ethereum'),
        ('BITCOIN', 'Bitcoin'),
        ('SOLANA', 'Solana')
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete'),
        ('CANCELLED', 'Cancelled'),
        ('DECLINED', 'Declined')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, blank=True, default=generate_tracking_id)

    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    proof_of_pay = CloudinaryField("zorevina", default=None)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now=False)  # Make date field not auto_now
    quantity = models.PositiveIntegerField(default=1)  # Add quantity field


    country = CountryField(multiple=False, null=True, blank=True)

    full_name = models.CharField(max_length=255, default="nil")
    street_address = models.CharField(max_length=200, default="nil")
    apartment_address = models.CharField(max_length=200, default="nil")
    phone_number = models.CharField(max_length=200, default="nil")

    def update_balance(self):
        if self.status == 'COMPLETE':
            self.user.balance += self.amount
        elif self.status == 'CANCELLED':
            self.user.balance -= self.amount
        self.user.save()    

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
        self.amount = self.product.price * self.quantity  # Calculate total amount
        super().save(*args, **kwargs)
        
        if self.pk:  # Check if the CryptoPayment instance exists (i.e., it's being updated)
            old_status = CryptoPayment.objects.get(pk=self.pk).status
            if old_status != self.status:  # Check if status has changed
                self.update_balance()
        elif self.status == 'COMPLETE':
            self.user.balance += self.amount
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} for {self.product}"

    class Meta:
        verbose_name = "2- Crypto Payment"
        verbose_name_plural = "2- Crypto Payments"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete'),
        ('CANCELLED', 'Cancelled')
    ]
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, blank=True, default='')
    payment_id = models.CharField(max_length=100, blank=True, default=generate_tracking_id)

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now=False)  # Make date field not auto_now
    quantity = models.PositiveIntegerField(default=1)  # Add quantity field

    
    country = CountryField(multiple=False, null=True, blank=True)
    full_name = models.CharField(max_length=255, default="nil")
    street_address = models.CharField(max_length=200, default="nil")
    apartment_address = models.CharField(max_length=200, default="nil")
    phone_number = models.CharField(max_length=200, default="nil")

    proof_of_pay = CloudinaryField('payment_proofs/', default="default_payment_proof.png")
    gift_card_type = models.CharField(choices=[('apple', 'Apple Card'), ('amazon', 'Amazon Card'), ('steam', 'Steam Card'), ('xbox', 'Xbox Card')], max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    completed = models.BooleanField(default=False)

    def update_balance(self):
        if self.status == 'COMPLETE':
            self.user.balance += self.amount
        elif self.status == 'CANCELLED':
            self.user.balance -= self.amount
        self.user.save()    

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now()
        self.amount = self.product.price * self.quantity  # Calculate total amount
        super().save(*args, **kwargs)
        
        if self.pk:  # Check if the Payment instance exists (i.e., it's being updated)
            old_status = Payment.objects.get(pk=self.pk).status
            if old_status != self.status:  # Check if status has changed
                self.update_balance()
        elif self.status == 'COMPLETE':
            self.user.balance += self.amount
            self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount} for {self.product}"

    class Meta:
        verbose_name = "1- CARD Payment"
        verbose_name_plural = "1- CARD Payment"


class BusinessEmail(models.Model):
    email_address = models.EmailField(unique=True, verbose_name='Email Address')
    type = models.CharField(
        max_length=50,
        choices=(
            ('Corporate', 'Corporate'),
            ('Marketing', 'Marketing'),
            ('Support', 'Support'),
            ('Sales', 'Sales'),
            ('Airline', 'Airline'),
            ('Other', 'Other'),
        ),
        default='Corporate',
        verbose_name='Email Type'
    )
    category = models.CharField(max_length=100, verbose_name='Email Category')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    description = RichTextUploadingField( blank=True, verbose_name='Mail Description')
    image = CloudinaryField('business_email_images/', blank=True, null=True)

    def __str__(self):
        return self.email_address

    class Meta:
        verbose_name = 'C - Business Email'
        verbose_name_plural = 'Business Emails'



class Review(models.Model):
    customer_name = models.CharField(max_length=255, verbose_name='Customer Name')
    image = CloudinaryField('reviews/', default="default_product_image.png")

    content = RichTextUploadingField( blank=True, verbose_name='Review Content')
    star_rating = models.PositiveIntegerField(
        verbose_name='Star Rating',
        choices=((1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=0)  # Set the default product to Product with ID 1

    def __str__(self):
        return f"{self.customer_name}'s Review"

    class Meta:
        verbose_name = 'D - REVIEWS'
        verbose_name_plural = 'D - REVIEWSs'



class Document(models.Model):
    # Document Types
    DOCUMENT_TYPES = (
        ('Consignment', 'Consignment'),
        ('Bank Documents', 'Bank Documents'),
        ('Email Write-ups', 'Email Write-ups'),
        ('Crypto Request Documents', 'Crypto Request Documents'),
        ('Real Estate Documents', 'Real Estate Documents'),
        ('Legal Affairs', 'Legal Affairs'),
        ('Travel/Ticket', 'Travel/Ticket'),
        # Add more document types as needed
    )
    document_type = models.CharField(max_length=255, choices=DOCUMENT_TYPES, verbose_name='Document Type')
    categories = models.ManyToManyField(Category, related_name='documents', blank=True)
    features = models.ManyToManyField('Feature', related_name='Document_products', blank=True)

    # Document Title
    title = models.CharField(max_length=255, verbose_name='Document Title')
    sold = models.IntegerField(verbose_name='Copies-Sold', null=True, blank=True)

    # Document Description
    description = RichTextUploadingField( blank=True, verbose_name='Document Description')

    # Upload Document File
    document_file = CloudinaryField('documents/',default=('qww.png'))
    document_file1 = CloudinaryField('documents/',default=('qww.png'), null=True, blank=True )
    document_file2 = CloudinaryField('documents/',default=('qww.png'), null=True, blank=True )
    document_file3 = CloudinaryField('documents/',default=('qww.png'), null=True, blank=True )
    document_file4 = CloudinaryField('documents/',default=('qww.png'), null=True, blank=True )

    # Date Created
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date Created')

    # Document Status
    LEGAL_STATUS_CHOICES = (
        ('Legal', 'Legal'),
        ('Legitimate', 'Legitimate'),
    )
    document_status = models.CharField(max_length=20, choices=LEGAL_STATUS_CHOICES, default='Legal', verbose_name='Document Status')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'B- Documents'


class Terms(models.Model):
    name= models.CharField(max_length=255, verbose_name='Privacy/conditions Title')
    conditions = RichTextUploadingField( blank=True, verbose_name='Condition Description')

    class Meta:
        verbose_name_plural = 'Policy'



class Blog(models.Model):
    topic = models.CharField(max_length=255)
    image = models.ImageField('blog_images/')
    body = models.CharField(max_length=255)
    date = models.DateField()
    read_more = models.CharField(max_length=255, default='GiftCard')

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'xBlog'
        verbose_name_plural = 'xBlogs'

class Contactor(models.Model):
  name = models.CharField(max_length=200)
  email = models.CharField(max_length=100)
  subject = models.CharField(max_length=200, blank=True)

  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)

  def __str__(self):
    return self.name

    class Meta:
        verbose_name = "xContacts"
        verbose_name_plural = "xContacts"

class Notification(models.Model):    
  name = models.CharField(max_length=200)
  user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notify',)
  image =  CloudinaryField('notification_images/', default="default_notification_image.png")
  subject = models.CharField(max_length=200, blank=True)
  message = models.TextField(blank=True)
  contact_date = models.DateTimeField(default=datetime.now, blank=True)


  def __str__(self):
    return self.name

    class Meta:
        verbose_name = 'xNotification'
        verbose_name_plural = 'xNotifications'
