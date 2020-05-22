

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
    
    return df
