from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("apps.landing.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("events/", include("apps.events.urls")),
    path("applications/", include("apps.applications.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("matching/", include("apps.matching.urls")),
    prefix_default_language=False,
)
