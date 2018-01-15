# -*- coding: utf-8 -*-
import sys
from collections import deque
from heapq import heappop, heappush
import math
import os
from time import sleep
import time

######################################
#                                    #
#    Função para ler o lerArquivo    #
#                                    #
######################################
def lerArquivo(fileName):

	arquivo = open(fileName, 'r')

	labirinto = []

	linhas = 0
	colunas = 0
	i = 0

	for linha in arquivo:
		if(i == 0):
			linhas = int(linha.split(" ")[0])
			colunas = int(linha.split(" ")[1])
			i += 1
		else:
			labirinto.append(linha)
			i += 1

	arquivo.close()

	return (linhas, colunas), labirinto

#########################################################################
#                                                                       #
#    Função para achar o lugar onde esta o objetivo e retorna o ponto   #
#                                                                       #
#########################################################################
def posicaoObjetivo(labirinto):

	i=0

	for linha in labirinto:
		objetivo = linha.find("$")
		if(objetivo > -1):
			objetivoL = i
			objetivoC = objetivo
		i += 1

	return objetivoL, objetivoC

#######################################################################
#                                                                     #
#    Função para achar o lugar onde esta o inicio e retorna o ponto   #
#                                                                     #
#######################################################################
def posicaoInicio(labirinto):

	i=0

	for linha in labirinto:
		inicio = linha.find("#")
		if(inicio > -1):
			inicioL = i
			inicioC = inicio
		i += 1

	return inicioL, inicioC


######################################################
#                                                    #
#    Função para converter o labirinto em um grafo   #
#                                                    #
######################################################
def corverteGrafo(labirinto):

    altura = len(labirinto)
    largura = len(labirinto[1]) - 1

    grafo = {(i, j): [] for j in range(largura) for i in range(altura) if not (labirinto[i][j] == "-")}

    # Direções
    # 1 - Norte
    # 2 - Leste
    # 3 - Sul
    # 4 - Oeste
    # 5 - Nordeste
    # 6 - Sudeste
	# 7 - Sudoeste
	# 8 - Noroeste

    for linha, coluna in grafo.keys():
        if linha < altura - 1 and not (labirinto[linha + 1][coluna]  == "-"):
            grafo[(linha, coluna)].append(("3", (linha + 1, coluna)))
            grafo[(linha + 1, coluna)].append(("1", (linha, coluna)))
        if coluna < largura - 1 and not (labirinto[linha][coluna + 1]  == "-"):
            grafo[(linha, coluna)].append(("2", (linha, coluna + 1)))
            grafo[(linha, coluna + 1)].append(("4", (linha, coluna)))
        if linha < altura - 1 and coluna < largura - 1 and not (labirinto[linha - 1][coluna + 1]  == "-") and linha > 0 and coluna >= 0:
            grafo[(linha, coluna)].append(("5", (linha - 1, coluna + 1)))
            grafo[(linha - 1, coluna + 1)].append(("7", (linha, coluna)))
        if coluna < largura - 1 and linha < altura - 1 and not (labirinto[linha + 1][coluna + 1]  == "-") and linha >= 0 and coluna >= 0:
            grafo[(linha, coluna)].append(("6", (linha + 1, coluna + 1)))
            grafo[(linha + 1, coluna + 1)].append(("8", (linha, coluna)))
    return grafo

####################################################################
#                                                                  #
#    Função para mostrar os pontos que o caminho final percorreu   #
#                                                                  #
####################################################################
def converteSaida(caminho):
	lista = []
	tam = len(caminho)

	posicao = posicaoInicio(labirinto)
	lista.append(posicao)

	for i in range(0,tam):
		direcao = caminho[i]
		if direcao == "1":
			posicao = list(posicao)
			posicao[0] = posicao[0]-1
			posicao = tuple(posicao)
		elif direcao == "3":
			posicao = list(posicao)
			posicao[0] = posicao[0]+1
			posicao = tuple(posicao)
		elif direcao == "2":
			posicao = list(posicao)
			posicao[1] = posicao[1]+1
			posicao = tuple(posicao)
		elif direcao == "4":
			posicao = list(posicao)
			posicao[1] = posicao[1]-1
			posicao = tuple(posicao)
		elif direcao == "5":
			posicao = list(posicao)
			posicao[0] = posicao[0]-1
			posicao[1] = posicao[1]+1
			posicao = tuple(posicao)
		elif direcao == "6":
			posicao = list(posicao)
			posicao[0] = posicao[0]+1
			posicao[1] = posicao[1]+1
			posicao = tuple(posicao)
		elif direcao == "7":
			posicao = list(posicao)
			posicao[0] = posicao[0]+1
			posicao[1] = posicao[1]-1
			posicao = tuple(posicao)
		elif direcao == "8":
			posicao = list(posicao)
			posicao[0] = posicao[0]-1
			posicao[1] = posicao[1]-1
			posicao = tuple(posicao)
		
		lista.append(posicao)

	return lista

################################################
#                                              #
#    Função que imprime o caminho percorrido   #
#                                              #
################################################
def imprimeSaida(caminho):
	caminho = converteSaida(caminho)
	print "Caminho até a solução:"
	print caminho

#######################################################################
#                                                                     #
#    Função para mostrar o caminho percorrido pelo algoritmo          #
#                                                                     #
#######################################################################
def passoApasso(labirinto, caminho):
	linhas = len(labirinto)
	colunas = len(labirinto[0])-1

	caminho = converteSaida(caminho)

	os.system('cls' if os.name == 'nt' else 'clear')
	
	for k in range (0, len(caminho)):
		for i in range(0, linhas):
			ln = ""
			for j in range (0, colunas):
				if i == caminho[k][0] and j == caminho[k][1]:
					ln += "0"
				else:
					ln += labirinto[i][j]
			print ln
		sleep(0.5)
		os.system('cls' if os.name == 'nt' else 'clear')

################################
#                              #
#    Função do algoritmo BFS   #
#                              #
################################
def bfs(labirinto):

    inicio, objetivo = posicaoInicio(labirinto), posicaoObjetivo(labirinto)
    fila = deque([("", inicio)])
    visitado = set()
    grafo = corverteGrafo(labirinto)
    Expansoes = 0

    while fila:
        caminho, atual = fila.popleft()
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminho)
        	return caminho
        if atual in visitado:
        	continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
            fila.append((caminho + direcao, vizinho))
            Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"

################################
#                              #
#    Função do algoritmo DFS   #
#                              #
################################
def dfs(labirinto):

    inicio, objetivo = posicaoInicio(labirinto), posicaoObjetivo(labirinto)
    pilha = deque([("", inicio)])
    visitado = set()
    grafo = corverteGrafo(labirinto)
    Expansoes = 0

    while pilha:
        caminho, atual = pilha.pop()
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminho)
        	return caminho
        if atual in visitado:
            continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
            pilha.append((caminho + direcao, vizinho))
            Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"

#######################################
#                                     #
#   Heuristicas para os algoritmos    #
#                                     #
#######################################
def heuristicas(atual, objetivo, opt):
	if opt == 1:
		return (math.sqrt(math.pow(atual[0] - objetivo[0],2) + math.pow(atual[1] - objetivo[1],2)))
	if opt == 2:
		return (abs(atual[0] - objetivo[0]) + abs(atual[1] - objetivo[1]))

#######################################
#                                     #
#    Função do algoritmo Best FIrst   #
#                                     #
#######################################
def bestFirst(labirinto):

    inicio, objetivo = posicaoInicio(labirinto), posicaoObjetivo(labirinto)
    pr_queue = []
    heappush(pr_queue, (0, 0, "", inicio))

    visitado = set()
    grafo = corverteGrafo(labirinto)
    Expansoes = 0

    while pr_queue:
        _, custo, caminho, atual = heappop(pr_queue)
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminho)
        	return caminho
        if atual in visitado:            
            continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
        	if direcao >= 5:
        		dist = 14
        	else:
        		dist = 10
        	heappush(pr_queue, (custo, custo + dist, caminho + direcao, vizinho))
        	Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"


################################
#                              #
#    Função do algoritmo A*    #
#                              #
################################
def aEstrela(labirinto):

    inicio, objetivo = posicaoInicio(labirinto), posicaoObjetivo(labirinto)
    pr_queue = []
    heappush(pr_queue, (heuristicas(inicio, objetivo,1), 0, "", inicio))

    visitado = set()
    grafo = corverteGrafo(labirinto)
    Expansoes = 0

    while pr_queue:
        _, custo, caminho, atual = heappop(pr_queue)
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminho)
        	return caminho
        if atual in visitado:            
            continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
        	if direcao >= 5:
        		dist = 14
        	else:
        		dist = 10
        	heappush(pr_queue, (custo + heuristicas(vizinho, objetivo,2), custo + 10, caminho + direcao, vizinho))
        	Expansoes += 1
    print ("Expansoes: %s" %Expansoes)        
    return "IMPOSSIVEL!"



############
#          #
#   MAIN   #
#          #
############
if __name__ == "__main__":
	info = lerArquivo(sys.argv[1])
	labirinto = info[1]
	
	tipoBusca = int(sys.argv[2])

	start_time = time.time()

	if tipoBusca == 1:
		print "DFS:"
		caminho = dfs(labirinto)
	if tipoBusca == 2:
		print "BFS:"
		caminho = bfs(labirinto)
	if tipoBusca == 3:
		print "Best-First:"
		caminho = bestFirst(labirinto)
	if tipoBusca == 4:
		print "A*:"
		caminho = aEstrela(labirinto)

	end_time = time.time()

	if caminho == "IMPOSSIVEL!":
		print "Nao existe caminho possivel!"
	else:
		if len(sys.argv) == 4:
			passoApasso(labirinto,caminho)

	print("Tempo: %s segundos" % (end_time - start_time))