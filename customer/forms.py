from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email', 'building', 'flat_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username',
                'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc; background-color: #f9f9f9;'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc;'
            }),
            'building': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your building name',
                'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc; background-color: #f9f9f9;'
            }),
            'flat_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your flat number',
                'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        
        # Explicitly set the class and attributes for password1
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1); background-color: #f9f9f9;'
        })
        
        # Explicitly set the class and attributes for password2
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'style': 'border-radius: 8px; padding: 10px; border: 1px solid #ccc; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);'
        })

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'building', 'flat_number', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'flat_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import GarbagePickup
from datetime import date
from dateutil.relativedelta import relativedelta
class GarbagePickupForm(forms.ModelForm):
    class Meta:
        model = GarbagePickup
        fields = ['pickup_date', 'frequency', 'weight', 'remarks', 'duration', 'points', 'supercoins', 'payment_status']
        widgets = {
            'pickup_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'min': date.today().strftime('%Y-%m-%d'),
                }
            ),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Extra Weight (kg)'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional Remarks'
            }),
            'duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter duration (months or weeks)',
                'min': 1
            }),
            'points': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Points earned'
            }),
            'supercoins': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Supercoins earned'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-control',
                'choices': GarbagePickup.PAYMENT_STATUS_CHOICES
            })
        }

    def clean_weight(self):
        weight = self.cleaned_data.get('weight', None)
        if weight is not None and weight < 0:
            raise forms.ValidationError('Weight cannot be negative.')
        return weight

    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get('frequency')
        pickup_date = cleaned_data.get('pickup_date')
        weight = cleaned_data.get('weight')
        duration = cleaned_data.get('duration')

        if frequency in ['daily', 'weekly', 'monthly'] and not pickup_date:
            self.add_error('pickup_date', 'Pickup date is required for daily, weekly, and monthly subscriptions.')

        if frequency == 'special' and weight is None:
            self.add_error('weight', 'Weight is required for special events.')

        if pickup_date and duration:
            if frequency == 'daily':
                cleaned_data['subscription_end_date'] = pickup_date + relativedelta(months=duration)
            elif frequency == 'weekly':
                cleaned_data['subscription_end_date'] = pickup_date + relativedelta(weeks=duration * 4)
            elif frequency == 'monthly':
                cleaned_data['subscription_end_date'] = pickup_date + relativedelta(months=duration)
            elif frequency == 'special':
                cleaned_data['subscription_end_date'] = None
        else:
            cleaned_data['subscription_end_date'] = None

        return cleaned_data

# forms.py
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['pickup_schedule', 'complaint_text']
