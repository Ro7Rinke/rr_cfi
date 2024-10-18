from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
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
    permission_classes = [IsAuthenticated]


# ViewSet para TransactionType
class TransactionTypeViewSet(viewsets.ModelViewSet):
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ViewSet para Entry
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            data = kwargs.get('data', {})
            if isinstance(data, dict):
                data['id_user'] = self.request.user.id
            kwargs['data'] = data

        return super().get_serializer(*args, **kwargs)

# ViewSet para EntryTag
class EntryTagViewSet(viewsets.ModelViewSet):
    queryset = EntryTag.objects.all()
    serializer_class = EntryTagSerializer
    permission_classes = [IsAuthenticated]


# ViewSet para PeriodicType
class PeriodicTypeViewSet(viewsets.ModelViewSet):
    queryset = PeriodicType.objects.all()
    serializer_class = PeriodicTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


# ViewSet para PeriodicEntry
class PeriodicEntryViewSet(viewsets.ModelViewSet):
    queryset = PeriodicEntry.objects.all()
    serializer_class = PeriodicEntrySerializer
    permission_classes = [IsAuthenticated]


# ViewSet para Installment
class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

class InstallmentsListByMonthYearView(generics.ListAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        # Verifique se os parâmetros foram fornecidos
        if month is None or year is None:
            return Response({"error": "Month and year must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month)
            year = int(year)

            # Verifica se o mês está dentro do intervalo válido
            if month < 1 or month > 12:
                return Response({"error": "Month must be between 1 and 12."}, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({"error": "Invalid month or year."}, status=status.HTTP_400_BAD_REQUEST)

        # Calcular o primeiro e o último dia do mês
        start_date = timezone.datetime(year, month, 1)
        if month == 12:
            end_date = timezone.datetime(year + 1, 1, 1)  # Início de janeiro do próximo ano
        else:
            end_date = timezone.datetime(year, month + 1, 1)  # Início do próximo mês

        id_user = self.request.user.id

        # Filtrar installments com base na data de referência
        return self.queryset.filter(reference_date__gte=start_date, reference_date__lt=end_date, id_entry__id_user=id_user)

    def get(self, request, *args, **kwargs):
        # Chama o método get_queryset e retorna uma resposta apropriada
        return super().get(request, *args, **kwargs)