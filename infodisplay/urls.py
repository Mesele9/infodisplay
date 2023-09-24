import os
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from display import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('display.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

