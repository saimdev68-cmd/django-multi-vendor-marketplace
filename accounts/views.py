from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

from .forms import SignUpForm, LoginForm
from django.contrib import messages
from vendor.models import Vendor

class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(self.request,"Account created successfully! You can now log in.")
        return super().form_valid(form)
    

class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm  

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(
            self.request,
            email=email,
            password=password
        )

        if user is not None:
            login(self.request, user)

            if user.is_vendor:
                vendor = Vendor.objects.filter(owner=user).first()

                if vendor and vendor.status in [Vendor.VendorStatus.ACTIVE, Vendor.VendorStatus.SUSPENDED]:
                    return redirect("vendor:dashboard")
                elif vendor:
                    return redirect("vendor:vendor_detail")
                else:
                    return redirect("vendor:vendor_create")

            return redirect("store:home")

        form.add_error(None, "Invalid email or password.")
        return self.form_invalid(form)


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect("accounts:login")



class CustomPasswordResetView(PasswordResetView):
    template_name = "password_reset.html"
    email_template_name = "password_reset_email.html"
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password_reset_complete.html"


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "password_change.html"
    success_url = reverse_lazy("accounts:password_change_done")

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "password_change_done.html"