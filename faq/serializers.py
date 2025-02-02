from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    """
    Serializer for FAQ model with multilingual support.
    Handles translations based on the language parameter in the request.
    """
    question = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_question(self, obj):
        """Get the question in the requested language."""
        lang = self.context.get('request').query_params.get('lang', 'en')
        return obj.get_question(lang)

    def get_answer(self, obj):
        """Get the answer in the requested language."""
        lang = self.context.get('request').query_params.get('lang', 'en')
        return obj.get_answer(lang)

    def create(self, validated_data):
        """Create a new FAQ."""
        return FAQ.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an FAQ."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
