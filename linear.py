import pandas as pd
from scipy import stats
from pytable import PyTable

table = PyTable()

data = pd.read_csv("tensoes.csv") # Le os dados

vfluke = data[data.columns[0]].values # Coluna do multímetro
analog = data[data.columns[1]].values # Coluna do arduino

slope, intercept, r, p, std_err = stats.linregress(x= analog, y= vfluke) # Faz a regressão linear

def calibrate(volt): # Funcao de calibração
    return round(slope*volt+intercept, 1)

calibrated = list(map(calibrate, analog)) # Pega todos os valores da lista analog, joga na equação de calibração e cria uma lista

table.alignmentDigits = 12 # Quantos digitos por palavra na tabela
table.printHeader(['CALIBRATED ERROR', 'CALIBRATED', 'FLUKE', 'ANALOG', 'ANALOG ERROR']) # Cabeçalho da tabela

for i in range(len(vfluke)): # Mapea todos os valores
    vreal = vfluke[i] # Valor do fluke
    vanalog = analog[i] # Valor do analogico
    vcalibrated = calibrated[i] # Valor calibrado

    eanalog = round(abs(vreal - vanalog)/vreal * 100, 2) # Erro do analogico
    ecalibrated = round(abs(vreal - vcalibrated)/vreal * 100, 2) # Erro do calibrado

    table.addRow([str(ecalibrated) + '%', vcalibrated, vreal, vanalog, str(eanalog) + '%']) # Imprime na tabela

print(f"ROUNDED CALIBRATION: V={round(slope, 4)}*X+({round(intercept, 4)}) R: {round(r, 4)}") # Mostra a equação de calibração arredondada.
print(f"CALIBRATION: V={slope}*X+({intercept}) R: {r}") # Mostra a equação de calibração.
