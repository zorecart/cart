
from django.contrib import admin
from .models import *



class TermsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

admin.site.register(Terms, TermsAdmin)


class ContactorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_date')
    list_filter = ('name', 'email')
    search_fields = ('email', 'name')
    date_hierarchy = 'contact_date'

admin.site.register(Contactor, ContactorAdmin)

"""
class BusinessEmailAdmin(admin.ModelAdmin):
    list_display = ['email_address', 'type', 'category', 'is_active']
    list_filter = ['type', 'category', 'is_active']
    search_fields = ['email_address', 'category']
    list_editable = ['is_active']

admin.site.register(BusinessEmail, BusinessEmailAdmin)
"""


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'content', 'star_rating']  # Add 'star_rating' to the list_display

admin.site.register(Review, ReviewAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'get_categories')
    list_filter = ('status', 'categories',)
    search_fields = ('name',)

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'product', 'amount', 'status', 'completed')
    list_filter = ('status', 'completed')
    actions = ['mark_as_complete']

    def mark_as_complete(self, request, queryset):
        queryset.update(status='COMPLETED', completed=True)
    mark_as_complete.short_description = "Mark selected payments as complete"

    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'User'
"""
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_type', 'document_status', 'created_at')
    list_filter = ('document_type', 'document_status')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

admin.site.register(Document, DocumentAdmin)
"""

"""
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_email', 'subject', 'contact_date')
    list_filter = ('contact_date',)
    search_fields = ('name', 'user__username', 'user__email')
    date_hierarchy = 'contact_date'
    ordering = ('-contact_date',)
    list_per_page = 20

    def user_email(self, obj):
        return obj.user.email if obj.user else None
    user_email.short_description = 'User Email'
"""
admin.site.register(CryptoCurrency)
admin.site.register(CryptoPayment)
