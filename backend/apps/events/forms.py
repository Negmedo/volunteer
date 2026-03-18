from django import forms

from .models import Event, EventRequirement, Application


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "is_public",
            "city",
            "district",
            "start_date",
            "end_date",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "city": forms.Select(attrs={"class": "form-select"}),
            "district": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class EventRequirementForm(forms.ModelForm):
    class Meta:
        model = EventRequirement
        fields = [
            "direction",
            "task_type",
            "required_skills",
            "optional_skills",
            "required_languages",
            "preferred_availability_slots",
            "min_experience_level",
            "requires_car",
            "requires_night_shift",
            "allows_other_districts",
            "volunteers_needed",
        ]
        widgets = {
            "direction": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "required_skills": forms.CheckboxSelectMultiple(),
            "optional_skills": forms.CheckboxSelectMultiple(),
            "required_languages": forms.CheckboxSelectMultiple(),
            "preferred_availability_slots": forms.CheckboxSelectMultiple(),
            "min_experience_level": forms.Select(attrs={"class": "form-select"}),
            "requires_car": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "requires_night_shift": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "allows_other_districts": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "volunteers_needed": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["motivation_text"]
        widgets = {
            "motivation_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Коротко напишите, почему хотите участвовать (необязательно).",
                }
            ),
        }
        labels = {
            "motivation_text": "Комментарий к отклику",
        }