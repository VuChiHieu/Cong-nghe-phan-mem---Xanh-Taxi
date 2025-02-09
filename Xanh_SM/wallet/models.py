from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from app_admin.models import Student, Driver

class Wallet(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, null=True, blank=True)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def clean(self):
        """ Đảm bảo một ví chỉ thuộc về một người duy nhất """
        if self.student and self.driver:
            raise ValidationError("Ví chỉ có thể thuộc về Student hoặc Driver, không thể thuộc cả hai!")

    def __str__(self):
        owner = self.student.user if self.student else self.driver.user
        return f"Wallet of {owner}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Nạp tiền'),
        ('withdrawal', 'Rút tiền'),
        ('refund', 'Hoàn tiền'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.wallet}"


@receiver(post_save, sender=Transaction)
def update_wallet_balance(sender, instance, **kwargs):
    """ Tự động cập nhật số dư khi có giao dịch """
    wallet = instance.wallet
    try:
        with transaction.atomic():
            if instance.transaction_type == 'deposit':
                wallet.balance += instance.amount
            elif instance.transaction_type == 'withdrawal':
                if wallet.balance >= instance.amount:
                    wallet.balance -= instance.amount
                else:
                    raise ValidationError("Số dư không đủ để rút tiền")
            elif instance.transaction_type == 'refund':
                wallet.balance += instance.amount

            wallet.save()
    except ValidationError as e:
        print(f"Lỗi: {e}")