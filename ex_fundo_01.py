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

preto = (0, 0, 0)
branco = (255, 255, 255)

# Função para mostrar a tela de "Game Over"
def mostrar_tela_game_over(position, tiles, pos_y ,pode_subir,caindo):
    screen.fill(dia)  # Preenche a tela com a cor de fundo
    imagem = pygame.image.load("./img/cenario/gamer_over.png")

    # Adicione elementos gráficos, como texto e imagens, para criar a tela de "Game Over"
    
    posicao_imagem = imagem.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    terreno_00( position, tiles, pos_y ,pode_subir,caindo)
    screen.blit(imagem, posicao_imagem)
    pygame.display.flip()


## para imagens que terao mudanca de movimentacao
##  eh preciso add mais fatias de imagens
def terreno_00( position, tiles, pos_y ,pode_subir,caindo):
    for index, img in enumerate( reversed( bg_images ) ):
        veloc = 1
        
        ## add mais fatias para o paralaxe
        if index < 1:
            tiles += 3
        for i in range( 0, tiles ):
            if index == 0: veloc += 0.3     # mais distante, maior velocidade
            if index == 1: veloc += 0.1
            new_pos_x = i*bg_width + ( position*veloc )
            new_pos_y = pos_y

            if new_pos_x > SCREEN_WIDTH:
                new_pos_x = -bg_width + ( position*veloc )
               # Verifique se o personagem pode subir
            if pode_subir and i == 1:  # Adapte isso conforme necessário
                new_pos_y -= 5
            if caindo:
                new_pos_y += 5

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
                game_map[(x, y )] = "."
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
vermelho = (255, 0, 0)  # Cor vermelha: (R, G, B) = (255, 0, 0)

fonte = pygame.font.Font(None, 36)
# Função para mostrar os atributos do personagem no canto da tela
def mostrar_atributos(poder_ataque,vida):
   
   texto_poder_ataque = fonte.render(f"Poder de Ataque: {poder_ataque}", True, branco)
   texto_vida = fonte.render(f"Vida: {vida}", True, vermelho)
    
    # Posições para exibir o texto no canto superior esquerdo
   posicao_poder_ataque = (10, 60)
   posicao_vida = (10, 100)

   screen.blit(texto_poder_ataque, posicao_poder_ataque)
   screen.blit(texto_vida, posicao_vida)

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

## musica

pygame.mixer.music.load('./musicas/nassor_v2.wav')
pygame.mixer.music.play(-1)

pos_bg = 517
pos_inimigo = 1067
inimigo = Inimigo(position + pos_bg, 188, 2,10,1)
inimigo2 = Inimigo( position + pos_inimigo  , 232, 2,10,1)
personagem = Personagem(position + 138, posicao_y,3, 2)
screen_teste = screen
pode_subir = False
caindo = False
on_platform = False

while run:
  

  screen.fill( dia )

  
    # ...

  clock.tick(FPS)
  if debug:
    print("direcao", position, tiles, bg_width )

  if cenario_02 == True:
      #for index, img in enumerate( reversed( bg_images ) ):
      terreno_00( position, tiles, pos_y,pode_subir, caindo)
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
      pode_subir = True
      
  if position == -267:  # Altura da plataforma (ajuste conforme necessário)
    on_platform = True

  print("Debug de posicao:")
  print(position)

  mostrar_atributos(personagem.poder_ataque,personagem.vida)
 #inimigos
  personagem.x = position
  personagem.y = pos_ator[1]

  inimigo.update(position + pos_bg, personagem)
  inimigo.draw(screen_teste)
  inimigo2.update(position + pos_inimigo, personagem )
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
      pos_ator = (pos_ator[0], pos_ator[1] - 11)
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
                personagem.atacar(inimigo,-170)
                personagem.atacar(inimigo2,-170)

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
                personagem.atacar(inimigo,-170)
                personagem.atacar(inimigo2,-170)

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
        if on_platform:
                if event.key == pygame.K_UP:
                    if pode_subir:  # Adapte isso com base na lógica do seu jogo
                        pos_ator = (pos_ator[0], pos_ator[1] - 11)
                if event.key == pygame.K_DOWN:
                        caindo = True
                        pos_ator = (pos_ator[0], pos_ator[1] + 11)
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
        if cima >= 4:
            cima = -1
            desce = 0
        if desce >= 0 :
            desce += 2
            pos_aux += desce
            
            pos_ator = (pos_ator[0],pos_aux)
        if desce >= 4 :
            id_ator = 0
            pulando = False


  print( 'ID', id_ator )
 
  if id_ator > 9: id_ator = 0 #mexe aqui qualquer para outras versoes +
  if id_ator == 6 : id_ator = 0 #mexe aqui qualquer coisa sobre ataque
  if id_ator < 0 : id_ator = 6

  if personagem.morto:
      run = False

#print( 'ID', id_ator )
  pygame.display.update()

mostrar_tela_game_over(position,tiles,pos_y,False,False)
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
#  print( bg_rect[0], bg_rect[1], bg_rect[2], bg_rect[3],'...' )
