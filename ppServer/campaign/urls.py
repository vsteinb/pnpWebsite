from django.urls import path

from . import views

app_name = 'campaign'

urlpatterns = [
	path('auswertung/<int:pk>', views.AuswertungView.as_view(), name='auswertung'),
	path('hub/<int:pk>', views.HubView.as_view(), name='hub'),
	path('hub/<int:pk>/attribute', views.HubAttributeView.as_view(), name='hub_attribute'),
	path('hub/<int:pk>/fertigkeiten', views.HubFertigkeitenView.as_view(), name='hub_fertigkeiten'),
	path('hub/<int:pk>/vorteile', views.HubVorteileView.as_view(), name='hub_vorteile'),
	
	path('<int:pk>', views.HubView.as_view(), name='hub'),
]
