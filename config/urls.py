"""
URL configuration for FlyCure.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("marketplace.urls")),
    path("accounts/", include("accounts.urls")),
    path("records/", include("records.urls")),
    path("", include("care.urls")),
]
