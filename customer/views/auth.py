from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from customer.forms import LoginForm, RegisterModelForm


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

        return render(request, 'success_template.html')  #