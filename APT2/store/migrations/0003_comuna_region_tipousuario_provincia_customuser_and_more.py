# Generated by Django 4.1.6 on 2023-10-25 13:57

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("store", "0002_alter_producto_precio"),
    ]

    operations = [
        migrations.CreateModel(
            name="comuna",
            fields=[
                ("id_comuna", models.BigAutoField(primary_key=True, serialize=False)),
                ("nombre_comuna", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="region",
            fields=[
                ("id_region", models.BigAutoField(primary_key=True, serialize=False)),
                ("nombre_region", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="TipoUsuario",
            fields=[
                (
                    "id",
                    models.CharField(max_length=3, primary_key=True, serialize=False),
                ),
                ("nombre_tipo_usuario", models.CharField(max_length=100)),
                ("descripcion", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="provincia",
            fields=[
                (
                    "id_provincia",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("nombre_provincia", models.CharField(max_length=100)),
                (
                    "id_region",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="store.region",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="customuser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("username", models.CharField(max_length=150, unique=True)),
                ("password", models.CharField(max_length=128)),
                ("rut", models.CharField(max_length=100)),
                (
                    "comuna",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="store.comuna",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="customuser_groups", to="auth.group"
                    ),
                ),
                (
                    "id_tipo_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="store.tipousuario",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="customuser_user_permissions", to="auth.permission"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name="comuna",
            name="id_provincia",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="store.provincia",
            ),
        ),
    ]
