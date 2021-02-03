"""
Helpers for Student app emails.
"""


from string import capwords

from django.conf import settings

from lms.djangoapps.verify_student.services import IDVerificationService
from openedx.core.djangoapps.ace_common.template_context import get_base_template_context
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from xmodule.modulestore.django import modulestore


def generate_activation_email_context(user, registration):
    """
    Constructs a dictionary for use in activation email contexts

    Arguments:
        user (User): Currently logged-in user
        registration (Registration): Registration object for the currently logged-in user
    """
    context = get_base_template_context(None)
    context.update({
        'name': user.profile.name,
        'key': registration.activation_key,
        'lms_url': configuration_helpers.get_value('LMS_ROOT_URL', settings.LMS_ROOT_URL),
        'platform_name': configuration_helpers.get_value('PLATFORM_NAME', settings.PLATFORM_NAME),
        'support_url': configuration_helpers.get_value(
            'ACTIVATION_EMAIL_SUPPORT_LINK', settings.ACTIVATION_EMAIL_SUPPORT_LINK
        ) or settings.SUPPORT_SITE_LINK,
        'support_email': configuration_helpers.get_value('CONTACT_EMAIL', settings.CONTACT_EMAIL),
    })
    return context


def generate_proctoring_requirements_email_context(user, course_id):
    """
    Constructs a dictionary for use in proctoring requirements email context

    Arguments:
        user: Currently logged-in user
        course_id: ID of the proctoring-enabled course the user is enrolled in
    """
    course_module = modulestore().get_course(course_id)
    return {
        'user': user,
        'course_name': course_module.display_name,
        'proctoring_provider': capwords(course_module.proctoring_provider.replace('_', ' ')),
        'proctoring_requirements_url': settings.PROCTORING_SETTINGS.get('LINK_URLS', {}).get('faq', ''),
        'id_verification_url': IDVerificationService.get_verify_location(),
    }