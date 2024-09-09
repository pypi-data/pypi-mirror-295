from collections import deque
from typing import List, Callable, Any, Tuple
import math

class CompetitiveProgrammingLib:
    @staticmethod
    def sieve_of_eratosthenes(n: int) -> List[int]:
        """
        Generate a list of prime numbers up to n using the Sieve of Eratosthenes.
        
        :param n: Upper limit for prime numbers
        :return: List of prime numbers
        """
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(n**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, n + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, n + 1) if sieve[i]]

    @staticmethod
    def dfs(graph: dict, start: Any, visited: set = None) -> List[Any]:
        """
        Perform Depth-First Search on a graph.
        
        :param graph: Dictionary representing the graph
        :param start: Starting node
        :param visited: Set of visited nodes (used for recursion)
        :return: List of nodes in DFS order
        """
        if visited is None:
            visited = set()
        
        visited.add(start)
        result = [start]
        
        for neighbor in graph.get(start, []):
            if neighbor not in visited:
                result.extend(CompetitiveProgrammingLib.dfs(graph, neighbor, visited))
        
        return result

    @staticmethod
    def bfs(graph: dict, start: Any) -> List[Any]:
        """
        Perform Breadth-First Search on a graph.
        
        :param graph: Dictionary representing the graph
        :param start: Starting node
        :return: List of nodes in BFS order
        """
        visited = set()
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                queue.extend(neighbor for neighbor in graph.get(node, []) if neighbor not in visited)
        
        return result

    @staticmethod
    def binary_search(arr: List[Any], target: Any) -> int:
        """
        Perform Binary Search on a sorted array.
        
        :param arr: Sorted array to search in
        :param target: Value to search for
        :return: Index of the target if found, -1 otherwise
        """
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1

    @staticmethod
    def quicksort(arr: List[Any]) -> List[Any]:
        """
        Sort an array using the Quicksort algorithm.
        
        :param arr: Array to be sorted
        :return: Sorted array
        """
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return CompetitiveProgrammingLib.quicksort(left) + middle + CompetitiveProgrammingLib.quicksort(right)

    @staticmethod
    def knapsack(values: List[int], weights: List[int], capacity: int) -> int:
        """
        Solve the 0/1 Knapsack problem using dynamic programming.
        
        :param values: List of item values
        :param weights: List of item weights
        :param capacity: Knapsack capacity
        :return: Maximum value that can be achieved
        """
        n = len(values)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(1, capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
                else:
                    dp[i][w] = dp[i-1][w]
        
        return dp[n][capacity]

    @staticmethod
    def longest_common_subsequence(s1: str, s2: str) -> str:
        """
        Find the Longest Common Subsequence of two strings.
        
        :param s1: First string
        :param s2: Second string
        :return: Longest Common Subsequence
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Reconstruct the LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if s1[i-1] == s2[j-1]:
                lcs.append(s1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))
    
    @staticmethod
    def dijkstra(graph: dict, start: Any) -> Tuple[dict, dict]:
        """
        Perform Dijkstra's algorithm for finding shortest paths.
        
        :param graph: Dictionary representing the weighted graph
        :param start: Starting node
        :return: Tuple of (distances, predecessors)
        """
        distances = {node: float('inf') for node in graph}
        distances[start] = 0
        predecessors = {node: None for node in graph}
        pq = [(0, start)]
        
        while pq:
            current_distance, current_node = min(pq)
            pq.remove((current_distance, current_node))
            
            if current_distance > distances[current_node]:
                continue
            
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    pq.append((distance, neighbor))
        
        return distances, predecessors

    @staticmethod
    def bellman_ford(graph: List[Tuple[Any, Any, int]], V: int, start: Any) -> Tuple[dict, dict]:
        """
        Perform Bellman-Ford algorithm for finding shortest paths with negative edges.
        
        :param graph: List of edges (u, v, weight)
        :param V: Number of vertices
        :param start: Starting node
        :return: Tuple of (distances, predecessors)
        """
        distances = {node: float('inf') for node in range(V)}
        distances[start] = 0
        predecessors = {node: None for node in range(V)}
        
        for _ in range(V - 1):
            for u, v, w in graph:
                if distances[u] != float('inf') and distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
        
        # Check for negative-weight cycles
        for u, v, w in graph:
            if distances[u] != float('inf') and distances[u] + w < distances[v]:
                raise ValueError("Graph contains a negative-weight cycle")
        
        return distances, predecessors

    @staticmethod
    def floyd_warshall(graph: List[List[int]]) -> List[List[int]]:
        """
        Perform Floyd-Warshall algorithm for all-pairs shortest paths.
        
        :param graph: 2D list representing the graph (INF for no edge)
        :return: 2D list of shortest distances between all pairs of vertices
        """
        V = len(graph)
        dist = [row[:] for row in graph]
        
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
        
        return dist

    @staticmethod
    def kruskal(graph: List[Tuple[Any, Any, int]], V: int) -> List[Tuple[Any, Any, int]]:
        """
        Perform Kruskal's algorithm for finding Minimum Spanning Tree.
        
        :param graph: List of edges (u, v, weight)
        :param V: Number of vertices
        :return: List of edges in the Minimum Spanning Tree
        """
        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])
        
        def union(parent, rank, x, y):
            xroot = find(parent, x)
            yroot = find(parent, y)
            if rank[xroot] < rank[yroot]:
                parent[xroot] = yroot
            elif rank[xroot] > rank[yroot]:
                parent[yroot] = xroot
            else:
                parent[yroot] = xroot
                rank[xroot] += 1
        
        result = []
        i, e = 0, 0
        graph = sorted(graph, key=lambda item: item[2])
        parent = list(range(V))
        rank = [0] * V
        
        while e < V - 1:
            u, v, w = graph[i]
            i += 1
            x = find(parent, u)
            y = find(parent, v)
            if x != y:
                e += 1
                result.append((u, v, w))
                union(parent, rank, x, y)
        
        return result

    @staticmethod
    def trie_insert(trie: dict, word: str) -> None:
        """
        Insert a word into a trie.
        
        :param trie: The trie dictionary
        :param word: Word to insert
        """
        for char in word:
            trie = trie.setdefault(char, {})
        trie['#'] = '#'  # Mark end of word

    @staticmethod
    def trie_search(trie: dict, word: str) -> bool:
        """
        Search for a word in a trie.
        
        :param trie: The trie dictionary
        :param word: Word to search
        :return: True if word is found, False otherwise
        """
        for char in word:
            if char not in trie:
                return False
            trie = trie[char]
        return '#' in trie

    @staticmethod
    def segment_tree_build(arr: List[int]) -> List[int]:
        """
        Build a segment tree for range sum queries.
        
        :param arr: Input array
        :return: Segment tree as a list
        """
        n = len(arr)
        tree = [0] * (4 * n)
        
        def build(node, start, end):
            if start == end:
                tree[node] = arr[start]
                return
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            tree[node] = tree[2 * node] + tree[2 * node + 1]
        
        build(1, 0, n - 1)
        return tree

    @staticmethod
    def segment_tree_query(tree: List[int], n: int, l: int, r: int) -> int:
        """
        Query the segment tree for range sum.
        
        :param tree: Segment tree
        :param n: Length of the original array
        :param l: Left bound of the query (inclusive)
        :param r: Right bound of the query (inclusive)
        :return: Sum of the range [l, r]
        """
        def query(node, start, end, l, r):
            if r < start or end < l:
                return 0
            if l <= start and end <= r:
                return tree[node]
            mid = (start + end) // 2
            return (query(2 * node, start, mid, l, r) +
                    query(2 * node + 1, mid + 1, end, l, r))
        
        return query(1, 0, n - 1, l, r)

    @staticmethod
    def segment_tree_update(tree: List[int], n: int, index: int, value: int) -> None:
        """
        Update a value in the segment tree.
        
        :param tree: Segment tree
        :param n: Length of the original array
        :param index: Index to update
        :param value: New value
        """
        def update(node, start, end, index, value):
            if start == end:
                tree[node] = value
                return
            mid = (start + end) // 2
            if index <= mid:
                update(2 * node, start, mid, index, value)
            else:
                update(2 * node + 1, mid + 1, end, index, value)
            tree[node] = tree[2 * node] + tree[2 * node + 1]
        
        update(1, 0, n - 1, index, value)

    @staticmethod
    def tarjan_scc(graph: dict) -> List[List[Any]]:
        """
        Find Strongly Connected Components using Tarjan's algorithm.
        
        :param graph: Dictionary representing the graph
        :return: List of Strongly Connected Components
        """
        index = 0
        stack = []
        on_stack = set()
        indices = {}
        lowlinks = {}
        sccs = []
        
        def strongconnect(v):
            nonlocal index
            indices[v] = index
            lowlinks[v] = index
            index += 1
            stack.append(v)
            on_stack.add(v)
            
            for w in graph.get(v, []):
                if w not in indices:
                    strongconnect(w)
                    lowlinks[v] = min(lowlinks[v], lowlinks[w])
                elif w in on_stack:
                    lowlinks[v] = min(lowlinks[v], indices[w])
            
            if lowlinks[v] == indices[v]:
                scc = []
                while True:
                    w = stack.pop()
                    on_stack.remove(w)
                    scc.append(w)
                    if w == v:
                        break
                sccs.append(scc)
        
        for v in graph:
            if v not in indices:
                strongconnect(v)
        
        return sccs

    @staticmethod
    def suffix_array(s: str) -> List[int]:
        """
        Construct a suffix array for a string.
        
        :param s: Input string
        :return: Suffix array
        """
        n = len(s)
        sa = list(range(n))
        rank = [ord(c) for c in s]
        tmp = [0] * n
        k = 1
        
        while k < n:
            sa.sort(key=lambda i: (rank[i], rank[i+k] if i+k < n else -1))
            tmp[sa[0]] = 0
            for i in range(1, n):
                tmp[sa[i]] = tmp[sa[i-1]] + (
                    (rank[sa[i]], rank[sa[i]+k] if sa[i]+k < n else -1) >
                    (rank[sa[i-1]], rank[sa[i-1]+k] if sa[i-1]+k < n else -1)
                )
            rank = tmp[:]
            k *= 2
        
        return sa

    @staticmethod
    def lca_build(graph: dict, root: Any) -> Tuple[List[List[Any]], List[int], List[int]]:
        """
        Build data structures for LCA (Lowest Common Ancestor) queries using binary lifting.
        
        :param graph: Dictionary representing the tree
        :param root: Root node of the tree
        :return: Tuple of (parent table, depths, first occurrence)
        """
        n = len(graph)
        log_n = math.ceil(math.log2(n))
        parent = [[None] * n for _ in range(log_n)]
        depth = [0] * n
        first_occurrence = [0] * n
        visited = [False] * n
        
        def dfs(node, d):
            nonlocal time
            visited[node] = True
            depth[node] = d
            first_occurrence[node] = time
            time += 1
            
            for child in graph[node]:
                if not visited[child]:
                    parent[0][child] = node
                    dfs(child, d + 1)
        
        time = 0
        dfs(root, 0)
        
        for i in range(1, log_n):
            for j in range(n):
                if parent[i-1][j] is not None:
                    parent[i][j] = parent[i-1][parent[i-1][j]]
        
        return parent, depth, first_occurrence

    @staticmethod
    def lca_query(parent: List[List[Any]], depth: List[int], u: Any, v: Any) -> Any:
        """
        Query for the Lowest Common Ancestor of two nodes.
        
        :param parent: Parent table from lca_build
        :param depth: Depth list from lca_build
        :param u: First node
        :param v: Second node
        :return: Lowest Common Ancestor of u and v
        """
        if depth[u] < depth[v]:
            u, v = v, u
        
        log_n = len(parent)
        for i in range(log_n - 1, -1, -1):
            if depth[u] - (1 << i) >= depth[v]:
                u = parent[i][u]
        
        if u == v:
            return u
        
        for i in range(log_n - 1, -1, -1):
            if parent[i][u] != parent[i][v]:
                u = parent[i][u]
                v = parent[i][v]
        
        return parent[0][u]