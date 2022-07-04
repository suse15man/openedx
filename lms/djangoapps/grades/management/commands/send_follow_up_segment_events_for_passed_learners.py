"""
Send segment events for passed learners so that Braze can send 90 day follow up email.
"""

import logging

from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from django.utils import timezone

from common.djangoapps.track import segment
from lms.djangoapps.grades.constants import (
    LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE,
    LEARNER_PASSED_COURSE_FIRST_TIME_FOLLOW_UP_EVENT_TYPE
)
from lms.djangoapps.grades.models import LearnerCourseEvent

log = logging.getLogger(__name__)


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
        follow_up_events = LearnerCourseEvent.objects.filter(
            follow_up_date=today,
            event_type=LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE,
        )

        paginator = Paginator(follow_up_events, 500)
        for page_number in paginator.page_range:
            page = paginator.page(page_number)

            for follow_up_event in page:
                if should_fire_event:
                    segment.track(follow_up_event.user_id, LEARNER_PASSED_COURSE_FIRST_TIME_FOLLOW_UP_EVENT_TYPE, follow_up_event.data)

                follow_up_event_ids.append(follow_up_event.id)

                log.info(
                    "{} Segment event fired for passed learner. Event: [{}], Data: [{}]".format(
                        log_prefix,
                        LEARNER_PASSED_COURSE_FIRST_TIME_FOLLOW_UP_EVENT_TYPE,
                        follow_up_event.data
                    )
                )

        log.info(f"{log_prefix} Command completed. Segment event triggered for ids: [{follow_up_event_ids}")
