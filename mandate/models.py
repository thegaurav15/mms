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

class Office(models.Model):
	type_choices = [
		('BO', 'Branch'),
		('RO', 'Regional Office'),
		('HO', 'Head Office'),
	]

	region_choices = (
		('AMB', 'Ambala'),
		('BHI', 'Bhiwani'),
		('FTH', 'Fatehbad'),
		('GGN', 'Gurgaon'),
		('HIS', 'Hisar'),
		('KTL', 'Kaithal'),
		('MDG', 'Mahendergarh'),
		('NUH', 'Nuh'),
		('PPT', 'Panipat'),
		('RWR', 'Rewari'),
		('RTK', 'Rohtak'),
	)

	type = models.CharField(max_length=2, choices=type_choices)
	region = models.CharField(max_length=50, null=True, blank=True, choices=region_choices)
	sol_id = models.CharField(max_length=4)
	name = models.CharField(max_length=350)

	def __str__(self):
		return self.sol_id + ': ' + self.name

	class Meta:
		constraints = [
			UniqueConstraint(
				name = 'office_sol_unique',
				fields = ["sol_id"]
			),
			CheckConstraint(
				check = (Q(type__exact = 'HO') | Q(region__isnull = False)),
				name = 'region_mandatory',
				violation_error_message='Please select a region name.'
			)
		]


class DebtorBank(models.Model):
	name = models.CharField(max_length=400)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	
	class Meta:
		ordering = ["name"]

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
	office = models.ForeignKey(Office, on_delete=models.PROTECT)
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
	debit_date = models.CharField(max_length=2, choices=debit_date_choices, verbose_name='Date of EMI Collection')
	credit_account = models.CharField(max_length=100, verbose_name='Credit Account', help_text="The loan/other account in SHGB in which the installment is to be credited.")

	phone = models.CharField(max_length=10, null=True, blank=True, validators=[phone_validator], verbose_name='Customer Mobile No.')
	email = models.EmailField(null=True, blank=True, verbose_name='Customer EMail ID')
	
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

	def get_status(self):
		try:
			return self.presentation_set.latest().get_status()
		except Presentation.DoesNotExist:
			return {
				'short': 'New',
				'message': 'The mandate has been submitted and pending at HO:DBD',
				'class': 'primary'
			}

	def __str__ (self):
		return str(self.id)
	
	class Meta:
		ordering = ["id"]
		constraints = [
			CheckConstraint(
    			check = Q(start_date__gte = F("date")),
    			name = "startDate_gte_date",
				violation_error_message = '"Start Date" can not be before the "Date of Mandate"',
			),
			UniqueConstraint(
				name = 'mandate_ref_unique',
				fields = ["ref"]
			)
		]


class Zip(models.Model):
	date = models.DateField()
	seq_no = models.IntegerField()
	npci_username = models.CharField(max_length=35, default = 'HGBX344857')
	filename = models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.filename
	
	class Meta:
		get_latest_by = ["date", "seq_no"]
		ordering = ["date", "seq_no"]
		constraints = [
			UniqueConstraint(
				name = 'zip_date_seq_unique',
				fields = ["date", "seq_no"]
			)
		]


class Presentation(models.Model):
	npci_codes = {
		'M093': 'Aadhaar not mapped to account number',
		'M090': 'Aadhaar Number mismatch in X509cert and bank CBS',
		'M089': 'Aadhaar Number mismatch in X509certfic and mandate',
		'M037': 'Account closed',
		'C003': 'Account closed',
		'C004': 'Account frozen',
		'M026': 'Account frozen or Blocked',
		'M057': 'Account Holder Name Mismatch with CBS',
		'C005': 'Account inoperative',
		'M055': 'Account Inoperative',
		'ac01': 'ACK Default Accept Reason',
		'M007': 'Alterations require drawers authentication',
		'M024': 'Amount in words and figures differ',
		'M034': 'Amount of EMI more than limit allowed for the acct',
		'M088': 'API Data mismatch with cust info and data mandate',
		'M094': 'Appropriate NACH Mandate not uploaded',
		'sack': 'Automatic cancel request acceptance',
		'C002': 'Cancellation on corporate request',
		'C001': 'Cancellation on customer request',
		'M008': 'Company for stamp required or Wrong',
		'M074': 'Data mismatch with image_account number',
		'M075': 'Data mismatch with image_account type',
		'M080': 'Data mismatch with image_amount',
		'M035': 'Data mismatch with image_Corporate name mismatch',
		'M079': 'Data mismatch with image_debit type',
		'M084': 'Data mismatch with image_debtor bank name',
		'M082': 'Data mismatch with image_end date',
		'M077': 'Data mismatch with image_frequency',
		'M085': 'Data mismatch with image_more than one field',
		'M083': 'Data mismatch with image_payer name',
		'M078': 'Data mismatch with image_period',
		'M081': 'Data mismatch with image_start date',
		'ncfe': 'Default forced not acknowledge acceptance reason',
		'pc01': 'Default PreCancel reason',
		'rv01': 'Default Revoke Reason',
		'sp01': 'Default Suspend Reason',
		'M006': 'Drawers authority to operate account not received',
		'M003': 'Drawers signature differs',
		'M050': 'Drawers signature illegible in mandate form',
		'M049': 'Drawers signature not updated in Bank CBS',
		'M004': 'Drawers signature required',
		'M021': 'Duplicate mandate_first presented mandate already ',
		'M091': 'eSign Signature is tampered or corrupt',
		'M027': 'Image not clear',
		'M096': 'Instrument out dated and stale',
		'M060': 'Invalid frequency',
		'M066': 'Joint signature required',
		'M009': 'Mandate not in standard format',
		'M052': 'Mandate Not Registered_Minor Account',
		'M056': 'Mandate Not Registered_ not maintaining req balanc',
		'M051': 'Mandate Not Registered_NRE Account',
		'M095': 'Mandate Presented with thumb Impression',
		'M030': 'Mandate registration not allowed for CC account',
		'M054': 'Mandate registration not allowed for PPF account',
		'M038': 'No such account',
		'M036': 'Not a CBS act no.or old act no.representwithCBS no',
		'A001': 'On customer request',
		'M011': 'Payment stopped by attachment order',
		'M012': 'Payment stopped by court order',
		'M025': 'Present under proper mandate category',
		'M023': 'Refer to the branch_KYC not completed',
		'M032': 'Rejected as per customer confirmation',
		'M092': 'signed Content doesnot tally with data mandate',
		'ncex': 'TAT expired',
		'M067': 'Thumb Impression in CBS but cust sign in mandate',
		'M013': 'Withdrawal stopped owing to death of account holde',
		'M015': 'Withdrawal stopped owing to insolvency of account ',
		'M014': 'Withdrawal stopped owing to lunacy of account hold',
	}

	date = models.DateField()
	seq_no = models.IntegerField()
	npci_username = models.CharField(max_length=35, default = 'HGBX344857')
	npci_MsgId = models.CharField(max_length=35)
	filename_prefix = models.CharField(max_length=100, null=True)
	mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE)
	zip = models.ForeignKey(Zip, on_delete=models.CASCADE)

	npci_upload_time = models.DateTimeField(null=True)
	npci_umrn = models.CharField(max_length=35, null=True)
	npci_upload_error = models.CharField(max_length=1000, null=True)
	npci_status = models.CharField(max_length=35, null=True, choices=npci_codes)
	npci_reason_code = models.CharField(max_length=10, null=True)
	npci_response_time = models.DateTimeField(null=True)

	def __str__(self):
		return self.filename_prefix
	
	def get_status(self):
		status = {}
		if self.npci_upload_time == None:
			raise Presentation.DoesNotExist
		
		elif self.npci_upload_error != None:
			status['short'] = 'Error'
			status['message'] = "Error: " + self.npci_upload_error
			status['class'] = "danger"
		
		elif self.npci_status == None:
			status['short'] = 'NPCI'
			status['message'] = "Mandate uploaded at NPCI portal"
			status['class'] = "secondary"
		
		elif self.npci_status == 'Active':
			status['short'] = 'Active'
			status['message'] = "Mandate has been accepted by the debtor bank"
			status['class'] = "success"
		
		elif self.npci_status == 'Rejected':
			status['short'] = 'Rejected'
			status['message'] = "Rejected - " 
			status['class'] = "danger"
			if self.npci_reason_code != None:
				status['message'] = status['message'] + self.npci_reason_code + ' - ' + self.npci_codes[self.npci_reason_code]
	
		else:
			status['short'] = 'Unknown'
			status['message'] = "Status unknown. Contact HO:DBD"
			status['class'] = "dark"
		
		return status
	
	def get_st(self):
		if self.npci_upload_time == None:
			return 'New'
		elif self.npci_upload_error != None:
			return 'Error'
		elif self.npci_status == None:
			return 'NPCI'
		else:
			return self.npci_status

	class Meta:
		get_latest_by = ["date", "seq_no"]
		ordering = ["date", "seq_no"]
		constraints = [
			UniqueConstraint(
				name = 'presentation_date_seq_unique',
				fields = ["date", "seq_no"]
			)
		]