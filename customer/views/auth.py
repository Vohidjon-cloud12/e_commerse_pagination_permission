from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from customer.forms import LoginForm, RegisterModelForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import FormView
from django.template.loader import render_to_string
from django.shortcuts import redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from customer.tokens import account_activation_token
from customer.models import Customer



# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('customers')
#     else:
#         form = LoginForm()
#
#     return render(request, 'auth/login.html', {'form': form})

class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request,'auth/login.html',{'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user :
                login(request, user)
                return redirect('customers')

def logout_page(request):
    if request.method == 'GET   ':
        logout(request)
        return redirect('customers')
    return render(request, 'auth/logout.html')

#
# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterModelForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             password = form.cleaned_data['password']
#
#             user.set_password(password)
#             user.save()
#
#             login(request, user)
#             return redirect('customers')
#     else:
#         form = RegisterModelForm()
#
#     return render(request, 'auth/register.html', {'form': form})

class RegisterFormView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.password = form.cleaned_data['password']
        user.save()
        login(self.request, user)
        return redirect('customers')


from django.core.mail import send_mail
from django.views.generic import View
from django.shortcuts import render

class EmailSenderView(View):
    def post(self, request, *args, **kwargs):
        # Get form data (assuming you have a form with 'name', 'email', and 'message' fields)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Your email sending logic here
        subject = f"New message from {name}"
        body = f"From: {email}\n\nMessage:\n{message}"
        from_email = 'vohidjonboyqoziyev@gmail.com'
        recipient_list = ['recipient@email.com']

        send_mail(subject, body, from_email, recipient_list)

        return render(request, 'success_template.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Customer.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account activated successfully!')
        return redirect('customers')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')


def activate_email(request, user, to_email):
    subject = 'Activate your account'
    message = render_to_string('auth/account-activation.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'protocol': 'https' if request.is_secure() else 'http',
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject, message, to=[to_email])
    try:
        email.send()
        messages.success(request,
                         'Activation link sent to your email address. '
                         'Please activate your account.')
    except Exception as e:
        messages.error(request, f'Sorry, there was an error : {str(e)}')
