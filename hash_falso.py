"""
Tabela Hash Manual - Implementação sem usar dicionários do Python
Implementa sondagem linear para tratamento de colisões e remoção com "túmulos"
"""


class TabelaHash:
    """
    Classe que implementa uma tabela hash manual usando lista fixa.
    Não utiliza dicionários nativos do Python.
    """

    DELETADO = "DELETADO"

    def __init__(self, tamanho=20):
        """
        Inicializa a tabela hash com tamanho fixo.

        Args:
            tamanho (int): Tamanho fixo da tabela (padrão: 20)
        """
        self.tamanho = tamanho
        self.dados = [None] * tamanho

    def _funcao_hash(self, chave):
        """
        Função hash manual: transforma uma string em um índice.
        Soma os códigos ASCII de cada caractere e faz módulo pelo tamanho.

        Args:
            chave (str): String a ser transformada em índice

        Returns:
            int: Índice calculado (0 a tamanho-1)
        """
        if not isinstance(chave, str):
            chave = str(chave)

        soma_ascii = 0
        for caractere in chave:
            soma_ascii += ord(caractere)

        indice = soma_ascii % self.tamanho
        return indice

    def inserir(self, chave):
        """
        Insere uma chave na tabela hash usando sondagem linear para colisões.

        Args:
            chave (str): Item a ser inserido

        Returns:
            tuple: (indice, houve_colisao) - índice onde foi inserido e se houve colisão
        """
        indice_inicial = self._funcao_hash(chave)
        indice = indice_inicial
        houve_colisao = False

        tentativas = 0
        while tentativas < self.tamanho:
            if self.dados[indice] is None or self.dados[indice] == self.DELETADO:
                self.dados[indice] = chave
                return (indice, houve_colisao)

            if self.dados[indice] == chave:
                return (indice, False)

            houve_colisao = True
            indice = (indice + 1) % self.tamanho
            tentativas += 1

        raise Exception("Tabela hash está cheia! Não é possível inserir mais itens.")

    def buscar(self, chave):
        """
        Busca uma chave na tabela hash.

        Args:
            chave (str): Item a ser buscado

        Returns:
            int ou None: Índice onde a chave está, ou None se não encontrada
        """
        indice_inicial = self._funcao_hash(chave)
        indice = indice_inicial
        tentativas = 0

        while tentativas < self.tamanho:
            if self.dados[indice] is None:
                return None

            if self.dados[indice] == chave:
                return indice

            indice = (indice + 1) % self.tamanho
            tentativas += 1

        return None

    def remover(self, chave):
        """
        Remove uma chave da tabela hash usando "túmulos" (DELETADO).
        Não coloca None para não quebrar a busca de itens que colidiram.

        Args:
            chave (str): Item a ser removido

        Returns:
            bool: True se removeu com sucesso, False se não encontrou
        """
        indice = self.buscar(chave)

        if indice is not None:
            self.dados[indice] = self.DELETADO
            return True

        return False

    def mostrar_tabela(self):
        """
        Mostra o estado atual da tabela hash (para debug/visualização).

        Returns:
            list: Lista representando o estado da tabela
        """
        return self.dados.copy()

    def contar_itens(self):
        """
        Conta quantos itens válidos (não None, não DELETADO) existem na tabela.

        Returns:
            int: Número de itens válidos
        """
        count = 0
        for item in self.dados:
            if item is not None and item != self.DELETADO:
                count += 1
        return count


if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DA TABELA HASH MANUAL")
    print("=" * 60)
    print()

    tabela = TabelaHash(tamanho=20)
    print(f"Tabela hash criada com tamanho fixo: {tabela.tamanho}")
    print()

    print(">>> Teste 1: Inserir 'Espada'")
    indice, colisao = tabela.inserir("Espada")
    print(f"✓ 'Espada' inserida no índice {indice}")
    if colisao:
        print("  ⚠ Colisão detectada!")
    print()

    print(">>> Teste 2: Buscar 'Espada'")
    indice_busca = tabela.buscar("Espada")
    if indice_busca is not None:
        print(f"✓ 'Espada' encontrada no índice {indice_busca}")
    else:
        print("✗ 'Espada' não encontrada")
    print()

    print(">>> Teste 3: Inserir mais itens")
    itens = ["Escudo", "Arco", "Poção", "Chave"]
    for item in itens:
        indice, colisao = tabela.inserir(item)
        status_colisao = " (COLISÃO!)" if colisao else ""
        print(f"✓ '{item}' inserido no índice {indice}{status_colisao}")
    print()

    print(">>> Teste 4: Estado da tabela")
    estado = tabela.mostrar_tabela()
    for i, item in enumerate(estado):
        if item is not None:
            status = f"[DELETADO]" if item == tabela.DELETADO else f"'{item}'"
            print(f"  Índice {i:2d}: {status}")
    print()

    print(">>> Teste 5: Remover 'Espada'")
    if tabela.remover("Espada"):
        print("✓ 'Espada' removida (marcada como DELETADO)")
    else:
        print("✗ 'Espada' não encontrada para remover")
    print()

    print(">>> Teste 6: Verificar túmulo após remoção")
    estado = tabela.mostrar_tabela()
    indice_espada = tabela._funcao_hash("Espada")
    print(f"  Índice {indice_espada} (onde 'Espada' estava): {estado[indice_espada]}")
    print()

    print(">>> Teste 7: Buscar 'Escudo' (deve funcionar mesmo com túmulo)")
    indice_escudo = tabela.buscar("Escudo")
    if indice_escudo is not None:
        print(f"✓ 'Escudo' encontrado no índice {indice_escudo}")
    else:
        print("✗ 'Escudo' não encontrado")
    print()

    print(">>> Teste 8: Inserir 'Machado' (pode usar slot do túmulo)")
    indice, colisao = tabela.inserir("Machado")
    print(f"✓ 'Machado' inserido no índice {indice}")
    if colisao:
        print("  ⚠ Colisão detectada!")
    print()

    print(">>> Teste 9: Estatísticas")
    print(f"  Itens válidos na tabela: {tabela.contar_itens()}")
    print()

    print("=" * 60)
    print("TESTES CONCLUÍDOS!")
    print("=" * 60)
