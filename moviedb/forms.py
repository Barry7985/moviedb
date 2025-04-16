from django import forms
from .models import Film

class FilmFilterForm(forms.Form):
    RATING_CHOICES = [
        ('', 'Toutes les notes'),
        (4, '4+ étoiles'),
        (3, '3+ étoiles'),
        (2, '2+ étoiles'),
        (1, '1+ étoile'),
    ]

    genre = forms.ChoiceField(
        choices=[('', 'Tous les genres')],  
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    annee = forms.ChoiceField(
        choices=[('', 'Toutes les années')],  
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    note_min = forms.ChoiceField(
        choices=RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Note minimum'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Retrieve all unique genres from the Film model
        genres = Film.objects.values_list('genre', flat=True).distinct()
        self.fields['genre'].choices += [(g, g) for g in genres]

        # Retrieve all unique years from the Film model
        annees = Film.objects.dates('date_sortie', 'year')
        self.fields['annee'].choices += [(date.year, date.year) for date in annees]


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un film...'
        })
    )