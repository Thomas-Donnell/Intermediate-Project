# Generated by Django 4.2.4 on 2023-11-10 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0021_studentquestion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentquestion',
            name='option1',
        ),
        migrations.RemoveField(
            model_name='studentquestion',
            name='option2',
        ),
        migrations.RemoveField(
            model_name='studentquestion',
            name='option3',
        ),
        migrations.RemoveField(
            model_name='studentquestion',
            name='option4',
        ),
        migrations.RemoveField(
            model_name='studentquestion',
            name='question_text',
        ),
        migrations.AddField(
            model_name='studentquestion',
            name='attempt',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentquestion',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.question'),
        ),
    ]