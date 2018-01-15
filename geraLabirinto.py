import random
import sys

def criaLabirinto(linhas, colunas):

	labirinto = [] #Inicia o labirinto com todos os espacos livres

	for i in range(0, linhas):
		aux = []
		for j in range(0, colunas):			
				aux.append("*")
		labirinto.append(aux[:])

	numeroParedes = random.randint(0, (linhas + colunas)*5) #Define a quantidade de paredes

	for i in range(1, numeroParedes): #Coloca as paredes em locais aleatorios
		linha = random.randint(0, linhas - 1)
		coluna = random.randint(0, colunas - 1)

		while(labirinto[linha][coluna] == "-"):			
			linha = random.randint(0, linhas - 1)
			coluna = random.randint(0, colunas - 1)
		labirinto[linha][coluna] = "-"

	inicialL = random.randint(0, linhas-1)
	inicialC = random.randint(0, colunas-1)
	labirinto[inicialL][inicialC] = "#" #Define a posicao inicial do labirinto

	objetivoL = random.randint(0, linhas-1)
	objetivoC = random.randint(0, colunas-1)
	labirinto[objetivoL][objetivoC] = "$" #Define a posicao do objetivo no labirinto

	return labirinto

#Definicao do tamanho do labirinto
if len(sys.argv) > 2:
	linhas = int(sys.argv[2])  
else:
	linhas = random.randint(10,40)

if len(sys.argv) > 3:
	colunas = int(sys.argv[3])  
else:
	colunas = random.randint(10,40)

labirinto = criaLabirinto(linhas, colunas)

#Imprime o labirinto na tela
for i in range(0, linhas):
	ln = ""
	for j in range(0, colunas):			
		ln += labirinto[i][j]
	print ln

#Salva o labirinto em um arquivo
saida = open(sys.argv[1], "w")

string = str(linhas) + " " + str(colunas)
saida.write(string + "\n")

for i in labirinto:
	string = ""
	for j in i:
		string += j
	saida.write(string + "\n")
saida.close()