from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.accounts.models import Profile, Role, VolunteerProfile
from apps.core.models import City, District


class Command(BaseCommand):
    help = "Create demo admin/org/volunteer users"

    def handle(self, *args, **options):
        city = City.objects.first()
        district = District.objects.filter(city=city).first() if city else None

        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "System",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created or not admin.check_password("admin12345"):
            admin.set_password("admin12345")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()
        Profile.objects.update_or_create(user=admin, defaults={"role": Role.ADMIN, "phone": "+77000000001"})

        org, created = User.objects.get_or_create(
            username="org_demo",
            defaults={
                "email": "org@example.com",
                "first_name": "Demo",
                "last_name": "Coordinator",
            },
        )
        if created or not org.check_password("org12345"):
            org.set_password("org12345")
            org.save()
        Profile.objects.update_or_create(
            user=org,
            defaults={"role": Role.ORG, "phone": "+77000000002", "organization_name": "Добрый штаб"},
        )

        volunteer, created = User.objects.get_or_create(
            username="volunteer_demo",
            defaults={
                "email": "volunteer@example.com",
                "first_name": "Demo",
                "last_name": "Volunteer",
            },
        )
        if created or not volunteer.check_password("vol12345"):
            volunteer.set_password("vol12345")
            volunteer.save()
        Profile.objects.update_or_create(user=volunteer, defaults={"role": Role.VOLUNTEER, "phone": "+77000000003"})
        VolunteerProfile.objects.get_or_create(
            user=volunteer,
            defaults={
                "city": city,
                "district": district,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo users created: admin/org/volunteer"))
