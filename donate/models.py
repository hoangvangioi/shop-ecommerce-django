from django.db import models

# Create your models here.


class Bank(models.Model):
	bank = models.CharField(max_length=100)

	def __str__(self):
		return f'{self.bank}'


class Donate(models.Model):
	bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
	stk = models.CharField(max_length=50, blank=True)
	qr_code = models.ImageField(upload_to='donate/qrcode', blank=True)
	name = models.CharField(max_length=150, default='HOANG VAN GIOI')
	link = models.URLField(blank=True)

	def __str__(self):
		return f'{self.bank}'