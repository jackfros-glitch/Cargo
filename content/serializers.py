from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Category, Content, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']



class ContentSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(required= True)
    tags = serializers.ListField(child=serializers.CharField(), write_only=True )
    
    class Meta:
        model = Content
        fields = ['id', 'title', 'description', 'category_id', 'tags', 'ai_relevance_score']
        read_only_fields = ['id', 'ai_relevance_score']
        
        
        
        
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id = category_id)
        content = Content.objects.create(category = category, **validated_data)
        for tag in tags:
            tag, created = Tag.objects.get_or_create(name=tag)
            content.tags.add(tag)
        
        return content
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.ai_relevance_score = validated_data.get('ai_relevance_score', instance.ai_relevance_score)
        instance.save()

        
        instance.tags.clear()
        for tag in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag)
            instance.tags.add(tag)

        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = [tag.name for tag in instance.tags.all()] 
        return data