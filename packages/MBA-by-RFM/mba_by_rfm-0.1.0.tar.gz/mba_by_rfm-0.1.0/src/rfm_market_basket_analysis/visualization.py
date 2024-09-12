import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import networkx as nx
import pandas as pd


def plot_rfm_segments(RFM):
    RFM['Segments'].value_counts().head(10).plot(kind='bar', title='RFM top 10 Segments')
    plt.show()
    
def transactions_graph(df):
    ax = pd.to_datetime(df['Date']).dt.month.value_counts().plot(kind='bar',figsize=(12,5),title='Number of Transactions per Month')
    for container in ax.containers:
        ax.bar_label(container)
        
    plt.show()

def plot_association_rules(rules_df, top_n=15):
    top_rules = rules_df.nlargest(top_n, 'confidence')
    apriori_heatmap_data = top_rules.pivot_table(index='antecedents', columns='consequents', values='confidence', fill_value=0)
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(apriori_heatmap_data, annot=True, cmap='YlGnBu', linewidths=0.5)
    plt.title('Top 15 Association Rules Heatmap')
    plt.xlabel('Consequents')
    plt.ylabel('Antecedents')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.show()

def plot_network_graph(rules_df, top_n=15):
    rules_df_copy = rules_df.copy(deep=True)

    top_rules = rules_df_copy.nlargest(top_n, 'confidence')
    G = nx.DiGraph()

    for _, row in top_rules.iterrows():
        # Convert lists to strings by joining them with commas or other delimiters
        antecedents = ', '.join(row['antecedents']) if isinstance(row['antecedents'], (list, set)) else row['antecedents']
        consequents = ', '.join(row['consequents']) if isinstance(row['consequents'], (list, set)) else row['consequents']
        
        G.add_node(antecedents, color='blue')
        G.add_node(consequents, color='red')
        G.add_edge(antecedents, consequents, weight=row['confidence'])

    pos = nx.spring_layout(G, seed=42)
    nodes = list(G.nodes)
    edges = list(G.edges)

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        hovertext=[],
        mode='markers',
        marker=dict(size=10, color=[], colorscale='Viridis', colorbar=dict(thickness=15, title='Node Color', xanchor='left', titleside='right')),
        textposition='top center'
    )

    for edge in edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    for node in nodes:
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['text'] += (node,)
        node_trace['hovertext'] += (node,)
        node_trace['marker']['color'] += (G.nodes[node].get('color', 'blue'),)

    fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                         showlegend=False,
                         xaxis=dict(showgrid=False, zeroline=False),
                         yaxis=dict(showgrid=False, zeroline=False),
                         hovermode='closest',
                         annotations=[
                             dict(
                                 x=1.05, y=1.1,
                                 xref='paper', yref='paper',
                                 text='Blue nodes: Antecedents<br>Red nodes: Consequents',
                                 showarrow=False,
                                 font=dict(size=12, color='black'),
                                 align='left'
                             )
                         ]
                     ))
    fig.update_layout(title='Top 15 Association Rules Network Diagram')
    fig.show()