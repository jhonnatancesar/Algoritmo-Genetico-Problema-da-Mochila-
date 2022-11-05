import pandas as pd
import random

probabilidade_cruzamento = 0.5      #Probabilidade de acontecer cruzamento
probabilidade_mutacao = 0.1         #Probabilidade e mutar
tamanho_populacao = 12              #Tamanho da populaçao (espaço na mochila)
tamanho_elite = 2                 #Seleciona dois melhores individuos
capacidade = 36                     #Capacidade da população(mopchila)
garacoes = 300                     #Aprendizagem do algoritmo

#Abre o arquivo com os objetos/individuos
objetos = pd.read_csv('Itens.txt', sep=';')
#coloca os objetos no vetor
genes = len(objetos)

#Cria um individuo
def individual():
    individual = [random.randint(0, 1) for i in range(genes)]
    validar(individual)
    return individual

#Validar individuos com base no peso da mochila
def validar(individual):
    load = calculo_recarga(individual)
    less_position = 0
    values = sorted(objetos['valor'])
    while (load > capacidade):
        load = 0
        less = values[less_position]
        index = objetos['valor'].values.tolist().index(less)
        individual[index] = 0
        less_position += 1
        load = calculo_recarga(individual)

#Cria a populaçao
def criar_populacao():
    return [individual() for i in range(tamanho_populacao)]

#Analisa o individuo para selecionar os melhores
def fitness(individual):
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            fitness += objetos.at[i, 'valor']
    return fitness

#Analisa o individuo selecionando pelo espaço da populaçao/mochila
def calculo_recarga(individual):
    load = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            load += objetos.at[i, 'peso']
    return load

#Faz o cruzamento dos individuos que cabem na população/mochila
def selecionar_cruzar(populacao):
    scored = organizar_populacao(populacao)
    populacao = scored
    elite = populacao[(len(populacao) - tamanho_elite):]
    for i in range(len(populacao) - tamanho_elite):
        if (random.random() <= probabilidade_cruzamento):
            point = random.randint(1, genes - 1)
            parents = random.sample(elite, 2)
            populacao[i][:point] = parents[0][:point]
            populacao[i][point:] = parents[1][point:]
            validar(populacao[i])
    return populacao

#Faz a mutação dos individuos
def mutacao(populacao):
    for i in range(len(populacao) - tamanho_elite):
        if (random.random() <= probabilidade_mutacao):
            point = random.randint(0, genes - 1)
            new_value = random.randint(0, 1)
            while (new_value == populacao[i][point]):
                new_value = random.randint(0, 1)
            populacao[i][point] = new_value
            validar(populacao[i])
    return populacao

#Ordena os individuos no vetor
def organizar_populacao(populacao):
    return [i[1] for i in sorted([(fitness(j), j) for j in populacao])]
#Fim das funções

#Main()

populacao = criar_populacao() 
elite = [None] * len(populacao)
elite = organizar_populacao(populacao)[(len(populacao) - tamanho_elite):]

geracao = []
geracao_fitness = []

for i in range(garacoes):
    geracao.append(i + 1)
    geracao_fitness.append(
        fitness(organizar_populacao(populacao)[tamanho_populacao - 1]))
    populacao = selecionar_cruzar(populacao)
    populacao = mutacao(populacao)
print('Resultados:\n')
elite = organizar_populacao(populacao)[(len(populacao) - tamanho_elite):]
for i in elite:
    print('Indivíduo: {} | Valor: {} | Peso: {}\n'.format(
        i, fitness(i), calculo_recarga(i)))
