import pygame
import sys
from cenas.jogo import Jogo

class Menu:
    def __init__(self):
        pygame.init()

        # Carregar efeitos sonoros
        pygame.mixer.init()
        
        self.som_menu = pygame.mixer.Sound("sons/menu.mp3")

        self.som_opcao_menu = pygame.mixer.Sound("sons/opcao.mp3")
        
        # Configurações da tela
        self.largura_tela = 800
        self.altura_tela = 600
        self.tela = pygame.display.set_mode((self.largura_tela, self.altura_tela))
        pygame.display.set_caption('ReciclaMack - Menu')
        
        # Cores
        self.BRANCO = (255, 255, 255)
        self.PRETO = (0, 0, 0)
        self.VERDE = (0, 128, 0)
        self.AZUL = (0, 100, 255)
        self.VERDE_CLARO = (144, 238, 144)
        
        # Configurações do menu
        self.relogio = pygame.time.Clock()
        self.fonte_titulo = pygame.font.Font(None, 72)
        self.fonte_opcoes = pygame.font.Font(None, 48)
        self.fonte_descricao = pygame.font.Font(None, 28)
        
        # Opções do menu
        self.opcoes = ['Iniciar Jogo', 'Como Jogar', 'Sair']
        self.opcao_selecionada = 0
        
    def desenhar_fundo(self):
        # Desenha um gradiente do topo até o fundo
        for i in range(self.altura_tela):
            # Gradiente de azul-claro para verde-claro
            fator = i / self.altura_tela
            r = int(135 * (1 - fator) + 144 * fator)
            g = int(206 * (1 - fator) + 238 * fator)
            b = int(235 * (1 - fator) + 144 * fator)
            pygame.draw.line(self.tela, (r, g, b), (0, i), (self.largura_tela, i))
        
        # Desenha símbolos de reciclagem simplificados
        for i in range(5):
            x = 100 + i * 150
            y = 500
            raio = 30
            
            # Desenha o círculo de reciclagem
            pygame.draw.circle(self.tela, self.VERDE, (x, y), raio)
            pygame.draw.circle(self.tela, self.VERDE_CLARO, (x, y), raio - 5)
            
            # Desenha as setas simplificadas
            pontos = [
                (x - 15, y - 5),
                (x, y - 20),
                (x + 15, y - 5),
                (x, y + 10)
            ]
            pygame.draw.polygon(self.tela, self.VERDE, pontos)
    
    def desenhar_menu(self):
        # Desenha o título
        texto_titulo = self.fonte_titulo.render('ReciclaMack', True, self.VERDE)
        self.tela.blit(texto_titulo, (self.largura_tela // 2 - texto_titulo.get_width() // 2, 100))
        
        # Desenha o subtítulo
        texto_subtitulo = self.fonte_descricao.render('Projeto de Extensão: Reciclagem de Eletrônicos', True, self.PRETO)
        self.tela.blit(texto_subtitulo, (self.largura_tela // 2 - texto_subtitulo.get_width() // 2, 170))
        
        # Desenha as opções
        for i, opcao in enumerate(self.opcoes):
            if i == self.opcao_selecionada:
                cor = self.AZUL
                # Desenha um indicador ao lado da opção selecionada
                pygame.draw.circle(self.tela, self.VERDE, (self.largura_tela // 2 - 130, 250 + i * 60), 10)
            else:
                cor = self.PRETO
                
            texto = self.fonte_opcoes.render(opcao, True, cor)
            self.tela.blit(texto, (self.largura_tela // 2 - 100, 240 + i * 60))
    
    def mostrar_instrucoes(self):

        self.tela.fill(self.VERDE_CLARO)
        
        # Título
        texto_titulo = self.fonte_titulo.render('Como Jogar', True, self.VERDE)
        self.tela.blit(texto_titulo, (self.largura_tela // 2 - texto_titulo.get_width() // 2, 50))
        
        # Instruções
        instrucoes = [
            "- Use as setas ESQUERDA e DIREITA para mover o coletor",
            "- Colete os lixos eletrônicos antes que caiam no chão",
            "- Cada lixo que cair no chão, você perde uma vida",
            "- Você tem 3 vidas para completar o maior número de níveis",
            "- Cada tipo de lixo vale uma pontuação diferente",
            "- Pressione ESC para pausar o jogo"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            texto = self.fonte_descricao.render(instrucao, True, self.PRETO)
            self.tela.blit(texto, (100, 150 + i * 50))
        
        # Informação sobre tipos de lixo
        texto_tipos = self.fonte_opcoes.render('Tipos de Lixo:', True, self.VERDE)
        self.tela.blit(texto_tipos, (100, 450))
        
        # Exemplos de lixo e suas pontuações
        tipos_lixo = [
            {'nome': 'Celular', 'cor': (150, 150, 150), 'pontos': 10, 'tamanho': (20, 35)},
            {'nome': 'Bateria', 'cor': (255, 215, 0), 'pontos': 5, 'tamanho': (15, 25)},
            {'nome': 'Computador', 'cor': (200, 200, 200), 'pontos': 20, 'tamanho': (40, 40)},
            {'nome': 'Televisão', 'cor': (50, 50, 50), 'pontos': 15, 'tamanho': (45, 30)}
        ]
        
        for i, tipo in enumerate(tipos_lixo):
            # Desenha o lixo
            x = 120 + i * 150
            y = 500
            largura, altura = tipo['tamanho']
            pygame.draw.rect(self.tela, tipo['cor'], (x, y, largura, altura))
            
            # Desenha o nome e pontuação
            texto_nome = self.fonte_descricao.render(tipo['nome'], True, self.PRETO)
            self.tela.blit(texto_nome, (x - 20, y + 50))
            
            texto_pontos = self.fonte_descricao.render(f"{tipo['pontos']} pts", True, self.PRETO)
            self.tela.blit(texto_pontos, (x - 10, y + 80))
        
        # Botão para voltar
        texto_voltar = self.fonte_opcoes.render('Voltar', True, self.AZUL)
        texto_rect = texto_voltar.get_rect(center=(self.largura_tela // 2, 570))
        self.tela.blit(texto_voltar, texto_rect)
        
        pygame.display.flip()
        
        # Loop das instruções
        instrucoes_ativas = True
        while instrucoes_ativas:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE or evento.key == pygame.K_RETURN:
                        instrucoes_ativas = False
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if texto_rect.collidepoint(evento.pos):
                        instrucoes_ativas = False
            
            self.relogio.tick(60)
    
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.som_opcao_menu.play() # Desencadeia efeito sonoro de opção do menu
                    self.opcao_selecionada = (self.opcao_selecionada - 1) % len(self.opcoes)
                elif evento.key == pygame.K_DOWN:
                    self.som_opcao_menu.play() # Desencadeia efeito sonoro de opção do menu
                    self.opcao_selecionada = (self.opcao_selecionada + 1) % len(self.opcoes)
                elif evento.key == pygame.K_RETURN:
                    self.selecionar_opcao()
    
    def selecionar_opcao(self):
        if self.opcao_selecionada == 0:  # Iniciar Jogo
            jogo = Jogo()
            self.som_menu.stop() # Para a música do menu
            jogo.run()
        elif self.opcao_selecionada == 1:  # Como Jogar
            self.mostrar_instrucoes()
        elif self.opcao_selecionada == 2:  # Sair
            pygame.quit()
            sys.exit()
    
    def run(self):
        self.som_menu.play(-1)  # Com -1 a música toca em loop
        while True:
            self.processar_eventos()
            
            self.desenhar_fundo()
            self.desenhar_menu()
            
            pygame.display.flip()
            self.relogio.tick(60)