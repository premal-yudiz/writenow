from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import signing


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class TemplateBlogPost(models.Model):
    """
    A model for blog posts with blog template name, blog subject, blog keyword and blog length.
    """
    BLOG_LENGTH_CHOICES = (
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('long', 'Long'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=16)
    blog_template = models.CharField(max_length=255)
    blog_subject = models.CharField(max_length=255)
    blog_keywords = models.CharField(max_length=255)
    blog_length = models.CharField(max_length=50, choices=BLOG_LENGTH_CHOICES, default='short')

    def get_sign_pk(self):
        """
        this function used to convert id value into big string for security purpose.
        """
        return signing.dumps(self.pk)

    def __str__(self):
        return self.blog_template


class EmailTemplate(models.Model):
    EMAIL_LENGTH_CHOICES = (
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('long', 'Long'),
    )
    email_type_choices = (
        ('custom', 'Custom Email'),
        ('cold', 'Cold Outreach Email'),
        ('followup', 'Followup'),
        ('promotional', 'Promotional Email'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=16)
    email_type = models.CharField(max_length=50, choices=email_type_choices)
    template_name = models.CharField(max_length=255)
    email_subject = models.CharField(max_length=255)
    email_keywords = models.CharField(max_length=255)
    email_length = models.CharField(max_length=50, choices=EMAIL_LENGTH_CHOICES, default='short')

    def get_sign_pk(self):
        """
        this function used to convert id value into big string for security purpose.
        """
        return signing.dumps(self.pk)

    def __str__(self):
        return self.template_name


class TemplateCustomContent(models.Model):
    CONTENT_LENGTH_CHOICES = (
        ('short', 'Short'),
        ('medium', 'Medium'),
        ('long', 'Long'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=16)
    template_name = models.CharField(max_length=255)
    custom_content_keywords = models.CharField(max_length=255)
    custom_content_length = models.CharField(max_length=50, choices=CONTENT_LENGTH_CHOICES, default='short')

    def get_sign_pk(self):
        """
        this function used to convert id value into big string for security purpose.
        """
        return signing.dumps(self.pk)

    def __str__(self):
        return self.template_name