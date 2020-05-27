""" This package contains the functions and settings used to create graphs for the Housing Sales Analysis"""

# visualization packages
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import numpy as np

import seaborn as sns

from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')


# Set specific parameters for the visualizations
large = 32; med = 16; small = 12
params = {'axes.titlesize': large,
          'legend.fontsize': med,
          'figure.figsize': (16, 10),
          'axes.labelsize': med,
          'xtick.labelsize': med,
          'xtick.minor.bottom':True,
          'ytick.labelsize': med,
          'figure.titlesize': large}


# Set style parameters
sns.set_style("ticks", { 'axes.spines.top': False, 'axes.spines.right': False, "xtick.major.size": med, "xtick.minor.size": 8, 'axes.titlesize': large, 'ytick.labelsize': med})
plt.rcParams.update(params)

# Map for variable names

map_var_names = {'HouseAge':'Age of House',
                 'TimeSinceRemodel':'Time Since Remodel',
                 'HasFence':'Has a Fence',
                 'KitchenAbvGr':'Number of Kitchens',
                 'MSSubClass':'Dwelling Code',
                 'OverallCond':'Overall House Condition',
                 'RemodFiveYrs':'Remodeled in Last 5 Years',
                 'YrSold':'Year of Sale',
                 'BsmtHalfBath': 'Number of Half Baths in basement',
                 'MoSold':'Month Sold',
                 'HasRemod':'Has Been Remodeled',
                 'GasAirHeat': 'Heat Forced Air',
                 'HasPool':'Has A Pool',
                 'HasBasement':"House has Basement",
                 'GarageAreaPerCar':'Square Feet per Car',
                 'BsmtPerFinished':'Percent of Basement Finished',
                 'HasFinishedBsmt':"At Least Partially Finished Basement",
                 'BsmtUnfSF':'Sqft of Unfinished Basement',
                 'BedroomAbvGr': "Count of Bedrooms Above Ground",
                 'BsmtFullBath': "Number of Full Baths in Basment",
                 'SBboxElectric':'Standard Circuit Breakers',
                 'HasGarage': 'Property has Garage', 
                 'HasCentralAir': "Home has Central air", 
                 'LotArea':'Size of Lot in sqft', 
                 'HasPorch':"Home has Porch", 
                 'HasDeck':"Home has Deck",
                 'HalfBath':'Number of Half Baths', 
                 'GaragebuiltWHouse': 'Garage Built with House', 
                 '2ndFlrSF': 'Sqft of Second Floor', 
                 'MasVnrArea':'Masonry veneer area in square feet',
                 'HasFirePlace':"Has as least one Fireplace", 
                 'TotRmsAbvGrd': 'Total Rooms above Ground', 
                 'FullBath': 'Count of Full Baths', 
                 'AverageRoomSize': 'Sqft of Average Room',
                 'GarageArea':'Sqft of Garage', 
                 '1stFlrSF':'Sqft of First Floor', 
                 'GarageCars':"Garage Cars Capacity", 
                 'TotalBsmtSF': "Sqft of Basement", 
                 'GrLivArea': 'Total living sapce in Sqft',
                 'OverallQual':'Overall Quality Ranking of Home', 
                 'SalePrice':'Price of Sale', 
                 'HasAlley':'Property connected to Alley'}

def remap_index(test_df):
    test_df2 = test_df.copy
    test_df2['two'] = test_df2.index.to_series().map(map_var_names)
    test_df2.reset_index(['two'], inplace=True)
    return test_df2

def dist_var_one(series_var,filename):

    fig = plt.figure(figsize=(16, 10), dpi=80) 
    # Creates one subplot within our figure and uses the classes fig and ax
    fig, ax = plt.subplots(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')
    chart = sns.boxplot( x=series_var)
    #ax.set_ylim(0, 100)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(100000.00))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(50000))
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

    ax.set_title("Distribution of Housing Sales in Ames, Iowa")
    ax.set_xlabel("House Price at Sale")


    #plt.show()

    file_name = filename
    path = './images/'+file_name+'.png'
    plt.savefig(path)
    plt.close(fig) 
    pass


def dist_var_hist_box(series_var,filename):

    fig = plt.figure(figsize=(16, 10), dpi=80) 
    # Creates one subplot within our figure and uses the classes fig and ax
    fig, (ax_box, ax_hist) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)}, dpi= 80, facecolor='w', edgecolor='k')
    
    sns.boxplot(series_var, ax=ax_box)
    sns.distplot(series_var, ax=ax_hist)
    #ax.set_ylim(0, 100)

    ax_hist.xaxis.set_major_locator(ticker.MultipleLocator(100000.00))
    ax_hist.xaxis.set_minor_locator(ticker.MultipleLocator(50000))
    ax_hist.xaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
    ax_hist.set_xlabel("House Price at Sale")
    
    ax_hist.yaxis.set_major_formatter(ticker.PercentFormatter())
    ax_hist.yaxis.set_major_locator(ticker.NullLocator())

    ax_box.set(xlabel='')

    fig.suptitle('Distribution of Housing Sales in Ames, Iowa', fontsize=26)

    file_name = filename
    path = './images/'+file_name+'.png'
    plt.savefig(path)
    plt.close(fig) 
    pass




def good_heat_map(test):
    fig = plt.figure(figsize=(8,11))
    fig, ax = plt.subplots(figsize=(8,11), facecolor='w', edgecolor='k')
    chart=sns.heatmap(test.corr()[['SalePrice']].sort_values(by='SalePrice'), cmap = 'RdYlGn',
                xticklabels=True, yticklabels=True, ax=ax, square=True)
    ax.set_title("Correlation of Each Independent Variable \n with the Target Variable \n")
    plt.tight_layout()
    file_name = "corr_heatmap"
    path = './images/'+file_name+'.png'
    plt.savefig(path)
    plt.close(fig)
    pass


def scatter_explore(test):
    fig = plt.figure(figsize=(16, 10), dpi=80) 
    # Creates one subplot within our figure and uses the classes fig and ax
    fig, ax = plt.subplots(figsize=(16, 10), dpi= 80, facecolor='w', edgecolor='k')
    chart = sns.scatterplot(x='GrLivArea', y='SalePrice', data = test,
                            hue=test.OverallQual.values, legend='full', alpha = .7,
                            palette="BrBG")

    ax.yaxis.set_major_locator(ticker.MultipleLocator(100000.00))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(50000))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))

    ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
    #ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x} sqft'))

    fig.suptitle("The Positive Correlations between Home Sale Price,\n Sq Footage and Quality Rating", fontsize=26)
    ax.set_xlabel("Total Square Feet")
    ax.set_ylabel("Sale Price")
    
    ax.get_legend().set_title("Overall Quality Ranking")
    
    plt.tight_layout()
    file_name = "scatter_price"
    path = './images/'+file_name+'.png'
    plt.savefig(path)
    plt.close(fig)
    pass


def full_heat_map(test):
    fig = plt.figure(figsize=(18, 12), dpi=80) 
    # Creates one subplot within our figure and uses the classes fig and ax
    fig, ax = plt.subplots(figsize=(18, 12), dpi= 80, facecolor='w', edgecolor='k')

    chart=sns.heatmap(test.corr(), cmap = 'RdYlGn',
                xticklabels=True, yticklabels=True, ax=ax, square=True)
    ax.set_title("Correlation Between Independent Variables")
    plt.tight_layout()
    file_name = "full_heatmap"
    path = './images/'+file_name+'.png'
    plt.savefig(path)
    plt.close(fig)
    pass