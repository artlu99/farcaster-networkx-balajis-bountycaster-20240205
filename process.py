import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from datetime import datetime
from time import time
from tqdm import tqdm

from utils.constants import ATTRIBUTION_TEXT
from utils.db import get_mutuals
from utils.timing import timer

MAX_FID_WHILE_DEBUGGING = 50


@timer
def generate_symmetric_graph(max_fid, fid_start_range, fid_end_range):
    G = nx.Graph()
    for fid in tqdm(range(1, max_fid + 1), desc="adding nodes from 1 to max_fid", leave=False):
        G.add_node(fid)
    for fid in tqdm(range(fid_start_range, fid_end_range + 1),
                    desc='adding edges for fids {} to {}'.format(
                        fid_start_range, fid_end_range),
                    leave=False):
        mutuals = get_mutuals(fid)  # symmetric relationships only
        for m in tqdm(mutuals, desc='edges for mutuals', leave=False):
            G.add_edge(fid, m)

    return G


if __name__ == '__main__':
    # simple networkx analysis adapted from https://www.datacamp.com/tutorial/social-network-analysis-python

    max_fid = min(max(get_mutuals(3)), MAX_FID_WHILE_DEBUGGING)
    print(f'generating graph for {max_fid} fids')

    # generate graph
    G, exec_time = generate_symmetric_graph(max_fid, 1, max_fid)
    print("graph has {} nodes and {} edges".format(
        G.number_of_nodes(), G.number_of_edges()))
    print("[graph generation took : {:.1f}s]".format(exec_time))

    # calculate clustering coefficient
    cc_t1 = time()
    cc = nx.average_clustering(G)
    cc_t2 = time()
    print("clustering coefficient: {:.2f}".format(cc))
    print("[cluster coefficient calculation took {:.1f}s]".format(
        cc_t2 - cc_t1))

    # draw graph in networkx
    print("starting to draw graph (this may take a long time, e.g., 1 minute for 100 fids)...")
    d_t1 = time()
    pos = nx.spring_layout(G)
    betCent = nx.betweenness_centrality(G, normalized=True, endpoints=True)
    node_size = [v * 10000 for v in betCent.values()]
    nx.draw_networkx(G, pos=pos, node_size=node_size, with_labels=False)
    plt.axis('off')
    plt.title("symmetric networkx graph of {} Farcaster fids".format(max_fid))
    plt.text(0.5, 0.5, ATTRIBUTION_TEXT,
             fontsize=16, color='gray', alpha=0.5,
             ha='center', va='bottom')
    d_t2 = time()

    most_central_fids = sorted(betCent, key=betCent.get, reverse=True)
    fid_centrality = pd.DataFrame(most_central_fids, columns=[
                                  'fid, by most central first'])

    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    plt.savefig('out/plot-{}.png'.format(ts))

    print("[drawing graph for {} fids took {:.1f}s]".format(max_fid, d_t2 - d_t1))
    print(fid_centrality.head())
