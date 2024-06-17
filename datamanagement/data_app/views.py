from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CheckerRegisterForm, MakerRegisterForm, LoginForm, CustomerForm
from .models import Customer, User

def base_view(request):
    return render(request, 'base.html')

@login_required
def maker_home(request):
    if request.user.user_type == 'maker':
        customers = Customer.objects.filter(maker=request.user)
        return render(request, 'maker_home.html', {'customers': customers})
    else:
        return redirect('base')

@login_required
def checker_home(request):
    if request.user.user_type == 'checker':
        assigned_makers = User.objects.filter(selected_checker=request.user)
        return render(request, 'checker_home.html', {'makers': assigned_makers, 'user': request.user})
    else:
        return redirect('base')

def checker_register(request):
    if request.method == 'POST':
        form = CheckerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('loginpage')
    else:
        form = CheckerRegisterForm()
    return render(request, 'checker_register.html', {'form': form})

def maker_register(request):
    if request.method == 'POST':
        form = MakerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('loginpage')
    else:
        form = MakerRegisterForm()
    return render(request, 'maker_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'maker':
                    return redirect('maker_home')
                elif user.user_type == 'checker':
                    return redirect('checker_home')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def create_customer(request):
    if request.user.user_type != 'maker':
        return redirect('base')
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.maker = request.user
            customer.save()
            return redirect('success_page')
    else:
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form})

@login_required
def success_page(request):
    return render(request, 'success.html')


@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.user.user_type != 'maker' or customer.maker != request.user:
        return redirect('maker_home')
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('view_customer', customer_id=customer.id)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {'form': form, 'customer': customer})

@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.user.user_type != 'maker' or customer.maker != request.user:
        return redirect('maker_home')
    if request.method == 'POST':
        customer.delete()
        return redirect('maker_home')
    return render(request, 'confirm_delete.html', {'customer': customer})

@login_required
def maker_list(request, maker_id):
    if request.user.user_type == 'checker':
        maker = get_object_or_404(User, id=maker_id, selected_checker=request.user)
        users_under_maker = Customer.objects.filter(maker=maker)
        return render(request, 'maker_list.html', {'maker': maker, 'users': users_under_maker})
    else:
        return redirect('base')

@login_required
def maker_detail(request, maker_id):
    if request.user.user_type == 'checker':
        maker = get_object_or_404(User, id=maker_id, selected_checker=request.user)
        customers = Customer.objects.filter(maker=maker)
        return render(request, 'maker_detail.html', {'maker': maker, 'customers': customers})
    else:
        return redirect('base')

@login_required
def delete_maker(request, maker_id):
    if request.user.user_type == 'checker':
        maker = get_object_or_404(User, id=maker_id, selected_checker=request.user)
        customers_to_delete = Customer.objects.filter(maker=maker)
        customers_to_delete.delete()
        maker.delete()
        return redirect('checker_home')
    else:
        return redirect('base')

@login_required
def update_customer_status(request, customer_id):
    if request.user.user_type == 'checker':
        customer = get_object_or_404(Customer, id=customer_id, maker__selected_checker=request.user)
        if request.method == 'POST':
            new_status = request.POST.get('status')
            if new_status in dict(Customer.STATUS_CHOICES).keys():
                customer.status = new_status
                customer.save()
                return redirect('maker_list', maker_id=customer.maker.id)
        else:
            return render(request, 'update_customer_status.html', {'customer': customer})
    else:
        return redirect('base')


@login_required
def view_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if (request.user.user_type == 'maker' and customer.maker == request.user) or \
       (request.user.user_type == 'checker' and customer.maker.selected_checker == request.user):
        return render(request, 'view_customer.html', {'customer': customer})
    else:
        return redirect('base')

@login_required
def view_customers(request):
    if request.user.user_type == 'checker':
        assigned_makers = User.objects.filter(selected_checker=request.user)
        customers = Customer.objects.filter(maker__in=assigned_makers)
        if request.method == 'POST':
            customer_id = request.POST.get('customer_id')
            new_status = request.POST.get('status')
            if customer_id and new_status:
                customer = get_object_or_404(Customer, id=customer_id, maker__in=assigned_makers)
                if new_status in dict(Customer.STATUS_CHOICES).keys():
                    customer.status = new_status
                    customer.save()
                    messages.success(request, f'Status for {customer.name} updated successfully!')
        return render(request, 'view_customers.html', {'customers': customers})
    else:
        return redirect('base')


@login_required
def logout_view(request):
    logout(request)
    return redirect('base')





