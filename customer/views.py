from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm
from .forms import EditProfileForm

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Save the user data
            user = form.save()

            # After saving, authenticate the user using password1
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, "Welcome, you have successfully signed up!")
                return redirect('customer:dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('customer:signin')  # Redirect to login page if authentication fails
        else:
            # If form is invalid, display errors
            messages.error(request, "There were errors in your form. Please check.")
    else:
        form = SignupForm()

    return render(request, 'csignup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('customer:dashboard')
        else:
            return render(request, 'csignin.html', {'error': 'Invalid credentials'})
    return render(request, 'csignin.html')

@login_required
def dashboard(request):
    customer_name = request.user.username  # Or you can use request.user.first_name if set
    return render(request, 'cindex.html', {'customer_name': customer_name})

@login_required
def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('customer:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=request.user)
    
    return render(request, 'cprofile.html', {
        'form': form,
        'user': request.user
    })


def clogout(request):
    logout(request)  # Logs out the user
    return redirect('customer:signin')  # Redirect to the login page

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import GarbagePickup, UserProfile
from .forms import GarbagePickupForm

@login_required
def addgarbage(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = GarbagePickupForm(request.POST)
        if form.is_valid():
            garbage_pickup = form.save(commit=False)
            garbage_pickup.user = request.user
            
            # Capture points, supercoins, payment method, and payment status
            points = int(request.POST.get('points', 0))
            supercoins = int(request.POST.get('supercoins', 0))
            payment_method = request.POST.get('payment_method', 'cash')  # Default to 'cash'
            payment_status = int(request.POST.get('payment_status', 0))  # Default to 'Not Paid'

            # Save data to the model
            garbage_pickup.points = points
            garbage_pickup.supercoins = supercoins
            garbage_pickup.payment_method = payment_method
            garbage_pickup.payment_status = payment_status  # Save payment status

            # Calculate total payment and other fields
            garbage_pickup.calculate_payment()
            garbage_pickup.save()

            # Update user profile points and supercoins
            garbage_pickup.update_user_points_and_supercoins()

            # Display appropriate message based on payment status
            if payment_status == 1:  # 1 means "Paid"
                messages.success(request, 'Payment successful! Your garbage pickup has been scheduled.')
            else:
                messages.warning(request, 'Garbage pickup scheduled, but payment is pending.')

            return redirect('customer:viewgarbage')  # Redirect to the dashboard after saving
            
    else:
        form = GarbagePickupForm()

    return render(request, 'addgarbage.html', {'form': form, 'user_profile': user_profile})

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from customer.models import GarbagePickup  # User's garbage pickup schedules
from gadmin.models import DriverAssigned  # Driver assignment model

@login_required
def viewgarbage(request):
    # Fetch all pickup schedules for the logged-in user
    user_schedules = GarbagePickup.objects.filter(user=request.user)

    # Access the user's profile points and supercoins
    user_profile = request.user.userprofile
    user_points = user_profile.points
    user_supercoins = user_profile.supercoins

    # Attach driver assignment details to each schedule
    for schedule in user_schedules:
        try:
            assignment = DriverAssigned.objects.get(garbage_pickup=schedule)
            schedule.assigned_driver = assignment.driver.name if assignment.driver else "Not Assigned"
            schedule.status = assignment.status
        except DriverAssigned.DoesNotExist:
            schedule.assigned_driver = "Not Assigned"
            schedule.status = "Pending"

        # Set correct payment status (0 → Not Paid, 1 → Paid)
        schedule.payment_status = "Paid" if schedule.payment_status == 1 else "Not Paid"

        # Fetch subscription end date
        schedule.subscription_end_date_display = (
            schedule.subscription_end_date.strftime("%d-%m-%Y") if schedule.subscription_end_date else "N/A"
        )

    # Pass data to the template
    return render(request, 'viewgarbage.html', {
        'user_schedules': user_schedules,
        'user_points': user_points,
        'user_supercoins': user_supercoins,
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import GarbagePickup

def editgarbage(request, schedule_id):
    schedule = get_object_or_404(GarbagePickup, id=schedule_id, user=request.user)

    if request.method == 'POST':
        # Update the schedule with form data
        schedule.pickup_date = request.POST['pickup_date']
        schedule.frequency = request.POST['frequency']
        schedule.duration = request.POST['duration']
        schedule.total_payment = request.POST['total_payment']
        schedule.weight = request.POST['weight']
        schedule.subscription_end_date = request.POST.get('subscription_end_date')  # Update the new field
        schedule.save()
        
        return redirect('customer:viewgarbage')  # Redirect to view after saving
    
    return render(request, 'editgarbage.html', {'schedule': schedule})

@login_required
def deletegarbage(request, schedule_id):
    # Get the GarbagePickup object for the logged-in user
    schedule = get_object_or_404(GarbagePickup, id=schedule_id, user=request.user)
    
    if request.method == 'POST':
        # Delete the schedule
        schedule.delete()
        return redirect('customer:viewgarbage')  # Redirect to the view schedule page after deletion
    
    return render(request, 'deletegarbage.html', {'schedule': schedule})


# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Complaint, GarbagePickup
from .forms import ComplaintForm

@login_required
def addcomplaint(request):
    user_schedules = GarbagePickup.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return redirect('customer:viewcomplaint')
    else:
        form = ComplaintForm()

    return render(request, 'addcomplaint.html', {
        'form': form,
        'user_schedules': user_schedules,
    })
from django.shortcuts import render
from .models import Complaint

@login_required
def viewcomplaint(request):
    # Fetch complaints for the logged-in user, or all complaints if the user is an admin
    if request.user.is_staff:
        complaints = Complaint.objects.all()  # Admin can see all complaints
    else:
        complaints = Complaint.objects.filter(user=request.user)  # Users see only their own complaints

    return render(request, 'viewcomplaint.html', {
        'complaints': complaints,
    })




