import pygame

class HUD:
    def __init__(self, tela, fonte):
        self.tela = tela
        self.fonte = fonte
        
        # Carregar imagem para o ícone de vida
        self.vida_img = pygame.image.load('assets/imagens/hud/vida.png').convert_alpha()
        self.vida_img = pygame.transform.scale(self.vida_img, (30, 30))

    def update(self, pontuacao, vidas, nivel):
        # Exibe a pontuação
        score_surf = self.fonte.render(f'Pontuação: {pontuacao}', False, (255, 255, 255))
        score_rect = score_surf.get_rect(topleft=(10, 10))
        self.tela.blit(score_surf, score_rect)
        
        # Exibe o nível
        nivel_surf = self.fonte.render(f'Nível: {nivel}', False, (255, 255, 255))
        nivel_rect = nivel_surf.get_rect(midtop=(400, 10))
        self.tela.blit(nivel_surf, nivel_rect)
        
        # Exibe as vidas
        for i in range(vidas):
            vida_rect = self.vida_img.get_rect(topleft=(700 - i * 35, 10))
            self.tela.blit(self.vida_img, vida_rect)