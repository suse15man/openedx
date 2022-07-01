"""
Send segment events for passed learners so that Braze can send 90 day follow up email.
"""

import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from common.djangoapps.track import segment
from lms.djangoapps.grades.models import PassedLearnerEvent

log = logging.getLogger(__name__)

EVENT_NAME = 'edx.course.learner.passed.first_time.followup'


class Command(BaseCommand):
    """
    Example usage:
        $ ./manage.py lms send_follow_up_segment_events_for_passed_learners
    """

    help = 'Send follow up segment events for passed learners.'

    def add_arguments(self, parser):
        """
        Entry point to add arguments.
        """
        parser.add_argument(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Dry Run, print log messages without firing the segment event.',
        )

    def handle(self, *args, **options):
        """
        Command's entry point.
        """
        should_fire_event = not options['dry_run']

        log_prefix = '[SEND_FOLLOW_UP_SEGMENT_EVENTS_FOR_PASSED_LEARNERS]'
        if not should_fire_event:
            log_prefix = '[DRY RUN]'

        follow_up_event_ids = []
        log.info(f'{log_prefix} Command started.')

        today = timezone.now().date()
        follow_up_events = PassedLearnerEvent.objects.filter(follow_up_date=today)

        for follow_up_event in follow_up_events:
            if should_fire_event:
                segment.track(follow_up_event.user_id, EVENT_NAME, follow_up_event.data)

            follow_up_event_ids.append(follow_up_event.id)

            log.info(
                "{} Segment event fired for passed learner. Event: [{}], Data: [{}]".format(
                    log_prefix,
                    EVENT_NAME,
                    follow_up_event.data
                )
            )

        log.info(f"{log_prefix} Command completed. Segment event triggered for ids: [{follow_up_event_ids}")
