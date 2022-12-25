from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from items.models import Item, MediaFile, Category, Brand


class MediaFileSerializer(ModelSerializer):
    class Meta:
        model = MediaFile
        fields = '__all__'


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ItemGetSerializer(ModelSerializer):
    media_group = MediaFileSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    brand = BrandSerializer(many=True, read_only=True)
    gender = serializers.SerializerMethodField(read_only=True)
    quality = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Item
        fields = '__all__'

    def get_gender(self, obj):
        return obj.get_gender_display()

    def get_quality(self, obj):
        return obj.get_quality_display()


class ItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'
