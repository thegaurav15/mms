from django.db import models
from django.db.models import Q, F, CheckConstraint, UniqueConstraint
from django.contrib.auth.models import User, AnonymousUser
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
	regex = r'^\d{10}$',
	code = 'invalid_phone',
	message = 'The phone number is invalid'
)

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
	]

	acc_type_choices = [
		(None, ''),
		('SAVINGS', 'SAVINGS'),
		('CURRENT', 'CURRENT'),
		('CC', 'CC'),
		('Other', 'Other'),
	]

	debit_date_choices = [
		(None, ''),
		('3', '3rd day of month'),
		('11', '11th day of month'),
		('19', '19th day of month'),
		('26', '26th day of month'),
	]

	#mandatory mandate fields
	seq_no = models.IntegerField(default=0)
	ref = models.CharField(max_length=35, null=False)
	currency = models.CharField(max_length=5, default='INR', verbose_name='Currency')
	debit_type = models.CharField(max_length=1, choices=debit_type_choices, default='F', verbose_name='Debit Type')
	amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Installment Amount')
	category = models.CharField(max_length=4, default='L001', verbose_name='Category')
	frequency = models.CharField(max_length=4, choices=frequency_choices, default='MNTH', verbose_name='Frequency')
	date = models.DateField(verbose_name='Date of Mandate')
	start_date = models.DateField(verbose_name='Start Date', help_text="The start date should be on or after the date of mandate.")
	end_date = models.DateField(verbose_name='End Date', help_text="The end date can not be beyond 40 years after start date ")
	debtor_name = models.CharField(max_length=300, verbose_name='Name of Debor Account Holder', help_text="The name as per the debit account.")
	debtor_joint = models.BooleanField(default=False, verbose_name='Is the Debtor Account jointly held?', help_text="Select this if the debtor account requires signatures of multiple persons")
	debtor_name_2 = models.CharField(blank=True, null=True, max_length=300, verbose_name='Name of Debor Account Holder 2', help_text='At least one additional name required for joint account.')
	debtor_name_3 = models.CharField(blank=True, null=True, max_length=300, verbose_name='Name of Debor Account Holder 3')
	debtor_bank = models.ForeignKey(DebtorBank, on_delete=models.PROTECT, verbose_name='Debtor Bank')
	debtor_acc_type = models.CharField(max_length=10, choices=acc_type_choices, verbose_name='Debtor Account Type')
	debtor_acc_no = models.CharField(max_length=100, verbose_name='Debtor Legal Account Number')
	debtor_acc_ifsc = models.CharField(max_length=11, verbose_name='Debtor Account IFSC')
	creditor_name = models.CharField(max_length=300, verbose_name='Creditor Name')
	creditor_bank = models.CharField(max_length=300, default="SARVA HARYANA GRAMIN BANK", verbose_name='Creditor Bank')
	creditor_utility_code = models.CharField(max_length=100, default="HGBX00002000017848", verbose_name='Creditor Utility Code')
	mandate_image = models.ImageField(upload_to="mandate/images/mandate/", null=True, verbose_name='Mandate Image')
	mandate_file = models.FileField(null=True, blank=True, verbose_name='Mandate File')
	phone = models.CharField(max_length=10, null=True, blank=True, validators=[phone_validator], verbose_name='Customer Mobile No.')
	email = models.EmailField(null=True, blank=True, verbose_name='Customer EMail ID')
	debit_date = models.CharField(max_length=2, choices=debit_date_choices, verbose_name='Date of EMI Collection')

	credit_account = models.CharField(max_length=100, verbose_name='Credit Account', help_text="The loan/other account in SHGB in which the installment is to be credited.")

	#other model fields to manage flow
	create_time = models.DateTimeField(null=True)
	create_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="create", null=True)
	submit_time = models.DateTimeField(null=True)
	submit_user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="submit", null=True)
	lm_time = models.DateTimeField(null=True)
	is_deleted = models.BooleanField(default=False)

	def clean(self):
		if self.debtor_joint == True and self.debtor_name_2 is None:
			raise ValidationError("At lease one additional account holder name required for joint account.")

	def get_ref(self):
		return 'SHGB' + self.create_time.strftime(r'%Y%m%d') + str(self.seq_no).zfill(6)
	
	def set_ref(self):
		self.ref = 'SHGB' + self.create_time.strftime(r'%Y%m%d') + str(self.seq_no).zfill(6)

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


class Zip(models.Model):
	date = models.DateField()
	seq_no = models.IntegerField()
	npci_username = models.CharField(max_length=35, default = 'HGBX344857')
	filename = models.CharField(max_length=35, null=True)

	def __str__(self):
		return self.filename
	
	class Meta:
		ordering = ["date", "seq_no"]
		constraints = [
			UniqueConstraint(
				name = 'zip_date_seq_unique',
				fields = ["date", "seq_no"]
			)
		]


class Presentation(models.Model):
	date = models.DateField()
	seq_no = models.IntegerField()
	npci_username = models.CharField(max_length=35, default = 'HGBX344857')
	npci_MsgId = models.CharField(max_length=35)
	filename_prefix = models.CharField(max_length=35, null=True)
	mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)
	zip = models.ForeignKey(Zip, on_delete=models.CASCADE)

	npci_upload_time = models.DateTimeField(null=True)
	npci_umrn = models.CharField(max_length=35, null=True)
	npci_upload_error = models.CharField(max_length=1000, null=True)
	npci_status = models.CharField(max_length=35, null=True)
	npci_reason_code = models.CharField(max_length=10, null=True)
	npci_response_time = models.DateTimeField(null=True)

	def __str__(self):
		return self.filename_prefix
	
	class Meta:
		ordering = ["date", "seq_no"]
		constraints = [
			UniqueConstraint(
				name = 'presentation_date_seq_unique',
				fields = ["date", "seq_no"]
			)
		]