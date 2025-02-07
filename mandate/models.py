from django.db import models
from django.db.models import Q, F, CheckConstraint
from django.contrib.auth.models import User, AnonymousUser
from datetime import datetime


class DebtorBank(models.Model):
	name = models.CharField(max_length=400)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Mandate(models.Model):
	debit_type_choices = [
		(None, ''),
		('F', 'Fixed Amount'),
		('M', 'Max Amount'),
	]

	frequency_choices = [
		(None, ''),
		('ADHO', 'As and when presented'),
		('INDA', 'Intra Day'),
		('DAIL', 'Daily'),
		('WEEK', 'Weekly'),
		('BIMN', 'Bi-Monthly'),
		('MNTH', 'Monthly '),
		('QURT', 'Quaterly'),
		('MIAN', 'Semi annually'),
		('YEAR', 'Yearly'),
		('BIMN', 'Bi-Monthly'),
	]

	acc_type_choices = [
		(None, ''),
		('SAVINGS', 'SAVINGS'),
		('CURRENT', 'CURRENT'),
		('CC', 'CC'),
		('Other', 'Other'),
	]

	#mandatory mandate fields
	seq_no = models.IntegerField(default=0)
	currency = models.CharField(max_length=5, default='INR', verbose_name='Currency')
	debit_type = models.CharField(max_length=1, choices=debit_type_choices, verbose_name='Debit Type')
	amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
	category = models.CharField(max_length=4, default='L001', verbose_name='Category')
	frequency = models.CharField(max_length=4, choices=frequency_choices, verbose_name='Frequency')
	date = models.DateField(verbose_name='Date of Mandate')
	start_date = models.DateField(verbose_name='Start Date', help_text="The start date should be on or after the date of mandate.")
	end_date = models.DateField(verbose_name='End Date', help_text="The end date can not be beyond 40 years after start date ")
	debtor_name = models.CharField(max_length=300, verbose_name='Name of Debor Account Holder', help_text="The name as per the debit account.")
	debtor_bank = models.ForeignKey(DebtorBank, on_delete=models.PROTECT, verbose_name='Debtor Bank')
	debtor_acc_type = models.CharField(max_length=10, choices=acc_type_choices, verbose_name='Debtor Account Type')
	debtor_acc_no = models.CharField(max_length=100, verbose_name='Debtor Legal Account Number')
	debtor_acc_ifsc = models.CharField(max_length=11, verbose_name='Debtor Account IFSC')
	creditor_name = models.CharField(max_length=300, verbose_name='Creditor Name')
	creditor_bank = models.CharField(max_length=300, default="SARVA HARYANA GRAMIN BANK", verbose_name='Creditor Bank')
	creditor_utility_code = models.CharField(max_length=100, default="HGBX00002000017848", verbose_name='Creditor Utility Code')
	mandate_image = models.ImageField(upload_to="mandate/images/mandate/", null=True, verbose_name='Mandate Image')
	mandate_file = models.FileField(null=True, blank=True, verbose_name='Mandate File')

	credit_account = models.CharField(max_length=100, verbose_name='Credit Account', help_text="The loan/other account in SHGB in which the installment is to be credited.")

	#other model fields to manage flow
	create_time = models.DateTimeField(null=True)
	create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="create", null=True)
	submit_time = models.DateTimeField(null=True)
	submit_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="submit", null=True)
	lm_time = models.DateTimeField(null=True)
	is_deleted = models.BooleanField(default=False)

	def get_ref(self):
		return 'HGBX' + self.create_time.strftime(r'%Y%m%d') + str(self.seq_no).zfill(6)

	def __str__ (self):
		return str(self.id)
	
	class Meta:
		ordering = ["id"]
		constraints = [
			CheckConstraint(
    			check = Q(start_date__gte = F("date")),
    			name = "startDate_gte_date",
				violation_error_message = '"Start Date" can not be before the "Date of Mandate"',
			)
		]