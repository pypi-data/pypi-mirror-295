import pandas as pd
from .rfm_analysis import calculate_rfm
from .association_rules import apriori_association_rules,fpgrowth_association_rules
from .visualization import plot_rfm_segments, plot_association_rules, plot_network_graph,transactions_graph
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from IPython.display import display
from mlxtend.frequent_patterns import association_rules


from collections import defaultdict
from itertools import combinations
def get_eclat_support(df, min_support=0.001):
    item_sets = defaultdict(list)
    for index, row in df.iterrows():
        for item in row.index[row == 1]:
            item_sets[frozenset([item])].append(index)
    
    eclat_result = {itemset: len(indices) / len(df) for itemset, indices in item_sets.items() if len(indices) / len(df) >= min_support}
    return eclat_result

def eclat_func(df, min_support=0.001):
    eclat_result = get_eclat_support(df, min_support)
    k = 2
    while True:
        new_eclat_result = {}
        itemsets = list(eclat_result.keys())
        for i in range(len(itemsets)):
            for j in range(i+1, len(itemsets)):
                itemset1, itemset2 = itemsets[i], itemsets[j]
                union_set = itemset1.union(itemset2)
                if len(union_set) == k:
                    indices1 = set(df.index[df[list(itemset1)].all(axis=1)])
                    indices2 = set(df.index[df[list(itemset2)].all(axis=1)])
                    intersection_indices = indices1.intersection(indices2)
                    support = len(intersection_indices) / len(df)
                    if support >= min_support:
                        new_eclat_result[union_set] = support
        if not new_eclat_result:
            break
        eclat_result.update(new_eclat_result)
        k += 1
    return eclat_result
from mlxtend.frequent_patterns import apriori

def eclat_to_association_rules(eclat_itemsets_df, min_confidence=0.06):
    rules = []
    for _, row in eclat_itemsets_df.iterrows():
        items = list(row['itemsets'])
        support = row['support']
        for i in range(1, len(items)):
            antecedents = frozenset(items[:i])
            consequents = frozenset(items[i:])
            antecedent_support = eclat_itemsets_df.loc[eclat_itemsets_df['itemsets'] == antecedents, 'support']
            consequent_support = eclat_itemsets_df.loc[eclat_itemsets_df['itemsets'] == consequents, 'support']
            if not antecedent_support.empty and not consequent_support.empty:
                antecedent_support = antecedent_support.values[0]
                consequent_support = consequent_support.values[0]
                confidence = support / antecedent_support
                if confidence >= min_confidence:
                    rules.append({
                        'antecedents': ', '.join(list(antecedents)),
                        'consequents': ', '.join(list(consequents)),
                        'antecedent support': antecedent_support,
                        'consequent support': consequent_support,
                        'support': support,
                        'confidence': confidence,
                        'lift': (support / (antecedent_support * consequent_support)),
                        'leverage': (support - (antecedent_support * consequent_support)),
                        'conviction': (1 - consequent_support) / (1 - confidence) if confidence < 1 else None,
                    })
    return pd.DataFrame(rules)
    

def main(df):
    
    # Clean and preprocess data (Example: remove missing values, filter data)
    df.info()
    df.describe()
    df.isnull().sum()
    df[df['Description'].isnull()]
    df.dropna(subset=['CustomerID'], inplace=True)
    df[df['Description'].isnull()]
    df.isnull().sum()
    df.describe()
    df = df[(df['Quantity']>0) & (df['UnitPrice']>0)]
    df.describe()
    print("We have" , df.duplicated().sum(), "duplicates")
    df[df.duplicated()].head()
    df = df.drop_duplicates()
    print("We now have" , df.duplicated().sum(), "duplicates")
    df.describe()
    fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,6))
    ax1 = sns.scatterplot(data=df['Quantity'], ax=ax1)
    ax2 = sns.scatterplot(data=df['UnitPrice'], ax=ax2)
    plt.tight_layout()
    df[(df['UnitPrice']>5000) | (df['Quantity']>50000)]
    df = df[(df['UnitPrice']<5000) & (df['Quantity']<50000)]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))
    ax1 = sns.scatterplot(data=df['Quantity'], ax=ax1)
    ax2 = sns.scatterplot(data=df['UnitPrice'], ax=ax2)
    plt.tight_layout()
    df['Total'] = df['Quantity'] * df['UnitPrice']
        
    # Step 2: Calculate RFM
    RFM = calculate_rfm(df)
    print("RFM Calculation Complete")
    print(RFM.head())   
    
    sns.set_style('whitegrid')
    ax = RFM['Group'].value_counts().sort_values().plot(kind='barh',figsize=(10,5), title='Number of Customers')
    for container in ax.containers:
        ax.bar_label(container)
    plt.show()
    new_df = pd.merge(df,RFM,on='CustomerID')
    new_df.head()
    
    ax = new_df.groupby('Group').agg(count = ("CustomerID","nunique")).sort_values('count').plot(kind='barh',figsize=(10,5))

    for container in ax.containers:
        ax.bar_label(container)
        
    plt.show()
    
    Gold_df = new_df[new_df['Group']=='Gold']
    Silver_df = new_df[new_df['Group']=='Silver']
    Bronze_df = new_df[new_df['Group']=='Bronze']
    
    Gold_df['Month'] = pd.to_datetime(Gold_df['Date']).dt.month
    Gold_df.groupby(['Month','Description']).agg(count=('Quantity','count')).sort_values(by='count').groupby(level=0).tail(1)
    
    transactions_graph(Gold_df)
    countries = pd.DataFrame(Gold_df['Country'].value_counts().head(5)).reset_index()

    countries.columns = ['Country','Count']

    px.bar(data_frame=countries, x='Country',y='Count').update_layout(title_text='Top 5 countries', title_x=0.5).update_xaxes(tickangle=90)
    Gold_df.groupby(['InvoiceNo','Description'])['Quantity'].sum()
    Gold_df.groupby(['InvoiceNo','Description'])['Quantity'].sum().unstack()
    Gold_df.groupby(['InvoiceNo','Description'])['Quantity'].sum().unstack().reset_index().fillna(0)
    Gold_set = Gold_df.groupby(['InvoiceNo','Description'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceNo').astype(int)
    print(Gold_set)
    Gold_set.drop(columns=['POSTAGE'],inplace=True)
    golden_set = Gold_set.copy()
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    
    # Step 3: Generate Association Rules with Apriori
    apriori_rules = apriori_association_rules(Gold_set)
    print("Apriori Association Rules Calculation Complete")
    print(apriori_rules)
    print('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # Step 4: Generate Association Rules with FP-Growth
    fpgrowth_rules = fpgrowth_association_rules(Gold_set)
    print("FP-Growth Association Rules Calculation Complete")
    print(fpgrowth_rules)
    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    
    # Step 5: Generate Association Rules with ECLAT
    print('ECLAT Association rules start here')
    eclat_itemsets = eclat_func(Gold_set, min_support=0.007)
    print(eclat_itemsets)
    eclat_itemsets_df = pd.DataFrame(list(eclat_itemsets.items()), columns=['itemsets', 'support'])
    print(eclat_itemsets_df)
    eclat_rules_df = eclat_to_association_rules(eclat_itemsets_df, min_confidence=0.007)
    print(eclat_rules_df)
    if not eclat_rules_df.empty:
        eclat_rules_df['size_of_consequents'] = eclat_rules_df['consequents'].apply(lambda x: len(x.split(',')))
        display(eclat_rules_df[eclat_rules_df['size_of_consequents'] > 2].sort_values(by='confidence', ascending=False).head(3))
    else:
        print("No ECLAT rules found.")
    
    

  
# Step 6: Plot Visualizations
    plot_rfm_segments(RFM)
    print("RFM Segments Plot Complete")
    
    plot_association_rules(apriori_rules)
    print("Apriori Association Rules Plot Complete")
    
    plot_association_rules(fpgrowth_rules)
    print("FP Growth Association Rules Plot Complete")
    
    plot_association_rules(eclat_rules_df)
    print("Eclat Association Rules Plot Complete")
    print(eclat_rules_df)
    
    plot_network_graph(apriori_rules)
    print("Association Rules Network Graph for Apriori Plot Complete")
    
    plot_network_graph(fpgrowth_rules)
    print("Association Rules Network Graph for FP Growth Plot Complete")
    
    plot_network_graph(eclat_rules_df)
    print("Association Rules Network Graph for Eclat Plot Complete")
    print(eclat_rules_df)
    
    # Extract top 15 rules for each algorithm
    top_apriori_rules = apriori_rules.sort_values(by='confidence', ascending=False).head(5)
    top_fpgrowth_rules = fpgrowth_rules.sort_values(by='confidence', ascending=False).head(5)
    top_eclat_rules = eclat_rules_df.sort_values(by='confidence', ascending=False).head(5)

    # Prepare data for the bar charts
    # Prepare data for the bar charts
    def prepare_data(rules_df):
        def convert_rule(rule):
          antecedent_str = ', '.join(list(rule["antecedents"])) if isinstance(rule["antecedents"], frozenset) else str(rule["antecedents"])
          consequent_str = ', '.join(list(rule["consequents"])) if isinstance(rule["consequents"], frozenset) else str(rule["consequents"])
          return f'{antecedent_str} → {consequent_str}'

        return {
            'Rule': [convert_rule(rule) for _, rule in rules_df.iterrows()],
            'Support': rules_df['support'],
            'Confidence': rules_df['confidence'],
            'Lift': rules_df['lift']
        }

    apriori_data = prepare_data(top_apriori_rules)
    fpgrowth_data = prepare_data(top_fpgrowth_rules)
    eclat_data = prepare_data(top_eclat_rules)



    # Create subplots for comparison
    fig, axs = plt.subplots(3, 3, figsize=(18, 18), sharex='col')

    # Bar charts for Apriori
    axs[0, 0].barh(apriori_data['Rule'], apriori_data['Support'], color='skyblue')
    axs[0, 0].set_title('Apriori - Support')
    axs[0, 1].barh(apriori_data['Rule'], apriori_data['Confidence'], color='lightgreen')
    axs[0, 1].set_title('Apriori - Confidence')
    axs[0, 1].yaxis.set_visible(False)  # Hide the entire y-axis

    axs[0, 2].barh(apriori_data['Rule'], apriori_data['Lift'], color='salmon')
    axs[0, 2].set_title('Apriori - Lift')
    axs[0, 2].yaxis.set_visible(False)

    # Bar charts for FP-Growth
    axs[1, 0].barh(fpgrowth_data['Rule'], fpgrowth_data['Support'], color='skyblue')
    axs[1, 0].set_title('FP-Growth - Support')
    axs[1, 1].barh(fpgrowth_data['Rule'], fpgrowth_data['Confidence'], color='lightgreen')
    axs[1, 1].set_yticklabels([])
    axs[1, 1].set_title('FP-Growth - Confidence')
    axs[1, 2].barh(fpgrowth_data['Rule'], fpgrowth_data['Lift'], color='salmon')
    axs[1, 2].set_title('FP-Growth - Lift')
    axs[1, 2].set_yticklabels([])


    axs[2, 0].barh(eclat_data['Rule'], eclat_data['Support'], color='skyblue')
    axs[2, 0].set_title('ECLAT - Support')
    axs[2, 1].barh(eclat_data['Rule'], eclat_data['Confidence'], color='lightgreen')
    axs[2, 1].set_title('ECLAT - Confidence')
    axs[2, 1].yaxis.set_visible(False)
    axs[2, 2].barh(eclat_data['Rule'], eclat_data['Lift'], color='salmon')
    axs[2, 2].set_title('ECLAT - Lift')
    axs[2, 2].yaxis.set_visible(False)

    fig.tight_layout()
    fig.suptitle('Rule Comparison Dashboard', fontsize=16, y=1.02)
    plt.show()

if __name__ == "__main__":
    example_df = pd.read_csv("data.csv",encoding='ISO-8859-1')  # Load an example DataFrame from a CSV file
    main(example_df)
    