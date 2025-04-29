import pygame
import random
import sys
from entidades.jogador import Jogador
from entidades.lixo import Lixo

class Jogo:
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.largura_tela = 800
        self.altura_tela = 600
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('ReciclaMack')
        
        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.VERDE = (0, 128, 0)
        self.VERMELHO = (255, 0, 0)
        self.AZUL_CLARO = (135, 206, 235)  # Cor do céu
        self.VERDE_GRAMA = (34, 139, 34)   # Cor da grama
        self.AMARELO = (255, 255, 0)       # Cor para seleção
        
        # Configurações do jogo
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 24)
        
        # Estados do jogo
        self.jogo_ativo = True
        self.game_over = False
        self.paused = False
        self.quit_game = False
        
        # Opções de menu de pausa
        self.opcoes_pausa = ['Continuar', 'Reiniciar', 'Sair']
        self.opcao_pausa_selecionada = 0
        
        # Opções de menu de game over
        self.opcoes_game_over = ['Reiniciar', 'Sair']
        self.opcao_game_over_selecionada = 0
        
        # Pontuação e jogador
        self.pontuacao = 0
        self.vidas = 3
        self.nivel = 1
        
        # Entidades
        self.jogador = pygame.sprite.GroupSingle()
        self.jogador.add(Jogador(self.largura_tela, self.altura_tela))
        self.grupo_lixos = pygame.sprite.Group()
        
        # Timer para spawn de lixo - ajustado para começar mais lento
        self.spawn_interval = 2000  # aumentado de 1500 para 2000 milissegundos
        self.lixo_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.lixo_timer, self.spawn_interval)
        
        # Objetivo para passar de nível
        self.lixo_para_proximo_nivel = 10
        
    def desenhar_fundo(self):
        # Desenha o céu
        self.tela.fill(self.AZUL_CLARO)
        
        # Desenha a grama/chão
        pygame.draw.rect(self.tela, self.VERDE_GRAMA, (0, self.altura_tela - 30, self.largura_tela, 30))
        
        # Desenha o sol
        pygame.draw.circle(self.tela, (255, 255, 0), (50, 50), 30)
        
        # Desenha algumas nuvens
        for x in [150, 350, 600]:
            raio = 25
            pygame.draw.circle(self.tela, self.BRANCO, (x, 80), raio)
            pygame.draw.circle(self.tela, self.BRANCO, (x + 20, 70), raio)
            pygame.draw.circle(self.tela, self.BRANCO, (x + 40, 80), raio)
            
        # As lixeiras foram removidas conforme solicitado
    
    def desenhar_hud(self):
        # Pontuação
        texto_pontuacao = self.fonte.render(f'Pontuação: {self.pontuacao}', True, self.PRETO)
        self.tela.blit(texto_pontuacao, (10, 10))
        
        # Nível
        texto_nivel = self.fonte.render(f'Nível: {self.nivel}', True, self.PRETO)
        self.tela.blit(texto_nivel, (self.largura_tela // 2 - 50, 10))
        
        # Vidas
        texto_vidas = self.fonte.render(f'Vidas: {self.vidas}', True, self.PRETO)
        self.tela.blit(texto_vidas, (self.largura_tela - 120, 10))
        
        # Progresso do nível
        progresso = self.pontuacao % self.lixo_para_proximo_nivel
        porcentagem = progresso / self.lixo_para_proximo_nivel
        largura_barra = 300
        pygame.draw.rect(self.tela, (150, 150, 150), (self.largura_tela // 2 - largura_barra // 2, 50, largura_barra, 20))
        pygame.draw.rect(self.tela, self.VERDE, (self.largura_tela // 2 - largura_barra // 2, 50, int(largura_barra * porcentagem), 20))
        
    def mostrar_pausa(self):
        # Escurece a tela
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.tela.blit(overlay, (0, 0))
        
        # Desenha um painel para o menu
        painel_largura = 300
        painel_altura = 250
        painel_x = self.largura_tela // 2 - painel_largura // 2
        painel_y = self.altura_tela // 2 - painel_altura // 2
        
        pygame.draw.rect(self.tela, (50, 50, 50), (painel_x, painel_y, painel_largura, painel_altura))
        pygame.draw.rect(self.tela, (100, 100, 100), (painel_x, painel_y, painel_largura, painel_altura), 3)
        
        # Texto do menu de pausa
        texto_pausa = self.fonte.render('PAUSA', True, self.BRANCO)
        texto_pausa_rect = texto_pausa.get_rect(center=(self.largura_tela // 2, painel_y + 40))
        self.tela.blit(texto_pausa, texto_pausa_rect)
        
        # Desenha as opções com a seleção atual destacada
        for i, opcao in enumerate(self.opcoes_pausa):
            if i == self.opcao_pausa_selecionada:
                cor = self.AMARELO
                # Desenha um indicador de seleção (triângulo)
                pygame.draw.polygon(self.tela, self.AMARELO, [
                    (painel_x + 60, painel_y + 100 + i * 45),
                    (painel_x + 75, painel_y + 110 + i * 45),
                    (painel_x + 60, painel_y + 120 + i * 45)
                ])
            else:
                cor = self.BRANCO
                
            texto = self.fonte.render(opcao, True, cor)
            texto_rect = texto.get_rect(midleft=(painel_x + 90, painel_y + 110 + i * 45))
            self.tela.blit(texto, texto_rect)
        
        # Instruções de navegação
        instrucao = self.fonte_pequena.render("Use as setas e ENTER para selecionar", True, self.BRANCO)
        instrucao_rect = instrucao.get_rect(center=(self.largura_tela // 2, painel_y + painel_altura - 30))
        self.tela.blit(instrucao, instrucao_rect)
    
    def mostrar_game_over(self):
        # Escurece a tela
        overlay = pygame.Surface((self.largura_tela, self.altura_tela), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        self.tela.blit(overlay, (0, 0))
        
        # Desenha um painel para o menu
        painel_largura = 400
        painel_altura = 300
        painel_x = self.largura_tela // 2 - painel_largura // 2
        painel_y = self.altura_tela // 2 - painel_altura // 2
        
        pygame.draw.rect(self.tela, (50, 50, 50), (painel_x, painel_y, painel_largura, painel_altura))
        pygame.draw.rect(self.tela, (200, 0, 0), (painel_x, painel_y, painel_largura, painel_altura), 3)
        
        # Textos de game over
        texto_game_over = self.fonte.render('GAME OVER', True, self.VERMELHO)
        texto_game_over_rect = texto_game_over.get_rect(center=(self.largura_tela // 2, painel_y + 50))
        self.tela.blit(texto_game_over, texto_game_over_rect)
        
        texto_pontuacao = self.fonte.render(f'Pontuação final: {self.pontuacao}', True, self.BRANCO)
        texto_pontuacao_rect = texto_pontuacao.get_rect(center=(self.largura_tela // 2, painel_y + 100))
        self.tela.blit(texto_pontuacao, texto_pontuacao_rect)
        
        # Desenha as opções com a seleção atual destacada
        for i, opcao in enumerate(self.opcoes_game_over):
            if i == self.opcao_game_over_selecionada:
                cor = self.AMARELO
                # Desenha um indicador de seleção (triângulo)
                pygame.draw.polygon(self.tela, self.AMARELO, [
                    (painel_x + 110, painel_y + 170 + i * 45),
                    (painel_x + 125, painel_y + 180 + i * 45),
                    (painel_x + 110, painel_y + 190 + i * 45)
                ])
            else:
                cor = self.BRANCO
                
            texto = self.fonte.render(opcao, True, cor)
            texto_rect = texto.get_rect(midleft=(painel_x + 140, painel_y + 180 + i * 45))
            self.tela.blit(texto, texto_rect)
        
        # Instruções de navegação
        instrucao = self.fonte_pequena.render("Use as setas e ENTER para selecionar", True, self.BRANCO)
        instrucao_rect = instrucao.get_rect(center=(self.largura_tela // 2, painel_y + painel_altura - 30))
        self.tela.blit(instrucao, instrucao_rect)
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Controles no jogo ativo
            if self.jogo_ativo:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        # Reset da seleção quando abre o menu
                        if self.paused:
                            self.opcao_pausa_selecionada = 0
                
                # Navegação no menu de pausa
                if self.paused and evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.opcao_pausa_selecionada = (self.opcao_pausa_selecionada - 1) % len(self.opcoes_pausa)
                    elif evento.key == pygame.K_DOWN:
                        self.opcao_pausa_selecionada = (self.opcao_pausa_selecionada + 1) % len(self.opcoes_pausa)
                    elif evento.key == pygame.K_RETURN:
                        # Executa a ação da opção selecionada
                        if self.opcoes_pausa[self.opcao_pausa_selecionada] == 'Continuar':
                            self.paused = False
                        elif self.opcoes_pausa[self.opcao_pausa_selecionada] == 'Reiniciar':
                            self.reiniciar_jogo()
                            self.paused = False
                        elif self.opcoes_pausa[self.opcao_pausa_selecionada] == 'Sair':
                            self.quit_game = True
                
                # Spawn de lixo quando timer dispara
                if evento.type == self.lixo_timer and not self.paused:
                    novo_lixo = Lixo(self.largura_tela, self.altura_tela)
                    self.grupo_lixos.add(novo_lixo)
            
            # Controles no game over
            elif self.game_over and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.opcao_game_over_selecionada = (self.opcao_game_over_selecionada - 1) % len(self.opcoes_game_over)
                elif evento.key == pygame.K_DOWN:
                    self.opcao_game_over_selecionada = (self.opcao_game_over_selecionada + 1) % len(self.opcoes_game_over)
                elif evento.key == pygame.K_RETURN:
                    # Executa a ação da opção selecionada
                    if self.opcoes_game_over[self.opcao_game_over_selecionada] == 'Reiniciar':
                        self.reiniciar_jogo()
                    elif self.opcoes_game_over[self.opcao_game_over_selecionada] == 'Sair':
                        self.quit_game = True
    
    def atualizar_jogo(self):
        if self.paused:
            return
            
        # Atualiza o jogador
        self.jogador.update()
        
        # Atualiza e verifica os lixos
        for lixo in list(self.grupo_lixos):
            if lixo.update():  # Lixo caiu no chão
                self.vidas -= 1
                if self.vidas <= 0:
                    self.jogo_ativo = False
                    self.game_over = True
                    self.opcao_game_over_selecionada = 0  # Reset da seleção
        
        # Verifica colisões (coleta de lixo)
        colisoes = pygame.sprite.spritecollide(self.jogador.sprite, self.grupo_lixos, True)
        for lixo in colisoes:
            self.pontuacao += lixo.pontos
            
            # Verifica se alcançou pontos para próximo nível
            if self.pontuacao >= self.nivel * self.lixo_para_proximo_nivel:
                self.nivel += 1
                # Aumenta frequência de spawn conforme o nível, mas de forma mais gradual
                self.spawn_interval = max(1000, 2000 - (self.nivel - 1) * 100)  # Ajustado para ser mais gradual
                pygame.time.set_timer(self.lixo_timer, self.spawn_interval)
    
    def desenhar(self):
        self.desenhar_fundo()
        
        # Desenha os lixos
        self.grupo_lixos.draw(self.tela)
        
        # Desenha o jogador
        self.jogador.draw(self.tela)
        
        # Desenha a interface
        self.desenhar_hud()
        
        # Se o jogo estiver pausado, mostra o menu de pausa
        if self.paused:
            self.mostrar_pausa()
            
        # Se for game over, mostra a tela de game over
        if self.game_over:
            self.mostrar_game_over()
    
    def reiniciar_jogo(self):
        self.jogo_ativo = True
        self.game_over = False
        self.paused = False
        self.pontuacao = 0
        self.vidas = 3
        self.nivel = 1
        self.grupo_lixos.empty()
        self.jogador.sprite.rect.midbottom = (self.largura_tela // 2, self.altura_tela - 20)
        self.spawn_interval = 2000  # Resetado para 2000ms (valor inicial mais lento)
        pygame.time.set_timer(self.lixo_timer, self.spawn_interval)
    
    def run(self):
        while not self.quit_game:
            self.processar_eventos()
            
            if self.jogo_ativo and not self.paused:
                self.atualizar_jogo()
                
            self.desenhar()
            
            pygame.display.flip()
            self.relogio.tick(60)