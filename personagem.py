"""! @brief Personagem principal do jogo Fugindo da escola"""
##
# @file personagem.py
#
# @brief Arquivo com imagens do personagem principal
#
# @section Descrição
# O arquivo é responsável pela importacao das imagens utilizadas como animações do personagem TREX
#
# @author Claudio Rogerio 16.11.2022
#
# @subsection TODO
#   - Caminhar
#
# @subsection MAKED
#   - Movimentacao de pulo
#   - Movimentacao para baixo


from inimigos import *
import math
import pygame
dir = './img/personagens/principal/'
DEBUG = 1

malha = 'mapeamento.txt'

personagem = []
personagem_left = []

map_pos = {}
passos_max = 4
dim_persona = (0, 0)
altura_persona = 0

for i in range(1,11):
    if DEBUG: print( f"ator_{i}.png" )
    aux_img = pygame.image.load( dir + f"ator_{i}.png" )
    altura_persona = aux_img.get_height()
    personagem.append( aux_img )
    personagem_left.append( pygame.transform.flip( aux_img, True, False ) ) # reflexao horizontal 



def show_persona( screen, pos, id_pers, direcao ):
    global personagem, personagem_left
    if DEBUG: print(pos, id_pers)

    if direcao == 'esquerda':
        screen.blit( personagem_left[id_pers], pos ) # var global com ID em posicao
    else:
        screen.blit( personagem[id_pers], pos )



class Personagem:
    def __init__(self, x, y, poder_ataque):
        self.x = x
        self.y = y
        self.poder_ataque = poder_ataque  # Poder de ataque do personagem
        # Outros atributos do personagem...
    def atacar(self, inimigo, limite_ataque):
        distancia = self.calcular_distancia_entre_personagem_e_inimigo(inimigo)
        print("rolando")
        print(distancia)
        if distancia <= limite_ataque:
            inimigo.sofrer_dano(self.poder_ataque)
            print("rolando aqui")

    def calcular_distancia_entre_personagem_e_inimigo(self, inimigo):
        dx = inimigo.x + self.x  # Substitua pelo atributo de posição do personagem
        dy = inimigo.y + self.y  # Substitua pelo atributo de posição do personagem
       #distancia = math.sqrt(dx ** 2 + dy ** 2)
        distancia = dx
        return distancia
