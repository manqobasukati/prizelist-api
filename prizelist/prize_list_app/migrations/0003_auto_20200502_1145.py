# Generated by Django 3.0.5 on 2020-05-02 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prize_list_app', '0002_auto_20200502_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='prize_list_app.Order'),
        ),
    ]
