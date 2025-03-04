from django.forms import ModelForm, Form
from django import forms
from .models import Mandate, DebtorBank, Office
from .custom_functions import get_office_queryset
from django.contrib.admin.widgets import AdminDateWidget

attrs_bs = {
	'class': 'selectpicker',
	'data-width':'100%',
	'data-style':'',
	'data-size': "8",
	'data-style-base': 'form-control'
}

attrs_bs_search = attrs_bs.copy()
attrs_bs_search['data-live-search'] = 'true'

class MandateForm(ModelForm):
	# debit_type = forms.ChoiceField(choices=Mandate.debit_type_choices, widget = forms.Select(attrs=attrs_bs))
	# frequency = forms.ChoiceField(choices=Mandate.frequency_choices, widget = forms.Select(attrs=attrs_bs))
	debtor_bank = forms.ModelChoiceField(DebtorBank.objects.all(), empty_label="", widget = forms.Select(attrs=attrs_bs_search))
	debtor_acc_type = forms.ChoiceField(choices=Mandate.acc_type_choices, widget = forms.Select(attrs=attrs_bs))
	debit_date = forms.ChoiceField(choices=Mandate.debit_date_choices, widget = forms.Select(attrs=attrs_bs), label='Date of EMI Collection')
	office = forms.ModelChoiceField(None, empty_label="", widget = forms.Select(attrs=attrs_bs_search), label="Branch")

	class Meta:
		model = Mandate
		fields = [
			# "debit_type",
			# "frequency",
			"office",
			"date",
			"start_date",
			"end_date",
			"amount",
			"debit_date",
			"debtor_name",
			"debtor_joint",
			"debtor_name_2",
			"debtor_name_3",
			"debtor_bank",
			"debtor_acc_type",
			"debtor_acc_no",
			"debtor_acc_ifsc",
			"credit_account",
			"phone",
			"email"
		]
		widgets = {
			"date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"start_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"end_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"amount": forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01', 'min': '0.01', 'max': '10000000'}),
			"debtor_name": forms.TextInput(attrs={'class': 'form-control'}),
			"debtor_name_2": forms.TextInput(attrs={'class': 'form-control'}),
			"debtor_name_3": forms.TextInput(attrs={'class': 'form-control'}),
			"debtor_acc_no": forms.TextInput(attrs={'class': 'form-control'}),
			"debtor_acc_ifsc": forms.TextInput(attrs={'class': 'form-control', 'pattern': r'[A-Za-z]{4}\w{7}'}),
			"credit_account": forms.TextInput(attrs={'class': 'form-control', 'maxlength': '14', 'pattern': r'\d{4}\w{10}'}),
			"phone": forms.TextInput(attrs={'class': 'form-control', 'pattern': r'\d{10}'}),
			"email": forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
		}
	
	def __init__(self, branch, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["office"].queryset = get_office_queryset(branch)

class MandateImageForm(ModelForm):

	class Meta:
		model = Mandate
		fields = [
			"mandate_image"
		]

class NpciAckForm(Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'application/zip'}))

class NpciStatusForm(Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'text/csv'}))

class SearchAcc(Form):
	account = forms.CharField(widget=forms.TextInput(attrs={'maxlength': '14'}))


class FilterMandates(Form):
	status_choices = (
		(None, 'All'),
		('new', 'New'),
		('npci', 'Pending at NPCI'),
		('Rejected', 'Rejected'),
		('Active', 'Active'),
		('error', 'Error'),
	)

	pages_choices = (
		(10, '10'),
		(25, '25'),
		(50, '50'),
	)

	status = forms.ChoiceField(choices=status_choices, required=False, widget = forms.Select(attrs={'class': 'form-control mr-sm-2 form-control-sm'}))
	pages = forms.ChoiceField(choices=pages_choices, required=False, widget = forms.Select(attrs={'class': 'form-control mr-sm-2 form-control-sm'}))
