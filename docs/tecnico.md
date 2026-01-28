# 🛠️ Especificações Técnicas - QuizMaster

Este documento descreve a arquitetura e as dependências técnicas do projeto.

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.x
* **Interface Gráfica:** `customtkinter` (Modernização da biblioteca Tkinter).
* **Sons:** `winsound` (Nativo do Windows para feedbacks sonoros).
* **Persistência de Dados:** Arquivos de texto (.txt) para o ranking local.

## 🏗️ Estrutura de Dados
O quiz opera baseado em uma lista de tuplas estruturada da seguinte forma:
- `(pergunta, [opções], resposta_correta)`

## ⚙️ Funcionalidades Implementadas
1.  **Sistema de Timer:** Utiliza o método `.after()` do Tkinter para contagem regressiva não-bloqueante.
2.  **Lógica de Ranking:** * Leitura/Escrita de arquivos na pasta `/ranking`.
    * Ordenação automática por score (Top 3).
3.  **Interface Adaptativa:** Mudança de cores dinâmica para indicar acertos (Verde) ou erros (Vermelho).

## 📥 Instalação de Dependências
Para rodar o projeto, instale o CustomTkinter:
```bash
pip install customtkinter
