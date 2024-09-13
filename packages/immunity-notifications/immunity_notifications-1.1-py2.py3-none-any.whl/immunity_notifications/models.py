from swapper import swappable_setting

from immunity_notifications.base.models import (
    AbstractIgnoreObjectNotification,
    AbstractNotification,
    AbstractNotificationSetting,
)


class Notification(AbstractNotification):
    class Meta(AbstractNotification.Meta):
        abstract = False
        app_label = 'immunity_notifications'
        swappable = swappable_setting('immunity_notifications', 'Notification')


class NotificationSetting(AbstractNotificationSetting):
    class Meta(AbstractNotificationSetting.Meta):
        abstract = False
        swappable = swappable_setting('immunity_notifications', 'NotificationSetting')


class IgnoreObjectNotification(AbstractIgnoreObjectNotification):
    class Meta(AbstractIgnoreObjectNotification.Meta):
        abstract = False
        swappable = swappable_setting(
            'immunity_notifications', 'IgnoreObjectNotification'
        )
