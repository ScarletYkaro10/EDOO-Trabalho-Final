import pygame
import sys

from estrutura_dados import TabelaHash

LARGURA = 950
ALTURA = 600
TAMANHO_HASH = 20
COR_FUNDO = (30, 33, 40)
COR_TEXTO = (255, 255, 255)

COR_VAZIO = (60, 63, 70)
COR_OCUPADO = (70, 200, 100)
COR_COLISAO_DESTINO = (220, 180, 50)
COR_TUMULO = (200, 60, 60)
COR_DESTAQUE = (50, 150, 255)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Gerenciador de Inventário RPG - Estrutura Hash")

    fonte = pygame.font.SysFont("Verdana", 14)
    fonte_bold = pygame.font.SysFont("Verdana", 14, bold=True)
    fonte_grande = pygame.font.SysFont("Verdana", 20)

    inventario = TabelaHash(TAMANHO_HASH)

    texto_input = ""
    mensagem_status = "Bem-vindo! Digite um item para começar."
    indice_destaque = -1
    cor_mensagem = (255, 200, 0)

    relogio = pygame.time.Clock()

    while True:
        tela.fill(COR_FUNDO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                    indice_destaque = -1

                elif evento.key == pygame.K_RETURN:
                    if texto_input:
                        try:
                            indice_real, houve_colisao = inventario.inserir(texto_input)

                            if houve_colisao:
                                indice_calculado = inventario._funcao_hash(texto_input)
                                mensagem_status = f"Colisão! Hash: {indice_calculado} -> Alocado em: {indice_real}"
                                cor_mensagem = (255, 100, 100)
                            else:
                                mensagem_status = f"Item '{texto_input}' guardado no slot {indice_real}."
                                cor_mensagem = (100, 255, 100)

                            texto_input = ""

                        except Exception as e:
                            mensagem_status = f"Erro: {str(e)}"
                            cor_mensagem = (255, 50, 50)

                elif evento.key == pygame.K_DELETE:
                    if texto_input:
                        if inventario.remover(texto_input):
                            mensagem_status = (
                                f"Item '{texto_input}' jogado fora (Túmulo criado)."
                            )
                            cor_mensagem = (255, 200, 0)
                        else:
                            mensagem_status = "Item não encontrado na mochila."
                            cor_mensagem = (255, 100, 100)
                        texto_input = ""

                elif evento.key == pygame.K_TAB:
                    if texto_input:
                        resultado = inventario.buscar(texto_input)
                        if resultado is not None:
                            indice_destaque = resultado
                            mensagem_status = f"Item encontrado no slot {resultado}!"
                            cor_mensagem = (100, 200, 255)
                        else:
                            mensagem_status = "Este item não está na mochila."
                            indice_destaque = -1
                            cor_mensagem = (255, 100, 100)

                else:
                    if len(texto_input) < 18:
                        texto_input += evento.unicode

        colunas = 5
        margem_x = 320
        margem_y = 140
        tamanho_quad = 100
        espaco = 10

        for i in range(inventario.tamanho):
            linha = i // colunas
            coluna = i % colunas
            x = margem_x + coluna * (tamanho_quad + espaco)
            y = margem_y + linha * (tamanho_quad + espaco)

            conteudo = inventario.dados[i]

            if i == indice_destaque:
                cor = COR_DESTAQUE
            elif conteudo is None:
                cor = COR_VAZIO
            elif conteudo == "DELETADO":
                cor = COR_TUMULO
            else:
                cor = COR_OCUPADO

            pygame.draw.rect(
                tela, cor, (x, y, tamanho_quad, tamanho_quad), border_radius=8
            )
            pygame.draw.rect(
                tela, (150, 150, 150), (x, y, tamanho_quad, tamanho_quad), 1
            )

            texto_idx = fonte.render(str(i), True, (200, 200, 200))
            tela.blit(texto_idx, (x + 5, y + 5))

            if conteudo and conteudo != "DELETADO":
                texto_item = fonte_bold.render(conteudo, True, (20, 20, 20))
                largura_txt = texto_item.get_width()
                tela.blit(texto_item, (x + (tamanho_quad - largura_txt) // 2, y + 40))

            elif conteudo == "DELETADO":
                texto_tumulo = fonte_bold.render("X", True, (50, 0, 0))
                tela.blit(texto_tumulo, (x + 40, y + 35))

        x_instrucoes = 30
        y_instrucoes = 140
        espaco_linha = 30

        tela.blit(
            fonte_grande.render("COMO JOGAR:", True, (100, 255, 200)),
            (x_instrucoes, y_instrucoes - 40),
        )

        comandos = [
            ("Digite o nome do item...", (200, 200, 200)),
            ("", (0, 0, 0)),
            ("TECLA ENTER:", (255, 255, 255)),
            ("-> Guardar Item", (180, 180, 180)),
            ("", (0, 0, 0)),
            ("TECLA TAB:", (255, 255, 255)),
            ("-> Buscar Item (Azul)", (180, 180, 180)),
            ("", (0, 0, 0)),
            ("TECLA DELETE:", (255, 255, 255)),
            ("-> Jogar fora (Vermelho)", (180, 180, 180)),
        ]

        y_atual = y_instrucoes
        for texto, cor in comandos:
            render = fonte.render(texto, True, cor)
            tela.blit(render, (x_instrucoes, y_atual))
            y_atual += 22

        pygame.draw.rect(tela, (50, 50, 55), (margem_x, 50, 400, 50), border_radius=8)
        pygame.draw.rect(tela, (100, 100, 100), (margem_x, 50, 400, 50), 1)

        superficie_texto = fonte_grande.render(texto_input, True, COR_TEXTO)
        tela.blit(superficie_texto, (margem_x + 15, 60))

        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = margem_x + 15 + superficie_texto.get_width()
            pygame.draw.rect(tela, (255, 255, 255), (cursor_x, 62, 2, 25))

        status_surface = fonte.render(f"{mensagem_status}", True, cor_mensagem)
        tela.blit(status_surface, (margem_x, 110))

        pygame.display.flip()
        relogio.tick(30)


if __name__ == "__main__":
    main()
