# RPG Gerente de Inventário - Trabalho Final EDOO

**Alunos:**
- Gabriel Ykaro Rodrigues da Silva
- Wesley Julio

**Disciplina:** Estrutura de Dados Orientada a Objetos
**Data de Entrega:** 12/2025

## 1. Descrição do Projeto
Este projeto é uma simulação interativa de um inventário de RPG. O sistema gerencia a inserção, busca e remoção de itens (como espadas, poções e escudos) dentro de uma "mochila" com capacidade limitada. O projeto foi desenvolvido em **Python** utilizando a biblioteca **Pygame** para a interface gráfica.

## 2. Estrutura de Dados Utilizada
Utilizamos uma **Tabela Hash (Hash Table)** com tratamento de colisão por **Sondagem Linear (Linear Probing)**.
- **Justificativa:** A Tabela Hash foi escolhida pois permite acesso aos itens com complexidade média de O(1) (constante), o que é ideal para inventários de jogos onde o acesso rápido ao equipamento é crucial.
- **Implementação:** A estrutura foi implementada manualmente ("na raça"), sem uso de dicionários prontos do Python, demonstrando o cálculo de hash e a lógica de rehash em caso de colisão.

## 3. Instruções de Execução
Necessário ter Python e Pygame instalados.

1. Instale as dependências:
   ```bash
   pip install pygame