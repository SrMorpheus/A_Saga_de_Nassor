import pygame
from personagem import *
dir = './img/personagens/inimigo/'
dir_ataque = './img/personagens/inimigo/atacando/'
dir_morto = './img/personagens/inimigo/morte/'


DEBUG = 1

malha = 'mapeamento.txt'

personagem = []
personagem_ataque = []
personagem_morto = []
personagem_morto_left = []
personagem_ataque_left = []
personagem_left = []

map_pos = {}
passos_max = 4
dim_persona = (0, 0)
altura_persona = 0

for i in range(1,7):
    if DEBUG: print( f"inimigo_{i}.png" )
    aux_img = pygame.image.load( dir + f"inimigo_{i}.png" )
    altura_persona = aux_img.get_height()
    personagem.append( aux_img )
    personagem_left.append( pygame.transform.flip( aux_img, True, False ) ) # reflexao horizontal 

for i in range(1,7):
    if DEBUG: print( f"inimigo_01_atacando_arma{i}.png" )
    aux_img = pygame.image.load( dir_ataque + f"inimigo_01_atacando_arma{i}.png" )
    altura_persona = aux_img.get_height()
    personagem_ataque.append( aux_img )
    personagem_ataque_left.append( pygame.transform.flip( aux_img, True, False ) ) # reflexao horizontal 

    
aux_img = pygame.image.load( dir_morto + f"morte_inimigo.png" )
altura_persona = aux_img.get_height()
personagem_morto.append( aux_img )
personagem_morto_left.append( pygame.transform.flip( aux_img, True, False ) ) # reflexao horizontal 



def show_inimigo( screen, pos, id_pers,direcao ):
    global personagem, personagem_left
    if DEBUG: print(pos, id_pers)

    if direcao == 'esquerda':
        screen.blit( personagem_left[id_pers], pos ) # var global com ID em posicao
    else:
        screen.blit( personagem[id_pers], pos )


class Inimigo:
    def __init__(self, x, y, speed,vida,poder):
        self.x = x
        self.y = y
        self.poder_ataque = poder
        self.atacando = False
        self.posicao_fixa_x = x          
        self.speed = speed
        self.direction = 1  # 1 para a direita, -1 para a esquerda
        self.animation_frames = personagem
        self.ataque_frames = personagem_ataque
        self.morto_frames = personagem_morto
        self.current_ataque = 0
        self.current_frame = 0
        self.animation_speed = 0.9  # Velocidade da animação
        self.controle = 0
        self.vida = vida
        self.sumindo = False

    def update(self,position,personagem ):
        
        if not self.sumindo:
            if not self.atacando:
            # Lógica de movimento normal
                print("debuf Posicao inimigo")
                print(position)
                self.controle += self.direction * self.speed
                self.x = self.controle + position
                print("debuf Posicao inimigo")
                print(self.x)

           
             # Lógica para alternar a direção quando atinge os limites
                if  self.direction == 1 and self.x >=  (position + 50 ):
                    self.atacando = True
                    self.direction = -1
                elif self.direction == -1 and self.x <=  (position - 50):
                    self.atacando = True
                    self.direction = 1

        # Atualize a animação de andar
                self.current_frame += self.animation_speed
                if self.current_frame >= len(self.animation_frames):
                    self.current_frame = 0
            else:
        # Lógica de ataque
                self.current_ataque += 0.8  # Ajuste a velocidade da animação de ataque
                if self.current_ataque >= len(self.ataque_frames):
                    self.current_ataque = 0
                    self.atacar(personagem)
                    self.atacando = False
        else:
            self.x = position

    def draw(self, screen):
        if not self.sumindo:
            if not self.atacando:
        # Desenhe o inimigo na tela com base na animação de andar atual
                if self.direction == 1:
                    screen.blit(self.animation_frames[int(self.current_frame)], (self.x, self.y))
                else:
                    screen.blit(personagem_left[int(self.current_frame)], (self.x, self.y))
            else:
        # Desenhe o inimigo na tela com base na animação de ataque atual
                if self.direction == -1:
                    screen.blit(self.ataque_frames[int(self.current_ataque)], (self.x, self.y))
                else:
                    screen.blit(personagem_ataque_left[int(self.current_ataque)], (self.x, self.y))
        else:

            screen.blit(personagem_morto_left[int(0)], (self.x, self.y))


    def sofrer_dano(self, poder_ataque_personagem):
        self.vida -= poder_ataque_personagem
        if self.vida <= 0:
            self.vida = 0
            self.sumindo = True
    def atacar(self, personagem ):
        distancia = self.calcular_distancia_entre_personagem_e_inimigo(personagem)
        if distancia <= -140:
            personagem.sofrer_dano(self.poder_ataque)

    def calcular_distancia_entre_personagem_e_inimigo(self, personagem):
        dx = personagem.x + self.x  # Substitua pelo atributo de posição do personagem
        dy = personagem.y + self.y  # Substitua pelo atributo de posição do personagem
       #distancia = math.sqrt(dx ** 2 + dy ** 2)
        distancia = dx
        return distancia
