# Generated by Django 4.1.6 on 2023-10-27 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_comuna_region_tipousuario_provincia_customuser_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="customuser",
        ),
        migrations.DeleteModel(
            name="TipoUsuario",
        ),
    ]