import networkx as nx
from scipy.special import xlogy
from collections import defaultdict
import numpy as np
import multiprocessing as mp


def _compute_community_entropy(G, partition, community, volume):
    """
    Compute the entropy contribution of a single community.
    """
    nodes = [node for node, comm in partition.items() if comm == community]
    subgraph = G.subgraph(nodes)

    # Internal volume: sum of the degrees of nodes within the community
    internal_volume = sum(dict(subgraph.degree()).values())

    # External volume: total volume minus internal volume
    external_volume = volume - internal_volume

    # Calculate probabilities
    p = internal_volume / volume if volume > 0 else 0
    q = external_volume / volume if volume > 0 else 0

    entropy = 0
    # Compute entropy contribution if probabilities are non-zero
    if p > 0:
        entropy -= xlogy(p, p)
    if q > 0:
        entropy -= xlogy(q, q)

    # Cross-community edges: count edges between nodes in this community and others
    external_edges = 0
    for node in nodes:
        external_edges += sum(
            1 for neighbor in G.neighbors(node) if partition[neighbor] != community
        )

    # Adjust entropy based on external edges
    if external_edges > 0:
        external_probability = external_edges / (2 * G.number_of_edges())
        entropy -= xlogy(external_probability, external_probability)

    return entropy


def compute_structural_entropy_mp(G, partition):
    """
    Compute the structural entropy of a graph partition.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    partition : dict
        A dictionary mapping node labels to community labels

    Returns
    -------
    float
        The structural entropy of the partition
    """
    volume = sum(dict(G.degree()).values())
    communities = set(partition.values())

    # Use multiprocessing to compute entropy for each community in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            _compute_community_entropy,
            [(G, partition, community, volume) for community in communities],
        )

    # Sum up the entropy contributions from all communities
    total_entropy = sum(results)

    return total_entropy


def compute_structural_entropy(G, partition):
    """
    Compute the structural entropy of a graph partition.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    partition : dict
        A dictionary mapping node labels to community labels

    Returns
    -------
    float
        The structural entropy of the partition
    """
    volume = sum(dict(G.degree()).values())
    entropy = 0
    # Loop over each community
    for community in set(partition.values()):
        nodes = [node for node, comm in partition.items() if comm == community]
        subgraph = G.subgraph(nodes)

        # Internal volume: sum of the degrees of nodes within the community
        internal_volume = sum(dict(subgraph.degree()).values())

        # External volume: total volume minus internal volume
        external_volume = volume - internal_volume

        # Calculate probabilities
        p = internal_volume / volume if volume > 0 else 0
        q = external_volume / volume if volume > 0 else 0

        # Compute entropy contribution if probabilities are non-zero
        if p > 0:
            entropy -= xlogy(p, p)
        if q > 0:
            entropy -= xlogy(q, q)

        # Cross-community edges: count edges between nodes in this community and others
        external_edges = 0
        for node in nodes:
            external_edges += sum(
                1 for neighbor in G.neighbors(node) if partition[neighbor] != community
            )

        # Adjust entropy based on external edges
        if external_edges > 0:
            external_probability = external_edges / (2 * G.number_of_edges())
            entropy -= xlogy(external_probability, external_probability)

    return entropy


def _swap_entropy(G, partition, node_i, node_j, initial_entropy):
    """
    Helper function to compute the entropy after swapping two nodes.
    """
    partition[node_i], partition[node_j] = partition[node_j], partition[node_i]
    new_entropy = compute_structural_entropy(G, partition)
    entropy_gain = initial_entropy - new_entropy
    partition[node_i], partition[node_j] = (
        partition[node_j],
        partition[node_i],
    )  # Revert swap
    return (entropy_gain, node_i, node_j)


def _kernighan_lin(G, initial_partition, max_iterations: int = 100):
    """
    Refine the partition using the Kernighan-Lin algorithm.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    initial_partition : dict
        The initial partition mapping nodes to community labels.
    max_iterations : int, optional
        Maximum number of iterations (default is 100).

    Returns
    -------
    dict
        The refined partition.
    """
    nodes = list(G.nodes())
    partition = initial_partition.copy()
    initial_entropy = compute_structural_entropy(G, initial_partition)

    for _ in range(max_iterations):
        improved = False
        gains = []
        best_partition = partition.copy()
        best_entropy = initial_entropy

        # Create a multiprocessing pool to parallelize swaps
        with mp.Pool(processes=mp.cpu_count()) as pool:
            swap_results = pool.starmap(
                _swap_entropy,
                [
                    (G, partition, nodes[i], nodes[j], initial_entropy)
                    for i in range(len(nodes))
                    for j in range(i + 1, len(nodes))
                    if partition[nodes[i]] != partition[nodes[j]]
                ],
            )

        # Process the swap results
        for entropy_gain, node_i, node_j in swap_results:
            if entropy_gain > 0:
                gains.append((entropy_gain, node_i, node_j))

        # If no improvements, break early
        if not gains:
            break

        # Find the best swap
        best_gain, best_i, best_j = max(gains, key=lambda x: x[0])

        # Apply the best swap
        partition[best_i], partition[best_j] = partition[best_j], partition[best_i]
        best_entropy -= best_gain
        best_partition = partition.copy()  # Update the best partition
        improved = True

        if not improved:
            break

    return best_partition


def _two_way_partition(G, max_iterations=100):
    # Initial partition: spectral bisection
    laplacian = nx.laplacian_matrix(G)
    eigenvalues, eigenvectors = np.linalg.eigh(laplacian.toarray())
    fiedler_vector = eigenvectors[:, 1]
    initial_partition = {
        node: 0 if fiedler_vector[i] >= 0 else 1 for i, node in enumerate(G.nodes())
    }

    # Refine the partition using Kernighan-Lin algorithm
    refined_partition = _kernighan_lin(G, initial_partition, max_iterations)

    return refined_partition


def _recursive_partition(
    G,
    level=0,
    entropy_threshold=0.01,
    max_depth=10,
    max_iterations=100,
    min_community_size=2,
):
    if G.number_of_nodes() <= min_community_size or level >= max_depth:
        return {node: f"{level}.0" for node in G.nodes()}

    partition = _two_way_partition(G, max_iterations)

    original_entropy = compute_structural_entropy(G, {node: 0 for node in G.nodes()})
    new_entropy = compute_structural_entropy(G, partition)

    if new_entropy >= original_entropy - entropy_threshold:
        return partition

    subgraphs = [
        G.subgraph([node for node, part in partition.items() if part == i])
        for i in set(partition.values())
    ]

    for i, subgraph in enumerate(subgraphs):
        # Only continue partitioning if the subgraph size is above the minimum threshold
        if subgraph.number_of_nodes() > min_community_size:
            sub_partition = _recursive_partition(
                subgraph, level + 1, entropy_threshold, max_depth, max_iterations
            )
            for node, sub_comm in sub_partition.items():
                partition[node] = f"{i}.{sub_comm}"
        else:
            # Assign a unique label if subgraph is too small to partition further
            for node in subgraph.nodes():
                partition[node] = f"{i}.0"

    return partition


def _merge_node(G, partition, small_communities, node):
    comm = partition[node]
    if comm in small_communities:
        neighbors = list(G.neighbors(node))
        neighbor_comms = [
            partition[neigh]
            for neigh in neighbors
            if partition[neigh] not in small_communities
        ]
        if neighbor_comms:
            return node, max(set(neighbor_comms), key=neighbor_comms.count)
    return node, comm


def _merge_small_communities(G, partition, size_threshold=5):
    community_sizes = defaultdict(int)
    for comm in partition.values():
        community_sizes[comm] += 1

    small_communities = [
        comm for comm, size in community_sizes.items() if size < size_threshold
    ]

    # Use multiprocessing to merge small communities in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            _merge_node, [(G, partition, small_communities, node) for node in G.nodes()]
        )

    # Update the partition based on the results
    for node, new_comm in results:
        partition[node] = new_comm

    return partition


def _optimize_node(G, partition, node):
    current_community = partition[node]
    neighbor_comms = defaultdict(float)
    for neighbor in G.neighbors(node):
        neighbor_comm = partition[neighbor]
        edge_weight = G[node][neighbor].get(
            "weight", 1
        )  # Use edge weight if present, otherwise assume 1
        neighbor_comms[neighbor_comm] += edge_weight

    best_community = max(
        neighbor_comms, key=neighbor_comms.get, default=current_community
    )

    if best_community != current_community:
        original_partition = partition.copy()
        partition[node] = best_community
        old_entropy = compute_structural_entropy(G, original_partition)
        new_entropy = compute_structural_entropy(G, partition)

        if new_entropy > old_entropy:
            return node, current_community
        return node, best_community

    return node, current_community


def _optimize_boundary_nodes(G, partition):
    """
    Optimize the boundary nodes by reassigning them to their most appropriate community,
    considering both the number and strength of connections to neighboring communities.

    Parameters
    ----------
    G : networkx.Graph
        The input graph.
    partition : dict
        The current partition mapping nodes to community labels.

    Returns
    -------
    dict
        The optimized partition.
    """
    # Use multiprocessing to optimize boundary nodes in parallel
    # Use multiprocessing to optimize boundary nodes in parallel
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(
            _optimize_node, [(G, partition, node) for node in G.nodes()]
        )

    # Update the partition based on the results
    for node, new_comm in results:
        partition[node] = new_comm

    return partition


def community_detection(
    G,
    size_threshold=5,
    entropy_threshold=0.001,
    max_depth=15,
    max_iterations=100,
    minimum_community_size=2,
):
    """
    Detect communities in a graph based on structural entropy minimizing.

    Parameters
    ----------
    G : networkx.Graph
        The input graph
    level : int, optional
        The current level of recursion, by default 0
    entropy_threshold : float, optional
        Minimum improvement in entropy to continue partitioning, by default 0.01
    size_threshold : int, optional
        Communities with fewer nodes than this threshold will be merged with their neighbors, by default 5
    max_depth : int, optional
        Maximum depth of recursion for partitioning, by default 10
    max_iterations : int, optional
        Maximum number of iterations for the Kernighan-Lin algorithm, by default 100

    Returns
    -------
    dict
        A dictionary mapping node labels to community labels
    """
    partition = _recursive_partition(
        G, 0, entropy_threshold, max_depth, max_iterations, minimum_community_size
    )

    # Merge small communities
    partition = _merge_small_communities(G, partition, size_threshold)

    # Optimize boundary nodes
    partition = _optimize_boundary_nodes(G, partition)

    # Convert hierarchical labels to flat numeric labels
    unique_labels = sorted(set(partition.values()))
    label_map = {label: i for i, label in enumerate(unique_labels)}
    return {node: label_map[partition[node]] for node in G.nodes()}
