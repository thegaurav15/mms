from django.shortcuts import render
from .forms import MandateForm, MandateImageForm
from .models import Mandate
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from datetime import date
from django.db.models import Q
import tempfile
import zipfile
from django.core.files import File
from extras.mandate_image import makeJpg
import os


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

def test_form(request):
	if request.method == 'POST':
		for item in request.POST.getlist('name'):
			print(item)
	return render(request, "mandate/test_form.html")

def mandate_download(request):
	if request.method == 'POST':
		if request.POST.getlist('download'):
			file_zip = tempfile.TemporaryFile()
			zip = zipfile.ZipFile(file_zip, 'w')
		else:
			print(os.getcwd())
			mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
			context = {"mandates": mandates}
			return render(request, "mandate/mandate_download.html", context)

		for id in request.POST.getlist('download'):
			m = Mandate.objects.get(id=id)
			print(m.id, m.mandate_image)
			imgfile = makeJpg(m.mandate_image)
			imgfile.seek(0)
			with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
				fp.write(imgfile.read())
				imgfile.close()
				fp.close()
				zip.write(fp.name, arcname='zipped_' + str(m.id) + '.jpg')
		
		zip.close()
		file_zip.seek(0)
		response = HttpResponse(
			file_zip,
			headers={
				"Content-Type": "application/zip",
				"Content-Disposition": 'attachment; filename="TestZip.zip"',
			},
		)
		return response

	mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
	context = {"mandates": mandates}
	return render(request, "mandate/mandate_download.html", context)