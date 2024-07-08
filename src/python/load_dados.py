#%%
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

BASE_DIR = os.path.abspath(
    os.path.dirname(
        os.path.dirname(
           os.path.dirname(__file__)
        )
    )
)

DATA_DIR = os.path.join(BASE_DIR, 'dados')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'resultados')
DATA_RES_DIR = os.path.join(DATA_DIR, 'resultado')

remessa = [f for f in os.listdir(DATA_RES_DIR) if os.path.isfile(os.path.join(DATA_RES_DIR, f)) and f.endswith('.xls')]

dados = pd.DataFrame()

for arq in remessa:
    competencia = os.path.basename(arq).split('.')[0].split(' ')[1]
    mes = int(competencia.split('-')[1])
    ano = int(competencia.split('-')[0])


    df = pd.read_csv(
        os.path.join(DATA_RES_DIR, arq),
        encoding="latin1",
        sep='\t',
        decimal=','
    )
    df["Competência"] = datetime(ano, mes, 1)
    
    dados = pd.concat([dados, df])

dados.head()
# %%
individuais = ['IF-VSI - (14)', 'IF-VSIF - (16)', 'VS CLASSIC - (72)', 'IF-VSIF+O - (29)', 'VOC - (74)']

df_ind = dados.query("Item in @individuais")

print(df_ind.head())
# %%
df_ind_geral = df_ind.groupby(by='Competência', as_index=False)[["Qt beneficiários", "Mensalidade", "Contas"]].sum()

print(df_ind_geral.head())
# %%
sns.set_theme(style="darkgrid")
plt.figure(figsize=(15, 6))

fig = sns.lineplot(x="Competência", y="Qt beneficiários", data=df_ind_geral)
fig.set_ylim((0,5000))
fig.set_title("Evolução na quantidade de vidas na modalidade IF Pós")
plt.show()

# %%
#df['12_month_cumsum'] = df['Qt beneficiários'].rolling(window=12).sum()

df_ind_geral['benefiario_pct_change'] = df_ind_geral['Qt beneficiários'].pct_change().rolling(window=12).sum() * 100

sns.set_theme(style="darkgrid")
plt.figure(figsize=(15, 6))

fig = sns.lineplot(x="Competência", y="benefiario_pct_change", data=df_ind_geral)
#fig.set_ylim((0,5000))
fig.set_title("Variação anualizada na quantidade de vidas na modalidade IF Pós")
plt.show()

# %%
df_ind_produto = df_ind.groupby(by=['Competência', "Item"], as_index=False)[["Qt beneficiários", "Mensalidade", "Contas"]].sum()

df_ind_produto.head()
# %%
sns.set_theme(style="darkgrid")

x = "Competência"
y = "Qt beneficiários"
hue = "Item"
def plotagem_multipla(x = "Competência", y = "Qt beneficiários", hue = "Item", data = df_ind_produto, tupla = (0,2500)):
    g= sns.relplot(
        data=df_ind_produto,
        x=x, y=y, hue=hue, col = hue,
        kind="line", palette="crest", linewidth=4, zorder=5,
        height=5, aspect=3, legend=False,
        col_wrap=1
    )
    g.despine(bottom=True, left=True)
    g.set(ylim=tupla)
    # Iterate over each subplot to customize further
    for produto, ax in g.axes_dict.items():

        # Add the title as an annotation within the plot
        ax.text(.01, .89, produto, transform=ax.transAxes, fontweight="bold")

        # Plot every year's time series in the background
        g2 = sns.lineplot(
            data=df_ind_produto, x=x, y=y, units=hue,
            estimator=None, color=".7", linewidth=1, ax=ax,
        )

        # Reduce the frequency of the x axis ticks
        #ax.set_xticks(ax.get_xticks()[::2])
        #g2.set_xticks([19417., 19539., 19662., 19783.])
        g2.set_xticks(ax.get_xticks())
        xticklabels = mdates.num2date(ax.get_xticks())
        formatted_labels = [dt.strftime("%m-%y") for dt in xticklabels]
        ax.set_xticklabels(formatted_labels)
        g2.set_xticklabels(formatted_labels)
        g.set_xticklabels(formatted_labels)
        #g2.set_axis_labels(x, ax.yaxis)
        #g2.set_titles(ax.axes.title)
        g2.set_title(f'{y} - {produto}')
        g2.set_axis_on()
        plt.xlabel(x)
        ax.axis('on')
        #g2.set_ylim(tupla)
    plt.show()
    
plotagem_multipla(x = "Competência", y = "Qt beneficiários", hue = "Item", data = df_ind_produto)
# %%
df_ind_produto['benef_pct_change'] = df_ind_produto.groupby(by=["Item"])['Qt beneficiários'].pct_change() * 100
df_ind_produto['benef_pct_change12'] = df_ind_produto.groupby(by=["Item"])['Qt beneficiários'].pct_change().rolling(window=12).sum() * 100

#%%
x = "Competência"
y = 'benef_pct_change12'
hue = "Item"
data = df_ind_produto
z=1000
tupla=(-z,z)

g= sns.relplot(
    data=data,
    x=x, y=y, hue=hue, col = hue,
    kind="line", palette="crest", linewidth=4, zorder=5,
    height=5, aspect=3, legend=False,
    col_wrap=1
)
g.despine(bottom=True, left=True)
g.set(ylim=tupla)
# Iterate over each subplot to customize further
for produto, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    ax.text(.01, .89, produto, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    g2 = sns.lineplot(
        data=data, x=x, y=y, units=hue,
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

    # Reduce the frequency of the x axis ticks
    #ax.set_xticks(ax.get_xticks()[::2])
    #g2.set_xticks([19417., 19539., 19662., 19783.])
    g2.set_xticks(ax.get_xticks())
    xticklabels = mdates.num2date(ax.get_xticks())
    formatted_labels = [dt.strftime("%m-%y") for dt in xticklabels]
    ax.set_xticklabels(formatted_labels)
    g2.set_xticklabels(formatted_labels)
    g.set_xticklabels(formatted_labels)
    #g2.set_axis_labels(x, ax.yaxis)
    #g2.set_titles(ax.axes.title)
    g2.set_title(f'{y} - {produto}')
    g2.set_axis_on()
    plt.xlabel(x)
    ax.axis('on')
    g2.set_ylim(tupla)
plt.show()

# %%
#plotagem_multipla(x = "Competência", y="benefiario_pct_change12", hue = "Item", data = df_ind_produto, tupla = (0,10))
# %%
vsclassic = df_ind_produto.query("Item == 'VS CLASSIC - (72)' & Competência > '2023-01-01'")
vsclassic["pct_change"] = vsclassic['Qt beneficiários'].pct_change() * 100
vsclassic.head()
plt.figure(figsize=(15, 6))
fig = sns.lineplot(x="Competência", y="pct_change", data=vsclassic)
#fig.set_ylim((0,5000))
fig.set_title("Variação na quantidade de vidas do Produto VS CLASSIC")
plt.axvline(pd.Timestamp('2024-03-01'), color='green', linestyle='--', label='Linha Vertical')
plt.show()

# %%
df_ind_produto['receita'] = df_ind_produto.groupby(by=["Item"])['Mensalidade'].transform(lambda x: x.rolling(12).sum())
df_ind_produto['despesa'] = df_ind_produto.groupby(by=["Item"])['Contas'].transform(lambda x: x.rolling(12).sum())

df_ind_produto['sinistralidade'] = df_ind_produto['despesa'] / df_ind_produto['receita'] * 100

#%%
df_ind_produto
# %%
x = "Competência"
y = 'sinistralidade'
hue = "Item"
data = df_ind_produto.query("Competência >= '2023-01-01'")

tupla=(0,550)

g= sns.relplot(
    data=data,
    x=x, y=y, hue=hue, col = hue,
    kind="line", palette="crest", linewidth=4, zorder=5,
    height=5, aspect=3, legend=False,
    col_wrap=1
)
g.despine(bottom=True, left=True)
g.set(ylim=tupla)
# Iterate over each subplot to customize further
for produto, ax in g.axes_dict.items():

    # Add the title as an annotation within the plot
    #ax.text(.01, .89, produto, transform=ax.transAxes, fontweight="bold")

    # Plot every year's time series in the background
    g2 = sns.lineplot(
        data=data, x=x, y=y, units=hue,
        estimator=None, color=".7", linewidth=1, ax=ax,
    )

    # Reduce the frequency of the x axis ticks
    #ax.set_xticks(ax.get_xticks()[::2])
    #g2.set_xticks([19417., 19539., 19662., 19783.])
    g2.set_xticks(ax.get_xticks())
    xticklabels = mdates.num2date(ax.get_xticks())
    formatted_labels = [dt.strftime("%m-%y") for dt in xticklabels]
    ax.set_xticklabels(formatted_labels)
    g2.set_xticklabels(formatted_labels)
    g.set_xticklabels(formatted_labels)
    #g2.set_axis_labels(x, ax.yaxis)
    #g2.set_titles(ax.axes.title)
    g2.set_title(f'{y} - {produto}')
    g2.set_axis_on()
    plt.xlabel(x)
    ax.axis('on')
    g2.set_ylim(tupla)
plt.show()
# %%
df_ind_produto.query("Competência == '2024-04-01'")
# %%
df_if = df_ind_produto.groupby(by="Competência")[["Mensalidade", "Contas"]].sum()
df_if['receita'] = df_if['Mensalidade'].rolling(12).sum()
df_if['despesa'] = df_if['Contas'].rolling(12).sum()
df_if['Sinistralidade'] = df_if['Contas']/df_if['Mensalidade']*100
df_if['Sinistralidade12'] = df_if['despesa']/df_if['receita']*100
#df_if = df_if.query("Competência >= '2022-01-01'")
# %%
plt.figure(figsize=(15, 6))
fig = sns.lineplot(x="Competência", y="Mensalidade", data=df_if, label="Receita")
sns.lineplot(x='Competência', y='Contas', data=df_if, label='Despesa')
fig.set_ylim((0,5*(10**6)))
fig.set_title("Comparativo da Evolução da Receita e da Despesa Mensal com Planos Individuais Familiares")
plt.axvline(pd.Timestamp('2020-03-11'), color='red', linestyle='--', label='Pandemia')
milhoes = ['{:,.0f}'.format(x / 1000000) + 'M' for x in plt.gca().get_yticks()]
plt.gca().set_yticklabels(milhoes)
plt.show()
# %%
plt.figure(figsize=(15, 6))
fig = sns.lineplot(x="Competência", y="receita", data=df_if, label="Receita")
sns.lineplot(x='Competência', y='despesa', data=df_if, label='Despesa')
fig.set_ylim((0,0.5*(10**8)))
fig.set_title("Comparativo da Evolução da Receita e da Despesa Anualizadas com Planos Individuais Familiares")
plt.axvline(pd.Timestamp('2020-03-11'), color='red', linestyle='--', label='Pandemia')
milhoes = ['{:,.0f}'.format(x / 1000000) + 'M' for x in plt.gca().get_yticks()]
plt.gca().set_yticklabels(milhoes)
plt.show()
# %%
df_if = df_if.query("Competência >= '2022-01-01'")
plt.figure(figsize=(15, 6))
fig = sns.lineplot(x="Competência", y="Sinistralidade", data=df_if, label="Sinistralidade")
fig.set_ylim((0,250))
fig.set_title("Evolução da Sinistralidade Mensal com Planos Individuais Familiares")
plt.axhline(75, color='red', linestyle='--', label='Meta de Sinistralidade')
plt.show()
# %%
plt.figure(figsize=(15, 6))
fig = sns.lineplot(x="Competência", y="Sinistralidade12", data=df_if, label="Receita")
fig.set_ylim((0,250))
fig.set_title("Evolução da Sinistralidade Anualizada com Planos Individuais Familiares")
plt.axhline(75, color='red', linestyle='--', label='Meta de Sinistralidade')
plt.show()
# %%
