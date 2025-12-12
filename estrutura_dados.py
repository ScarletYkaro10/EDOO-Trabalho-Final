#### 3. No arquivo `estrutura_dados.py` (Placebo para você não travar)
##Como o Wesley ainda não terminou, cole esse código **temporário** só para o seu `main.py` não dar erro quando você começar a codar a tela. Quando o Wesley terminar, ele apaga isso e cola a lógica real dele.

##```python
# ARQUIVO TEMPORÁRIO DO WESLEY
# TODO: Wesley, substituir isso pela implementação real da Hash com Colisão!

class TabelaHash:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho 

    def inserir(self, chave, valor):
        print(f"SIMULAÇÃO: Inserindo {chave}")
        return True

    def remover(self, chave):
        print(f"SIMULAÇÃO: Removendo {chave}")
        return True
        
    def buscar(self, chave):
        return None