from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from random import randint

from django.urls import reverse_lazy

from . import models

class GameView(LoginRequiredMixin, View):
	def get(self, request, pk):
		partida = models.Game.objects.filter(id = pk).first()
		if partida.player_one == partida.player_two:
			if partida.player_two != self.request.user:
				partida.player_two = self.request.user
				partida.status = 1
				partida.save()
				cards = models.Card.objects.all()
				for num in range (1, 17):
					card = randint(1, len(cards))
					if num > 8:
						collection = models.Collection(user = partida.player_two, card = cards[card - 1], game = partida)
						collection.save()
					else:
						collection = models.Collection(user = partida.player_one, card = cards[card - 1], game = partida)
						collection.save()
				return render(request, 'trunfo/game/game.html', {'cards': models.Collection.objects.filter(user = self.request.user, game = partida, used = 0), 'partida': partida})
			else:
				return render(request, 'trunfo/game/game.html', {'mensage': 'Aguardando oponente!!'})
		else:
			return render(request, 'trunfo/game/game.html', {'cards': models.Collection.objects.filter(user = self.request.user, game = partida, used = 0), 'partida': partida})

class SelectCard(LoginRequiredMixin, View):
	pass

class ProfileView(LoginRequiredMixin, TemplateView):
	def get_context_data(self, **kwargs):
		kwargs['partidas'] = models.Game.objects.filter(player_one = self.request.user)
		kwargs['partidas'] = models.Game.objects.filter(player_two = self.request.user)
		return super(ProfileView, self).get_context_data(**kwargs)

class CreateGameView(LoginRequiredMixin, View):
	def get(self, request):
		return redirect('trunfo:profile')

	def post(self, request):
		categoria = models.Category.objects.all()
		game_category = randint(1, len(categoria))
		partida = models.Game(player_one = self.request.user, player_two = self.request.user, category = categoria[game_category - 1])
		partida.save()
		return redirect('trunfo:profile')
