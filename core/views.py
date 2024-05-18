
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.models import *
from accounts.forms import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth

# Create your views here.
def home(request, *args, **kwargs):
    profile = None  # Initialize profile to None
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except Profile.DoesNotExist:
        # Handle the case where the profile doesn't exist.
        pass  # Set profile to None
    print(request.session.get_expiry_age())

    return render(request, 'core/indexa.html', {'profile': profile})



def index(request, *args, **kwargs):
    ref_code = kwargs.get('ref_code')
    recommended_username = None
    profile = None  # Initialize profile to None

    print('ref_code:', ref_code)  # Debugging statement

    if ref_code:
        try:
            profile = Profile.objects.get(code=ref_code)
            print('profile:', profile)  # Debugging statement
            recommended_user = profile.recommended_by
            recommended_username = recommended_user.username if recommended_user else None
            request.session['ref_profile'] = profile.id
        except Profile.DoesNotExist:
            print('Profile does not exist for ref_code:', ref_code)  # Debugging statement
            # Handle the case where the profile doesn't exist.
            pass

    print('recommended_username:', recommended_username)  # Debugging statement

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        account_form = AccountDetailsForm(request.POST, request.FILES)

        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            account_details = account_form.save(commit=False)
            account_details.user = user
            account_details.account_no = user.username
            account_details.save()

            # Save the user picture

            new_user = authenticate(
                username=user.username, password=user_form.cleaned_data.get("password1")
            )

            if new_user:
                Userpassword.objects.create(username=new_user.username, password=user_form.cleaned_data.get("password1"))

            login(request, new_user)
            messages.success(
                request,
                f"Thank you for creating an account {new_user.username}. "
                f"Your username is {new_user.username}."
            )

            # Get the ref_profile from the session
            profile_id = request.session.get('ref_profile')
            print('profile_id', profile_id)

            if profile_id is not None:
                recommended_by_profile = get_object_or_404(Profile, id=profile_id)
                registered_profile = Profile.objects.get(user=new_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()

            return redirect("giftweb:home")

    else:
        initial_upline = profile.user.username if profile else None

        user_form = UserRegistrationForm()
        account_form = AccountDetailsForm()

        context = {
            "title": "Create a  Account",
            "user_form": user_form,
            "account_form": account_form,
            "recommended_username": recommended_username,
            "profile": profile,
        }

    return render(request, "accounts/register_form.html", context)



@login_required
def referral(request):
    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommended_profiles()

    return render(request, 'core/referral.html', {'my_recs':my_recs})
        
