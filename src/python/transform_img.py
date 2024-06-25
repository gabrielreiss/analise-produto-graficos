#%%
import pandas as pd
import os
from PIL import Image
import glob
import tqdm

BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
           os.path.dirname(__file__)
        )
    )
)

DATA_DIR = os.path.join(BASE_DIR, 'dados')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'resultados')

df = pd.read_excel(os.path.join(DATA_DIR, 'analise 2023-03.xlsx'))

lista_arquivos_png = glob.glob(os.path.join(RESULTADOS_DIR, "*.png"))

#%%
temp = lista_arquivos_png[0]

#%%
aumento = 498 #maior que 497, menor que 498
topo = [i for i in range(0, 27*aumento, aumento) if 1 == True]
baixo = [i for i in range(485, 27*aumento, aumento) if 1 == True]

for arq in tqdm.tqdm(lista_arquivos_png):
    arquivo = os.path.basename(arq).split('.')[0]
# Carregue as imagens
    imagem_1 = Image.open(arq)

    for i in range(0,26):
        # Defina as áreas de corte para cada imagem (esquerda, topo, direita, baixo)
        area_corte_1 = (0, topo[i], 1480, baixo[i])  # Recorta a parte superior esquerda da imagem 1
        area_corte_base = (0, 12925, 1480, 12980)  # Recorta a parte central da imagem 2

        # Recorte as imagens usando as áreas definidas
        imagem_cortada_1 = imagem_1.crop(area_corte_1)
        imagem_cortada_base = imagem_1.crop(area_corte_base)

        # Crie uma nova imagem com a largura total das imagens cortadas e a altura da imagem mais alta
        largura_nova = max(imagem_cortada_1.width, imagem_cortada_base.width)
        altura_nova = imagem_cortada_1.height + imagem_cortada_base.height

        # Crie uma nova imagem em branco com as dimensões definidas
        imagem_nova = Image.new("RGB", (largura_nova, altura_nova))

        # Cole a primeira imagem cortada na nova imagem
        imagem_nova.paste(imagem_cortada_1, (0, 0))

        # Cole a segunda imagem cortada na nova imagem, ajustando a posição
        imagem_nova.paste(imagem_cortada_base, (0, imagem_cortada_1.height))

        # Salve a imagem final com o nome desejado
        imagem_nova.save(os.path.join(RESULTADOS_DIR, 'ind', f'{arquivo}-{i}.png'))

# %%
