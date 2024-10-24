# Generated by Django 3.2.25 on 2024-10-24 08:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RideEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('ride', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='ride.ride')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]