from django.contrib import admin
from django.urls import path, include
from django.conf import settings
# from django.views.generic.base import TemplateView
from django.conf.urls.static import static

urlpatterns = [
    #path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('admin/', admin.site.urls),
    path('faicon/', include('faicon.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    #path('accounts/', include('allauth.urls')),
    path('', include('cardapp.urls', namespace='usercard')),
    path('', include('social_django.urls', namespace='social')),
    #path('chaining/', include('smart_selects.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# custom error pages
handler404 = 'accounts.views.custom_page_not_found_view'
handler500 = 'accounts.views.custom_error_view'
handler403 = 'accounts.views.custom_permission_denied_view'
handler400 = 'accounts.views.custom_bad_request_view'


