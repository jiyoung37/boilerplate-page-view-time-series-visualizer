import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
filename = r'C:\Users\europ\Documents\PythonProjects\boilerplate-page-view-time-series-visualizer\fcc-forum-pageviews.csv'
df = pd.read_csv(filename, index_col='date', parse_dates=True)

# Clean data
df =  df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(17,5))
    ax.plot(df.index, df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    # Draw bar plot
    df_bar['year'] = df.index.year
    df_bar['month'] = df_bar.index.strftime('%B')  # Full month name
    
    df_bar = df_bar.groupby(['year','month'])['value'].mean().unstack()

    months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                    'July', 'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar[months_order]

    fig, ax = plt.subplots(figsize=(8, 7))
    df_bar.plot(kind='bar', ax=ax)
    #ax.set_title('Average Page Views per month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months')
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
    year_palette = sns.color_palette("tab10", len(df_box['year'].unique())) 
    month_palette = sns.color_palette("husl", 12) 
     
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(15,6))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax1, palette=year_palette)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, order=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], ax=ax2, palette=month_palette)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    plt.tight_layout(pad=3.0) 

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
