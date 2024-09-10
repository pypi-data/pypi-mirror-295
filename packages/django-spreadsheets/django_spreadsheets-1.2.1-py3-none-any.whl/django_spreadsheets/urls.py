# Django
from django.urls import path

# Local application / specific library imports
from . import views

app_name = "spreadsheets"

urlpatterns = [
    path("import/", views.ImportIndex.as_view(), name="import-index"),
    path(
        "import/all/",
        views.ImportAllModelsWizardView.as_view(),
        name="import-all-objects",
    ),
    path(
        "import/<int:pk>/",
        views.ImportSingleModelWizardView.as_view(),
        name="import-single-object",
    ),
    path("export/", views.ExportIndex.as_view(), name="export-index"),
    path("export/all/", views.ExportAllModelsView.as_view(), name="export-all-objects"),
    path(
        "export/<int:pk>/",
        views.ExportSingleModelView.as_view(),
        name="export-single-object",
    ),
    path(
        "import/template/",
        views.DownloadImportTemplateFile.as_view(),
        name="import-template",
    ),
    path("done/", views.DoneView.as_view(), name="done"),
]
