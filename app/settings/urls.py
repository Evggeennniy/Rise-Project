from django.contrib import admin
from django.urls import include, path
from services import views as services_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    # path('payments/', include('payments.urls')),

    path('account/', include('accounts.urls')),
    path('comments/', include('comments.urls')),
    path('posts/', include('posts.urls')),
    path('services/', include('services.urls')),
    path('support/', include('support.urls')),
    
    path('', services_views.IndexView.as_view(), name='index')
]



# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
