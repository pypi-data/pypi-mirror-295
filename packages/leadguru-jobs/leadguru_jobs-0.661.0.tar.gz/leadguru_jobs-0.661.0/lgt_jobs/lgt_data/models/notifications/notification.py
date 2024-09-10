from datetime import datetime, UTC, timedelta
from lgt_jobs.env import portal_url
from lgt_jobs.lgt_data.enums import NotificationType
from lgt_jobs.lgt_data.models.base import DictionaryModel
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.post.post import Post
from lgt_jobs.lgt_data.models.user_leads.extended_user_lead import ExtendedUserLeadModel
from lgt_jobs.lgt_data.models.user_leads.user_lead import UserLeadModel


class Notification(DictionaryModel):
    def __init__(self):
        self.enabled: bool = True
        self.type: NotificationType = NotificationType.INSTANTLY
        self.day: int | None = None
        self.hour: int | None = None
        self.minute: int | None = None
        self.last_notification: datetime | None = None
        self.need_to_notify: bool = False
        self.attributes: list = []

    @property
    def need_to_notify_now(self) -> bool:
        if not self.enabled or not self.need_to_notify:
            return False

        now = datetime.now(UTC)
        current_week_day = datetime.isoweekday(now)
        if self.last_notification:
            self.last_notification = self.last_notification.replace(tzinfo=UTC)

        if (self.type == NotificationType.UNREAD_FOR_FEW_MINUTES
                and self.last_notification and (now.minute - self.minute <= self.last_notification.minute)):
            return False

        if self.type == NotificationType.ONCE_A_WEEK and current_week_day != self.day:
            return False

        if ((self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK)
                and (now.hour != self.hour or now.minute < self.minute)):
            return False

        if ((self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK)
                and self.last_notification and self.last_notification > now - timedelta(hours=1)):
            return False

        return True

    @staticmethod
    def need_to_notify_week_before(date: datetime) -> bool:
        return datetime.now(UTC) < (date + timedelta(7))


class IncomingMessageNotification(Notification):
    @staticmethod
    def get_button_name() -> str:
        return 'View message'

    @staticmethod
    def get_button_url(sender_id: str, source_id: str) -> str:
        return f'{portal_url}/feed?senderId={sender_id}&sourceId={source_id}'

    def get_subject_text(self, users: list) -> str:
        if self.type == NotificationType.INSTANTLY or self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            return 'New message from your lead'
        elif len(users) > 1:
            return 'Unread messages from your lead'
        return 'Unread message from your lead'

    def get_notification_text(self, users: list):
        if self.type == NotificationType.INSTANTLY:
            return f'{users[-1]} has just sent you a message.'
        elif self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            return f'{users[-1]} sent you a message {self.minute} minutes ago.'
        elif (self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK) and users:
            match len(users):
                case 1:
                    return f'You have unread message(s) from {users[0]}.'
                case 2 | 3:
                    return f'You have unread messages from {", ".join(users)}.'
                case _:
                    return f'You have unread messages from {", ".join(users[:3])} and other leads.'


class InboxNotification(Notification):

    @staticmethod
    def get_button_name():
        return 'View message request'

    @staticmethod
    def get_button_url():
        return f'{portal_url}/feed?requests=true'

    def get_subject_text(self, users: list) -> str:
        if self.type == NotificationType.INSTANTLY:
            return 'New message request on Leadguru'
        elif len(users) > 1:
            return 'Message requests on Leadguru'
        return 'Message request on Leadguru'

    def get_notification_text(self, users: list):
        if self.type == NotificationType.INSTANTLY:
            return f'{users[0]} has just sent you message request.'
        elif (self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK) and users:
            match len(users):
                case 1:
                    return f'You have unread message request from {users[0]}.'
                case 2 | 3:
                    return f'You have unread message request from {", ".join(users)}.'
                case _:
                    return f'You have unread message requests from {", ".join(users[:3])} and other leads.'


class SourceDeactivationNotification(Notification):
    @staticmethod
    def get_button_name() -> str:
        return 'Show community'

    @staticmethod
    def get_button_url() -> str:
        return f'{portal_url}/communities?inactive=true'

    @staticmethod
    def get_subject_text() -> str:
        return 'Inactivation of Community on Leadguru'

    def get_notification_text(self, bots: list[DedicatedBotModel]):
        names = [bot.source.source_name.capitalize() for bot in bots]
        if self.type == NotificationType.INSTANTLY:
            return f'{bots[-1].source.source_name.capitalize()} became inactive on Leadguru.'
        elif (self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.ONCE_A_WEEK) and bots:
            match len(bots):
                case 1:
                    return f'{names[-1]} became inactive on Leadguru.'
                case 2 | 3:
                    return f'{", ".join(names)} became inactive on Leadguru.'
                case _:
                    return f'{", ".join(names[:3])} and other became inactive on Leadguru.'


class BulkRepliesNotification(Notification):

    @staticmethod
    def get_button_name() -> str:
        return 'View post'

    @staticmethod
    def get_button_url(post: Post) -> str:
        return f'{portal_url}/bulk-post/form/{post.id}'

    def get_subject_text(self, post: Post) -> str:
        replied_messages = [message.id for message in post.messages if message.id in self.attributes]
        if len(replied_messages) > 1:
            return 'New replies to your bulk post'
        return 'New reply to your bulk post'

    @staticmethod
    def get_notification_text(post: Post):
        if len(post.messages) <= 1:
            source_name = post.messages[0].server_name
            channel_name = post.messages[0].channel_name
            return f'You have new reply in #{channel_name} from {source_name.capitalize()} to your {post.title} post.'

        channels = set([message.channel_id for message in post.messages])
        sources = set([message.server_id for message in post.messages])
        return (f'You have new replies in {len(channels)} from {len(sources)} communities '
                f'to your {post.title} post.')


class BulkReactionsNotification(Notification):

    @staticmethod
    def get_button_name() -> str:
        return 'View post'

    @staticmethod
    def get_button_url(post: Post) -> str:
        return f'{portal_url}/bulk-post/form/{post.id}'

    @staticmethod
    def get_subject_text() -> str:
        return 'People are reacting to your post'

    @staticmethod
    def get_notification_text(post: Post):
        if len(post.messages) <= 1:
            source_name = post.messages[0].server_name
            channel_name = post.messages[0].channel_name
            return (f'You have new reaction in #{channel_name} from {source_name.capitalize()} '
                    f'to your {post.title} post.')

        channels = set([message.channel_id for message in post.messages])
        sources = set([message.server_id for message in post.messages])
        return (f'You have new reactions in {len(channels)} from {len(sources)} communities '
                f'to your {post.title} post.')


class FollowUpNotification(Notification):

    @property
    def need_to_notify_now(self) -> bool:
        allowed_types = [NotificationType.ONCE_A_DAY, NotificationType.ONCE_A_DAY,
                         NotificationType.UNREAD_FOR_FEW_MINUTES]
        if not self.enabled or self.type not in allowed_types:
            return False

        now = datetime.now(UTC)
        if self.last_notification:
            self.last_notification = self.last_notification.replace(tzinfo=UTC)

        if (self.type == NotificationType.ONCE_A_DAY and self.last_notification
                and (self.last_notification.day == now.day or self.hour != now.hour)):
            return False

        if (self.type == NotificationType.ONCE_A_WEEK and self.last_notification
                and (self.last_notification.day == now.day or (now.hour != self.hour or now.day != self.day))):
            return False

        return True

    def has_not_notified_leads(self, actual: list[UserLeadModel]) -> bool:
        if self.type == NotificationType.UNREAD_FOR_FEW_MINUTES and self.last_notification:
            self.last_notification = self.last_notification.replace(tzinfo=UTC)
            not_notified_leads = [lead for lead in actual if lead.followup_date.replace(tzinfo=UTC) >
                                  (self.last_notification + timedelta(minutes=self.minute))]
            return bool(not_notified_leads)

        return True

    @staticmethod
    def get_button_name(actual: list[UserLeadModel]) -> str:
        if len(actual) > 1:
            return 'View calendar'
        return 'Send message'

    def get_button_url(self, actual: list[UserLeadModel]) -> str:
        if len(actual) > 1:
            if self.type == NotificationType.ONCE_A_DAY or self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
                return f'{portal_url}/dashboard/calendar?view=day'
            return f'{portal_url}/dashboard/calendar?view=week'
        return f'{portal_url}/feed?senderId={actual[0].message.sender_id}&sourceId={actual[0].message.source.source_id}'

    def get_subject_text(self, actual: list[UserLeadModel]) -> str:
        subject_text = 'You have planned follow-ups' if len(actual) > 1 else 'You have planned follow-up'

        if self.type == NotificationType.ONCE_A_DAY:
            return f'{subject_text} for today'
        elif self.type == NotificationType.ONCE_A_WEEK:
            return f'{subject_text} for this week'
        elif self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            return f'{subject_text} for today in {self.minute} minutes'

        return subject_text

    def get_notification_text(self, actual: list[ExtendedUserLeadModel], overdue: list[ExtendedUserLeadModel]) -> str:
        notification_text = ''
        names = [lead.contact.real_name for lead in actual]
        if self.type == NotificationType.ONCE_A_DAY:
            match len(actual):
                case 1:
                    notification_text = f'You have planned to send follow-up today to {names[0]}.'
                case 2 | 3:
                    notification_text = f'You have planned to send follow-up today to {", ".join(names)}.'
                case _:
                    notification_text = (f'You have planned to send follow-up today to {", ".join(names[:3])} '
                                         f'and {len(names) - 3} other leads.')
        elif self.type == NotificationType.ONCE_A_WEEK:
            match len(actual):
                case 1:
                    notification_text = f'You have planned to send follow-up to {names[0]} this week.'
                case 2 | 3:
                    notification_text = f'You have planned to send follow-up to {", ".join(names)} this week.'
                case _:
                    notification_text = (f'You have planned to send follow-up to {", ".join(names[:3])} '
                                         f'and {len(names) - 3} other leads this week.')
        elif self.type == NotificationType.UNREAD_FOR_FEW_MINUTES:
            match len(actual):
                case 1:
                    notification_text = (f'You have planned to send follow-up today in '
                                         f'{self.minute} minutes to {names[0]}.')
                case 2 | 3:
                    notification_text = (f'You have planned to send follow-up today in '
                                         f'{self.minute} minutes to {", ".join(names)}.')
                case _:
                    notification_text = (f'You have planned to send follow-up today in '
                                         f'{self.minute} minutes to {", ".join(names[:3])} '
                                         f'and {len(names) - 3} other leads.')

        return f'{notification_text} Plus you have {len(overdue)} overdue follow-ups.' if overdue else notification_text


class BillingNotifications(Notification):
    pass
