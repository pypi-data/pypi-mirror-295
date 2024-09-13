from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _

from . import settings as app_settings


class OpenwispNotificationsConfig(AppConfig):
    name = 'immunity_notifications'
    label = 'immunity_notifications'
    verbose_name = _('Notifications')

    def ready(self):
        from immunity_notifications.handlers import (
            notification_type_registered_unregistered_handler,
            notify_handler,
        )
        from immunity_notifications.signals import notify

        notify.connect(
            notify_handler, dispatch_uid='immunity_notifications.model.notifications'
        )
        if app_settings.POPULATE_PREFERENCES_ON_MIGRATE:
            post_migrate.connect(
                notification_type_registered_unregistered_handler,
                sender=self,
                dispatch_uid='register_unregister_notification_types',
            )

        # Add CORS configuration checks
        from immunity_notifications.checks import check_cors_configuration  # noqa
