# Generated by Django 3.2.12 on 2022-02-23 08:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import opaque_keys.edx.django.models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lti_consumer', '0013_auto_20210712_1352'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCourseLiveConfiguration',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('course_key', opaque_keys.edx.django.models.CourseKeyField(db_index=True, max_length=255)),
                ('enabled', models.BooleanField(default=True, help_text='If disabled, the LTI in the associated course will be disabled.')),
                ('provider_type', models.CharField(help_text="The LTI provider's id", max_length=50, verbose_name='LTI provider')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('lti_configuration', models.ForeignKey(blank=True, db_constraint=False, help_text='The LTI configuration data for this course/provider.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lti_consumer.lticonfiguration')),
            ],
            options={
                'verbose_name': 'historical course live configuration',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='CourseLiveConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('course_key', opaque_keys.edx.django.models.CourseKeyField(db_index=True, max_length=255)),
                ('enabled', models.BooleanField(default=True, help_text='If disabled, the LTI in the associated course will be disabled.')),
                ('provider_type', models.CharField(help_text="The LTI provider's id", max_length=50, verbose_name='LTI provider')),
                ('lti_configuration', models.ForeignKey(blank=True, help_text='The LTI configuration data for this course/provider.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='lti_consumer.lticonfiguration')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]