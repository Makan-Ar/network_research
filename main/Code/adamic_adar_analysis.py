import sys
import helpers as h
import networkx as nx
import numpy as np


def get_nodes_of_formed_and_non_formed_edges_between_ego_and_second_hop(current_snapshot, next_snapshot, ego_node):
    current_snap_first_hop_nodes = set(current_snapshot.neighbors(ego_node))

    current_snap_second_hop_nodes = set(current_snapshot.nodes()) - current_snap_first_hop_nodes
    current_snap_second_hop_nodes.remove(ego_node)

    next_snap_first_hop_nodes = set(next_snapshot.neighbors(ego_node))

    formed_edges_nodes_with_second_hop = next_snap_first_hop_nodes.intersection(current_snap_second_hop_nodes)

    not_formed_edges_nodes_with_second_hop = current_snap_second_hop_nodes - formed_edges_nodes_with_second_hop

    return formed_edges_nodes_with_second_hop, not_formed_edges_nodes_with_second_hop


def run_hop_global_degree_analysis(ego_net_snapshots, ego_node, ego_net_num, save_plot=False, plot_save_path=''):

    # Exit if plot should be saved, put there is no path
    if save_plot and plot_save_path == '':
        print(sys.stderr, "Please provide the path to which plots should be saved.")
        sys.exit(1)

    mfem = []
    mnfem = []

    # degree_formed_in_snapshots = []
    # degree_not_formed_in_snapshots = []
    # num_nodes_in_snapshots = []

    # only goes up to one to last snap, since it compares every snap with the next one, to find formed edges.
    # for i in range(len(ego_net_snapshots) - 1):
    # for i in range(6, len(ego_net_snapshots) - 1):
    for i in range(0, 5):
        if nx.degree(ego_net_snapshots[i], ego_node) < 30:
            continue

        formed_edges_nodes_with_second_hop, not_formed_edges_nodes_with_second_hop = \
            get_nodes_of_formed_and_non_formed_edges_between_ego_and_second_hop(ego_net_snapshots[i],
                                                                                ego_net_snapshots[i + 1], ego_node)

        if len(formed_edges_nodes_with_second_hop) == 0:
            continue

        # <editor-fold desc="Analyze formed edges">
        # List of degrees of nodes in the second hop which formed an edge with the ego node
        degree_formed = []
        for u in formed_edges_nodes_with_second_hop:
            common_neighbors = nx.common_neighbors(ego_net_snapshots[i], u, ego_node)
            temp_degree_formed = []

            for c in common_neighbors:
                temp_degree_formed.append(nx.degree(ego_net_snapshots[i], c))

            degree_formed.append(np.mean(temp_degree_formed))
        # </editor-fold>
        # <editor-fold desc="Analyze not formed edges">
        # List of degrees of nodes in the second hop which did not form an edge with the ego node
        degree_not_formed = []
        for u in not_formed_edges_nodes_with_second_hop:
            common_neighbors = nx.common_neighbors(ego_net_snapshots[i], u, ego_node)
            temp_degree_not_formed = []

            for c in common_neighbors:
                temp_degree_not_formed.append(nx.degree(ego_net_snapshots[i], c))

            degree_not_formed.append(np.mean(temp_degree_not_formed))
        # </editor-fold>

        if len(degree_formed) != 0 and len(degree_not_formed) != 0:
            snap_len = len(ego_net_snapshots[i])
            mfem.append(np.mean(degree_formed) / snap_len)
            mnfem.append(np.mean(degree_not_formed) / snap_len)
            # degree_formed_in_snapshots.append(degree_formed)
            # degree_not_formed_in_snapshots.append(degree_not_formed)
            # num_nodes_in_snapshots.append(snap_len)

    # if len(degree_formed_in_snapshots) != 0:
    #     if save_plot:
    #         plot_save_path += '/ego_net_%d_global_degree.png' % ego_net_num
    #
    #     mfem, mnfem = h.plot_formed_vs_not_local_degree(degree_formed_in_snapshots, degree_not_formed_in_snapshots,
    #                                                     num_nodes_in_snapshots, ego_net_num,
    #                                                     save_plot=save_plot, save_path=plot_save_path)

    if len(mfem) > 0:
        # print("Graph analyzed! {0}".format(ego_net_num))
        return np.mean(mfem), np.mean(mnfem)

    # print("Graph analyzed! {0}".format(ego_net_num))
    return 0, 0
