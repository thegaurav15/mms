from django.urls import path

from django.views.i18n import JavaScriptCatalog


from . import views

app_name = "mandate"

urlpatterns = [
	path("", views.index, name="index"),
    path("<int:page>/", views.paginate, name="paginate"),
    path("paginate_api/<int:page>/", views.paginate_api, name="paginate_api"),
	path("create/", views.mandate_create, name="mandate_create"),
	path("mandate/<int:id>/", views.mandate_detail, name="mandate_detail"),
	path("mandate/<int:id>/print/", views.mandate_print, name="mandate_print"),
	path("test/", views.test_form, name="test"),
    path("download/", views.mandate_download, name="mandate_download"),
]