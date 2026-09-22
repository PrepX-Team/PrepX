import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ('subjects', '0002_alter_subject_options_alter_topic_options_and_more')]
    operations = [migrations.CreateModel(name='Certificate', fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('certificate_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
        ('issued_at', models.DateTimeField(auto_now_add=True)),
        ('completed_at', models.DateTimeField()),
        ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificates', to=settings.AUTH_USER_MODEL)),
        ('topic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certificates', to='subjects.topic')),
    ], options={'ordering': ['-issued_at']}),
    migrations.AddConstraint(model_name='certificate', constraint=models.UniqueConstraint(fields=('student', 'topic'), name='one_certificate_per_student_topic'))]
