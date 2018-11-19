import io
import random

import networkx as nx
import matplotlib.pyplot as plt

from dijkstra_path import dijkstra_path


def draw_graph():
    plt.figure(figsize=(16, 8), dpi=80)

    # -------------------------------------------
    # Сгенерируем граф, например квадратную сетку со случайными весами ребер

    G = nx.grid_2d_graph(5, 5)
    for u, v in G.edges(): G.edges[u, v]['weight'] = random.randint(1, 10)

    # -------------------------------------------
    # Определим имена начального и конечного узла

    nlist = list(G.nodes)

    for i, n in enumerate(nlist):
        G.nodes[n]['index'] = i

    N = len(nlist)
    ns = nlist[0]
    nt = nlist[N - 1]

    # Apply color for source and target nodes

    G.node[ns]['color'] = 'g'
    G.node[nt]['color'] = 'b'

    # -------------------------------------------
    # Найдем кратчайший путь в графе, сначала используя встроенный алгоритм библиотеки

    path1 = nx.dijkstra_path(G, ns, nt)
    # print('nx.dijkstra_path:', path1)

    # -------------------------------------------
    # Теперь используем наш алгоритм

    # Сначала надо построить список связанности, т.к. наш алгоритм работает именно с ним

    g = [[] for _ in range(len(nlist))]
    for u, v, w in G.edges.data('weight'):
        ui = G.nodes[u]['index']
        vi = G.nodes[v]['index']
        g[ui].append((vi, w))
        g[vi].append((ui, w))

    # print(g)

    path = dijkstra_path(g, 0, N - 1)

    # превратим индексы обратно в имена нод
    path = [nlist[p] for p in path]

    # print('   dijkstra_path:', path)

    for u, v in zip(path, path[1:]):
        G.edges[u, v]['path'] = True

    # -------------------------------------------
    # Нарисуем граф

    pos = nx.spring_layout(G)

    nx.draw(
        G, pos,
        node_color=[G.node[n].get('color', 'r') for n in G.nodes()],
        edge_color=[['lightgray', 'lime'][bool(G.edges[u, v].get('path'))] for u, v in G.edges()],
        width=[[1, 5][bool(G.edges[u, v].get('path'))] for u, v in G.edges()],
    )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))


def result():
    draw_graph()

    # -------------------------------------------
    # Отдадим рисунок серверу

    with io.BytesIO() as f:
        plt.savefig(f, format='png')
        return 200, 'image/png', f.getvalue()


if __name__ == "__main__":
    draw_graph()
    # plt.savefig('test.png')
    plt.show()
