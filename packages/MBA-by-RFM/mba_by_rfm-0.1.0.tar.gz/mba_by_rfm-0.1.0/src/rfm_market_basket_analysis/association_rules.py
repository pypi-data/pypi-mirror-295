import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth
from IPython.display import display


def apriori_association_rules(df, min_support=0.01, min_confidence=0.06):
    frequent_gold_itemsets = apriori(df.astype('bool'), min_support=0.01,use_colnames=True,verbose=1)
    frequent_gold_itemsets.sort_values(by='support',ascending=False).head(10)
    frequent_gold_itemsets['size'] = frequent_gold_itemsets['itemsets'].apply(lambda x : len(x))
    apriori_rules = association_rules(frequent_gold_itemsets, metric="confidence", min_threshold=0.06)
    apriori_rules = association_rules(frequent_gold_itemsets, metric="confidence", min_threshold=0.06)
    apriori_rules['size_of_consequents'] = apriori_rules['consequents'].apply(lambda x: len(x))
    display(apriori_rules[apriori_rules['size_of_consequents'] > 2].sort_values(by='confidence', ascending=False).head(3))
    
    return apriori_rules

def fpgrowth_association_rules(df, min_support=0.01, min_confidence=0.06):
    df_bool = df.astype('bool')
    frequent_itemsets_fp = fpgrowth(df_bool, min_support=min_support, use_colnames=True)
    frequent_itemsets_fp['size'] = frequent_itemsets_fp['itemsets'].apply(lambda x: len(x))
    fpgrowth_rules = association_rules(frequent_itemsets_fp, metric="confidence", min_threshold=min_confidence)
    fpgrowth_rules['size_of_consequents'] = fpgrowth_rules['consequents'].apply(lambda x: len(x))
    filtered_rules = fpgrowth_rules[fpgrowth_rules['size_of_consequents'] > 2].sort_values(by='confidence', ascending=False).head(5)
    display(filtered_rules)
    return filtered_rules