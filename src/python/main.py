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

#%%
df = pd.read_excel(os.path.join(DATA_DIR, 'analise 2023-03.xlsx'))

#%%
#sns.set_theme(style="darkgrid")
#
#columns = df.columns[2:,]
#
#for item in df['Item']:
#    for i in columns:
#        temp = df[df["Item"] == item]
#        print(temp.head())
#        g = sns.lineplot(x='Competência', 
#                         y=i,
#                         data=temp).set_title(f"{item}-{i}")
#        fig = g.get_figure()
#        fig.savefig(os.path.join(RESULTADOS_DIR, f"{item}-{i}.png"))

# %%
#columns = df.columns[2:,]
#
#for item in ['VS CLASSIC - (72)']:
#    for i in ['% Sinistralidade']:
#        temp = df[df["Item"] == item]
#        print(temp.head())
#        g = sns.lineplot(x='Competência', 
#                         y=i,
#                         data=temp).set_title(f"{item} - {i}")
#        fig = g.get_figure()
#        fig.savefig(os.path.join(RESULTADOS_DIR, f"{item}-{i}.png"))

# %%
sns.set_theme(style="darkgrid")
#columns = df.columns[2:,]
#columns = ['% Sinistralidade']
columns = df.columns[2:,] # type: ignore
x = "Competência"
hue = "Item"
for i in columns:
    y = i
    g = sns.relplot(
        data=df,
        x="Competência", y=i, hue="Item", col = 'Item',
        kind="line", palette="crest", linewidth=4, zorder=5,
        height=5, aspect=3, legend=False,
        col_wrap=1
    )
    g.despine(bottom=True, left=True)

    # Iterate over each subplot to customize further
    for produto, ax in g.axes_dict.items():

        # Add the title as an annotation within the plot
        ax.text(.01, .89, produto, transform=ax.transAxes, fontweight="bold")

        # Plot every year's time series in the background
        g2 = sns.lineplot(
            data=df, x="Competência", y=i, units="Item",
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
        #plt.savefig(os.path.join(RESULTADOS_DIR, f"{produto}-{i}.png"))

    g.savefig(os.path.join(RESULTADOS_DIR, f"{i}.png"))

# %%
