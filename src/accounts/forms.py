import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q

from .models import Profile


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea,
        help_text='Tell everybody something about yourself',
        required=False)
    date_birth = forms.DateField(
        input_formats=('%d/%m/%Y',), label='Data urodzenia')

    class Meta:
        model = Profile
        fields = [
            'bio',
            'date_birth',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        email = self.fields['date_birth']
        print(email.initial)

    def clean_date_birth(self):
        date_birth = self.cleaned_data['date_birth']
        if date_birth:
            today = datetime.datetime.now().date()
            eighteen_year_age = datetime.date(
                (today.year-18),
                today.month,
                today.day
            )
            is_adult = self.cleaned_data['date_birth'] < eighteen_year_age
            if not is_adult:
                raise ValidationError('Podana data wskazuje, że nie jesteś dorosły.')

        return date_birth


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data['email']
        user_id = self.instance.id
        same_email = (
            User.objects.exclude(id=user_id)
                .filter(email=email)
                .exclude(Q(email__isnull=True) | Q(email=''))
        )
        if same_email.exists():
            msg = "Podany email jest niepoprawny"
            raise forms.ValidationError(msg)
        return email


class CustomPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = 'Pamiętaj o bezpieczeństwie'
        self.fields['new_password1'].label = 'Nowe hasło'
        self.fields['new_password2'].help_text = 'Powtórz dokładnie to samo hasło!'
        self.fields['new_password2'].label = 'Potwierdz hasło'
