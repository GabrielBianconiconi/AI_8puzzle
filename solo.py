import copy
import random

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

def verificar_solubilidade(tabuleiro):
    """
    Verifica se o quebra-cabeça tem solução.
    Um 8-puzzle é solúvel se o número de inversões for par.
    """
    lista_plana = [num for linha in tabuleiro for num in linha if num != 0]
    inversoes = 0
    for i in range(len(lista_plana)):
        for j in range(i + 1, len(lista_plana)):
            if lista_plana[i] > lista_plana[j]:
                inversoes += 1
    return inversoes % 2 == 0

def gerar_tabuleiro_aleatorio():
    """
    Gera um tabuleiro aleatório que tenha solução.
    """
    while True:
        numeros = list(range(9))
        random.shuffle(numeros)
        tabuleiro = [numeros[i:i+3] for i in range(0, 9, 3)]
        if verificar_solubilidade(tabuleiro):
            return tabuleiro

def mover(tabuleiro, movimento):
    """
    Executa um movimento no tabuleiro.
    """
    # Encontrar posição do espaço vazio
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0:
                espaco_i, espaco_j = i, j
                break
    
    # Calcular nova posição
    if movimento == "cima" and espaco_i > 0:
        novo_i, novo_j = espaco_i - 1, espaco_j
    elif movimento == "baixo" and espaco_i < 2:
        novo_i, novo_j = espaco_i + 1, espaco_j
    elif movimento == "esquerda" and espaco_j > 0:
        novo_i, novo_j = espaco_i, espaco_j - 1
    elif movimento == "direita" and espaco_j < 2:
        novo_i, novo_j = espaco_i, espaco_j + 1
    else:
        return False  # Movimento inválido
    
    # Executar o movimento
    tabuleiro[espaco_i][espaco_j] = tabuleiro[novo_i][novo_j]
    tabuleiro[novo_i][novo_j] = 0
    
    return True

def obter_movimentos_validos(tabuleiro):
    """
    Retorna uma lista de movimentos válidos para o estado atual.
    """
    movimentos_validos = []
    
    # Encontrar posição do espaço vazio
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == 0:
                espaco_i, espaco_j = i, j
                break
    
    # Verificar movimentos possíveis
    if espaco_i > 0:
        movimentos_validos.append("cima")
    if espaco_i < 2:
        movimentos_validos.append("baixo")
    if espaco_j > 0:
        movimentos_validos.append("esquerda")
    if espaco_j < 2:
        movimentos_validos.append("direita")
    
    return movimentos_validos

def esta_resolvido(tabuleiro):
    """
    Verifica se o quebra-cabeça está resolvido.
    """
    objetivo = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    return tabuleiro == objetivo

def calcular_heuristica(tabuleiro):
    """
    Calcula a heurística do estado atual usando distância Manhattan e peças fora do lugar.
    """
    distancia_manhattan = 0
    pecas_fora_lugar = 0
    
    for i in range(3):
        for j in range(3):
            valor = tabuleiro[i][j]
            if valor != 0:
                objetivo_i, objetivo_j = (valor-1) // 3, (valor-1) % 3
                distancia_manhattan += abs(i - objetivo_i) + abs(j - objetivo_j)
                if valor != i*3 + j + 1:
                    pecas_fora_lugar += 1
    
    return distancia_manhattan + pecas_fora_lugar

def jogar():
    """
    Função principal do jogo manual.
    """
    print("\n=== MODO JOGO MANUAL ===")
    print("Embaralhando tabuleiro...")
    tabuleiro = gerar_tabuleiro_aleatorio()
    
    # Mapeamento de comandos
    comandos = {
        'w': 'cima',
        's': 'baixo',
        'a': 'esquerda',
        'd': 'direita'
    }
    
    movimentos = 0
    
    while not esta_resolvido(tabuleiro):
        limpar_tela()
        print("\n=== QUEBRA-CABEÇA 8-PUZZLE ===")
        print("Organize os números em ordem crescente:")
        imprimir_tabuleiro(tabuleiro)
        
        print(f"\nHeurística atual: {calcular_heuristica(tabuleiro)}")
        print("\nMovimentos válidos:", ", ".join(obter_movimentos_validos(tabuleiro)))
        print("\nControles: [W] Cima, [S] Baixo, [A] Esquerda, [D] Direita, [Q] Sair")
        print(f"Movimentos realizados: {movimentos}")
        
        comando = input("\nDigite seu comando: ").lower()
        
        if comando == 'q':
            print("Saindo do jogo...")
            return
        
        elif comando in comandos:
            movimento = comandos[comando]
            if mover(tabuleiro, movimento):
                movimentos += 1
            else:
                input("Movimento inválido! Pressione Enter para continuar...")
        
        else:
            input("Comando inválido! Pressione Enter para continuar...")
    
    # Quebra-cabeça resolvido
    limpar_tela()
    print("\n=== PARABÉNS! ===")
    print("Você resolveu o quebra-cabeça em", movimentos, "movimentos!")
    imprimir_tabuleiro(tabuleiro)
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    jogar()