import pygame

class Jogador(pygame.sprite.Sprite):
    def __init__(self, tela_largura, tela_altura):
        super().__init__()
        # Cria uma superfície para o jogador (círculo azul)
        self.raio = 20
        self.image = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 100, 255), (self.raio, self.raio), self.raio)
        
        # Retângulo de colisão
        self.rect = self.image.get_rect()
        self.rect.midbottom = (tela_largura // 2, tela_altura - 20)
        
        # Atributos de movimento
        self.velocidade = 8
        self.tela_largura = tela_largura

    def update(self):
        # Movimento baseado no teclado
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < self.tela_largura:
            self.rect.x += self.velocidade