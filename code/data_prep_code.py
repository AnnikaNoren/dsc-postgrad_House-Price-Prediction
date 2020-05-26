import pandas as pd

def address_nas(df):
    
    # fix alley variable
    df['HasAlley'] = 0
    df.Alley.fillna("not",inplace=True)
    df.loc[(df.Alley.str.contains("Grvl|Pave")), 'HasAlley'] = 1
    df.drop(columns = ['Alley'], inplace=True)
    
    # fix pool variable
    df['HasPool'] = 0
    df.loc[(df.PoolArea > 0), 'HasPool'] = 1
    df.drop(columns = ['PoolArea', 'PoolQC'], inplace=True)
    
    df['HasFence'] = 0
    df.loc[(~df.Fence.isna()), 'HasFence'] = 1
    df.drop(columns = ['Fence'], inplace=True)
    
    df.drop(columns=["MiscFeature"], inplace = True)
    
    df.LotFrontage.fillna(0,inplace=True)
    
    test = df.columns.tolist()
    redundant = [k for k in test if ('Qual' in k or 'Cond' in k) and ("Overall" not in k) and (k!= "SaleCondition")]
    df.drop(columns = redundant, inplace = True )
    
    df['HasFirePlace'] = 0
    df.loc[(df.Fireplaces > 0), 'HasFirePlace'] = 1
    df.drop(columns = ['Fireplaces', 'FireplaceQu'], inplace=True)
    
    df['GarageAreaPerCar'] = df.GarageArea/df.GarageCars
    df['HasGarage'] = 0
    df.loc[(df.GarageArea > 0), 'HasGarage'] = 1
    df.drop(columns = ['GarageArea'], inplace=True)
    
    df['GarageType_u'] = 'Other'
    df.loc[(df.GarageType == 'Attchd'), 'GarageType_u'] = 'Attached'
    df.loc[(df.GarageType == 'Attchd'), 'GarageType_u'] = 'Attached'
    
    return df
