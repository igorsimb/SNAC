def registration_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                messages.info(request, 'You have registered and are now logged in!')
                return redirect('main')
            else:
                context['registration_form'] = form
        else:
            form = RegistrationForm()
            context['registration_form'] = form
        return render(request, 'users/register.html', context)