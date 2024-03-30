from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import CustomUser, TemplateBlogPost, EmailTemplate, TemplateCustomContent
from django.db import IntegrityError
from django.contrib.auth import logout
from dotenv import load_dotenv
from django.core import signing

from django.http import JsonResponse
import google.generativeai as genai
import os

from django.http import StreamingHttpResponse
from django.views.decorators.http import require_POST

# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.getenv('GENAI_API_KEY')
genai.configure(api_key=gemini_api_key)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email1')

        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'Username already exists'})
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'signup.html',
                          {'error_message': 'Email address is already in use. Please choose another email.'})

        # Create user
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, name=username)
            if user is not None:
                return redirect(
                    'login')  # Redirect to the home page or wherever you want after successful registration and login
            else:
                return render(request, 'signup.html', {'error_message': 'Error creating user'})
        except IntegrityError as e:
            return render(request, 'signup.html', {'error_message': 'An error occurred. Please try again.'})

    return render(request, 'signup.html')


def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        return render(request, 'login.html')
    except Exception as e:
        print(e)


def Dashboard(request):
    return render(request, 'index.html')


def blog_writing(request):
    if request.method == 'POST':
        blog_subject = request.POST['blogSubject']
        keywords = request.POST['keywords']
        length = request.POST['length']

        # Function to generate email content
        def generate_blog_content():
            model = genai.GenerativeModel('gemini-pro')

            # Construct the prompt
            prompt = f"Write a blog post on '{blog_subject}' using keywords '{keywords}' with proper blog title.**\n**Target length: {length}.  "

            try:
                # Generate content using the Gemini model
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    yield chunk.text.encode('utf-8')  # Encode text as bytes for streaming

            except Exception as e:  # Catch any unexpected errors during generation
                yield b"Error generating blog content"

        # Return streaming response with generated email content
        return StreamingHttpResponse(generate_blog_content(), content_type="text/html")

    else:
        ids = request.GET.get('id')

        if ids is None:
            return render(request, 'blog-essay.html')

        else:
            template = TemplateBlogPost.objects.get(id=signing.loads(ids))
            context = {
                "subject": template.blog_subject,
                "length": template.blog_length,
                "keyword": template.blog_keywords
            }

            return render(request, 'blog-essay.html', context)


def email_writing(request):
    if request.method == 'POST':
        email_type = request.POST['emailType']
        email_subject = request.POST['emailSubject']
        keywords = request.POST['emailKeywords']
        length = request.POST['length']

        # Function to generate email content
        def generate_email_content():
            model = genai.GenerativeModel('gemini-pro')  # Assuming you have GenAI installed and configured

            # Construct the prompt
            prompt = f"Write an '{email_type}' email on '{email_subject}' using keywords '{keywords}' with proper email subject.**\n**Target length: {length}."

            try:
                # Generate content using the Gemini model
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    yield chunk.text.encode('utf-8')  # Encode text as bytes for streaming

            except Exception as e:  # Catch any unexpected errors during generation
                yield b"Error generating email content"

        # Return streaming response with generated email content
        return StreamingHttpResponse(generate_email_content(), content_type="text/html")

    else:
        ids = request.GET.get('id')

        if ids is None:
            return render(request, 'email-writing.html')

        else:
            template = EmailTemplate.objects.get(id=signing.loads(ids))

            context = {
                "email_type": template.email_type,
                "subject": template.email_subject,
                "keyword": template.email_keywords,
                "length": template.email_length
            }

            return render(request, 'email-writing.html', context)


def custom_writing(request):
    if request.method == 'POST':

        keywords = request.POST.get('contentKeywords')
        length = request.POST.get('length')

        # Function to generate email content
        def generate_custom_content():
            model = genai.GenerativeModel('gemini-pro')  # Assuming you have GenAI installed and configured

            # Construct the prompt
            prompt = f"Write custom content using keywords '{keywords}'.\n**Target length: {length}."

            try:
                # Generate content using the Gemini model
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    yield chunk.text.encode('utf-8')  # Encode text as bytes for streaming

            except Exception as e:  # Catch any unexpected errors during generation
                yield b"Error generating custom content"

        # Return streaming response with generated email content
        return StreamingHttpResponse(generate_custom_content(), content_type="text/html")

    else:

        ids = request.GET.get('id')

        if ids is None:
            return render(request, 'custom-content.html')

        else:
            template = TemplateCustomContent.objects.get(id=signing.loads(ids))

            context = {
                "keyword": template.custom_content_keywords,
                "length": template.custom_content_length
            }

            return render(request, 'custom-content.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


def saved_templates(request):

    if request.method == "POST":
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        keyword = request.POST.get('keyword')
        length = request.POST.get('length')

        # Create an instance of TemplateBlogPost model
        new_template = TemplateBlogPost(
            blog_template=name,
            blog_subject=subject,
            blog_keywords=keyword,
            blog_length=length,
            user=request.user
        )

        # Save the instance
        new_template.save()
        return redirect('saved_templates')

    # If it's a GET request or after POST request handling
    if request.method == "GET":
        templates = TemplateBlogPost.objects.filter(user=request.user)
        emailtemplates = EmailTemplate.objects.filter(user=request.user)
        custom_template = TemplateCustomContent.objects.filter(user=request.user)

        context = {'templates': templates,
                   'emailtemplates': emailtemplates,
                   'custom_template': custom_template,

                   }
        return render(request, 'saved-template.html', context)


def get_template_details(request, template_id):
    template = TemplateBlogPost.objects.get(id=signing.loads(template_id))
    data = {
        'name': template.blog_template,
        'subject': template.blog_subject,
        'keyword': template.blog_keywords,
        'length': template.blog_length,
        'sign_pk': template.get_sign_pk()
    }
    return JsonResponse(data)


@require_POST
def update_template(request, template_id):
    try:
        # Get the template object from the database
        template = TemplateBlogPost.objects.get(id=signing.loads(template_id))

        # Update the template object with the new values
        template.blog_template = request.POST.get('name')
        template.blog_subject = request.POST.get('subject')
        template.blog_keywords = request.POST.get('keyword')
        template.blog_length = request.POST.get('length')

        # Save the updated template object
        template.save()
        return redirect('saved_templates')

    except TemplateBlogPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Template not found'})


def email_templates(request):
    templates = EmailTemplate.objects.all()
    context = {'templates': templates}
    return render(request, 'saved-template.html', context)


def delete_template_blog(request, template_id):
    # Get the template object or return 404 if not found
    template_obj = get_object_or_404(TemplateBlogPost, id=signing.loads(template_id))

    # Check if the logged-in user is the owner of the template
    if request.user == template_obj.user:
        # Delete the template
        template_obj.delete()
        return JsonResponse({'message': 'Template deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'You do not have permission to delete this template'}, status=403)


def delete_template_email(request, template_id):
    # Get the template object or return 404 if not found
    template_obj = get_object_or_404(EmailTemplate, id=signing.loads(template_id))

    # Check if the logged-in user is the owner of the template
    if request.user == template_obj.user:
        # Delete the template
        template_obj.delete()
        return JsonResponse({'message': 'Template deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'You do not have permission to delete this template'}, status=403)


def delete_template_custom(request, template_id):
    # Get the template object or return 404 if not found
    template_obj = get_object_or_404(TemplateCustomContent, id=signing.loads(template_id))

    # Check if the logged-in user is the owner of the template
    if request.user == template_obj.user:
        # Delete the template
        template_obj.delete()
        return JsonResponse({'message': 'Template deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'You do not have permission to delete this template'}, status=403)


def get_email_template_details(request, template_id):
    template = EmailTemplate.objects.get(id=signing.loads(template_id))
    data = {
        'name': template.template_name,
        'type': template.email_type,
        'subject': template.email_subject,
        'keyword': template.email_keywords,
        'length': template.email_length,
        'sign_pk': template.get_sign_pk()

    }
    return JsonResponse(data)


def save_email(request):
    if request.method == "POST":
        name = request.POST.get('email_name')
        subject = request.POST.get('email_subject')
        keyword = request.POST.get('email_keyword')
        length = request.POST.get('email_length')
        email_type = request.POST.get('email_type')

        # Create an instance of TemplateBlogPost model
        new_email = EmailTemplate(
            template_name=name,
            email_subject=subject,
            email_keywords=keyword,
            email_length=length,
            email_type=email_type,
            user=request.user
        )

        # Save the instance
        new_email.save()
        return redirect('saved_templates')


@require_POST
def update_email(request, email_id):
    try:
        # Get the template object from the database
        email_template = EmailTemplate.objects.get(id=signing.loads(email_id))
        # Update the template object with the new values
        email_template.email_type = request.POST.get('email_type')
        email_template.template_name = request.POST.get('email_name')
        email_template.email_subject = request.POST.get('email_subject')
        email_template.email_keywords = request.POST.get('email_keyword')
        email_template.email_length = request.POST.get('email_length')

        # Save the updated template object
        email_template.save()
        return redirect('saved_templates')

    except TemplateBlogPost.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Template not found'})


def get_custom_content_details(request, custom_content_id):
    custom_content = TemplateCustomContent.objects.get(id=signing.loads(custom_content_id))
    data = {
        'name': custom_content.template_name,
        'keyword': custom_content.custom_content_keywords,
        'length': custom_content.custom_content_length,
        'sign_pk': custom_content.get_sign_pk()
    }
    return JsonResponse(data)


def saved_custom_content(request):
    if request.method == "POST":
        # Access form data
        name = request.POST.get('custom_name')
        keyword = request.POST.get('custom_keyword')
        length = request.POST.get('custom_length')

        # Create an instance of TemplateBlogPost model
        new_custom_content = TemplateCustomContent(
            template_name=name,
            custom_content_keywords=keyword,
            custom_content_length=length,
            user=request.user

        )

        # Save the instance
        new_custom_content.save()
        return redirect('saved_templates')


@require_POST
def update_custom_content(request, custom_content_id):
    if custom_content_id:
        try:
            # Get the template object from the database
            custom_content_template = TemplateCustomContent.objects.get(id=signing.loads(custom_content_id))
            # Update the template object with the new values
            custom_content_template.template_name = request.POST.get('custom_name')
            custom_content_template.custom_content_keywords = request.POST.get('custom_keyword')
            custom_content_template.custom_content_length = request.POST.get('custom_length')

            # Save the updated template object
            custom_content_template.save()
            return redirect('saved_templates')

        except TemplateBlogPost.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Template not found'})
