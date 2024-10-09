from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly
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
from .serializers import (
    CategorySerializer,
    TagSerializer,
    TransactionTypeSerializer,
    EntrySerializer,
    EntryTagSerializer,
    PeriodicTypeSerializer,
    PeriodicEntrySerializer,
    InstallmentSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ViewSet para Tag
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# ViewSet para TransactionType
class TransactionTypeViewSet(viewsets.ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ViewSet para Entry
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer


# ViewSet para EntryTag
class EntryTagViewSet(viewsets.ModelViewSet):
    queryset = EntryTag.objects.all()
    serializer_class = EntryTagSerializer


# ViewSet para PeriodicType
class PeriodicTypeViewSet(viewsets.ModelViewSet):
    queryset = PeriodicType.objects.all()
    serializer_class = PeriodicTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ViewSet para PeriodicEntry
class PeriodicEntryViewSet(viewsets.ModelViewSet):
    queryset = PeriodicEntry.objects.all()
    serializer_class = PeriodicEntrySerializer


# ViewSet para Installment
class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer