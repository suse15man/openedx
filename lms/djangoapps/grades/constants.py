"""
Constants and Enums used by Grading.
"""


class ScoreDatabaseTableEnum:
    """
    The various database tables that store scores.
    """
    courseware_student_module = 'csm'
    submissions = 'submissions'
    overrides = 'overrides'


class GradeOverrideFeatureEnum:
    proctoring = 'PROCTORING'
    gradebook = 'GRADEBOOK'
    grade_import = 'grade-import'


LEARNER_PASSED_COURSE_FIRST_TIME_EVENT_TYPE = 'edx.course.learner.passed.first_time'
LEARNER_PASSED_COURSE_FIRST_TIME_FOLLOW_UP_EVENT_TYPE = 'edx.course.learner.passed.first_time.followup'
