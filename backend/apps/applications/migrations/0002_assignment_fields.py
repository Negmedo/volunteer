from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='coordinator_rating',
            field=models.PositiveSmallIntegerField(
                blank=True, null=True,
                help_text='Оценка координатора от 1 до 5'
            ),
        ),
        migrations.AddField(
            model_name='assignment',
            name='hours_worked',
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text='Фактическое количество часов участия'
            ),
        ),
        migrations.AddField(
            model_name='assignment',
            name='coordinator_note',
            field=models.TextField(blank=True, default='', help_text='Комментарий координатора'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        # motivation_text уже есть в Application из 0001, но на всякий случай
        # убеждаемся что blank=True
        migrations.AlterField(
            model_name='application',
            name='motivation_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]