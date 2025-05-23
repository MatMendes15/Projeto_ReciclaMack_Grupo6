import pygame
import random

class Lixo(pygame.sprite.Sprite):
    def __init__(self, tela_largura, tela_altura):
        super().__init__()
        
        # Tipos de lixo (cada um com uma forma e cor diferente)
        self.tipos_lixo = {
            'celular': {
                'cor': (150, 150, 150),
                'forma': 'retangulo',
                'tamanho': (20, 35),
                'pontos': 10
            },
            'bateria': {
                'cor': (255, 215, 0),
                'forma': 'retangulo',
                'tamanho': (15, 25),
                'pontos': 5
            },
            'computador': {
                'cor': (200, 200, 200),
                'forma': 'quadrado',
                'tamanho': (40, 40),
                'pontos': 20
            },
            'televisao': {
                'cor': (50, 50, 50),
                'forma': 'retangulo',
                'tamanho': (45, 30),
                'pontos': 15
            }
        }
        
        # Escolhe um tipo aleatório
        self.tipo = random.choice(list(self.tipos_lixo.keys()))
        self.info = self.tipos_lixo[self.tipo]
        self.pontos = self.info['pontos']
        
        # Cria uma superfície para o lixo
        largura, altura = self.info['tamanho']
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        
        # Desenha a forma apropriada
        if self.info['forma'] == 'retangulo' or self.info['forma'] == 'quadrado':
            pygame.draw.rect(self.image, self.info['cor'], (0, 0, largura, altura))
        
        # Adiciona detalhes para diferenciar visualmente
        if self.tipo == 'celular':
            # Adiciona tela como um retângulo interno mais claro
            # pygame.draw.rect(self.image, (200, 200, 255), (3, 3, largura-6, 15))
            self.image = pygame.image.load( 'imagens/celular.png')
            self.image = pygame.transform.scale(self.image, (60,30))
        elif self.tipo == 'computador':
            # Adiciona uma "tela" e "teclado"
            # pygame.draw.rect(self.image, (150, 150, 255), (5, 5, largura-10, 20))
            # pygame.draw.rect(self.image, (100, 100, 100), (5, 28, largura-10, 8))
            self.image = pygame.image.load( 'imagens/computador.png')
            self.image = pygame.transform.scale(self.image, (40,60))
        elif self.tipo == 'televisao':
            # Adiciona tela como um retângulo interno
            # pygame.draw.rect(self.image, (30, 30, 30), (3, 3, largura-6, altura-6))
            self.image = pygame.image.load( 'imagens/tv.png')
            self.image = pygame.transform.scale(self.image, (40,60))
        elif self.tipo == 'bateria':
            self.image = pygame.image.load( 'imagens/bateria.png')
            self.image = pygame.transform.scale(self.image, (40,60))
        
        # Posição inicial aleatória no topo da tela
        self.rect = self.image.get_rect(midtop=(random.randint(largura, tela_largura - largura), 0))
        
        # Velocidade de queda - REDUZIDA para facilitar o jogo
        self.velocidade = random.uniform(1, 3)  # Reduzido de 2-5 para 1-3
        self.tela_altura = tela_altura

    def update(self):
        # Move o lixo para baixo
        self.rect.y += self.velocidade
        
        # Retorna True se o lixo saiu da tela (para reduzir vidas)
        if self.rect.top > self.tela_altura:
            self.kill()
            return True
        return False