from rest_framework import serializers
from .models import Category, Subcategory, App
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

class SubcategorySerializer(serializers.ModelSerializer):
    apps = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'category', 'name', 'apps']

class AppSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'points', 'category', 'subcategory', 'created_by']
        extra_kwargs = {
            'category': {'required': True},
            'subcategory': {'required': True},
        }

    def validate(self, data):
        """
        Check that the subcategory is related to the category.
        """
        category = data.get('category')
        subcategory = data.get('subcategory')
        
        if category and subcategory:
            if subcategory.category != category:
                raise serializers.ValidationError({
                    'subcategory': 'The selected subcategory does not belong to the selected category.'
                })

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = {
            'id': instance.category.id,
            'name': instance.category.name,
        }
        representation['subcategory'] = {
            'id': instance.subcategory.id,
            'name': instance.subcategory.name,
        }
        representation['created_by'] = {
            'id': instance.created_by.id,
            'username': instance.created_by.full_name
        }
        return representation

    



