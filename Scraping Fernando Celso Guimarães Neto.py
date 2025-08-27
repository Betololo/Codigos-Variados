from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

#Desenvolvido por Fernando Celso Guimarães Neto

driver = webdriver.Chrome()

#SELECIOANAR A PÁGINA DESEJADA - No caso, será para câmbio e etanol.
driver.get("https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&Data=&Mercadoria=ETH")
time.sleep(2) #Esperar um tempo para garantir que a página carregue completamente.
pag_alvo = driver.page_source
soup = BeautifulSoup(pag_alvo, "html.parser")

#Scraping
nome_tabelas = soup.findAll("td", attrs={"class":"TabelaItem"})#Obtido através do estudo do HTML da página
#Container da tabela que contem apenas os valores
container = soup.find("td", attrs={"id": "MercadoFut2"})#container = soup.find("table", attrs={"class": "tabConteudo"})
#Container da tabela que contém os períodos
container2 = soup.find("td", attrs={"id": "MercadoFut0"})#container = soup.find("table", attrs={"class": "tabConteudo"})
#Buscando valores dentro do primeiro container
valores_das_tabelas = container.findAll("td", attrs={"class": "tabelaConteudo1"})#Obtido através do estudo do HTML da página
valores_das_tabelas2 = container.findAll("td", attrs={"class": "tabelaConteudo2"})#Obtido através do estudo do HTML da página
#Buscando valores dentro do segundo container
dados_periodo =  container2.findAll("td", attrs={"class": "tabelaConteudo1"})#Obtido através do estudo do HTML da página
dados_periodo2 =  container2.findAll("td", attrs={"class": "tabelaConteudo2"})#Obtido através do estudo do HTML da página
#Criando o vetor que contém os períodos
peridos = dados_periodo[:8]
peridos2 = dados_periodo2[:7]
#Criando o vetor que contém o nome das colunas
vetor_nome_tabelas = nome_tabelas[:11]
#Criando uma matriz de 9 colunas e 8 linhas - Pegar os DADOS
matriz_dados = []
for i in range(8):
    linha = valores_das_tabelas[i*9:(i+1)*9]#Pegando blocos de 9 elementos
    matriz_dados.append([valor.text.strip() for valor in linha])
#Criando uma matriz de 9 colunas e 7 linhas - Pegar os DADOS
matriz_dados2 = []
for i in range(7):
    linha2 = valores_das_tabelas2[i*9:(i+1)*9]#Pegando blocos de 9 elementos
    matriz_dados2.append([valor2.text.strip() for valor2 in linha2])

#Teste e validação
print("Número de nomes:", len(nome_tabelas))#Apenas teste de verificação.
print("Número de valores:", len(valores_das_tabelas))#Apenas teste de verificação.
print("Número de valores2:", len(valores_das_tabelas2))#Apenas teste de verificação.
print("\n\n\n")
#Imprimindo o resultado
#Imprimindo o vetor de tamanho 11
print(" ".join([nome.text.strip() for nome in vetor_nome_tabelas]))
#Imprimindo os períodos e os dados em uma única linha
print(peridos[0].text.strip(), " ".join(matriz_dados[0]))
print(peridos2[0].text.strip(), " ".join(matriz_dados2[0]))
print(peridos[1].text.strip(), " ".join(matriz_dados[1]))
print(peridos2[1].text.strip(), " ".join(matriz_dados2[1]))
print(peridos[2].text.strip(), " ".join(matriz_dados[2]))
print(peridos2[2].text.strip(), " ".join(matriz_dados2[2]))
print(peridos[3].text.strip(), " ".join(matriz_dados[3]))
print(peridos2[3].text.strip(), " ".join(matriz_dados2[3]))
print(peridos[4].text.strip(), " ".join(matriz_dados[4]))
print(peridos2[4].text.strip(), " ".join(matriz_dados2[4]))
print(peridos[5].text.strip(), " ".join(matriz_dados[5]))
print(peridos2[5].text.strip(), " ".join(matriz_dados2[5]))
print(peridos[6].text.strip(), " ".join(matriz_dados[6]))
print(peridos2[6].text.strip(), " ".join(matriz_dados2[6]))
print(peridos[7].text.strip(), " ".join(matriz_dados[7]))

#Gerando os resultados em formato .csv para que o resultado possa ser aberto em qualquer leiotor de planilhas
with open('Teste4.csv', 'w', newline='', encoding='utf-8') as csvfile:#Aqui, o usuário pode editar o nome do arquivo a ser gerado, é só mudar onde está escrito 'resultado final'
    writer = csv.writer(csvfile)    
    #Escrevendo o cabeçalho com os nomes das colunas (vetor_nome_tabelas)
    writer.writerow([nome.text.strip() for nome in vetor_nome_tabelas])    
    #Intercalando os períodos e os dados no CSV com célula vazia entre eles
    for i in range(len(peridos)):
        writer.writerow([peridos[i].text.strip(), ''] + matriz_dados[i])#Linha para matriz_dados
        if i < len(peridos2):
            writer.writerow([peridos2[i].text.strip(), ''] + matriz_dados2[i]) #Linha para matriz_dados2
print("Arquivo CSV gerado com sucesso!")



