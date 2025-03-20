from django.urls import path

from django.views.i18n import JavaScriptCatalog


from . import views

app_name = "mandate"

urlpatterns = [
	path("", views.index, name="index"),
    path("mandates-list/<int:pagenum>/", views.paginate, name="paginate"),
    path("paginate_api/<int:page>/", views.paginate_api, name="paginate_api"),
	path("create/", views.mandate_create, name="mandate_create"),
	path("mandate/<int:id>/", views.mandate_detail, name="mandate_detail"),
	path("mandate/<int:id>/print/", views.mandate_print, name="mandate_print"),
    path("mandate/<int:id>/reinit_request/", views.reinit_request, name="reinit_request"),
    path("mandate/<int:id>/delete_image/", views.delete_image, name="delete_image"),
	path("ack/", views.npciAck, name="npciack"),
    path("status/", views.npciStatus, name="npcistatus"),
    path("download/", views.mandate_download, name="mandate_download"),
    path("searchacc/", views.searchAcc, name="search_acc"),
    path("create/checkacc/", views.check_mandate_by_acc_api, name="checkacc"),
]