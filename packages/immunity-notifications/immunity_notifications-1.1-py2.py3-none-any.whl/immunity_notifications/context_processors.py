from django.templatetags.static import static

from immunity_notifications import settings as app_settings


def notification_api_settings(request):
    return {
        'IMMUNITY_NOTIFICATIONS_HOST': app_settings.HOST,
        'IMMUNITY_NOTIFICATIONS_SOUND': static(app_settings.SOUND),
    }
