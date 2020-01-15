# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 19:30:14 2020

@author: cansu
"""


import pandas as pd
df = pd.read_csv( r"tester.csv" )

#range_limit: search radius
#n_neighbors: number of neighbors
#field: field to be used for IDW
def idw( df , row , range_limit , n_neighbors , field  ):
    
    row = row.to_frame().transpose()
    df = df[ df.index != row.index.tolist()[0] ].copy() #Avoid self
    s = gpd.GeoSeries( row.geometry )
    s = s.repeat( len(df) )
    s.index = [i for i in df.index ]
    df['Dist'] = df.geometry.distance( s ) #Calculate distance to all points
    df = df[ df.Dist < range_limit ] #Limit by Distance
    if len( df.index) != 0: #If the object has neighbors
        df = df.sort_values('Dist', ascending= True )[:n_neighbors] #Sort by distance and get first N
        if df['Dist'].sum() != 0: 
            weighted_avg = np.average( df[ field ] , weights= 1 / df['Dist'] ) #Get weighted average
            return ( round( weighted_avg,2 ) )  
        else:
            return None
    else:
        return None


df[ 'idw' ] = df.apply( lambda x: idw( df , x , 400 , 32 , 'field' ) , axis = 1  )
