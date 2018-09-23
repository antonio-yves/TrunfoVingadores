from django.db import models
from app.core.models import UUIDUser, CreateUpdateModel

class Category(CreateUpdateModel):
	name = models.CharField(max_length = 80, verbose_name = 'Nome')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Categoria'
		verbose_name_plural = 'Categorias'

class Card(CreateUpdateModel):
	name = models.CharField(max_length = 50, verbose_name = 'Nome')
	card = models.ImageField(upload_to='cards/', verbose_name = 'Carta')
	force = models.IntegerField(verbose_name = 'Força', default = 0)
	speed = models.IntegerField(verbose_name = 'Velocidade', default = 0)
	ability = models.IntegerField(verbose_name = 'Habilidade', default = 0)
	equipment = models.IntegerField(verbose_name = 'Equipamento', default = 0)
	intelligence = models.IntegerField(verbose_name = 'Inteligência', default = 0)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["name"]
		verbose_name = 'Carta'
		verbose_name_plural = 'Cartas'

class Composition(CreateUpdateModel):
	card_one = models.ForeignKey('Collection', on_delete = models.CASCADE, related_name = 'cardone', verbose_name = 'Carta Um')
	card_two = models.ForeignKey('Collection', on_delete = models.CASCADE, related_name = 'cardtwo', verbose_name = 'Carta Dois')
	game = models.ForeignKey('Game', on_delete = models.CASCADE, related_name = 'games', verbose_name = 'Partida')
	status = models.IntegerField(verbose_name = 'Status', default = 0)

	def __str__(self):
		return 'Composição da Partida do Jogador: %s' % self.game.player_one.username

	class Meta:
		verbose_name = 'Composição'
		verbose_name_plural = 'Composições'

class Game(CreateUpdateModel):
	player_one = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'playerone', verbose_name = 'Jogador 1')
	player_two = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'playertwo',verbose_name = 'Jogador 2')
	category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name = 'category', verbose_name = 'Categoria')
	status = models.IntegerField(default = 0, verbose_name = 'Status')
	score_one = models.IntegerField(default = 0, verbose_name = 'Pontuação Jogador 1')
	score_two = models.IntegerField(default = 0, verbose_name = 'Pontuação Jogador 2')

	def __str__(self):
		return 'Partida do Jogador: %s' % self.player_one.username

	class Meta:
		verbose_name = 'Partida'
		verbose_name_plural = 'Partidas'

class Score(CreateUpdateModel):
	player = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'player', verbose_name = 'Jogador')
	score = models.IntegerField(default = 0, verbose_name = 'Pontos')

	def __str__(self):
		return 'Score do Jogador: %s' % self.player.username

	class Meta:
		verbose_name = 'Hanking'
		verbose_name_plural = 'Hankings'

class Collection(CreateUpdateModel):
	user = models.ForeignKey(UUIDUser, on_delete = models.CASCADE, related_name = 'user', verbose_name = 'Jogador')
	card = models.ForeignKey(Card, on_delete = models.CASCADE, related_name = 'cards', verbose_name = 'Carta')
	game = models.ForeignKey(Game, on_delete = models.CASCADE, related_name = 'game', verbose_name = 'Partida')
	used = models.IntegerField(default = 0, verbose_name = 'Status da Carta')

	def __str__(self):
		return 'Carta: %s do Jogador: %s' % (self.card.name, self.user.username)

	class Meta:
		verbose_name = 'Coleção'
		verbose_name_plural = 'Coleções'
