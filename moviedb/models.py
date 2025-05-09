from django.db import models
from django.db.models import Avg
from accounts.models import CustomUser
from django.utils import timezone
from django.utils.text import slugify
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
    date_ajout = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    tmdb_id = models.IntegerField(null=True, blank=True, unique=True)  # ID du film dans TMDB
    poster_url = models.URLField(max_length=500, null=True, blank=True)  # URL de l'affiche TMDB
    
    class Meta:
        ordering = ['-date_sortie']
        indexes = [
            models.Index(fields=['titre']),
            models.Index(fields=['genre']),
            models.Index(fields=['date_sortie']),
            models.Index(fields=['tmdb_id']),
        ]

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from title
            base_slug = slugify(self.titre)
            slug = base_slug
            n = 1
            # Check if slug exists and generate a unique one if needed
            while Film.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def update_note_moyenne(self):
        """Met à jour la note moyenne du film basée sur les critiques"""
        avg = self.critiques.aggregate(Avg('note'))['note__avg']
        self.note_moyenne = round(avg if avg else 0.0, 1)
        self.save()

    @property
    def get_poster_url(self):
        """Returns the poster URL with fallback to a random placeholder if no poster exists"""
        if self.poster_url:
            return self.poster_url
        elif self.affiche:
            return self.affiche.url
        else:
            # Use a random placeholder image from picsum
            return f'https://picsum.photos/300/450?random={self.id}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('moviedb:movie_detail', kwargs={'slug': self.slug})

class Critique(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='critiques')
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='critiques')
    titre = models.CharField(max_length=255)
    texte = models.TextField()
    note = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Note de 1 à 5
    date_publication = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_publication']
        unique_together = ['film', 'utilisateur']  # Un utilisateur ne peut avoir qu'une critique par film
        indexes = [
            models.Index(fields=['film', 'utilisateur']),
            models.Index(fields=['date_publication']),
        ]

    def __str__(self):
        return f"{self.titre} par {self.utilisateur.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.film.update_note_moyenne()

class Commentaire(models.Model):
    critique = models.ForeignKey(Critique, on_delete=models.CASCADE, related_name='commentaires')
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentaires')
    texte = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)
    est_modere = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['date_publication']
        indexes = [
            models.Index(fields=['critique', 'date_publication']),
        ]

    def __str__(self):
        return f"Commentaire par {self.utilisateur.username} sur {self.critique.titre}"