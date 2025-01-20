from django.shortcuts import render
from .forms import MandateForm, MandateImageForm
from .models import Mandate
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.db.models import Q


# Create your views here.

def index(request):
	mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
	mandates_pending_image = Mandate.objects.filter(Q(mandate_image__isnull=True) | Q(mandate_image__exact = ''))
	context = {"mandates": mandates, "mandates_pending_image": mandates_pending_image}
	return render(request, "mandate/index.html", context)


def mandate_create(request):
	if request.method == 'POST':
		form = MandateForm(request.POST)
		if form.is_valid():
			#save form
			mandate = form.save()
			mandate.message_reference = "HGBX" + date.today().strftime("%y%m%d") + str(mandate.id).zfill(6)
			mandate.save()
			return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
	else:
		form = MandateForm()
	return render(request, "mandate/mandate_form.html", {"form": form})


def mandate_detail(request, id):
	mandate = Mandate.objects.get(id=id)
	if request.method == 'POST':
		form = MandateImageForm(request.POST, request.FILES, instance=mandate)
		if form.is_valid():
			#save form
			form.save()
			return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
	else:
		form = MandateImageForm(instance=mandate)
	return render(request, "mandate/mandate_detail.html", {"mandate": mandate, "form": form})


def mandate_print(request, id):
	mandate = Mandate.objects.get(id=id)
	return render(request, "mandate/mandate_print.html", {"mandate": mandate})