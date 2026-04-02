from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet
from .models import Event, EventPosition, EventPositionRequiredSkill, EventPositionOptionalSkill, EventPositionLanguageRequirement
from apps.accounts.models import TimeOfDay, WEEKDAY_CHOICES


class UniqueInlineFormSet(BaseInlineFormSet):
    unique_field_name = None

    def clean(self):
        super().clean()
        seen = set()
        for form in self.forms:
            if not hasattr(form, "cleaned_data") or not form.cleaned_data or form.cleaned_data.get("DELETE"):
                continue
            if self.unique_field_name:
                value = form.cleaned_data.get(self.unique_field_name)
                if value in seen and value is not None:
                    raise forms.ValidationError("Нельзя добавлять одинаковые значения дважды.")
                seen.add(value)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "city", "district", "address_text", "start_date", "end_date", "is_public"]
        labels = {
            "title": "Название мероприятия",
            "description": "Описание",
            "city": "Город",
            "district": "Район",
            "address_text": "Локация / адрес",
            "start_date": "Дата начала",
            "end_date": "Дата окончания",
            "is_public": "Публичное мероприятие",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "city": forms.Select(attrs={"class": "form-select"}),
            "district": forms.Select(attrs={"class": "form-select"}),
            "address_text": forms.TextInput(attrs={"class": "form-control"}),
            "start_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        if start and end and start > end:
            raise forms.ValidationError("Дата начала мероприятия не может быть позже даты окончания.")
        return cleaned


class EventPositionForm(forms.ModelForm):
    availability_matrix = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[])

    class Meta:
        model = EventPosition
        fields = ["title", "description", "direction", "task_type", "slots_total", "requires_car", "requires_night_shift", "requires_physical_work", "requires_heavy_lifting", "avoid_large_crowds_sensitive"]
        labels = {
            "title": "Название роли",
            "description": "Описание роли",
            "direction": "Направление",
            "task_type": "Тип задачи",
            "slots_total": "Сколько волонтёров нужно",
            "requires_car": "Нужен автомобиль",
            "requires_night_shift": "Нужны ночные смены",
            "requires_physical_work": "Нужна физическая нагрузка",
            "requires_heavy_lifting": "Нужна переноска тяжестей",
            "avoid_large_crowds_sensitive": "Не подходит для людей с ограничением по большому потоку людей",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "direction": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "slots_total": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["availability_matrix"].choices = [
            (f"{weekday}:{slot}", f"{weekday_label} · {slot_label}")
            for weekday, weekday_label in WEEKDAY_CHOICES
            for slot, slot_label in TimeOfDay.choices
        ]
        if self.instance.pk and not self.is_bound:
            self.initial["availability_matrix"] = [
                f"{item.weekday}:{item.time_of_day}" for item in self.instance.availability_requirements.all()
            ]


class RequiredSkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skill"].empty_label = "Выберите значение"

    class Meta:
        model = EventPositionRequiredSkill
        fields = ["skill", "min_level"]
        labels = {"skill": "Навык", "min_level": "Минимальный уровень"}
        widgets = {
            "skill": forms.Select(attrs={"class": "form-select js-unique-select", "data-group": "required-skill"}),
            "min_level": forms.Select(attrs={"class": "form-select"}),
        }


class OptionalSkillForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["skill"].empty_label = "Выберите значение"

    class Meta:
        model = EventPositionOptionalSkill
        fields = ["skill", "min_level"]
        labels = {"skill": "Навык", "min_level": "Минимальный уровень"}
        widgets = {
            "skill": forms.Select(attrs={"class": "form-select js-unique-select", "data-group": "optional-skill"}),
            "min_level": forms.Select(attrs={"class": "form-select"}),
        }


class LanguageReqForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["language"].empty_label = "Выберите значение"

    class Meta:
        model = EventPositionLanguageRequirement
        fields = ["language", "min_level"]
        labels = {"language": "Язык", "min_level": "Минимальный уровень"}
        widgets = {
            "language": forms.Select(attrs={"class": "form-select js-unique-select", "data-group": "required-language"}),
            "min_level": forms.Select(attrs={"class": "form-select"}),
        }


class RequiredSkillFormSet(UniqueInlineFormSet):
    unique_field_name = "skill"


class OptionalSkillFormSet(UniqueInlineFormSet):
    unique_field_name = "skill"


class LanguageReqFormSet(UniqueInlineFormSet):
    unique_field_name = "language"


RequiredSkillFormSetFactory = inlineformset_factory(EventPosition, EventPositionRequiredSkill, form=RequiredSkillForm, formset=RequiredSkillFormSet, extra=0, can_delete=True)
OptionalSkillFormSetFactory = inlineformset_factory(EventPosition, EventPositionOptionalSkill, form=OptionalSkillForm, formset=OptionalSkillFormSet, extra=0, can_delete=True)
LanguageReqFormSetFactory = inlineformset_factory(EventPosition, EventPositionLanguageRequirement, form=LanguageReqForm, formset=LanguageReqFormSet, extra=0, can_delete=True)
