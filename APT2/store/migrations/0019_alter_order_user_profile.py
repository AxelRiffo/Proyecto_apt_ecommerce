# Generated by Django 4.2.6 on 2023-11-17 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_contacto_mostrar_comentarios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.userprofile'),
        ),
    ]
