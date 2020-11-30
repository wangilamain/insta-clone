from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def welcome_email(name,receiver):
    subject = 'Welcome to Instagramclone'
    sender = 'wangilayng@gmail.com'

    text_content = render_to_string('emails/email.txt',{'name':name})
    html_content = render_to_string('emails/email.html',{"name":name})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()