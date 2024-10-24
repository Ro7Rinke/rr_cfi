from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Tag(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)  # Alterado para id_user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class TransactionType(models.Model):
    title = models.CharField(max_length=255)
    is_debit = models.BooleanField()  # se está recebendo ou pagando o valor
    reference = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.BooleanField()  # Valor já foi pago, como um pix por exemplo
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Entry(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    is_periodic = models.BooleanField()
    total_value = models.DecimalField(max_digits=15, decimal_places=4)
    total_installments = models.IntegerField()
    id_transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)  # Alterado para id_transaction_type
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Alterado para id_category
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class EntryTag(models.Model):
    id_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)  # Alterado para id_entry
    id_tag = models.ForeignKey(Tag, on_delete=models.CASCADE)  # Alterado para id_tag
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class PeriodicType(models.Model):
    title = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True, null=True)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class PeriodicEntry(models.Model):
    id_entry = models.ForeignKey(Entry, on_delete=models.SET_NULL, null=True)  # Alterado para id_entry
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    reference_day = models.IntegerField()
    reference_month = models.IntegerField()
    reference_year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

class Installment(models.Model):
    id_entry = models.ForeignKey(Entry, on_delete=models.CASCADE)  # Alterado para id_entry
    value = models.DecimalField(max_digits=15, decimal_places=4)
    reference_date = models.DateTimeField()
    installment_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)