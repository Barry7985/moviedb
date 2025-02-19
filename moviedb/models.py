from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Film(models.Model):
    titre = models.CharField(max_length=255)
    synopsis = models.TextField()
    genre = models.CharField(max_length=100)
    date_sortie = models.DateField()
    casting = models.TextField()  # Liste des acteurs principaux
    duree = models.DurationField()  # Durée en minutes
    affiche = models.ImageField(upload_to='affiches/', null=True, blank=True)
    note_moyenne = models.FloatField(default=0.0)  # Calculée à partir des critiques

    def __str__(self):
        return self.titre
class Critique(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='critiques')
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='critiques')
    titre = models.CharField(max_length=255)
    texte = models.TextField()
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Note de 1 à 5
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titre} par {self.utilisateur.username}"
    
class Commentaire(models.Model):
    critique = models.ForeignKey(Critique, on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentaires')
    texte = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire par {self.utilisateur.username} sur {self.critique.titre}"