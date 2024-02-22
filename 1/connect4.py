import math
import random
import time

menor_tempo = 1
maior_tempo = 0

def escolher_modo_jogo():
    print("\033[96m1. Jogador vs. Computador\033[0m")
    print("\033[96m2. Computador vs Computador\033[0m")

    modo_jogo = input("\033[96mModo de jogo: \033[0m")

    print()

    if modo_jogo == "1" or modo_jogo == "2":
        return int(modo_jogo)

    return 1

def primeiro_jogador(modo_jogo):
    if modo_jogo == 2:
        primeiro_pc = input("\033[96mQual computador deve ir primeiro? (X/O) \033[0m").upper()
        return primeiro_pc if (primeiro_pc == "X" or primeiro_pc == "O") else "X"

    jogador_humano_primeiro = True if input("\033[96mDeseja jogar primeiro? (s/n) \033[0m").lower() == "s" else False
    return "X" if jogador_humano_primeiro else "O"

def anunciar_primeiro_jogador(modo_jogo, jogador):
    print()
    if modo_jogo == 1:
        if jogador == "X":
            print("\033[1;34mJogador irá primeiro...\033[0m")
        if jogador == "O":
            print("\033[1;31mComputador irá primeiro...\033[0m")
        print("\033[96mBoa sorte!\033[0m")
    else:
        if jogador == "X":
            print(f"\033[1;34mComputador {jogador} irá primeiro...\033[0m")
        if jogador == "O":
            print(f"\033[1;31mComputador {jogador} irá primeiro...\033[0m")
    print()

def proximo_jogador(jogador):
    return "O" if jogador == "X" else "X"

def exibir_tabuleiro(tabuleiro, highlight = None):
    for linha in range(6):
        print("|", end = "")
        for coluna in range(7):
            cel = tabuleiro[linha][coluna]
            if highlight and (linha, coluna) in highlight:
                print(f" \033[1;32m{cel}\033[0m |", end = "")
            elif cel == "X":
                print(f" \033[1;34m{cel}\033[0m |", end = "")
            elif cel == "O":
                print(f" \033[1;31m{cel}\033[0m |", end = "")
            else:
                print(f" {cel} |", end = "")
        print("\n" + "|---" * 7)
    print("  0   1   2   3   4   5   6\n")

def eh_vencedor(tabuleiro, jogador):
    for linha in range(6):
        for coluna in range(4):
            if all(tabuleiro[linha][coluna+i] == jogador for i in range(4)):
                return [(linha, coluna+i) for i in range(4)]

    for coluna in range(7):
        for linha in range(3):
            if all(tabuleiro[linha+i][coluna] == jogador for i in range(4)):
                return [(linha+i, coluna) for i in range(4)]

    for linha in range(3):
        for coluna in range(4):
            if all(tabuleiro[linha+i][coluna+i] == jogador for i in range(4)):
                return [(linha+i, coluna+i) for i in range(4)]

            if all(tabuleiro[linha+i][coluna+3-i] == jogador for i in range(4)):
                return [(linha+i, coluna+3-i) for i in range(4)]

    return None

def game_over(tabuleiro_estado):
    return eh_vencedor(tabuleiro_estado, "X") or eh_vencedor(tabuleiro_estado, "O") or len(get_colunas_validas(tabuleiro_estado)) == 0

def anunciar_resultado_jogo(tabuleiro_estado, modo_jogo, tempo_inicio):
    vencedor = ""
    placeholder_x = "Você"
    placeholder_o = "O computador"

    if modo_jogo == 2:
        placeholder_x = "Computador X"
        placeholder_o = "Computador O"

    if eh_vencedor(tabuleiro_estado, "X"):
        vencedor = "X"
        print(f"\033[1;34m{placeholder_x} venceu!\033[0m")
    elif eh_vencedor(tabuleiro_estado, "O"):
        vencedor = "O"
        print(f"\033[1;31m{placeholder_o} venceu!\033[0m")
    else:
        print("O jogo terminou em empate!")

    if vencedor:
        highlight_posicoes = eh_vencedor(tabuleiro_estado, vencedor)
        exibir_tabuleiro(tabuleiro_estado, highlight_posicoes)
    
    print(f"\033[96mO jogo teve duração total de\033[0m \033[92m{time.time() - tempo_inicio}\033[0m \033[96msegundos\033[0m")
    print(f"\033[96mMaior duração jogada pc: \033[0m \033[92m{maior_tempo}\033[0m \033[96msegundos\033[0m")
    print(f"\033[96mMenor duração jogada pc: \033[0m \033[92m{menor_tempo}\033[0m \033[96msegundos\033[0m")

def coluna_valida(tabuleiro_estado, coluna):
    return 0 <= coluna < 7 and tabuleiro_estado[0][coluna] == 0

def get_colunas_validas(tabuleiro_estado):
    return [coluna for coluna in range(7) if coluna_valida(tabuleiro_estado, coluna)]

def primeira_jogada_aleatoria():
    aleatorio = input("\033[96mAleatorizar primeira jogada? (s/n) \033[0m")
    return True if aleatorio.lower() == "s" else False

def vazia(lista):
    return len(lista) == 0

def num_aleatorio():
    return random.randint(0, 6)

def jogador_humano_escolher(tabuleiro_estado):
    try:
        coluna = int(input("\033[1;34mEscolha uma coluna (0-6):\033[0m "))
        if coluna_valida(tabuleiro_estado, coluna):
            return coluna
        else:
            print("\033[1;34mColuna inválida. Tente novamente.\033[0m")
            return jogador_humano_escolher(tabuleiro_estado)
    except ValueError:
        print("\033[1;34mEntrada inválida. Tente novamente.\033[0m")
        return jogador_humano_escolher(tabuleiro_estado)

def pc_escolher(tabuleiro_estado, profundidade):
    global menor_tempo
    global maior_tempo
    tempo_antes_minmax = time.time()
    coluna = minmax_alphabeta(tabuleiro_estado, profundidade, -math.inf, math.inf, True)[0]
    tempo_total_minmax = time.time() - tempo_antes_minmax
    if tempo_total_minmax < menor_tempo:
        menor_tempo = tempo_total_minmax
    if tempo_total_minmax > maior_tempo:
        maior_tempo = tempo_total_minmax
    return (coluna, tempo_total_minmax)

def get_escolha_coluna(tabuleiro_estado, jogador, profundidade, modo_jogo, lista_jogadas_predeterminadas):
    if not vazia(lista_jogadas_predeterminadas):
        coluna = lista_jogadas_predeterminadas.pop()
        print(f"\033[96mJogada predeterminada coluna\033[0m \033[93m{coluna}\033[0m")
        return coluna

    if modo_jogo == 2:
        print(f"\033[1;34mComputador {jogador} está pensando...\033[0m")
        coluna, tempo = pc_escolher(tabuleiro_estado, profundidade)
        print(f"\033[1;34mComputador {jogador} escolheu coluna\033[0m \033[93m{coluna}\033[0m em \033[92m{tempo}\033[0m \033[1;34msegundos\033[0m")
        return coluna

    if jogador == "X":
        return jogador_humano_escolher(tabuleiro_estado)

    print("\033[1;31mComputador está pensando...\033[0m")
    coluna, tempo = pc_escolher(tabuleiro_estado, profundidade)
    print(f"\033[1;34mComputador escolheu coluna\033[0m \033[93m{coluna}\033[0m em \033[92m{tempo}\033[0m \033[1;34msegundos\033[0m")
    return coluna

def atualizar_tabuleiro(tabuleiro_estado, proxima_escolha_coluna, jogador):
    novo_tabuleiro_estado = [linha.copy() for linha in tabuleiro_estado]

    for linha in range(5, -1, -1): # começa ultima linha de cima e desce ate linha 0
        if novo_tabuleiro_estado[linha][proxima_escolha_coluna] == 0:
            novo_tabuleiro_estado[linha][proxima_escolha_coluna] = jogador
            break

    return novo_tabuleiro_estado

def avaliar(janela, jogador):
    pontuacao = 0
    oponente = "X" if jogador == "O" else "O"

    if janela.count(jogador) == 4:
        pontuacao += 100
    elif janela.count(jogador) == 3 and janela.count(0) == 1:
        pontuacao += 5
    elif janela.count(jogador) == 2 and janela.count(0) == 2:
        pontuacao += 2

    if janela.count(oponente) == 3 and janela.count(0) == 1:
        pontuacao -= 4
    
    return pontuacao

def heuristica_valor(tabuleiro_estado, jogador):
    pontuacao = 0

    # linhas horizontais
    for linha in range(6):
        for coluna in range(4):
            janela = [tabuleiro_estado[linha][coluna + i] for i in range(4)]
            pontuacao += avaliar(janela, jogador)

    # colunas verticais
    for coluna in range(7):
        for linha in range(3):
            janela = [tabuleiro_estado[linha + i][coluna] for i in range(4)]
            pontuacao += avaliar(janela, jogador)

    # diagonais (/)
    for linha in range(3):
        for coluna in range(4):
            janela = [tabuleiro_estado[linha + i][coluna + i] for i in range(4)]
            pontuacao += avaliar(janela, jogador)

    # diagonais (\)
    for linha in range(3):
        for coluna in range(3, 7):
            janela = [tabuleiro_estado[linha + i][coluna - i] for i in range(4)]
            pontuacao += avaliar(janela, jogador)

    return pontuacao

def minmax_alphabeta(tabuleiro_estado, profundidade, alpha, beta, max_jogador):
    colunas_validas = get_colunas_validas(tabuleiro_estado)
    no_terminal = game_over(tabuleiro_estado)

    if profundidade == 0 or no_terminal:
        if no_terminal:
            if eh_vencedor(tabuleiro_estado, "O"):
                return (None, 100000000000000)
            elif eh_vencedor(tabuleiro_estado, "X"):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, heuristica_valor(tabuleiro_estado, "O"))

    if max_jogador:
        valor = -math.inf
        coluna = random.choice(colunas_validas)

        for col in colunas_validas:
            novo_tabuleiro = atualizar_tabuleiro(tabuleiro_estado, col, "O")
            novo_valor = minmax_alphabeta(novo_tabuleiro, profundidade - 1, alpha, beta, False)[1]
            
            if novo_valor > valor:
                valor = novo_valor
                coluna = col
            
            alpha = max(alpha, valor)
            
            if alpha >= beta:
                break
        return coluna, valor

    else: # minimizar
        valor = math.inf
        coluna = random.choice(colunas_validas)

        for col in colunas_validas:
            novo_tabuleiro = atualizar_tabuleiro(tabuleiro_estado, col, "X")
            novo_valor = minmax_alphabeta(novo_tabuleiro, profundidade - 1, alpha, beta, True)[1]

            if novo_valor < valor:
                valor = novo_valor
                coluna = col
            
            beta = min(beta, valor)

            if alpha >= beta:
                break
        return coluna, valor

def main():
    tabuleiro = [[0] * 7 for _ in range(6)]
    profundidade = 4
    modo_jogo = escolher_modo_jogo()
    jogador = primeiro_jogador(modo_jogo)
    lista_jogadas_predeterminadas = []

    if primeira_jogada_aleatoria():
        lista_jogadas_predeterminadas.append(num_aleatorio())
    
    anunciar_primeiro_jogador(modo_jogo, jogador)

    tempo_inicio = time.time()
    while True:
        if game_over(tabuleiro):
            break

        exibir_tabuleiro(tabuleiro)

        prox_jogada = get_escolha_coluna(tabuleiro, jogador, profundidade, modo_jogo, lista_jogadas_predeterminadas)

        tabuleiro = atualizar_tabuleiro(tabuleiro, prox_jogada, jogador)

        jogador = proximo_jogador(jogador)

    anunciar_resultado_jogo(tabuleiro, modo_jogo, tempo_inicio)

main()