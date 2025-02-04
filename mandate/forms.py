from django.forms import ModelForm
from django import forms
from .models import Mandate
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
			"fixed_or_max": forms.RadioSelect(attrs={'class': 'form-check form-check-inline pt-7 pb-7'}),
			"category": forms.Select(attrs=attrs_bs),
			"frequency": forms.Select(attrs=attrs_bs),
			"debtor_acc_type": forms.Select(attrs=attrs_bs),
			"debtor_bank": forms.Select(attrs=attrs_bs_search),
			"amount": forms.DateInput(attrs={'class': 'form-control', 'type': 'number', 'step': '0.01'}),
			"name_of_debtor_account_holder": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_legal_account_number": forms.DateInput(attrs={'class': 'form-control'}),
			"debtor_account_number_ifsc": forms.DateInput(attrs={'class': 'form-control'}),
			"credit_account": forms.DateInput(attrs={'class': 'form-control'}),
		}


class MandateImageForm(ModelForm):

	class Meta:
		model = Mandate
		fields = [
			"mandate_image"
		]