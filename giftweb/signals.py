import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils.dateformat import format
from .models import CryptoPayment, Payment

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CryptoPayment)
def send_crypto_payment_status_email(sender, instance, created, **kwargs):
    logger.debug(f"Signal triggered for instance {instance.id} with status {instance.status}")
    
    if instance.status == 'COMPLETE':
        subject = 'Payment Transaction Confirmed'
        html_message = (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #2e6c80;">Payment Transaction Confirmed</h2>
                <p>Dear Valued Customer,</p>
                <p>We are thrilled to inform you that your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} 
                has been successfully processed and is now confirmed. Your item is on delivery. Thank you for your trust and patience as we have processed your transaction.</p>
                <p>Warm regards,<br>The Zorevina Cart Online Store</p>
            </body>
            </html>
            '''
        )
    elif instance.status == 'DECLINED':
        subject = 'Payment Transaction Declined'
        html_message = (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #d9534f;">Payment Transaction Declined</h2>
                <p>Dear Valued Customer,</p>
                <p>We regret to inform you that your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} 
                has been declined. Please review your payment details and try again. If you have any questions, feel free to contact our support team at support@zorevinacart.store.</p>
                <p>Warm regards,<br>The Zorevina Cart Online Store</p>
            </body>
            </html>
            '''
        )
    elif instance.status == 'CANCELLED':
        subject = 'Payment Transaction Cancelled'
        html_message = (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #f0ad4e;">Payment Transaction Cancelled</h2>
                <p>Dear Valued Customer,</p>
                <p>We regret to inform you that your payment of <strong>${instance.amount}</strong> via {instance.get_payment_method_display()} 
                has been cancelled. If you have any questions or concerns, please contact our support team at support@zorevinacart.store. We apologize for any inconvenience caused.</p>
                <p>Warm regards,<br>The Zorevina Cart Online Store</p>
            </body>
            </html>
            '''
        )
    else:
        # Handle other status cases if needed
        return

    from_email = 'info@cargologistic.online'
    recipient_list = [instance.user.email]
    plain_message = strip_tags(html_message)  # Fallback plain text message

    send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=html_message)


@receiver(post_save, sender=Payment)
def send_payment_status_email(sender, instance, created, **kwargs):
    logger.debug(f"Signal triggered for instance {instance.id} with status {instance.status}")
    
    email_subjects = {
        'COMPLETE': 'Payment Transaction Confirmed',
        'CANCELLED': 'Payment Transaction Cancelled'
    }
    
    email_messages = {
        'COMPLETE': (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #2e6c80;">Payment Transaction Confirmed</h2>
                <p>Dear Valued Customer,</p>
                <p>We are thrilled to inform you that your payment of <strong>${instance.amount}</strong> via {instance.get_gift_card_type_display()} 
                has been successfully processed and is now confirmed. Your item is on delivery. Thank you for your trust and patience as we have processed your transaction.</p>
                <p>Warm regards,<br>The Zorevina Cart Online Store</p>
            </body>
            </html>
            '''
        ),
        'CANCELLED': (
            f'''
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                <h2 style="color: #f0ad4e;">Payment Transaction Cancelled</h2>
                <p>Dear Valued Customer,</p>
                <p>We regret to inform you that your payment of <strong>${instance.amount}</strong> via {instance.get_gift_card_type_display()} 
                has been cancelled. If you have any questions or concerns, please contact our support team at support@zorevinacart.store. We apologize for any inconvenience caused.</p>
                <p>Warm regards,<br>The Zorevina Cart Online Store</p>
            </body>
            </html>
            '''
        )
    }
    
    if instance.status in email_subjects:
        subject = email_subjects[instance.status]
        html_message = email_messages[instance.status]
        from_email = 'info@cargologistic.online'
        recipient_list = [instance.user.email]
        plain_message = strip_tags(html_message)  # Fallback plain text message

        send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=html_message)


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
        from_email = 'info@cargologistic.online'
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
        from_email = 'info@cargologistic.online'
        recipient_list = ['zorevinacart@gmail.com']
        plain_message = strip_tags(message)  # Fallback plain text message

        send_mail(subject, plain_message, from_email, recipient_list, fail_silently=False, html_message=message)
