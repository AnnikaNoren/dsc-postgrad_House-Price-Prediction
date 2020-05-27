import pandas as pd
import numpy as np

def address_nas(test):
    ## Drop observations with non-used homes
    df = test[~test.SaleType.isin(['New', 'COD'])].copy()
    df = df[~df.Electrical.isna()]
    
    ## Create new variables
    
    # Fix alley variable
    df['HasAlley'] =np.where((df.Alley.str.contains("Grvl|Pave")), 1,0)

    # Fix pool variable
    df['HasPool'] = np.where((df.PoolArea > 0), 1,0)

    # Fix fence variable
    df['HasFence'] = np.where((~df.Fence.isna()), 1,0)
    
    # Create Has Fire Place
    df['HasFirePlace'] =np.where((df.Fireplaces > 0), 1,0)
    
    # Has porch
    test = df.columns.tolist()
    porch_vars = [k for k in test if 'Porch' in k]
    df['HasPorch'] = 0
    df.loc[df[porch_vars].any(axis='columns'), 'HasPorch']=1
    
    # Has basement
    df['HasBasement'] = np.where((~df.BsmtExposure.isna()), 1,0)
    
    # Create Has Garage
    df['HasGarage'] = np.where((df.GarageArea > 0), 1, 0)
    
    # Create ratio of space per car
    df['GarageAreaPerCar'] = df.GarageArea/df.GarageCars
    
    # create % basement finished
    df['BsmtPerFinished'] = (df.BsmtFinSF1 + df.BsmtFinSF2)/df.TotalBsmtSF
    df.BsmtPerFinished.fillna(0,inplace=True)
    
    # Create condensed version of Garage Type
#     df['GarageType_u'] = 'Other'
#     df.loc[(df.GarageType == 'Attchd'), 'GarageType_u'] = 'Attached'
#     df.loc[(df.GarageType == 'Detchd'), 'GarageType_u'] = 'Detached'
    
    df['HasCentralAir'] = np.where(df.CentralAir=='Y',1,0)
    df['GasAirHeat']  = np.where(df.Heating == 'GasA', 1, 0)
    df['SBboxElectric'] = np.where(df.Electrical == 'SBrkr', 1, 0)
    df['HasDeck'] = np.where(df.WoodDeckSF > 0, 1, 0)
    df['HasRemod'] = np.where(df.YearBuilt==df.YearRemodAdd, 1, 0)
    
    df['HouseAge'] = df.YrSold - df.YearBuilt
    #df['GarageAge'] = df.YrSold -  df.GarageYrBlt
    df['TimeSinceRemodel'] = df.YrSold - df.YearRemodAdd

    df['RemodFiveYrs'] = np.where((df.YearBuilt!=df.YearRemodAdd )&( df.HouseAge > 5) & (df.TimeSinceRemodel <=5),1,0)
    df['GaragebuiltWHouse'] = np.where(df.YearBuilt==df.GarageYrBlt, 1, 0)
    
    ## Fill nas

    df.GarageAreaPerCar.fillna(0, inplace=True)
    df.LotFrontage.fillna(0, inplace=True)
    df.GarageFinish.fillna('Unf', inplace=True)
    df.MasVnrArea.fillna(0, inplace = True)
    
    ## Drop columns
    df.drop(columns = ['Id'], inplace=True)
    df.drop(columns = ['Alley'], inplace=True)
    df.drop(columns = ['GarageType'], inplace=True)
#    df.drop(columns = ['GarageArea'], inplace=True)
    df.drop(columns = ["MiscFeature", "MiscVal"], inplace = True)
    df.drop(columns = ['Fence'], inplace=True)
    df.drop(columns = ['Fireplaces', 'FireplaceQu'], inplace=True)
    df.drop(columns = ['BsmtExposure'], inplace = True)
    df.drop(columns = ['CentralAir', 'Electrical', 'Heating', 'WoodDeckSF'], inplace = True)
    df.drop(columns = ['YearBuilt', 'GarageYrBlt', 'YearRemodAdd'], inplace = True)
    df.drop(columns = ['PoolArea', 'PoolQC'], inplace=True)
    df.drop(columns = ['BsmtFinSF1', 'BsmtFinSF2'], inplace=True)
        
    test = df.columns.tolist()
    redundant = [k for k in test if ('Qual' in k or 'Cond' in k) and ("Overall" not in k) and (k!= "SaleCondition")]
    df.drop(columns = redundant, inplace = True )
    
    test = df.columns.tolist()
    type_col = [k for k in test if 'Type' in k]
    df.drop(columns = type_col, inplace = True )
    
    df.drop(columns = porch_vars, inplace = True)
    
    return df
