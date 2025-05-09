from rest_framework import serializers
from moviedb.models import Film, Critique, Commentaire
from accounts.models import CustomUser
from django.utils.timesince import timesince

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'avatar', 'date_inscription']
        read_only_fields = ['date_inscription']

class FilmSerializer(serializers.ModelSerializer):
    critiques = serializers.SerializerMethodField()
    
    class Meta:
        model = Film
        fields = ['id', 'titre', 'synopsis', 'genre', 'date_sortie', 'casting',
                 'duree', 'affiche', 'note_moyenne', 'date_ajout', 'slug', 'critiques']
        read_only_fields = ['note_moyenne', 'date_ajout', 'slug']
    
    def get_critiques(self, obj):
        critiques = Critique.objects.filter(film=obj)
        return CritiqueSerializer(critiques, many=True).data

class CritiqueSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    commentaires = serializers.SerializerMethodField()
    
    class Meta:
        model = Critique
        fields = ['id', 'film', 'utilisateur', 'titre', 'texte', 'note', 
                 'date_publication', 'date_modification', 'commentaires']
        read_only_fields = ['date_publication', 'date_modification']
    
    def get_commentaires(self, obj):
        commentaires = Commentaire.objects.filter(critique=obj)
        return CommentaireSerializer(commentaires, many=True).data

class CommentaireSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)
    
    class Meta:
        model = Commentaire
        fields = ['id', 'critique', 'utilisateur', 'texte', 'date_publication', 'est_modere']
        read_only_fields = ['date_publication', 'est_modere']

# For creating critiques (without nested representations)
class CreateCritiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Critique
        fields = ('film', 'titre', 'texte', 'note')
    
    def validate_note(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La note doit être entre 1 et 5")
        return value

# For creating comments (without nested representations)
class CreateCommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ('critique', 'texte')