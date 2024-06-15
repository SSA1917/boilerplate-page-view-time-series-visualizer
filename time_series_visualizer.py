import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
from datetime import datetime
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('./fcc-forum-pageviews.csv',index_col='date',parse_dates=True)

#Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots()
    df['value'].plot(kind='line',ax=ax)
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('MS').mean()
    df_bar.sort_index(key=lambda x: x.month,ascending=True,inplace=True)
    df_bar['years'] = df_bar.index.year
    df_bar['months'] = [d.strftime('%B') for d in df_bar.index]
    df_pivot = pd.pivot_table(df_bar,index='years',columns=['months'],values='value',sort=False)
    df_pivot.sort_values(by='years',ascending=True,inplace=True)

    # Draw bar plot
    ax = df_pivot.plot(kind='bar')
    fig = ax.get_figure()
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # Draw box plots (using Seaborn)

    fig, ax = plt.subplots(1,2,figsize=(12, 5))
    yearPlot = sns.boxplot(data=df_box,x='year',y='value',hue='year',legend=False,ax=ax[0])
    monthPlot = sns.boxplot(data=df_box,x='month',y='value',hue='month',ax=ax[1])
    yearPlot.set_xlabel('Year')
    yearPlot.set_ylabel('Page Views')
    yearPlot.set_title('Year-wise Box Plot (Trend)')
    monthPlot.set_xlabel('Month')
    monthPlot.set_ylabel('Page Views')
    monthPlot.set_title('Month-wise Box Plot (Seasonality)')
    fig.tight_layout()



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
