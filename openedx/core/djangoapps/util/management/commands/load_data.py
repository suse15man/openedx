#!/usr/bin/env python3
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from common.djangoapps.student.tests.factories import CourseEnrollmentFactory, UserFactory
from common.djangoapps.course_modes.models import CourseMode
from django.contrib.auth import get_user_model
import yaml
import codecs

from lms.djangoapps.verify_student.tests.factories import SoftwareSecurePhotoVerificationFactory

class Command(BaseCommand):
    """
    Use to populate your database with some essential basic data
    """

    def add_arguments(self, parser):
        parser.add_argument('--data-file-path', type=str, required=True, help="Path to file where your data is specified.")


    def handle(self, *args, **options):
        with open(options["data_file_path"], 'r') as f:
            data_spec = yaml.safe_load(f)
        for user_spec in data_spec.get('users', []):
            self.create_user(user_spec)
        for enrollment_spec in data_spec.get('enrollments', []):
            self.create_enrollment(enrollment_spec)

    def create_user(self, user):
        """
        Use to create users in your database.
        """
        return UserFactory.create(**user)

    def create_enrollment(self, enrollment_spec):
        """
        Use to create enrollments in your database.
        """
        User = get_user_model()
        try:
            user = User.objects.get(username=enrollment_spec['username'])
        except User.DoesNotExist:
            raise exception(f"User:{enrollment_spec['username']} not created before trying to create enrollment")
        if enrollment_spec['mode'] in CourseMode.VERIFIED_MODES:
            verfication = SoftwareSecurePhotoVerificationFactory(user=user)
        enrollment = CourseEnrollmentFactory(user=user, course_id=enrollment_spec['course_id'])
        if enrollment.mode != enrollment_spec['mode']:
            enrollment.mode = enrollment_spec['mode']
            enrollment.save()
        return enrollment