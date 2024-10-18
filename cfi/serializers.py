from rest_framework import serializers
from .models import (
    Category, 
    Tag, 
    TransactionType, 
    Entry, 
    EntryTag, 
    PeriodicType, 
    PeriodicEntry, 
    Installment
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# Serializer para Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'  # Inclui todos os campos do modelo Tag


# Serializer para TransactionType
class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'  # Inclui todos os campos do modelo TransactionType


# Serializer para Entry
class EntrySerializer(serializers.ModelSerializer):
    total_value = serializers.DecimalField(max_digits=15, decimal_places=4, coerce_to_string=False)
    class Meta:
        model = Entry
        fields = '__all__'  # Inclui todos os campos do modelo Entry


# Serializer para EntryTag
class EntryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryTag
        fields = '__all__'  # Inclui todos os campos do modelo EntryTag


# Serializer para PeriodicType
class PeriodicTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicType
        fields = '__all__'  # Inclui todos os campos do modelo PeriodicType


# Serializer para PeriodicEntry
class PeriodicEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicEntry
        fields = '__all__'  # Inclui todos os campos do modelo PeriodicEntry


# Serializer para Installment
class InstallmentSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField(max_digits=15, decimal_places=4, coerce_to_string=False)
    entry = serializers.SerializerMethodField()
    class Meta:
        model = Installment
        fields = '__all__'  # Inclui todos os campos do modelo Installment

    def get_entry(self, obj):
        serializer = EntrySerializer(obj.id_entry)
        return serializer.data