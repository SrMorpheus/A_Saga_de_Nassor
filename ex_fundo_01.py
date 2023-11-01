"""! @brief Jogo de fundo paralaxe """

##
# @file ex_fundo_01.py
#
# @brief Arquivo principal do jogo de fundo com paralaxe
#
# @section Descrição
#   Descrição de inicialização ao pygame a partir de construção de imagens de fundo
#   repetidas infinitamente com várias imagens para dar sensação de imagem 3D
#
# @author Claudio Rogerio 16.11.2022
# TODO:
#   - add texto de pontuacao
#   - add texto de informacao
#   - add personagem
#   - add inimigos
#   - add auxiliares
#   - movimentacao conforme a posicao do personagem

# MAKED:
#   - paralaxe de fundo (funcao: terreno_00)
#   - caixa de informacoes (retangulo - funcao:fundo)

import sys
import time
import pygame
import math
from personagem import *
from inimigos import *
#from terreno import * 

pygame.init()

clock = pygame.time.Clock()
FPS = 10

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500
DIM_SCREEN = (SCREEN_WIDTH, SCREEN_HEIGHT)

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption( "A Saga de Nassor" )

dir = './img/cenario-01/'

bg = pygame.image.load( dir + 'CenarioFundo0.png' )
bg_width = bg.get_width()   # dimensao do fundo
bg_rect = bg.get_rect()     # area de fundo

# quantidade de fatias de imagens por cenario
tiles = math.ceil(SCREEN_WIDTH  / bg_width) + 1

# vetor de imagens de fundo
bg_images = []
for i in range(4):  ###
    print('Imagem:', f"CenarioFundo{i}.png" )
    bg_img = pygame.image.load( dir + f"CenarioFundo{i}.png" )
    bg_images.append( bg_img )
bg_width = bg_images[0].get_width()   # dimensao do fundo
bg_rect = bg_images[0].get_rect()     # area de fundo


## para imagens que terao mudanca de movimentacao
##  eh preciso add mais fatias de imagens
def terreno_00( position, tiles, pos_y ):
    for index, img in enumerate( reversed( bg_images ) ):
        veloc = 1
        ## add mais fatias para o paralaxe
        if index < 1:
            tiles += 3
        for i in range( 0, tiles ):
            if index == 0: veloc += 0.3     # mais distante, maior velocidade
            if index == 1: veloc += 0.1
            new_pos_x = i*bg_width + ( position*veloc )

            if new_pos_x > SCREEN_WIDTH:
                new_pos_x = -bg_width + ( position*veloc )

            screen.blit( img, (new_pos_x, pos_y ) )


## funcao que add area de informacao apos o cenario principal
def fundo( screen, cor, dim_img, dim_screen, pos_img, debug = 0 ):
    # criar retangulo
    rect_dim = (0, dim_img[3]+pos_img , dim_screen[0], dim_screen[1] )
    # desenha retangulo
    pygame.draw.rect( screen, cor, rect_dim )
    if debug:
        print( dim_img[0], dim_img[1], dim_img[2], dim_img[3], dim_screen[0], dim_screen[1] )
        print(rect_dim)

## função para recuperar o arquivo de mapeamento

def load_map(file_path):
    game_map = {}
    with open(file_path, 'r') as file:
        for line in file:
            elements = line.strip().split(",")
            if len(elements) == 2:
                x, y = map(int, elements)
                game_map[(-x, y - 104)] = "."
    return game_map;

# função para salvar o arquivo de mapeamento
def save_map(file_path, game_map):
    with open(file_path, 'w') as file:
        for row in game_map:
            file.write(''.join(row) + '\n')


### testando 


def is_valid_move(game_map, x, y):
    height = len(game_map)
    width = max(len(row) for row in game_map)


    return  game_map.get((x, y)) == '.'


def check_collisions(game_map, x, y):
    if (x, y) in game_map:
        # Há uma colisão com um obstáculo
        return True
    return False
#==========================================================================================



pos_bg = (0,0)


#======================================================================================
#Configuração do mapeamento
file_path = 'mapeamento.txt'
game_map = load_map(file_path)


#teste do pulo 

posicao_y = 232  # A posição vertical inicial do personagem (ajuste conforme necessário)
velocidade_y = 0  # A velocidade vertical inicial
gravidade = 5  # A força da gravidade que afeta a descida
pulando = False  # Variável para rastrear se o personagem está pulando
altura_pulo = 20  # A altura do pulo (ajuste conforme necessário)
atacando = False

#movimentacao
velocity = 40 #verificar esse velocidade
direcao = None
position = -67

print( "Imagens fatiadas: ", tiles, SCREEN_WIDTH, bg_width )

# desenhar area da imagem de fundo
draw_border = False 

#game loop
run = True
debug = True

dia = ( 255, 255, 255 )
tarde = ( 155, 155, 55 )
noite = (50,50,50)
cor_piso = (52, 42, 35 )

cenario_01 = False
cenario_02 = True

pos_y = 5   # posicao da imagem do cenario

id_ator = 0
pos_ator=( position + 138, posicao_y )


#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
enemy_x = 100  # Posição inicial do inimigo no eixo X
enemy_y = 300  # Posição do inimigo no eixo Y (ajuste conforme necessário)
enemy_speed = 2  # Velocidade do inimigo (ajuste conforme necessário)
move_right = True  # Indica se o inimigo está se movendo para a direita





posicoes_x = []
posicoes_y = []

pos_bg = 517
pos_inimigo = 1067
inimigo = Inimigo(position + pos_bg, 188, 2)
inimigo2 = Inimigo( position + pos_inimigo  , 232, 2)
screen_teste = screen
while run:
  

  screen.fill( dia )

  
    # ...

  clock.tick(FPS)
  if debug:
    print("direcao", position, tiles, bg_width )

  if cenario_02 == True:
      #for index, img in enumerate( reversed( bg_images ) ):
      terreno_00( position, tiles, pos_y )
#      fundo( screen, cor_piso, bg_rect, DIM_SCREEN, pos_y )    # mesma cor do terreno
      show_persona( screen, pos_ator, id_ator, direcao )
      
      #show_inimigo(screen,(400,232), 1)
    
#      id_ator = 0
     # ...

 


  #scroll background
  if direcao == 'esquerda' and  (is_valid_move(game_map, position,pos_ator[1]) or is_valid_move(game_map,position + velocity,pos_ator[1])):
      position += velocity
  if direcao == 'direita' and  (is_valid_move(game_map, position,pos_ator[1]) or is_valid_move(game_map,position - velocity,pos_ator[1])):
      position -= velocity
      
 #inimigos
  inimigo.update(position + pos_bg)
  inimigo.draw(screen_teste)
  inimigo2.update(position + pos_inimigo )
  inimigo2.draw(screen_teste)
 

 

    

  #reset scroll
  if abs( position ) > bg_width:
    print( 'Scrooll maior!' )
    position = 0

  keys = pygame.key.get_pressed()  # checking pressed keys
      #testeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
  if keys[pygame.K_SPACE] and keys[pygame.K_RIGHT]:
            if not pulando:
                print("puladndooo para direita esse")
                cima = 0
                desce = -1
                pulando = True
                position -=30
  if keys[ pygame.K_RIGHT ]:
            print('dIREITA.................')
            id_ator = id_ator + 1

  if keys[ pygame.K_LEFT ]:
            print('esquErdA.................')
            id_ator = id_ator + 1

  if keys[pygame.K_SPACE]:
    if not pulando:
      print("puladndooo")
      pulando = True
      cima = 0
      desce = - 1
    if keys[pygame.K_SPACE] == 0 :
      # Se a tecla de espaço não estiver pressionada, interrompa o pulo
      pulando = False
  if keys[pygame.K_RETURN]:
    if event.key == pygame.K_RETURN:
            if not atacando:
                print("Atacandooo")
                id_ator = 7
                atacando = True
                pos_ator=( pos_ator[0], pos_ator[1])
            else:
                atacando = False
                id_ator = 9

  
 
  ## event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
      pygame.quit(); sys.exit();

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            time.sleep(1);
            pygame.quit(); sys.exit();
        
        if event.key == pygame.K_RETURN:
            if not atacando:
                print("Atacandooo")
                atacando = True
                id_ator = 7
                pos_ator=( pos_ator[0], pos_ator[1])
            else:
                atacando = False
                id_ator = 9

        if event.key == pygame.K_SPACE:
            if not pulando:
             print("Pular")
             pulando = True
             cima = 0
             desce = - 1
        if event.key == 0:
            pulando = False
        if event.key == pygame.K_LEFT:
             
             direcao = 'esquerda'
             id_ator = id_ator + 1
             print("INDOOooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooO")
    
        if event.key == pygame.K_RIGHT:
            direcao = 'direita'
            id_ator = id_ator + 1
            print("INDOOooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooO")
        
        if event.key == pygame.K_SPACE and event.key == pygame.K_RIGHT:
             print("puladndooo para direita")


    if event.type ==pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            abaixar = False
            print('Levanta-se!')
        if event.key == pygame.K_RIGHT:
            direcao=None
            act_terr = False
            id_ator = 0
        if event.key == pygame.K_LEFT:
            direcao = None
            act_terr = False
            id_ator = 0
        #id_ator = 0

    
    if pulando:
        pos_aux = pos_ator[1]
        if cima >= 0:
            cima += 2 
            pos_aux -= cima
            id_ator = 8
            pos_ator = (pos_ator[0],pos_aux)
        if cima >= 6:
            cima = -1
            desce = 0
        if desce >= 0 :
            desce += 2
            pos_aux += desce
            
            pos_ator = (pos_ator[0],pos_aux)
        if desce >= 6 :
            id_ator = 0
            pulando = False


  print( 'ID', id_ator )
 
  if id_ator > 9: id_ator = 0 #mexe aqui qualquer para outras versoes +
  if id_ator == 6 : id_ator = 0 #mexe aqui qualquer coisa sobre ataque
  if id_ator < 0 : id_ator = 6
  
#print( 'ID', id_ator )
  

  pygame.display.update()
#  print( bg_rect[0], bg_rect[1], bg_rect[2], bg_rect[3],'...' )
pygame.quit()
