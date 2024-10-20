# Generated by Django 5.1.1 on 2024-10-06 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_event_created_at_event_inserted_by_event_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketpurchase',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='event',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='tickets.organisation'),
        ),
    ]