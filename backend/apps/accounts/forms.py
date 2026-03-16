from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import VolunteerProfile


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Пароль"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Повтор пароля"
    )

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        label="Логин"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Пароль"
    )


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerProfile
        fields = [
            "city",
            "district",
            "languages",
            "skills",
            "preferred_directions",
            "preferred_task_types",
            "availability_slots",
            "experience_level",
            "has_car",
            "ready_for_night_shifts",
            "can_travel_to_other_districts",
            "short_bio",
        ]
        widgets = {
            "city": forms.Select(attrs={"class": "form-select"}),
            "district": forms.Select(attrs={"class": "form-select"}),
            "languages": forms.CheckboxSelectMultiple(),
            "skills": forms.CheckboxSelectMultiple(),
            "preferred_directions": forms.CheckboxSelectMultiple(),
            "preferred_task_types": forms.CheckboxSelectMultiple(),
            "availability_slots": forms.CheckboxSelectMultiple(),
            "experience_level": forms.Select(attrs={"class": "form-select"}),
            "has_car": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "ready_for_night_shifts": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "can_travel_to_other_districts": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "short_bio": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)

        if commit:
            profile.save()
            self.save_m2m()
            profile.calculate_completion_percent()
            profile.save(update_fields=["profile_completion_percent", "is_profile_completed"])

        return profile