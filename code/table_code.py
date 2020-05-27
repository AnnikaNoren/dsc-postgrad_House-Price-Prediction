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
                     ('border-style','solid'),
                     ('border-width','1px'),
                     ('font-family', 'verdana'),
                     ('white-space', 'nowrap'),
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

options = {'quiet': ''}


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
    
    improved = test.style.format({'Training R2': '{:.2%}','Testing R2':'{:.2%}' ,'Training MAE ':'${:,.2f}' ,'Testing MAE': '${:,.2f}'}).set_table_attributes('style="border-collapse:collapse"').set_table_styles([tb_styles, th_styles,td_styles,cap_style]).set_caption(caption_txt)


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