from rest_framework import serializers
from moviedb.models import Film, Critique, Commentaire
from accounts.models import CustomUser
from django.utils.timesince import timesince

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email')
        read_only_fields = fields

class FilmSerializer(serializers.ModelSerializer):
    # Add calculated fields or methods if needed
    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = ('note_moyenne',)

class CritiqueSerializer(serializers.ModelSerializer):
    # Nested serializers for related fields
    film = FilmSerializer(read_only=True)
    utilisateur = CustomUserSerializer(read_only=True)
    
    # Human-readable time since publication
    time_since_publication = serializers.SerializerMethodField()
    time_since_modification = serializers.SerializerMethodField()
    
    class Meta:
        model = Critique
        fields = '__all__'
        read_only_fields = ('date_publication', 'date_modification', 'utilisateur')
    
    def get_time_since_publication(self, obj):
        return timesince(obj.date_publication)
    
    def get_time_since_modification(self, obj):
        return timesince(obj.date_modification)

class CommentaireSerializer(serializers.ModelSerializer):
    # Nested serializers for related fields
    critique = serializers.PrimaryKeyRelatedField(queryset=Critique.objects.all())
    utilisateur = CustomUserSerializer(read_only=True)
    
    # Human-readable time since publication
    time_since_publication = serializers.SerializerMethodField()
    
    class Meta:
        model = Commentaire
        fields = '__all__'
        read_only_fields = ('date_publication', 'utilisateur')
    
    def get_time_since_publication(self, obj):
        return timesince(obj.date_publication)

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