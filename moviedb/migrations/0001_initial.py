# Generated by Django 5.1.5 on 2025-02-19 19:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('synopsis', models.TextField()),
                ('genre', models.CharField(max_length=100)),
                ('date_sortie', models.DateField()),
                ('casting', models.TextField()),
                ('duree', models.DurationField()),
                ('affiche', models.ImageField(blank=True, null=True, upload_to='affiches/')),
                ('note_moyenne', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Critique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('texte', models.TextField()),
                ('note', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='critiques', to='accounts.customuser')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='critiques', to='moviedb.film')),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texte', models.TextField()),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='accounts.customuser')),
                ('critique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to='moviedb.critique')),
            ],
        ),
    ]
