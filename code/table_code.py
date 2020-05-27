""" This package contains the functions and settings used to create tables for the house price analysis"""

# Standard data manipulation packages
import pandas as pd
import numpy as np

# Is a python wrapper for wkhtmltoimage. would need to install wkhtmltoimage to have it work locally 
# Note - I've only seen this work on Macs, there is some trouble getting it to work with PCs
import imgkit

# Image manipulation packages. PIL stands for Pillow. you need to `pip install Pillow`
import PIL
from PIL import Image, ImageOps


""" The css works with the pandas.dataframe.style object to data summaries be formatted nicely"""


# Css for table style
tb_styles = {'selector': 'table',
            'props':[('margin','0')]}

# Css for table headers
th_styles = {'selector': 'th', 
             'props': [('border', "1"),
                     ("border-color", "black"),
                       ('background', 'white'),
                     ('border-style','solid'),
                     ('border-width','1px'),
                     ('font-family', 'verdana'),
                     ('white-space', 'nowrap'),
                       ('padding-right',"10px"),
                     ("text-align", "left")]}

# Css for data rows
td_styles = {'selector': 'td',
             'props': [('font-family', 'verdana'),
                       ('border', "1"),
                       ("border-color", "black"),
                       ('border-style','solid'),
                       ('border-width','1px'),
                       ('white-space', 'nowrap'),
                       ('padding-right',"10px"),
                       ('padding',"10px")]}

# Css for table title
cap_style = {'selector':'caption',
             'props':[('font-family', 'verdana'),
                      ('white-space', 'nowrap'),
                      ("font-size", "large"),
                     ('padding-bottom',"10px")]}

# Css for even/odd rows
tr_odds = {'selector': 'tr:nth-of-type(odd)',
           'props': [('background', '#eee'), 
                     ("border", "0.2px solid black")]
          }

tr_evens =  {'selector': 'tr:nth-of-type(even)',
             'props': [('background', 'white'), 
                       ("border", "0.2px solid black")]
            }

options = {'quiet': ''}


map_var_names = {'HouseAge':'Age of House',
                 'TimeSinceRemodel':'Time Since Remodel',
                 'LotFrontage':'Feet of Street Adjacent to Lot',
                 'HasFence':'Has a Fence',
                 'KitchenAbvGr':'Number of Kitchens',
                 'MSSubClass':'Dwelling Class Code',
                 'OverallCond':'Overall House Condition',
                 'RemodFiveYrs':'Remodeled in Last 5 Years',
                 'YrSold':'Year of Sale',
                 'BsmtHalfBath': 'Number of Half Baths in Basement',
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
                 'SBboxElectric':'Standard Circuit Breaker',
                 'HasGarage': 'Property has Garage', 
                 'HasCentralAir': "Home has Central Air", 
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
                 'GrLivArea': 'Total living space in Sqft',
                 'OverallQual':'Overall Home Quality Ranking', 
                 'SalePrice':'Price of Sale', 
                 'HasAlley':'Property connected to Alley'}

def summary_table(test):
    """This function:
        - takes a df and converts it to a nicely saved table
         
        Parameters
        ----------
        test : df
            df of summary stats I want to convert to image
        
        Returns
        -------
        file_name.png : saves image of converted value_counts output"""
    caption_txt = "Comparison of Model Performance Metrics"
    
    # Formats the css and html to make it look nice
    
    improved = test.style.format({'Training R2': '{:.2%}','Testing R2':'{:.2%}' ,'Training MAE ':'${:,.2f}' ,'Testing MAE': '${:,.2f}'}).set_table_attributes('style="border-collapse:collapse"').set_table_styles([tb_styles, th_styles,td_styles,tr_odds, tr_evens, cap_style]).set_caption(caption_txt)


    # Renders the html
    html = improved.render()

    file_name = "summary_stats"
    # Renders the html & saves as image
    path = './images/'+file_name+'.png'
    imgkit.from_string(html, path, options=options)

    # Crops the image
    
    ## PIL opens image
    im = Image.open(path)
    
    ## Inverts the colors of the image, because getbbox looks for black boundaries, not white ones
    inverted = ImageOps.invert(im.convert('RGB'))
    
    ## Get the automated boundaries box from the inverted file
    boxed = inverted.getbbox()
    
    ## Slaps those crop boundaries on the orginal image
    cropped_image=im.crop(boxed)

    # BAM, saves the cropped image file over the orignal
    cropped_image.save(path)
    pass

def coefficient_table(test):
    test_df2 = test.copy()
    test_df2['two'] = test_df2.index.map(map_var_names)
    test_df2.set_index('two', inplace=True)
    del test_df2.index.name
    
    caption_txt = 'Impact of Home Variables on Sale Price'
    improved = test_df2.sort_values(by='Coefficients').tail(10).style.format("${:,.2f}").set_table_attributes('style="border-collapse:collapse"').set_table_styles([tb_styles, th_styles,td_styles,tr_odds, tr_evens, cap_style]).set_caption(caption_txt)
    
    
    # Renders the html
    html = improved.render()

    file_name = "model_coefficients"
    # Renders the html & saves as image
    path = './images/'+file_name+'.png'
    imgkit.from_string(html, path, options=options)

    # Crops the image
    
    ## PIL opens image
    im = Image.open(path)
    
    ## Inverts the colors of the image, because getbbox looks for black boundaries, not white ones
    inverted = ImageOps.invert(im.convert('RGB'))
    
    ## Get the automated boundaries box from the inverted file
    boxed = inverted.getbbox()
    
    ## Slaps those crop boundaries on the orginal image
    cropped_image=im.crop(boxed)

    # BAM, saves the cropped image file over the orignal
    cropped_image.save(path)
    
    # try to make white transparent
    img = Image.open(path)
    img = img.convert("RGBA")
    pixdata = img.load()
    
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    img.save(path, "PNG")
    
    pass

