import heapq
import copy
import random
import time
import os
import sys

class Estado:
    """
    Classe que representa um estado do quebra-cabeça 8-puzzle.
    Um estado é representado por uma matriz 3x3 onde 0 representa o espaço vazio.
    """
    def __init__(self, tabuleiro, pai=None, movimento=None, profundidade=0, custo=0):
        self.tabuleiro = tabuleiro
        self.pai = pai
        self.movimento = movimento  # Movimento que levou a este estado
        self.profundidade = profundidade  # Profundidade na árvore de busca
        self.custo = custo  # Custo para chegar a este estado (g(n))
        
        # Calcular a posição do espaço vazio (0)
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == 0:
                    self.espaco_vazio = (i, j)
                    break
        
        # Calcular valor de heurística h(n)
        self.heuristica = self.calcular_heuristica()
        
        # Função de avaliação f(n) = g(n) + h(n)
        self.avaliacao = self.custo + self.heuristica
    
    def calcular_heuristica(self):
        """
        Calcula a heurística do estado atual. Usamos duas heurísticas combinadas:
        1. Distância Manhattan: soma das distâncias de cada peça até sua posição objetivo
        2. Número de peças fora do lugar
        
        Esta é uma heurística admissível para o A*, pois nunca superestima o custo real.
        """
        distancia_manhattan = 0
        pecas_fora_lugar = 0
        
        # Estado objetivo: [[1,2,3], [4,5,6], [7,8,0]]
        for i in range(3):
            for j in range(3):
                valor = self.tabuleiro[i][j]
                if valor != 0:
                    # Calcular posição objetivo do valor
                    objetivo_i, objetivo_j = (valor-1) // 3, (valor-1) % 3
                    
                    # Distância Manhattan = |x1 - x2| + |y1 - y2|
                    distancia_manhattan += abs(i - objetivo_i) + abs(j - objetivo_j)
                    
                    # Verificar se a peça está fora do lugar
                    if valor != i*3 + j + 1 and not (i == 2 and j == 2 and valor == 0):
                        pecas_fora_lugar += 1
        
        # Combinar as heurísticas (damos mais peso à distância Manhattan)
        return distancia_manhattan + pecas_fora_lugar
    
    def __lt__(self, outro):
        """
        Comparação para a fila de prioridade do A*.
        """
        return self.avaliacao < outro.avaliacao
    
    def __eq__(self, outro):
        """
        Dois estados são iguais se seus tabuleiros são iguais.
        """
        return self.tabuleiro == outro.tabuleiro
    
    def __hash__(self):
        """
        Hash para usar o estado como chave em dicionários.
        """
        return hash(str(self.tabuleiro))
    
    def gerar_sucessores(self):
        """
        Gera todos os estados sucessores possíveis a partir do estado atual.
        Um sucessor é obtido movendo o espaço vazio para cima, baixo, esquerda ou direita.
        """
        sucessores = []
        i, j = self.espaco_vazio
        
        # Possíveis movimentos: cima, baixo, esquerda, direita
        movimentos = [
            ("cima", (-1, 0)), 
            ("baixo", (1, 0)), 
            ("esquerda", (0, -1)), 
            ("direita", (0, 1))
        ]
        
        for nome_movimento, (di, dj) in movimentos:
            novo_i, novo_j = i + di, j + dj
            
            # Verificar se o movimento é válido (dentro dos limites do tabuleiro)
            if 0 <= novo_i < 3 and 0 <= novo_j < 3:
                # Criar uma cópia do tabuleiro
                novo_tabuleiro = copy.deepcopy(self.tabuleiro)
                
                # Mover o espaço vazio (trocar os valores)
                novo_tabuleiro[i][j] = novo_tabuleiro[novo_i][novo_j]
                novo_tabuleiro[novo_i][novo_j] = 0
                
                # Criar um novo estado com o novo tabuleiro
                sucessor = Estado(
                    novo_tabuleiro, 
                    pai=self, 
                    movimento=nome_movimento, 
                    profundidade=self.profundidade + 1,
                    custo=self.profundidade + 1  # g(n) = profundidade
                )
                
                sucessores.append(sucessor)
        
        return sucessores
    
    def esta_resolvido(self):
        """
        Verifica se o estado atual é o estado objetivo (quebra-cabeça resolvido).
        """
        objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        return self.tabuleiro == objetivo
    
    def imprimir(self):
        """
        Imprime o tabuleiro de forma legível.
        """
        print("-" * 13)
        for i in range(3):
            print("| ", end="")
            for j in range(3):
                if self.tabuleiro[i][j] == 0:
                    print("  | ", end="")
                else:
                    print(f"{self.tabuleiro[i][j]} | ", end="")
            print()
            print("-" * 13)

def a_estrela(estado_inicial):
    """
    Implementação do algoritmo A* para encontrar a solução do quebra-cabeça.
    """
    # Fila de prioridade para os estados a serem explorados
    abertos = []
    heapq.heappush(abertos, estado_inicial)
    
    # Conjunto de estados já visitados
    fechados = set()
    
    # Contadores para estatísticas
    nodos_expandidos = 0
    max_nodos_memoria = 1
    
    # Iniciar temporizador
    inicio = time.time()
    
    print("\nIniciando busca A*...")
    print(f"Heurística inicial: {estado_inicial.heuristica}")
    
    while abertos:
        # Pegar o estado com menor valor de avaliação f(n)
        atual = heapq.heappop(abertos)
        
        # Verificar se chegamos ao objetivo
        if atual.esta_resolvido():
            fim = time.time()
            
            # Reconstruir o caminho
            caminho = []
            estado = atual
            while estado.pai:
                caminho.append(estado)
                estado = estado.pai
            caminho.append(estado_inicial)  # Adicionar o estado inicial
            caminho.reverse()  # Inverter para obter do início ao fim
            
            return {
                "sucesso": True,
                "caminho": caminho,
                "nodos_expandidos": nodos_expandidos,
                "max_nodos_memoria": max_nodos_memoria,
                "tempo": fim - inicio
            }
        
        # Adicionar aos fechados para não revisitar
        fechados.add(atual)
        nodos_expandidos += 1
        
        # A cada 1000 nodos expandidos, mostrar progresso
        if nodos_expandidos % 1000 == 0:
            print(f"Nodos expandidos: {nodos_expandidos}, Heurística atual: {atual.heuristica}")
        
        # Gerar sucessores
        for sucessor in atual.gerar_sucessores():
            # Verificar se já visitamos este estado
            if sucessor in fechados:
                continue
                
            # Verificar se já está na fila aberta com custo menor
            adicionar = True
            for i, estado in enumerate(abertos):
                if estado == sucessor and estado.avaliacao <= sucessor.avaliacao:
                    adicionar = False
                    break
            
            if adicionar:
                heapq.heappush(abertos, sucessor)
                
        # Atualizar máximo de nodos em memória
        max_nodos_memoria = max(max_nodos_memoria, len(abertos) + len(fechados))
        
        # Verificar se a busca está demorando muito
        if time.time() - inicio > 60:  # Limite de 60 segundos
            return {
                "sucesso": False,
                "mensagem": "Tempo limite excedido",
                "nodos_expandidos": nodos_expandidos,
                "max_nodos_memoria": max_nodos_memoria,
                "tempo": time.time() - inicio
            }
    
    # Se saímos do loop sem encontrar solução
    return {
        "sucesso": False,
        "mensagem": "Não foi possível encontrar uma solução",
        "nodos_expandidos": nodos_expandidos,
        "max_nodos_memoria": max_nodos_memoria,
        "tempo": time.time() - inicio
    }

def verificar_solubilidade(tabuleiro):
    """
    Verifica se o quebra-cabeça tem solução.
    Um 8-puzzle é solúvel se o número de inversões for par.
    """
    # Converter o tabuleiro para uma lista plana, ignorando o espaço vazio (0)
    lista_plana = [num for linha in tabuleiro for num in linha if num != 0]
    
    # Contar inversões
    inversoes = 0
    for i in range(len(lista_plana)):
        for j in range(i + 1, len(lista_plana)):
            if lista_plana[i] > lista_plana[j]:
                inversoes += 1
    
    # O quebra-cabeça é solúvel se o número de inversões for par
    return inversoes % 2 == 0

def gerar_tabuleiro_aleatorio():
    """
    Gera um tabuleiro aleatório que tenha solução.
    """
    while True:
        # Criar uma lista com os números de 0 a 8
        numeros = list(range(9))
        
        # Embaralhar os números
        random.shuffle(numeros)
        
        # Converter para formato de matriz 3x3
        tabuleiro = [numeros[i:i+3] for i in range(0, 9, 3)]
        
        # Verificar se tem solução
        if verificar_solubilidade(tabuleiro):
            return tabuleiro

def limpar_tela():
    """
    Limpa a tela do terminal.
    """
    print('\033c', end='')

def imprimir_tabuleiro(tabuleiro):
    """
    Imprime o tabuleiro de forma legível.
    """
    print("-" * 13)
    for i in range(3):
        print("| ", end="")
        for j in range(3):
            if tabuleiro[i][j] == 0:
                print("  | ", end="")
            else:
                print(f"{tabuleiro[i][j]} | ", end="")
        print()
        print("-" * 13)

def resolver_com_a_estrela(tabuleiro):
    """
    Resolve o quebra-cabeça usando o algoritmo A* e mostra o processo passo a passo.
    """
    # Criar estado inicial
    estado_inicial = Estado(copy.deepcopy(tabuleiro))
    
    print("\nResolvendo com A*...")
    print("Estado inicial:")
    estado_inicial.imprimir()
    print(f"Heurística inicial: {estado_inicial.heuristica}")
    
    # Executar A*
    resultado = a_estrela(estado_inicial)
    
    if resultado["sucesso"]:
        print("\n=== SOLUÇÃO ENCONTRADA! ===")
        print(f"Passos: {len(resultado['caminho']) - 1}")
        print(f"Nodos expandidos: {resultado['nodos_expandidos']}")
        print(f"Máximo de nodos em memória: {resultado['max_nodos_memoria']}")
        print(f"Tempo: {resultado['tempo']:.2f} segundos")
        
        for i, estado in enumerate(resultado["caminho"]):
            print(f"\nPasso {i} de {len(resultado['caminho']) - 1}")
            if i > 0:
                print(f"Movimento: {estado.movimento}")
            estado.imprimir()
            print(f"Heurística: {estado.heuristica}")
            print(f"Custo (g): {estado.custo}")
            print(f"Avaliação (f = g + h): {estado.avaliacao}")
            
            if sys.stdin.isatty() and i < len(resultado["caminho"]) - 1:
                input("Pressione Enter para o próximo passo...")
        
        print("\nQuebra-cabeça resolvido com sucesso!")
    else:
        print("\nNão foi possível encontrar uma solução.")
        print(f"Motivo: {resultado['mensagem']}")
        print(f"Nodos expandidos: {resultado['nodos_expandidos']}")
        print(f"Máximo de nodos em memória: {resultado['max_nodos_memoria']}")
        print(f"Tempo: {resultado['tempo']:.2f} segundos")

if __name__ == "__main__":
    print("\n=== DEMONSTRAÇÃO DO ALGORITMO A* ===")
    print("Gerando quebra-cabeça aleatório...")
    tabuleiro = gerar_tabuleiro_aleatorio()
    
    print("\nEstado inicial:")
    imprimir_tabuleiro(tabuleiro)

    if sys.stdin.isatty():
        input("\nPressione Enter para iniciar a resolução com A*...")
    
    resolver_com_a_estrela(tabuleiro)