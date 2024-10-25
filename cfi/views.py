from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
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
    RegisterSerializer,
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

class InstallmentsListByEntry(generics.ListAPIView):
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Recupera o usuário autenticado
        user = self.request.user
        
        # Recupera o id_entry da URL ou dos parâmetros de consulta
        id_entry = self.kwargs.get('id_entry', None) or self.request.query_params.get('id_entry', None)

        if not id_entry:
            raise ValidationError({'detail': 'O parâmetro "id_entry" é obrigatório.'})
        
        return Installment.objects.filter(id_entry=id_entry)

class InstallmentsListByMonthYearView(generics.ListAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')

        # Verifique se os parâmetros foram fornecidos
        if month is None or year is None:
            raise ValueError("Month and year must be provided.")  # Levanta uma exceção

        try:
            month = int(month)
            year = int(year)

            # Verifica se o mês está dentro do intervalo válido
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12.")  # Levanta uma exceção

        except ValueError as e:
            raise ValueError(str(e))  # Levanta uma exceção com a mensagem de erro

        # Calcular o primeiro e o último dia do mês
        start_date = timezone.datetime(year, month, 1)
        if month == 12:
            end_date = timezone.datetime(year + 1, 1, 1)  # Início de janeiro do próximo ano
        else:
            end_date = timezone.datetime(year, month + 1, 1)  # Início do próximo mês

        start_date = timezone.make_aware(start_date)
        end_date = timezone.make_aware(end_date)

        id_user = self.request.user.id

        # Filtrar installments com base na data de referência
        return self.queryset.filter(reference_date__gte=start_date, reference_date__lt=end_date, id_entry__id_user=id_user)

    def get(self, request, *args, **kwargs):
        try:
            # Chama o método get_queryset e retorna uma resposta apropriada
            return super().get(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)  # Retorna uma resposta de erro
        
class CheckTokenView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(True, status=status.HTTP_200_OK)
    
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
