from django.shortcuts import render
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound, Http404
from django.db.models import Q
import tempfile, zipfile
from datetime import datetime, date
from extras.mandate_image import makeJpg, makeTif
from extras.mandate_xml import makeXml
from extras.xml2csv import zip2dict
from djangoproject.settings import MEDIA_URL
from django.core.paginator import Paginator
from django.core import serializers
from .custom_functions import *
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_not_required


def index(request):
	base_queryset = get_mandate_queryset(request.user.userextended.office)
	mandates = base_queryset.exclude(mandate_image__exact = '')
	mandates_pending_image = base_queryset.filter(mandate_image__exact = '').order_by('id')
	context = {"mandates": mandates, "mandates_pending_image": mandates_pending_image}
	
	context['new'] = mandates.filter(init_req_flag=True).count()
	context['npci'] = mandates.filter(presentation__npci_status=None).exclude(presentation__npci_upload_time__exact=None).count()
	context['rejected'] = mandates.filter(presentation__npci_status='Rejected').count()
	context['rejected_no_response'] = mandates.filter(presentation__npci_status='Rejected', presentation__npci_reason_code__exact=None).count()
	context['active'] = mandates.filter(presentation__npci_status='Active').count()

	return render(request, "mandate/index.html", context)

def paginate(request, pagenum):
	print(request.GET)
	form = FilterMandates(request.GET)

	base_queryset = get_mandate_queryset(request.user.userextended.office)
	mandates = base_queryset.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')

	if 'status' in request.GET.keys() and request.GET['status']:
		status = request.GET['status']
		if status == 'Active' or status == 'Rejected':
			mandates = mandates.filter(presentation__npci_status__exact = request.GET['status'])
		elif status == 'new':
			mandates = mandates.filter(init_req_flag = True)
		elif status == 'npci':
			mandates = mandates.exclude(presentation__npci_upload_time = None).filter(presentation__npci_status = None, presentation__npci_upload_error = None)
		elif status == 'error':
			mandates = mandates.exclude(presentation__npci_upload_error = None)

	if 'debit_date' in request.GET.keys() and request.GET['debit_date']:
		mandates = mandates.filter(debit_date = request.GET['debit_date'])
	
	if 'records' in request.GET.keys() and request.GET['records']:
		num_records = request.GET['records']
	else:
		num_records = 10

	if 'pagenum' in request.GET.keys() and request.GET['pagenum']:
		page = request.GET['pagenum']
		print(page)
	else:
		page = 1

	p = Paginator(mandates, num_records)
	context = {"mandates": p.page(pagenum), "range": p.page_range}
	context['form'] = form

	return render(request, "mandate/paginate.html", context)

def paginate_api(request, page):
	mandates = Mandate.objects.exclude(mandate_image__isnull=True).exclude(mandate_image__exact = '')
	p = Paginator(mandates, 30)
	items = serializers.serialize("json", p.page(page), fields=[
		'name_of_debtor_account_holder',
		'debtor_bank',
		'debtor_legal_account_number',
		'umrn',
		'amount'])
	context = {"items": items}
	return JsonResponse(items, safe=False)

def mandate_create(request):
	branch = request.user.userextended.office
	if request.method == 'POST':
		form = MandateForm(branch, request.POST)
		if form.is_valid():
			#save form
			mandate = form.save()
			mandate.create_user = request.user
			mandate.create_time = datetime.now()
			try:
				mandate.seq_no = Mandate.objects.filter(create_time__gte=to_midnight(date.today())).latest("seq_no").seq_no + 1
			except Mandate.DoesNotExist:
				mandate.seq_no = 1
			mandate.set_ref()
			mandate.save()
			return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
	else:
		form = MandateForm(branch = branch)
	return render(request, "mandate/mandate_form.html", {"form": form})

def mandate_detail(request, id):
	try:
		mandate = Mandate.objects.get(id=id)
	except Mandate.DoesNotExist:
		raise Http404
	
	if not user_mandate_allowed(request.user, mandate):
		return HttpResponse('Unauthorized request')

	if request.method == 'POST':
		form = MandateImageForm(request.POST, request.FILES, instance=mandate)
		if form.is_valid():
			#save form
			form.save()
			mandate.submit_user = request.user
			mandate.submit_time = datetime.now()

			mandate.last_init_req_time = mandate.submit_time
			mandate.last_init_req_user = mandate.submit_user
			mandate.init_req_flag = True
			
			mandate.save()
			return HttpResponse(MEDIA_URL + mandate.mandate_image.name)
			return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
	else:
		form = MandateImageForm(instance=mandate)

	context = {"mandate": mandate, "form": form}
	
	if mandate.mandate_image:
		presentation = mandate.presentation_set.exclude(npci_upload_time__exact = None)
		context['presentation'] = presentation
	
	return render(request, "mandate/mandate_detail.html", context)


def mandate_print(request, id):
	try:
		mandate = Mandate.objects.get(id=id)
	except Mandate.DoesNotExist:
		raise Http404

	if not user_mandate_allowed(request.user, mandate):
		return HttpResponse('Unauthorized request')
	
	return render(request, "mandate/mandate_print.html", {"mandate": mandate})

def mandate_download(request):
	if request.method == 'POST':
		if request.POST.getlist('download'):
			file_zip = tempfile.TemporaryFile()
			zip = zipfile.ZipFile(file_zip, 'w')
			zip_object = zip_object_factory('HGBX344857')
			
			for id in request.POST.getlist('download'):
				m = Mandate.objects.get(id=id)
				print(m.id, m.mandate_image)

				p = presentation_object_factory('HGBX344857')
				p.mandate = m
				p.zip = zip_object
				p.save()
				
				with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
					fp.write(makeJpg(m.mandate_image).read())
					fp.close()
					zip.write(fp.name, arcname=p.filename_prefix + '_detailfront.jpg')
				
				with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
					fp.write(makeTif(m.mandate_image).read())
					fp.close()
					zip.write(fp.name, arcname=p.filename_prefix + '_front.tif')
				
				with tempfile.NamedTemporaryFile(delete_on_close=False) as fp:
					fp.write(makeXml(m, p.npci_MsgId).read())
					fp.close()
					zip.write(fp.name, arcname=p.filename_prefix + '-INP.xml')
			
			zip.close()
			file_zip.seek(0)
			response = HttpResponse(
				file_zip,
				headers={
					"Content-Type": "application/zip",
					"Content-Disposition": 'attachment; filename="' + zip_object.filename + '"',
				},
			)
			return response

	mandates = Mandate.objects.filter(init_req_flag = True).order_by('id')
	context = {"mandates": mandates}
	return render(request, "mandate/mandate_download.html", context)


def npciAck(request):
	if request.method == "POST":
		print('inside request.POST')
		form = NpciAckForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			ack_files = zip2dict(file)
			for f in ack_files:
				process_ack(f)
		
	else:
		form = NpciAckForm()
	return render(request, "mandate/npci_ack.html", {"form": form})

def npciStatus(request):
	ctx = {}

	if request.method == "POST":
		print('inside request.POST')
		form = NpciStatusForm(request.POST, request.FILES)
		if form.is_valid():
			messages = process_status(request.FILES['file'])
			ctx['messages'] = messages

	else:
		form = NpciStatusForm()

	ctx['form'] = form	
	return render(request, "mandate/npci_status.html", ctx)

def searchAcc(request):
	base_queryset = get_mandate_queryset(request.user.userextended.office)
	ctx = {}

	try:
		ctx['mandates'] = base_queryset.filter(credit_account__icontains = request.GET['account'])
		form = SearchAcc(request.GET)
	except MultiValueDictKeyError:
		form = SearchAcc()

	ctx['form'] = form
	return render(request, "mandate/search_acc.html", ctx)

def reinit_request(request, id):
	if request.method == "POST":
		mandate = Mandate.objects.get(id=id)
		mandate.init_req_flag = True
		mandate.last_init_req_time = datetime.now()
		mandate.last_init_req_user = request.user
		mandate.save()
		return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
	
def check_mandate_by_acc_api(request):
	acc = request.GET['account']
	mandates = Mandate.objects.filter(credit_account__exact = acc)
	
	if mandates.count() == 0:
		return HttpResponseNotFound('Not found: ' + acc)
	
	elif mandates.count() >= 0:
		ctx = {'mandates': mandates}
		return render(request, "mandate/include/mandate_table.html", ctx)
	
def delete_image(request, id):
	try:
		mandate = Mandate.objects.get(id=id)
	except Mandate.DoesNotExist:
		raise Http404
	
	if not user_mandate_allowed(request.user, mandate):
		return HttpResponse('Unauthorized request')
	
	if request.method == "POST":
		if mandate.delete_image():
			return HttpResponseRedirect("/mandates/mandate/" + str(mandate.id) + "/")
		else:
			return HttpResponse('Could not delete. There was some error.')

@login_not_required
def sop(request):
	return render(request, "mandate/sop.html")