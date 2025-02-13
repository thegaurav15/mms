from django.forms import ModelForm
from django import forms
from .models import Mandate, DebtorBank
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
	debit_type = forms.ChoiceField(choices=Mandate.debit_type_choices, widget = forms.Select(attrs=attrs_bs))
	frequency = forms.ChoiceField(choices=Mandate.frequency_choices, widget = forms.Select(attrs=attrs_bs))
	debtor_bank = forms.ModelChoiceField(DebtorBank.objects.all(), empty_label="", widget = forms.Select(attrs=attrs_bs_search))
	debtor_acc_type = forms.ChoiceField(choices=Mandate.acc_type_choices, widget = forms.Select(attrs=attrs_bs))

	class Meta:
		model = Mandate
		fields = [
			"debit_type",
			"amount",
			"frequency",
			"date",
			"start_date",
			"end_date",
			"debtor_name",
			"debtor_joint",
			"debtor_name_2",
			"debtor_name_3",
			"debtor_bank",
			"debtor_acc_type",
			"debtor_acc_no",
			"debtor_acc_ifsc",
			"credit_account"
		]
		widgets = {
			"date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"start_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"end_date": forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
			"amount": forms.DateInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01', 'min': '0.01', 'max': '10000000'}),
			"debtor_name": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_name_2": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_name_3": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_acc_no": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_acc_ifsc": forms.DateInput(attrs={'class': 'form-control', 'pattern': r'[A-Za-z]{4}\w{7}'}),
			"credit_account": forms.DateInput(attrs={'class': 'form-control', 'maxlength': '14', 'pattern': r'\d{4}\w{10}'}),
		}


class MandateImageForm(ModelForm):

	class Meta:
		model = Mandate
		fields = [
			"mandate_image"
		]