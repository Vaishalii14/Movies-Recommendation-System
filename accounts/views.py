from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from accounts.forms import UserForm



# Register user
class RegisterView(CreateView):
    form_class = UserForm 
    template_name = 'signUp.html' # mentioning template name
    success_url = reverse_lazy('movies:index') #defining url

    def form_valid(self, form):
        user_form = form.save(commit=False)
        form_username = form.cleaned_data['username'] # username field
        form_password = form.cleaned_data['password'] # password field
        user_form.set_password(form_password) 
        user_form.save()
        auth_user = authenticate(username=form_username, password=form_password) # authetication checking for username is already present or not 
        login(self.request, auth_user) # creating the session for the user
        return HttpResponseRedirect(self.success_url)


# Login User
class UserLoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        login_username = request.POST['username'] # feteching username from the form fields
        login_password = request.POST['password'] # feteching password from the form fields

        auth_user = authenticate(username=login_username, password=login_password) # checking username and password are valid or not 

        if not auth_user: # if user credentials are not valid so return template with error message
            return render(request, 'login.html', {'error_message': 'Invalid Login'})

        if not auth_user.is_active: # if user credentials are valid but account is disable so return template with error message
            return render(request, 'login.html', {'error_message': 'Your account disable'})

        login(request, auth_user)
        return redirect("movies:index")


# Logout user
def user_logout_view(request):
    logout(request) # removing session for the user
    return redirect("login")
