from django.contrib import admin
from .models import CustomUser, TemplateBlogPost, EmailTemplate, TemplateCustomContent
# Register your models here.


admin.site.register(CustomUser)
admin.site.register(TemplateBlogPost)
admin.site.register(EmailTemplate)
admin.site.register(TemplateCustomContent)
