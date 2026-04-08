from django.core.management.base import BaseCommand
from apps.core.models import City, District, Language, SkillCategory, Skill, VolunteerDirection, TaskType


class Command(BaseCommand):
    help = "Seed core dictionaries"

    def handle(self, *args, **options):
        cities = {
            "Петропавловск": ["19-й микрорайон", "Центр", "Рабочий поселок", "Береке"],
            "Сергеевка": ["Центральный"],
            "Булаево": ["Центральный"],
        }
        for city_name, districts in cities.items():
            city, _ = City.objects.get_or_create(name=city_name)
            for district_name in districts:
                District.objects.get_or_create(city=city, name=district_name)

        for name, code in [("Русский", "RU"), ("Казахский", "KZ"), ("Английский", "EN")]:
            Language.objects.get_or_create(name=name, code=code)

        skill_map = {
            "Социальные": ["Работа с детьми", "Работа с пожилыми", "Психологическая поддержка"],
            "Операционные": ["Логистика", "Регистрация участников", "Организация мероприятий"],
            "Медиа": ["SMM / Фото / Видео"],
            "Языковые": ["Переводы"],
            "Технические": ["Работа с документами / ПК"],
            "Медицинские": ["Первая помощь"],
        }
        for idx, (cat_name, skills) in enumerate(skill_map.items(), start=1):
            cat, _ = SkillCategory.objects.get_or_create(name=cat_name, defaults={"sort_order": idx})
            if cat.sort_order != idx:
                cat.sort_order = idx
                cat.save(update_fields=["sort_order"])
            for skill_name in skills:
                Skill.objects.get_or_create(category=cat, name=skill_name)

        for name in ["Экология", "Помощь детям", "Помощь пожилым", "ЧС", "Мероприятия"]:
            VolunteerDirection.objects.get_or_create(name=name)
        for name in ["Работа с людьми", "Организационная помощь", "Техническая поддержка", "Медпост", "Логистика"]:
            TaskType.objects.get_or_create(name=name)

        self.stdout.write(self.style.SUCCESS("Core dictionaries seeded"))
