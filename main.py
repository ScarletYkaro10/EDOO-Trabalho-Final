import pygame
import sys

# Importa a classe do arquivo de "ponte" do Wesley
from estrutura_dados import TabelaHash

# --- CONFIGURAÇÕES GERAIS ---
LARGURA = 900
ALTURA = 600
# O tamanho tem que bater com o default do Wesley (20) ou passar no construtor
TAMANHO_HASH = 20
COR_FUNDO = (30, 33, 40)
COR_TEXTO = (255, 255, 255)

# Cores dos Slots
COR_VAZIO = (60, 63, 70)
COR_OCUPADO = (70, 200, 100)  # Verde
COR_COLISAO_DESTINO = (220, 180, 50)  # Amarelo (Onde ele caiu após colidir)
COR_TUMULO = (200, 60, 60)  # Vermelho (Deletado)
COR_DESTAQUE = (50, 150, 255)  # Azul (Resultado da busca)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("RPG Inventory Manager - Estrutura Hash")
    fonte = pygame.font.SysFont("Verdana", 14)
    fonte_grande = pygame.font.SysFont("Verdana", 24)

    # Inicializa a Lógica (Backend do Wesley)
    inventario = TabelaHash(TAMANHO_HASH)

    # Variáveis de Interface
    texto_input = ""
    mensagem_status = "Digite o nome do item e aperte ENTER para inserir."
    indice_destaque = -1  # Nenhum slot destacado inicialmente
    cor_mensagem = (255, 200, 0)  # Cor amarela padrão

    relogio = pygame.time.Clock()

    while True:
        tela.fill(COR_FUNDO)

        # --- 1. CAPTURA DE EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                    indice_destaque = -1  # Limpa destaque ao digitar

                elif evento.key == pygame.K_RETURN:
                    # TENTA INSERIR
                    if texto_input:
                        try:
                            # O método do Wesley retorna (indice, houve_colisao)
                            indice_real, houve_colisao = inventario.inserir(texto_input)

                            if houve_colisao:
                                indice_calculado = inventario._funcao_hash(texto_input)
                                mensagem_status = f"Colisão! Hash: {indice_calculado} -> Alocado em: {indice_real}"
                                cor_mensagem = (255, 100, 100)  # Vermelho claro
                            else:
                                mensagem_status = f"Item '{texto_input}' inserido no slot {indice_real}."
                                cor_mensagem = (100, 255, 100)  # Verde claro

                            texto_input = ""  # Limpa campo sucesso

                        except Exception as e:
                            # Captura o erro "Tabela Cheia" do Wesley
                            mensagem_status = f"Erro: {str(e)}"
                            cor_mensagem = (255, 50, 50)  # Vermelho erro

                elif evento.key == pygame.K_DELETE:
                    # REMOVER
                    if texto_input:
                        if inventario.remover(texto_input):
                            mensagem_status = (
                                f"Item '{texto_input}' removido (Túmulo criado)."
                            )
                            cor_mensagem = (255, 200, 0)
                        else:
                            mensagem_status = "Item não encontrado para remover."
                            cor_mensagem = (255, 100, 100)
                        texto_input = ""

                elif evento.key == pygame.K_TAB:
                    # BUSCAR
                    if texto_input:
                        resultado = inventario.buscar(texto_input)
                        if resultado is not None:
                            indice_destaque = resultado
                            mensagem_status = f"Item encontrado no slot {resultado}!"
                            cor_mensagem = (100, 200, 255)
                        else:
                            mensagem_status = "Item não existe no inventário."
                            indice_destaque = -1
                            cor_mensagem = (255, 100, 100)

                else:
                    # Adiciona letra ao texto
                    if len(texto_input) < 15:  # Limite de caracteres visual
                        texto_input += evento.unicode

        # --- 2. DESENHO DA INTERFACE ---

        # Configuração da Grade (5 colunas x 4 linhas para 20 itens)
        colunas = 5
        margem_x = 150  # Centralizar um pouco mais
        margem_y = 150
        tamanho_quad = 100
        espaco = 10

        # Loop para desenhar os slots baseados na lista 'dados' do Wesley
        for i in range(inventario.tamanho):
            linha = i // colunas
            coluna = i % colunas
            x = margem_x + coluna * (tamanho_quad + espaco)
            y = margem_y + linha * (tamanho_quad + espaco)

            # Pega o conteúdo direto da lista do Wesley
            conteudo = inventario.dados[i]

            # Define a cor do slot
            if i == indice_destaque:
                cor = COR_DESTAQUE  # Item buscado brilha azul
            elif conteudo is None:
                cor = COR_VAZIO
            elif conteudo == "DELETADO":  # Wesley usa a string "DELETADO"
                cor = COR_TUMULO
            else:
                cor = COR_OCUPADO

            # Desenha Quadrado
            pygame.draw.rect(
                tela, cor, (x, y, tamanho_quad, tamanho_quad), border_radius=5
            )
            pygame.draw.rect(
                tela, (200, 200, 200), (x, y, tamanho_quad, tamanho_quad), 1
            )  # Borda

            # Escreve o Índice (número pequeno no canto)
            texto_idx = fonte.render(str(i), True, (200, 200, 200))
            tela.blit(texto_idx, (x + 5, y + 5))

            # Escreve o Conteúdo (Nome do Item ou X)
            if conteudo and conteudo != "DELETADO":
                # O conteudo na lista do Wesley é apenas a string (ex: "Espada")
                texto_item = fonte.render(conteudo, True, (0, 0, 0))
                tela.blit(texto_item, (x + 10, y + 40))

            elif conteudo == "DELETADO":
                texto_tumulo = fonte.render("X", True, (0, 0, 0))
                tela.blit(texto_tumulo, (x + 40, y + 30))

        # --- 3. PAINEL DE CONTROLE E MENSAGENS ---

        # Instruções Rodapé
        texto_instrucao = fonte.render(
            "Enter: Inserir | Tab: Buscar | Delete: Remover", True, (150, 150, 150)
        )
        tela.blit(texto_instrucao, (LARGURA // 2 - 150, ALTURA - 30))

        # Caixa de Input (Onde digita)
        pygame.draw.rect(tela, (50, 50, 55), (margem_x, 50, 400, 50), border_radius=5)
        superficie_texto = fonte_grande.render(texto_input, True, COR_TEXTO)
        tela.blit(superficie_texto, (margem_x + 10, 60))

        # Mensagem de Status (Abaixo do input)
        status_surface = fonte.render(f"Status: {mensagem_status}", True, cor_mensagem)
        tela.blit(status_surface, (margem_x, 110))

        pygame.display.flip()
        relogio.tick(30)


if __name__ == "__main__":
    main()
