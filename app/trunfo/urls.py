from django.urls import include, path
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import views as trunfo

app_name = 'trunfo'

urlpatterns = [
	path('', trunfo.ProfileView.as_view(template_name='trunfo/user/profile.html'), name='profile'),
	path('game/partida/<pk>', trunfo.GameView.as_view(), name = 'game'),
	path('game/new/', trunfo.CreateGameView.as_view(), name = 'create-game'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
