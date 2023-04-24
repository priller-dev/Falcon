from django.contrib.admin import AdminSite, register


class ClientSite(AdminSite):
    site_header = "Client site"
    site_title = "Client Portal"
    index_title = "Welcome to Client Portal"


client_site = ClientSite(name='client_site')
