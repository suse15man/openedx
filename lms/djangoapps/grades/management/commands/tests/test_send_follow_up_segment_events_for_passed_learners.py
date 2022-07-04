"""
Tests for `send_follow_up_segment_events_for_passed_learners` management command.
"""

from datetime import timedelta
from unittest import mock
from unittest.mock import patch

import ddt
from django.core.management import call_command
from django.utils import timezone

from lms.djangoapps.grades.constants import LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE
from lms.djangoapps.grades.management.commands import send_follow_up_segment_events_for_passed_learners
from lms.djangoapps.grades.management.commands.send_follow_up_segment_events_for_passed_learners import (
    LEARNER_PASSED_COURSE_FIRST_TIME_FOLLOW_UP_EVENT_TYPE
)
from lms.djangoapps.grades.models import LearnerCourseEvent
from openedx.core.djangoapps.content.course_overviews.tests.factories import CourseOverviewFactory
from xmodule.modulestore.tests.django_utils import \
    SharedModuleStoreTestCase  # lint-amnesty, pylint: disable=wrong-import-order


@ddt.ddt
class TestSendFollowupSegmentEventsForPassedLearnersCommand(SharedModuleStoreTestCase):
    """
    Tests `send_follow_up_segment_events_for_passed_learners` management command.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.command = send_follow_up_segment_events_for_passed_learners.Command()
        course_end = timezone.now() - timedelta(days=120)
        cls.course_overview = CourseOverviewFactory.create(end=course_end)

        cls.today = timezone.now().date()
        cls.yesterday = timezone.now().date() - timedelta(days=1)
        cls.test_data = [
            {
                'user_id': 100,
                'course_id': cls.course_overview.id,
                'data': {
                    'LMS_ENROLLMENT_ID': 1001,
                    'COURSE_TITLE': 'An introduction to Calculus',
                    'COURSE_ORG_NAME': 'MathX',
                },
                'follow_up_date': cls.today,
                'event_type': LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE,
            },
            {
                'user_id': 200,
                'course_id': cls.course_overview.id,
                'data': {
                    'LMS_ENROLLMENT_ID': 2001,
                    'COURSE_TITLE': 'An introduction to Python',
                    'COURSE_ORG_NAME': 'PythonX',
                },
                'follow_up_date': cls.today,
                'event_type': LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE,
            },
            {
                'user_id': 300,
                'course_id': cls.course_overview.id,
                'data': {
                    'LMS_ENROLLMENT_ID': 3001,
                    'COURSE_TITLE': 'An introduction to Databases',
                    'COURSE_ORG_NAME': 'DatabaseX',
                },
                'follow_up_date': cls.yesterday,
                'event_type': LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE,
            },
        ]

        for item in cls.test_data:
            LearnerCourseEvent.objects.create(**item)

    def construct_event_call_data(self):
        """
        Construct segment event call data for verification.
        """
        event_call_data = []
        for item in self.test_data:
            if item.get('follow_up_date') == self.today:
                event_call_data.append([
                    item.get('user_id'),
                    LEARNER_PASSED_COURSE_FIRST_TIME_FOLLOW_UP_EVENT_TYPE,
                    item.get('data'),
                ])
        return event_call_data

    @patch('lms.djangoapps.grades.management.commands.send_follow_up_segment_events_for_passed_learners.segment.track')
    def test_command_dry_run(self, segment_track_mock):
        """
        Verify that management command does not fire any segment event in dry run mode.
        """
        call_command(self.command, '--dry-run')
        segment_track_mock.assert_has_calls([])

    @patch('lms.djangoapps.grades.management.commands.send_follow_up_segment_events_for_passed_learners.segment.track')
    def test_command(self, segment_track_mock):
        """
        Verify that management command fires segment events with correct data.

        * Event should be fired for records having follow_up_date set to today.
        """
        call_command(self.command)
        expected_segment_event_calls = [mock.call(*event_data) for event_data in self.construct_event_call_data()]
        segment_track_mock.assert_has_calls(expected_segment_event_calls)
