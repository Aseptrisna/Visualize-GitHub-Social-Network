import pandas as pd

edges = pd.read_csv("github_edges_1.csv")
edges.head(10)
edges = edges.astype(str)
nodes = pd.read_csv("github_target_1.csv")
nodes.head(10)
# print(nodes)
nodes.id = nodes.id.astype(str)
nodes.ml_target = nodes.ml_target.astype(str)
percent_web, percent_ml = nodes.ml_target.value_counts(normalize=True)
import plotly.express as px

px.histogram(data_frame=nodes, x="ml_target", histnorm="probability density")
edges = edges.merge(nodes, how="left", left_on="id_1", right_on="id").merge(
    nodes, how="left", left_on="id_2", right_on="id", suffixes=("1", "2")
)[["id_1", "id_2", "name1", "name2", "ml_target1", "ml_target2"]]
edges.head(10)
# print(edges)
cross_edge = edges.query("ml_target1 != ml_target2")
percentage_cross_edge = cross_edge.shape[0] / edges.shape[0]
percentage_cross_edge

percentage_df = pd.DataFrame(
    [
        ["mixed_connection", percentage_cross_edge],
        ["same_connection", 1 - percentage_cross_edge],
    ],
    columns=["connection_type", "percentage"],
)
percentage_df
px.bar(percentage_df, x="connection_type", y="percentage")
percentage_cross_edge / percent_ml
percentage_cross_edge / percent_web
import graphistry
from dotenv import load_dotenv
import os
load_dotenv()
PASSWORD = os.getenv("GRAPHISTRY_PASSWORD")
USERNAME = os.getenv("GRAPHISTRY_USERNAME")

graphistry.register(api=3, username=USERNAME, password=PASSWORD)
g = graphistry.edges(edges, "id_1", "id_2")
g = g.nodes(nodes, "id").encode_point_icon(
    "ml_target", categorical_mapping={1: "area-chart", 0: "mouse-pointer"}
)
g.plot()
g2 = g.encode_point_color("ml_target", categorical_mapping={1: "silver", 0: "maroon"})
g2.plot()

import cudf
import cugraph
from cugraph.community.louvain import louvain
G = cugraph.from_pandas_edgelist(edges, "id_1", "id_2")
parts, modularity_score = cugraph.louvain(G)
parts.head(10)
parts.partition.unique().values
nodes_cudf = cudf.from_pandas(nodes)
nodes_part = nodes_cudf.merge(parts, how="left", left_on="id", right_on="vertex")
nodes_part.head(10)