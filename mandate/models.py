from django.db import models
from django.db.models import Q, F, CheckConstraint


class PaymentType(models.Model):
	type = models.CharField(max_length=20)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.type


class Category(models.Model):
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=200)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.code + " : " + self.name


class Frequency(models.Model):
	code = models.CharField(max_length=10)
	name = models.CharField(max_length=200)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class DebtorBank(models.Model):
	name = models.CharField(max_length=400)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class DebtorAccType(models.Model):
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name

fixed_or_max_choices = [
	('F', 'Fixed'),
	('M', 'Max'),
]

class Mandate(models.Model):
	#mandatory mandate fields
	umrn							= models.CharField(max_length=50, verbose_name='UMRN')
	message_reference				= models.CharField(max_length=100, null=True, verbose_name='Message Reference')
	currency						= models.CharField(max_length=5, default='INR', verbose_name='Currency')
	fixed_or_max					= models.CharField(max_length=1, choices=fixed_or_max_choices, default='F', verbose_name='Amount Type')
	amount							= models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
	category						= models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Category')
	frequency						= models.ForeignKey(Frequency, on_delete=models.PROTECT, verbose_name='Frequency')
	date_of_mandate					= models.DateField(verbose_name='Date of Mandate')
	start_date						= models.DateField(verbose_name='Start Date', 
										help_text="The start date should be on or after the date of mandate.")
	end_date						= models.DateField(verbose_name='End Date',
								  		help_text="The end date can not be beyond 40 years after start date ")
	name_of_debtor_account_holder	= models.CharField(max_length=300, verbose_name='Name of Debor Account Holder', 
										help_text="The name as per the debit account.")
	debtor_bank						= models.ForeignKey(DebtorBank, on_delete=models.PROTECT, verbose_name='Debtor Bank')
	debtor_acc_type					= models.ForeignKey(DebtorAccType, on_delete=models.PROTECT, verbose_name='Debtor Account Type')
	debtor_legal_account_number		= models.CharField(max_length=100, verbose_name='Debtor Legal Account Number')
	debtor_account_number_ifsc		= models.CharField(max_length=11, verbose_name='Debtor Account IFSC')
	creditor_name					= models.CharField(max_length=300, verbose_name='Creditor Name')
	creditor_bank					= models.CharField(max_length=300, default="SARVA HARYANA GRAMIN BANK", verbose_name='Creditor Bank')
	creditor_utility_code			= models.CharField(max_length=100, default="HGBX00002000017848", verbose_name='Creditor Utility Code')
	mandate_image					= models.ImageField(upload_to="mandate/images/mandate/", null=True, verbose_name='Mandate Image')
	mandate_file					= models.FileField(null=True, blank=True, verbose_name='Mandate File')

	credit_account					= models.CharField(max_length=100, verbose_name='Credit Account',
										help_text="The loan/other account in SHGB in which the installment is to be credited.")

	#other model fields to manage flow
	is_deleted						= models.BooleanField(default=False)
	image_uploaded					= models.BooleanField(default=False)
	locked							= models.BooleanField(default=False)
	confirmation					= models.BooleanField(default=False)
	uploaded_npci					= models.BooleanField(default=False)
	status_npci						= models.BooleanField(default=False)
	response_npci					= models.CharField(max_length=4, null=True)

	def __str__ (self):
		return str(self.id)
	
	class Meta:
		constraints = [
			CheckConstraint(
    			check = Q(start_date__gte = F("date_of_mandate")),
    			name = "startDate_gte_dateOfMandate",
				violation_error_message = '"Start Date" can not be before the "Date of Mandate"',
			)
		]