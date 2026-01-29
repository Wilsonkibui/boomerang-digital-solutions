from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_order_email(order):
    """
    Sends an order confirmation email to the customer and admin.
    """
    subject = f'Order Confirmation - {order.order_number}'
    html_message = render_to_string('store/emails/order_confirmation.html', {'order': order})
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [order.customer_email] if hasattr(order, 'customer_email') and order.customer_email else []
    
    # Always send a copy to the admin/official email
    admin_email = 'boomerangdigitalsolutions@gmail.com'
    bcc = [admin_email]
    
    if not to_email:
        # If no customer email (e.g. only phone provided), just send to admin
        to_email = [admin_email]
        bcc = []

    try:
        send_mail(
            subject,
            plain_message,
            from_email,
            to_email,
            html_message=html_message,
            fail_silently=False, # We want to know if it fails in dev, can set True in prod
            bcc=bcc
        )
        print(f"Email sent for order {order.order_number}")
    except Exception as e:
        print(f"Failed to send email: {e}")
