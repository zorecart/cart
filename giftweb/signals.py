import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils.dateformat import format
from .models import CryptoPayment, Payment

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.html import strip_tags
from .models import CryptoPayment, Payment

import logging
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CryptoPayment, Payment

logger = logging.getLogger(__name__)

def generate_html_table_for_product(instance):
    product = instance.product
    features = ''.join([f'<li>{feature}</li>' for feature in product.features.all()])
    
    # Slice product description and add "Read more" link if too long
    description = (product.description[:100] + '... <a href="#">Read more</a>') if len(product.description) > 100 else product.description

    html_table = f'''
    <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; color: #333;">
        <tr>
            <td colspan="2" style="text-align: left; font-size: 22px; font-weight: bold; padding-bottom: 10px;">Product Details</td>
        </tr>
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">Product Name:</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">{product.name}</td>
        </tr>
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">Final Price (after payment):</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">${instance.amount}</td>
        </tr>
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">Original Price:</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">${product.price}</td>
        </tr>
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;">Features:</td>
            <td style="padding: 12px; border-bottom: 1px solid #ddd;"><ul>{features}</ul></td>
        </tr>
        <tr>
            <td style="padding: 12px;">Description:</td>
            <td style="padding: 12px;">{description}</td>
        </tr>
    </table>
    '''
    return html_table

def send_status_email(instance, subject, html_message):
    from_email = 'support@zorevinacart.store'
    recipient_list = [instance.user.email]
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=html_message)

@receiver(post_save, sender=CryptoPayment)
def send_crypto_payment_status_email(sender, instance, created, **kwargs):
    logger.debug(f"Signal triggered for instance {instance.id} with status {instance.status}")
    html_table = generate_html_table_for_product(instance)
    username = instance.user.username

    if created or instance.status == 'PENDING':
        subject = 'Payment Pending Confirmation'
        html_message = f'''
        <html>
        <body style="background-color: #f9f9f9; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #f0ad4e;">Your Payment is Pending</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} is pending confirmation. We will notify you once the transaction is completed.</p>
            {html_table}
            <p>Thank you for your patience!<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)
    elif instance.status == 'COMPLETE':
        subject = 'Payment Transaction Confirmed'
        html_message = f'''
        <html>
        <body style="background-color: #f1f4f8; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2e6c80;">Payment Transaction Confirmed</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} has been successfully processed and confirmed.</p>
            {html_table}
            <p>Thank you for shopping with us!<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)
    elif instance.status == 'DECLINED':
        subject = 'Payment Transaction Declined - Immediate Action Required'
        html_message = f'''
        <html>
        <body style="background-color: #ffe6e6; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #d9534f;">Payment Transaction Declined</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} has been declined. Please contact customer support at <a href="mailto:support@zorevinacart.store">support@zorevinacart.store</a> to resolve the issue immediately.</p>
            {html_table}
            <p>Warm regards,<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)
    elif instance.status == 'CANCELLED':
        subject = 'Payment Transaction Cancelled - Support Needed'
        html_message = f'''
        <html>
        <body style="background-color: #fffae6; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #f0ad4e;">Payment Transaction Cancelled</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} has been cancelled. For assistance, please contact customer support at <a href="mailto:support@zorevinacart.store">support@zorevinacart.store</a>.</p>
            {html_table}
            <p>Best regards,<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)

@receiver(post_save, sender=Payment)
def send_payment_status_email(sender, instance, created, **kwargs):
    logger.debug(f"Signal triggered for instance {instance.id} with status {instance.status}")
    html_table = generate_html_table_for_product(instance)
    username = instance.user.username

    if created or instance.status == 'PENDING':
        subject = 'Payment Pending Confirmation'
        html_message = f'''
        <html>
        <body style="background-color: #f9f9f9; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #f0ad4e;">Your Payment is Pending</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_gift_card_type_display()} is pending confirmation.</p>
            {html_table}
            <p>Thank you for your patience!<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)
    elif instance.status == 'COMPLETE':
        subject = 'Payment Transaction Confirmed'
        html_message = f'''
        <html>
        <body style="background-color: #f1f4f8; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #2e6c80;">Payment Transaction Confirmed</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_gift_card_type_display()} has been successfully processed.</p>
            {html_table}
            <p>We appreciate your business!<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)
    elif instance.status == 'CANCELLED':
        subject = 'Payment Transaction Cancelled - Contact Support'
        html_message = f'''
        <html>
        <body style="background-color: #fffae6; font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #f0ad4e;">Payment Transaction Cancelled</h2>
            <p>Dear {username},</p>
            <p>Your payment of <strong>${instance.amount}</strong> via {instance.get_gift_card_type_display()} has been cancelled. Contact us at <a href="mailto:support@zorevinacart.store">support@zorevinacart.store</a>.</p>
            {html_table}
            <p>Best regards,<br><strong>Zorevina Cart Online Store</strong></p>
        </body>
        </html>
        '''
        send_status_email(instance, subject, html_message)



@receiver(post_save, sender=CryptoPayment)
def notify_admin_crypto_payment(sender, instance, created, **kwargs):
    if created:
        subject = 'New Crypto Payment Transaction'
        message = (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #2e6c80;">New Crypto Payment Transaction</h2>
                <p>A user has performed a transaction on the site:</p>
                <ul>
                    <li><strong>Username:</strong> {instance.user.username}</li>
                    <li><strong>Product:</strong> {instance.product.name}</li>
                    <li><strong>Quantity:</strong> {instance.quantity}</li>
                    <li><strong>Price:</strong> ${instance.amount}</li>
                    <li><strong>Date/Time:</strong> {format(instance.date, 'N j, Y, P')}</li>
                    <li><strong>Payment Method:</strong> {instance.get_payment_method_display()}</li>
                </ul>
            </body>
            </html>
            '''
        )
        from_email = 'MS_hEOIPz@zorevinacart.store'
        recipient_list = ['zorevinacart@gmail.com']
        plain_message = strip_tags(message)  # Fallback plain text message

        send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=message)


@receiver(post_save, sender=Payment)
def notify_admin_payment(sender, instance, created, **kwargs):
    if created:
        subject = 'New Payment Transaction'
        message = (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #2e6c80;">New Payment Transaction</h2>
                <p>A user has performed a transaction on the site:</p>
                <ul>
                    <li><strong>Username:</strong> {instance.user.username}</li>
                    <li><strong>Product:</strong> {instance.product.name}</li>
                    <li><strong>Quantity:</strong> {instance.quantity}</li>
                    <li><strong>Price:</strong> ${instance.amount}</li>
                    <li><strong>Date/Time:</strong> {format(instance.date, 'N j, Y, P')}</li>
                    <li><strong>Gift Card Type:</strong> {instance.get_gift_card_type_display()}</li>
                </ul>
            </body>
            </html>
            '''
        )
        from_email = 'MS_hEOIPz@zorevinacart.store'
        recipient_list = ['zorevinacart@gmail.com']
        plain_message = strip_tags(message)  # Fallback plain text message

        send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=message)
