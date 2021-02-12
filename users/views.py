from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # save the user to the database
            form.save()

            print(form.cleaned_data)
            messages.success(request, f'Account created! You are now able to log in.')

            return redirect('users-login')

    else:
        form = UserRegistrationForm()


    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)


# when log out, user access profile: redirect user to login, then -> profile (/login?next=/profile)
@login_required
def profile(request):
    if request.method == 'POST':
        # pass the instance parameter to prevent creating new user or new profile
        user_form = UserUpdateForm(
                                    data=request.POST,
                                    instance=request.user)

        profile_form = ProfileUpdateForm(
                                        data=request.POST,
                                        files=request.FILES,
                                        instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your account has been updated!')
            return redirect('users-profile')

    else: # request == 'GET'
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)


    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'users/profile.html', context=context)