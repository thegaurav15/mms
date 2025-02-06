from django.shortcuts import render
from .forms import MandateForm, MandateImageForm
from .models import Mandate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import date
from django.db.models import Q
import tempfile, zipfile
from datetime import datetime
from extras.mandate_image import makeJpg, makeTif
from extras.mandate_xml import makeXml
from django.views.decorators.cache import never_cache
from djangoproject.settings import MEDIA_URL
from django.core.paginator import Paginator
from django.core import serializers



# Create your views here.

def index(request):
	mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
	mandates_pending_image = Mandate.objects.filter(Q(mandate_image__isnull=True) | Q(mandate_image__exact = ''))
	context = {"mandates": mandates, "mandates_pending_image": mandates_pending_image}
	return render(request, "mandate/index.html", context)

def paginate(request, page):
	mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
	p = Paginator(mandates, 2)
	context = {"cur_page": p.page(page), "range": p.page_range}
	return render(request, "mandate/paginate.html", context)

def paginate_api(request, page):
	mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
	p = Paginator(mandates, 2)
	items = serializers.serialize("json", p.page(page), fields=[
		'name_of_debtor_account_holder',
		'debtor_bank',
		'debtor_legal_account_number',
		'umrn',
		'amount'])
	context = {"items": items}
	return JsonResponse(items, safe=False)


def mandate_create(request):
	if request.method == 'POST':
		form = MandateForm(request.POST)
		if form.is_valid():
			#save form
			mandate = form.save()
			mandate.ref = "HGBX" + date.today().strftime("%y%m%d") + str(mandate.id).zfill(6)
			mandate.save()
			return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
	else:
		form = MandateForm()
	return render(request, "mandate/mandate_form.html", {"form": form})

@never_cache
def mandate_detail(request, id):
	mandate = Mandate.objects.get(id=id)
	if request.method == 'POST':
		form = MandateImageForm(request.POST, request.FILES, instance=mandate)
		if form.is_valid():
			#save form
			form.save()
			return HttpResponse(MEDIA_URL + mandate.mandate_image.name)
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
			i = 1 #this is a temporary measure
			for id in request.POST.getlist('download'):
				i = i + 1
				#file names and numbering system has to be designed first
				name = "MMS-CREATE-HGBX-HGBX344857-" + datetime.now().strftime('%d%m%Y') + '-' + str(i).zfill(6)
				print(name)
				m = Mandate.objects.get(id=id)
				print(m.id, m.mandate_image)
				
				with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
					fp.write(makeJpg(m.mandate_image).read())
					fp.close()
					zip.write(fp.name, arcname=name + '_detailfront.jpg')
				
				with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
					fp.write(makeTif(m.mandate_image).read())
					fp.close()
					zip.write(fp.name, arcname=name + '_front.tif')
				
				with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
					fp.write(makeXml(m, 'HGBX' + datetime.now().strftime('%d%m%Y') + str(i).zfill(6)).read())
					fp.close()
					zip.write(fp.name, arcname=name + '-INP.xml')
			
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