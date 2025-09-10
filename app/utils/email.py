# ------------------------------
# Email Sending Function
# ------------------------------
import aiosmtplib
import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader

async def send_order_email(to_email: str, product: str = None, qty: int = None, type :str = None):
    message = EmailMessage()
    message["From"] = "yourshop@example.com"
    message["Subject"] = "Email subject"
    message["To"] = to_email
    message.set_content(
            f"Thank you for your order!\n\n"
            f"Product: {product}\n"
            f"Quantity: {qty}\n\n"
            f"We will notify you once your order is shipped."
        )
    if type == 'registration_route' :
        message.set_content(
            f"Thank you for your registration!\n\n"
        )

    # Use your SMTP server config
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="prasantakus@gmail.com",
        password="nhsjenfgtrhuyuno"  # Use App Password (not Gmail password!)
    )

# Setup Jinja2 template loader
env = Environment(loader=FileSystemLoader("templates"))

def send_email_with_template(to_email: str, subject: str, template_name: str, context: dict, attachment_path: str = None):
    # Render HTML from template
    template = env.get_template(template_name)
    html_content = template.render(context)

    msg = EmailMessage()
    msg["From"] = "yourshop@example.com"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content("This is an HTML email.")  # fallback for plain text
    msg.add_alternative(html_content, subtype="html")

    # Attach file if provided
    if attachment_path:
        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('prasantakus@gmail.com', 'nhsjenfgtrhuyuno')
        server.send_message(msg)
