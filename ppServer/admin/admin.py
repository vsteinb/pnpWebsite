from django.contrib import admin


class AdminCustomSite(admin.AdminSite):
    site_header = "Goren PnP"
    site_title = "Goren PnP"
