import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# 1. Importação dos dados e parsing da coluna 'date' como índice
# Definimos 'date' como índice e parseamos as datas para garantir manipulação correta de séries temporais.
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# 2. Limpeza dos dados
# Mantemos apenas os valores entre o 2.5º e 97.5º percentil para remover outliers.
df = df[df["value"].between(df["value"].quantile(0.025), df["value"].quantile(0.975))]

# Definição da ordem dos meses para os gráficos de barras e boxplot.
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def draw_line_plot():
    # 3. Criação de gráfico de linha com os dados limpos
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.lineplot(data=df, legend="brief", ax=ax)
    
    # 4. Configuração dos títulos e rótulos
    ax.set(title='Daily freeCodeCamp Forum Page Views 5/2016-12/2019',
           xlabel="Date", ylabel="Page Views")
    
    # 5. Salvamento da figura e retorno
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # 6. Criação de cópia dos dados e adição de colunas 'year' e 'month'
    df_bar = df.copy()
    df_bar["year"] = df.index.year  # Extraímos o ano do índice (coluna de datas)
    df_bar["month"] = df.index.month_name()  # Extraímos o nome do mês

    # 7. Criação do gráfico de barras com Seaborn
    fig, ax = plt.subplots(figsize=(15, 5))
    sns.barplot(x="year", hue="month", y="value", data=df_bar, hue_order=months, ci=None, ax=ax)
    
    # 8. Configuração dos rótulos e título
    ax.set(xlabel="Years", ylabel="Average Page Views", title="Monthly Average Page Views per Year")
    
    # 9. Salvamento da figura e retorno
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # 10. Preparação dos dados para os box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)  # Convertendo o índice 'date' em coluna
    df_box['year'] = df_box['date'].dt.year  # Extraímos o ano da coluna 'date'
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Extraímos o mês no formato abreviado (Jan, Feb, etc.)

    # 11. Ordenamos os dados por número do mês para o gráfico ficar na ordem correta
    df_box['monthnumber'] = df_box['date'].dt.month
    df_box = df_box.sort_values('monthnumber')  # Ordenamos para garantir que os meses apareçam na ordem certa

    # 12. Criação dos gráficos de boxplot (ano e mês)
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))  # Dois subplots (lado a lado)
    
    # 13. Gráfico de boxplot por ano
    sns.boxplot(x="year", y="value", data=df_box, ax=ax[0])
    ax[0].set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")
    
    # 14. Gráfico de boxplot por mês
    sns.boxplot(x="month", y="value", data=df_box, ax=ax[1])
    ax[1].set(xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")
    
    # 15. Salvamento da figura e retorno
    fig.savefig('box_plot.png')
    return fig
