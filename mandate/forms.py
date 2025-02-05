from django.forms import ModelForm
from django import forms
from .models import Mandate, Frequency, Category, DebtorBank, DebtorAccType
from django.contrib.admin.widgets import AdminDateWidget

attrs_bs = {
	'class': 'selectpicker',
	'data-width':'100%',
	'data-style':'',
	'data-style-base': 'form-control'
}

attrs_bs_search = attrs_bs.copy()
attrs_bs_search['data-live-search'] = 'true'

class MandateForm(ModelForm):
	category = forms.ModelChoiceField(Category.objects.all(), empty_label="", widget = forms.Select(attrs=attrs_bs))
	frequency = forms.ModelChoiceField(Frequency.objects.all(), empty_label="", widget = forms.Select(attrs=attrs_bs))
	debtor_bank = forms.ModelChoiceField(DebtorBank.objects.all(), empty_label="", widget = forms.Select(attrs=attrs_bs_search))
	debtor_acc_type = forms.ModelChoiceField(DebtorAccType.objects.all(), empty_label="", widget = forms.Select(attrs=attrs_bs))

	class Meta:
		model = Mandate
		fields = [
			"fixed_or_max",
			"amount",
			"category",
			"frequency",
			"date_of_mandate",
			"start_date",
			"end_date",
			"name_of_debtor_account_holder",
			"debtor_bank",
			"debtor_acc_type",
			"debtor_legal_account_number",
			"debtor_account_number_ifsc",
			"credit_account"
		]
		widgets = {
			"date_of_mandate": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"start_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"end_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"fixed_or_max": forms.Select(attrs=attrs_bs),
			"amount": forms.DateInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01', 'min': '0.01', 'max': '10000000'}),
			"name_of_debtor_account_holder": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_legal_account_number": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_account_number_ifsc": forms.DateInput(attrs={'class': 'form-control', 'pattern': '[A-Za-z]{4}\w{7}'}),
			"credit_account": forms.DateInput(attrs={'class': 'form-control', 'maxlength': '14', 'pattern': '\d{4}\w{10}'}),
		}


class MandateImageForm(ModelForm):

	class Meta:
		model = Mandate
		fields = [
			"mandate_image"
		]