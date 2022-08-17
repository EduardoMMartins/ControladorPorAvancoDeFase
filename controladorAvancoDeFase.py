#Código do Projeto de Controladores por Avanço de Fase


#Importando Funções
import numpy as np
import control.matlab as ml
import matplotlib.pyplot as plt
import math
import scipy
from scipy.interpolate import interp1d
from control import *

#Definindo a Função de Transferência e gerando o Diagrama de Bode 
num = np.array([0,0,4]) #[VALORES ADICIONADOS]
den = np.polymul(np.array([0,1,0]),np.array([0,1,2])) #[VALORES ADICIONADOS]
g = ml.tf(num,den)
print("Função de Transferência: ", g)

#Plotando o Diagrama de Bode
#plt.show()

#Definido valor da Constante de Erro Estático da Velocidade (kv) e Margem de Fase Desejada (pmd)
kv = 20 #[VALORES ADICIONADOS]
pmd = 50 #[VALORES ADICIONADOS]
print("Margem de Fase Desejada: ", pmd)
print("Constante de Erro Estático da Velocidade: ", kv)

#Calculando valor de ganho k conforme deduzido no caderno
k = kv/2 #[FÓRMULA ADICIONADA]
print("Ganho (k) = ", k)

#Calculando função G1(s)
g1 = k*g
print("Função G1(s): ", g1)
mag,phase,w = ml.bode(g1)

#Calculando a Margem de Ganho e Fase
gm,pm,wg,wp = ml.margin(g1)
print("Margem de Ganho: ", gm)
pm = math.ceil(pm) #Arredonda o valor da Margem de Fase para cima
print("Margem de Fase: ", pm)

#Calculando Angulo de Atenuação (PHIm)
anguloAvanco = 5 #[ADICIONAR VALOR ENTRE 5º E 12º]
phim = pmd - pm + anguloAvanco
print("PHIm = ", phim,"º")

#Calculando alpha
alpha = (1-np.sin(np.deg2rad(phim)))/(1+np.sin(np.deg2rad(phim)))
print("Alpha: ", alpha)

#Calculando o Módulo
modulo = -20*math.log10(1/np.sqrt(alpha))
print("Módulo = ", modulo)


#Calculando Wn
def myFunction(x):
    return 20*math.log10(x)

myFunction2 = np.vectorize(myFunction)
wq = interp1d(myFunction2(mag),w)
wn = wq(modulo)

print("wn = ", wn)


#Calculando Período (T)
t = 1/(wn*np.sqrt(alpha))
print("Período = ", t)

#Calculando zero e polo
zc = 1/t
pc = 1/(alpha*t)
print("Zero Controlador = ", zc)
print("Polo Controlador = ", pc)

#Calculando Kc
kc = k/alpha
print("Ganho do Controlador (kc) = ", kc)

#Definindo Função de transferência do controlador
numControlador = np.array([1,zc])
denControlador = np.array([1,pc])
ft = ml.tf(numControlador,denControlador)
gControlador = kc*ft
print("Função de Transferência do Controlador: ",gControlador)

#Multiplicando Gc(S) e G(S)
gcg = gControlador * g
print("Produto das Funções Gc(s) e G(s): ", gcg)
gmg,pmg,wgg,wpg = margin(gcg)
print("Margem de Fase Desejada: ", pmd)
print("Margem de Fase com o Controlador: ",pmg)
print("Diferença entre Fase Desejada e de Controle: ", pmd-pmg)
print("Margem de ganho com o Controlador: ", gmg)

