from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.forms import inlineformset_factory, BaseInlineFormSet

from .models import (
    Profile,
    VolunteerProfile,
    VolunteerLanguage,
    VolunteerSkill,
    Gender,
    LanguageLevel,
    SkillLevel,
    TimeOfDay,
    WEEKDAY_CHOICES,
)


class UniqueInlineFormSet(BaseInlineFormSet):
    unique_field_name = None

    def clean_birth_year(self):
        value = self.cleaned_data.get("birth_year")
        return value or 2000

    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data:
                continue
            if form.cleaned_data.get("DELETE"):
                continue
            field_name = self.unique_field_name
            if not field_name:
                continue
            value = form.cleaned_data.get(field_name)
            if not value:
                continue
            if value in seen:
                raise forms.ValidationError("Нельзя выбирать одинаковые значения дважды.")
            seen.add(value)


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Повтор пароля")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "username": "Логин",
            "email": "Email",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_password1(self):
        validate_password(self.cleaned_data["password1"], self.instance)
        return self.cleaned_data["password1"]

    def clean_birth_year(self):
        value = self.cleaned_data.get("birth_year")
        return value or 2000

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}), label="Логин")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Пароль")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone"]
        labels = {"phone": "Телефон"}
        widgets = {"phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 777 000 00 00"})}


class UserIdentityForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        labels = {"first_name": "Имя", "last_name": "Фамилия", "email": "Email"}
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class VolunteerProfileForm(forms.ModelForm):
    availability_matrix = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[],
        label="Доступность по дням и времени",
    )

    class Meta:
        model = VolunteerProfile
        fields = [
            "gender", "birth_year", "city", "district", "availability_start_date", "availability_end_date",
            "ready_for_night_shifts", "can_travel", "has_car", "physical_work_ok", "carry_heavy_ok",
            "restrictions_note", "avoid_night_shifts", "avoid_outdoor_winter_work", "avoid_large_crowds",
            "participation_goal", "motivation_text", "preferred_directions", "preferred_task_types",
        ]
        labels = {
            "gender": "Пол",
            "birth_year": "Год рождения",
            "city": "Город",
            "district": "Район",
            "availability_start_date": "Доступен с",
            "availability_end_date": "Доступен до",
            "ready_for_night_shifts": "Готов к ночным сменам",
            "can_travel": "Готов выезжать в другие районы",
            "has_car": "Есть автомобиль",
            "physical_work_ok": "Физическая нагрузка допустима",
            "carry_heavy_ok": "Могу переносить тяжести",
            "restrictions_note": "Ограничения и противопоказания",
            "avoid_night_shifts": "Нежелательны ночные смены",
            "avoid_outdoor_winter_work": "Нежелательна работа на улице зимой",
            "avoid_large_crowds": "Нежелательна работа с большим потоком людей",
            "participation_goal": "Цель участия",
            "motivation_text": "Мотивация",
            "preferred_directions": "Предпочтительные направления",
            "preferred_task_types": "Предпочтительные типы задач",
        }
        widgets = {
            "gender": forms.Select(attrs={"class": "form-select"}),
            "birth_year": forms.NumberInput(attrs={"class": "form-control", "min": 1940, "max": 2015, "value": 2000}),
            "city": forms.Select(attrs={"class": "form-select"}),
            "district": forms.Select(attrs={"class": "form-select"}),
            "availability_start_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "availability_end_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "participation_goal": forms.Select(attrs={"class": "form-select"}),
            "motivation_text": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "restrictions_note": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "preferred_directions": forms.CheckboxSelectMultiple(),
            "preferred_task_types": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["gender"].choices = [("", "---------")] + list(Gender.choices)
        self.fields["preferred_directions"].widget = forms.CheckboxSelectMultiple()
        self.fields["preferred_task_types"].widget = forms.CheckboxSelectMultiple()
        if not self.is_bound and not self.instance.birth_year:
            self.initial["birth_year"] = 2000
        city = None
        if self.is_bound:
            city_id = self.data.get(self.add_prefix("city"))
            if city_id:
                try:
                    city = self.fields["city"].queryset.get(pk=city_id)
                except Exception:
                    city = None
        else:
            city = getattr(self.instance, "city", None)
        self.fields["district"].queryset = city.districts.all() if city else self.fields["district"].queryset.none()
        self.fields["availability_matrix"].choices = [
            (f"{weekday}:{slot}", f"{weekday_label} · {slot_label}")
            for weekday, weekday_label in WEEKDAY_CHOICES
            for slot, slot_label in TimeOfDay.choices
        ]
        if self.instance.pk and not self.is_bound:
            self.initial["availability_matrix"] = [
                f"{item.weekday}:{item.time_of_day}" for item in self.instance.availability_items.all()
            ]

    def clean_birth_year(self):
        value = self.cleaned_data.get("birth_year")
        return value or 2000

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("availability_start_date")
        end = cleaned.get("availability_end_date")
        if start and end and start > end:
            raise forms.ValidationError("Дата начала не может быть позже даты окончания.")
        return cleaned


class VolunteerLanguageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"].empty_label = "Выберите язык"

    class Meta:
        model = VolunteerLanguage
        fields = ["language", "level"]
        labels = {"language": "Язык", "level": "Уровень"}
        widgets = {
            "language": forms.Select(attrs={"class": "form-select js-unique-select", "data-group": "volunteer-language"}),
            "level": forms.Select(attrs={"class": "form-select"}),
        }


class VolunteerSkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skill"].empty_label = "Выберите навык"

    class Meta:
        model = VolunteerSkill
        fields = ["skill", "level"]
        labels = {"skill": "Навык", "level": "Уровень"}
        widgets = {
            "skill": forms.Select(attrs={"class": "form-select js-unique-select", "data-group": "volunteer-skill"}),
            "level": forms.Select(attrs={"class": "form-select"}),
        }


class VolunteerLanguageFormSet(UniqueInlineFormSet):
    unique_field_name = "language"


class VolunteerSkillFormSet(UniqueInlineFormSet):
    unique_field_name = "skill"


VolunteerLanguageFormSetFactory = inlineformset_factory(
    VolunteerProfile,
    VolunteerLanguage,
    form=VolunteerLanguageForm,
    formset=VolunteerLanguageFormSet,
    extra=0,
    can_delete=True,
)
VolunteerSkillFormSetFactory = inlineformset_factory(
    VolunteerProfile,
    VolunteerSkill,
    form=VolunteerSkillForm,
    formset=VolunteerSkillFormSet,
    extra=0,
    can_delete=True,
)
