from django.db import transaction
from rest_framework.exceptions import ValidationError
from dateutil.parser import parse as parseDate
from dateutil.relativedelta import relativedelta

from .serializers import InstallmentSerializer

def calculateInstallmentValue(total_value, total_installments):
    if total_installments <= 1:
        return total_value, 0
    
    installment_value = round((total_value / total_installments), 2)

    extra_value = round((total_value - (installment_value * total_installments)), 2)

    return installment_value, extra_value

def createInstallments(installments):
    try:
        with transaction.atomic():  # Inicia uma transação
            for installment_data in installments:
                serializer = InstallmentSerializer(data=installment_data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()  # Salva a parcela no banco de dados
        return (True, None ) # Retorna True se todas as parcelas foram salvas com sucesso

    except ValidationError as e:
        return (False, str(e))  # Retorna False e o erro de validação

    except Exception as e:
        return (False, str(e))  # Retorna False e qualquer outro erro


def generateInstallmentsByEntry(entry):
    installments = []

    installment_value, extra_value = calculateInstallmentValue(entry.total_value, entry.total_installments)
    
    reference_date = entry.date

    for installment_number in range(1, entry.total_installments+1):
        installment = {}
        installment['id_entry'] = entry.id
        installment['installment_number'] = installment_number
        installment['value'] = installment_value + extra_value if installment_number == 1 else installment_value
        installment['reference_date'] = reference_date

        reference_date += relativedelta(months=1)

        installments.append(installment)

    return createInstallments(installments)
    
    


