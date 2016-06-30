from django.core.mail import send_mail


def send_tpl_mail(sender, recipients, subject, template, **kwargs):
    """
    Send emails from a template file
    Args:
        sender (str): Sender's email address
        recipients ([str]): An array of email's recipients
        subject (str): Email subject
        template (str): Full path to template
        **kwargs (str): All words in template that need interpolation

    Example:
        A template sample:
            Dear {name}, you have been invited to {event} at some place.

        Function call:
            send_tpl_mail(me@example.com,
                          [user1@example.com, user2@example.com],
                          'Hello there',
                          '/directory/containing/the/template/template.txt',
                          name='Darth Vader', event='Rebels Destruction')

    Returns:

    """
    with open(template, 'r') as txt:
        message = txt.read().format(**kwargs)
        send_mail(subject=subject, message=message, from_email=sender,
                  recipient_list=recipients, fail_silently=True)
