# 🔍 Resolução do 8-Puzzle com Algoritmo A*

Este projeto implementa o algoritmo **A\*** para resolver o clássico quebra-cabeça **8-Puzzle**, utilizando heurísticas admissíveis (distância de Manhattan e peças fora do lugar). O código é dividido em duas abordagens: uma **automática** controlada por IA e uma **manual**, onde o usuário resolve o puzzle.

## 📁 Estrutura do Projeto

```
├── puzzle.py   → Versão automática com IA (busca A*)
├── solo.py     → Versão manual (resolução pelo jogador)
```

## 🤖 `puzzle.py` – Resolução automática com IA

Neste arquivo, o jogo é resolvido automaticamente utilizando o **algoritmo A\***.  
A IA utiliza uma **fila de prioridade (heap)** para sempre escolher o estado mais promissor com base na função de avaliação:

[Collab](https://colab.research.google.com/drive/1c2x14WEmyIQRnmxII3-CEuzrTBBP9p0P?usp=sharing)

```
f(n) = g(n) + h(n)
```
- `g(n)`: custo do caminho até o estado atual
- `h(n)`: heurística estimada até o objetivo
  - Soma da **distância de Manhattan**
  - Número de **peças fora do lugar**

O algoritmo mostra passo a passo a resolução e estatísticas como:
- Tempo de execução
- Número de nós expandidos
- Memória máxima utilizada

## 🎮 `solo.py` – Jogo manual

Neste modo, o usuário interage com o quebra-cabeça manualmente, movendo as peças com comandos.  
Ideal para quem deseja testar suas habilidades de resolução lógica e comparar com a solução da IA.

[Collab](https://colab.research.google.com/drive/1cAcPTmUZLV-vKM4XkWDtjQV0yX2LDy2X?usp=sharing)

## 🧠 Heurísticas utilizadas

1. **Distância de Manhattan:**  
   Soma das distâncias horizontais e verticais que cada peça está da sua posição correta.

2. **Peças fora do lugar:**  
   Contagem de peças que não estão na posição correta.

A combinação dessas heurísticas permite uma busca eficiente, guiando o A\* pelas melhores decisões.

## 👨‍💻 Integrantes

| Nome                              | RA           |
|-----------------------------------|--------------|
| Gabriel Bianconi                  | 20.00822-8   |
| Carlos Alberto Matias da Costa   | 20.01308-6   |
| Bruno Augusto Lopes Fevereiro     | 20.02194-0   |

## 📌 Como executar

Certifique-se de estar com o Python 3 instalado.  
Clone o projeto e execute com:

```bash
python puzzle.py  # Executa IA com A*
python solo.py    # Joga manualmente
```

## ✅ Exemplo de Saída da IA

```
Passos: 12
Nodos expandidos: 130
Máximo de nodos em memória: 92
Tempo: 0.42 segundos
```

## 📃 Licença

Este projeto é acadêmico e foi desenvolvido para um projeto da disciplina de Inteligência Artificial do Instituto Mauá de Tecnologia.
