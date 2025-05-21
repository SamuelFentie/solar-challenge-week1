import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    countries = ['benin', 'sierraleone', 'togo']
    data = {}
    for country in countries:
        df = pd.read_csv(f"../data/{country.lower()}_clean.csv")
        df['Country'] = country
        data[country] = df
    return pd.concat(data.values(), ignore_index=True)

def plot_boxplots(df, metric):
    plt.figure(figsize=(8, 5))
    sns.boxplot(x='Country', y=metric, data=df, palette='Set2')
    plt.title(f'{metric} Distribution by Country')
    return plt.gcf()

def plot_bar_chart(summary_df):
    fig, ax = plt.subplots()
    summary_df['GHI_mean'].sort_values(ascending=False).plot.bar(
        ax=ax, color='cornflowerblue', edgecolor='black'
    )
    ax.set_title('Average GHI by Country')
    ax.set_ylabel('GHI (W/m²)')
    return fig

def compute_summary(df):
    summary = df.groupby('Country')[['GHI', 'DNI', 'DHI']].agg(['mean', 'median', 'std'])
    summary.columns = ['_'.join(col) for col in summary.columns]
    return summary
