from django.db import models
from product.models import Product
class Transaction(models.Model):
	TID = models.TextField()
	ResultCode = models.TextField()
	ResultMsg = models.TextField()
	MOID = models.TextField(db_index=True)
	ApplDate = models.TextField()
	ApplTime = models.TextField()
	ApplNum = models.TextField()
	PayMethod = models.TextField()
	TotPrice = models.TextField()

"""
class TransactionDetail(models.Model):
	transaction = models.ForeignKey(Transaction,db_index=True)

class CardTransaction(TransactionDetail):
	CARD_Num = models.TextField()

class HPPTransaction(TransactionDetail):
	HPP_Num = models.TextField()

class ArsTransaction(TransactionDetail):
	ARSB_Num = models.TextField()
"""
	
class Payment(models.Model):
	product = models.ForeignKey(Product,db_index=True)
	end_date = models.DateTimeField(null=True, db_index=True)

class PaymentMethod(models.Model):
	payment = models.ForeignKey(Payment,db_index=True)
	class Meta:
		abstract=True

class Dutch(PaymentMethod):
	slug = models.SlugField()	
	close_date = models.DateTimeField(db_index=True)


class DutchTable(models.Model):
	dutch = models.ForeignKey(Dutch, db_index=True)
	money = models.IntegerField()
	transaction = models.ForeignKey(Transaction, db_index=True, null=True)
	name = models.TextField(null=True)
	msg = models.TextField(null=True)
	payed = models.BooleanField(db_index=True)


class Buy(PaymentMethod):
	transaction = models.ForeignKey(Transaction, db_index=True)
	msg = models.TextField()

class Recipient(models.Model):
	payment=models.ForeignKey(Payment, db_index=True)
	class Meta:
		abstract=True

class SMSRecipient(Recipient):
	HPP_Num = models.TextField()

"""
class Buyer(models.Model):
	payment=ForeignKey(Payment, Field.db_index=True)
	class Meta:
		abstract=True
class Sponsor(models.Model):
"""
	

# Create your models here.
