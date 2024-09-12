import pandas as pd
import datetime
import matplotlib.pyplot as plt

def calculate_rfm(df):
    df['Date'] = pd.DatetimeIndex(df['InvoiceDate']).date
    df['Time'] = pd.DatetimeIndex(df['InvoiceDate']).time
    snapshot_day = df['Date'].max() + datetime.timedelta(1)
    
    RFM = df.groupby('CustomerID').agg(
        Recency=('Date', lambda x: (snapshot_day - x.max())),
        Frequency=('InvoiceNo', 'count'),
        Monetary=('Total', 'sum')
    )
    
    RFM = df.groupby('CustomerID').agg(Recency=('Date', lambda x: (snapshot_day - x.max())))
    RFM['Recency'] = RFM['Recency'].dt.days.astype(int)
    RFM['Frequency'] = df.groupby('CustomerID').agg(Frequency=('InvoiceNo', 'count')).Frequency
    df['Total'] = df['Quantity'] * df['UnitPrice']
    RFM['Monetary'] = df.groupby('CustomerID').agg(Monetary=('Total','sum'))
    recency_labels = range(4,0,-1) # notice that the lowest value is given the highest ranking. 

    RFM['R_score'] = pd.qcut(RFM['Recency'], q=4,labels=recency_labels)
    Frequency_labels = range(1,5)

    RFM['F_score'] = pd.qcut(RFM['Frequency'], q=4,labels=Frequency_labels)
    Monetary_labels = range(1,5)

    RFM['M_score'] = pd.qcut(RFM['Monetary'], q=4,labels=Monetary_labels)
    RFM['rfm_total_score'] = RFM['R_score'].astype(int)+RFM['F_score'].astype(int)+RFM['M_score'].astype(int)
    RFM_Segments = (RFM['R_score'].astype(str) + '.'+ RFM['F_score'].astype(str)+'.' + RFM['M_score'].astype(str))
    RFM_Segments.value_counts().head(10).plot(kind='bar', title='RFM top 10 Segments')
    plt.show()

    # adding it to the RFM df
    RFM['Segments'] = RFM_Segments
    RFM.groupby('rfm_total_score').agg({
        'Recency':'mean',
        'Frequency':'mean',
        'Monetary':['mean','sum']
    }).astype(int)
    def group_function(df):
        if df['rfm_total_score']>9:
            return'Gold'
        elif (df['rfm_total_score']>5) and (df['rfm_total_score']<= 9):
            return'Silver'
        else:
            return'Bronze'
    RFM['Group']= RFM.apply(group_function,axis=1)
    
    return RFM
