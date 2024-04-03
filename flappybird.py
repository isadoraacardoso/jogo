import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_KPT = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'kpta.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_SUPERMEN = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'superhomem.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'superhomem.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'superhomem.png'))), 
]
 
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('',50) 


class Supermen:
    IMGS = IMAGENS_SUPERMEN 
    # animações da rotação
    ROTACAO_MAXIMA = 40
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o angulo do supermen
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do supermen vai usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0


        # se o supermen tiver caindo eu não vou bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Kriptonita:
    DISTANCIA = 180
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.KPT_TOPO = pygame.transform.flip(IMAGEM_KPT, False, True)
        self.KPT_BASE = IMAGEM_KPT
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.KPT_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA   

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.KPT_TOPO, (self.x, self.pos_topo))
        tela.blit(self.KPT_BASE, (self.x, self.pos_base))

    def colidir(self, supermen):
        supermen_mask = supermen.get_mask()
        topo_mask = pygame.mask.from_surface(self.KPT_TOPO)
        base_mask = pygame.mask.from_surface(self.KPT_BASE)

        distancia_topo = (self.x - supermen.x, self.pos_topo - round(supermen.y))
        distancia_base = (self.x - supermen.x, self.pos_base - round(supermen.y))

        topo_ponto = supermen_mask.overlap(topo_mask, distancia_topo)
        base_ponto = supermen_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, supermens, kriptonitas, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for supermen in supermens:
        supermen.desenhar(tela)
    for kriptonita in kriptonitas:
        kriptonita.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", 1, (20, 20, 20))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    supermens = [Supermen(230, 350)]
    chao = Chao(730)
    kriptonitas = [Kriptonita(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        # interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for supermen in supermens:
                        supermen.pular()

        # mover as coisas
        for supermen in supermens:
            supermen.mover()
        chao.mover()

        adicionar_kriptonita = False
        remover_kriptonitas = []
        for kriptonita in kriptonitas:
            for i, supermen in enumerate(supermens):
                if kriptonita.colidir(supermen):
                    supermens.pop(i)
                if not kriptonita.passou and supermen.x > kriptonita.x:
                    kriptonita.passou = True
                    adicionar_kriptonita = True
            kriptonita.mover()
            if kriptonita.x + kriptonita.KPT_TOPO.get_width() < 0:
                remover_kriptonitas.append(kriptonita)

        if adicionar_kriptonita:
            pontos += 1
            kriptonitas.append(Kriptonita(600))
        for kriptonita in remover_kriptonitas:
            kriptonitas.remove(kriptonita)

        for i, supermen in enumerate(supermens):
            if (supermen.y + supermen.imagem.get_height()) > chao.y or supermen.y < 0:
                supermens.pop(i)

        desenhar_tela(tela, supermens, kriptonitas, chao, pontos)


if __name__ == '__main__':
    main()