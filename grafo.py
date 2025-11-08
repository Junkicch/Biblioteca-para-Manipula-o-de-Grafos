import time
from collections import deque, defaultdict

class Grafo:
    def __init__(self, num_vertices, representacao="lista"):
        self.num_vertices = num_vertices
        self.num_arestas = 0
        self.representacao = representacao.lower()

        if self.representacao == "matriz":
            self.matriz = [[0] * num_vertices for _ in range(num_vertices)]
            self.lista = None
        else:
            self.lista = defaultdict(list)
            self.matriz = None

    # ======= Adicionar Aresta =======
    def adicionar_aresta(self, v1, v2):
        if self.representacao == "matriz":
            self.matriz[v1][v2] = 1
            self.matriz[v2][v1] = 1
        else:
            self.lista[v1].append(v2)
            self.lista[v2].append(v1)
        self.num_arestas += 1

    # ======= Ler Grafo de Arquivo =======
    @classmethod
    def ler_arquivo(cls, nome_arquivo, representacao="lista"):
        with open(nome_arquivo, "r") as arq:
            linhas = [linha.strip() for linha in arq.readlines() if linha.strip()]

        num_vertices = int(linhas[0])
        g = cls(num_vertices, representacao)

        for linha in linhas[1:]:
            v1, v2 = map(int, linha.split())
            g.adicionar_aresta(v1 - 1, v2 - 1)

        return g

    # ======= Salvar informações básicas =======
    def salvar_info(self, nome_arquivo):
        with open(nome_arquivo, "w") as arq:
            arq.write(f"Número de vértices: {self.num_vertices}\n")
            arq.write(f"Número de arestas: {self.num_arestas}\n\n")

            arq.write("Grau de cada vértice:\n")
            for v in range(self.num_vertices):
                grau = self.grau(v)
                arq.write(f"Vértice {v+1}: grau = {grau}\n")

    # ======= Grau =======
    def grau(self, v):
        if self.representacao == "matriz":
            return sum(self.matriz[v])
        else:
            return len(self.lista[v])

    # ======= Impressão =======
    def imprimir(self):
        if self.representacao == "matriz":
            print("Matriz de Adjacência:")
            for linha in self.matriz:
                print(linha)
        else:
            print("Lista de Adjacência:")
            for v in range(self.num_vertices):
                print(f"{v+1} -> {[x+1 for x in self.lista[v]]}")

    # ======= Busca em Largura (BFS) =======
    def busca_largura(self, inicio, nome_arquivo):
        visitado = [False] * self.num_vertices
        pai = [-1] * self.num_vertices
        nivel = [-1] * self.num_vertices

        fila = deque([inicio])
        visitado[inicio] = True
        nivel[inicio] = 0

        while fila:
            v = fila.popleft()
            vizinhos = (
                [i for i, ligado in enumerate(self.matriz[v]) if ligado]
                if self.representacao == "matriz"
                else self.lista[v]
            )
            for u in vizinhos:
                if not visitado[u]:
                    visitado[u] = True
                    pai[u] = v
                    nivel[u] = nivel[v] + 1
                    fila.append(u)

        with open(nome_arquivo, "w") as arq:
            arq.write("Vértice\tPai\tNível\n")
            for i in range(self.num_vertices):
                arq.write(f"{i+1}\t{pai[i]+1 if pai[i]!=-1 else '-'}\t{nivel[i]}\n")

        return pai, nivel

    # ======= Busca em Profundidade (DFS) =======
    def busca_profundidade(self, inicio, nome_arquivo):
        visitado = [False] * self.num_vertices
        pai = [-1] * self.num_vertices
        nivel = [-1] * self.num_vertices

        def dfs(v, n):
            visitado[v] = True
            nivel[v] = n
            vizinhos = (
                [i for i, ligado in enumerate(self.matriz[v]) if ligado]
                if self.representacao == "matriz"
                else self.lista[v]
            )
            for u in vizinhos:
                if not visitado[u]:
                    pai[u] = v
                    dfs(u, n + 1)

        dfs(inicio, 0)

        with open(nome_arquivo, "w") as arq:
            arq.write("Vértice\tPai\tNível\n")
            for i in range(self.num_vertices):
                arq.write(f"{i+1}\t{pai[i]+1 if pai[i]!=-1 else '-'}\t{nivel[i]}\n")

        return pai, nivel

    # ======= Componentes Conexos =======
    def componentes_conexos(self, nome_arquivo):
        visitado = [False] * self.num_vertices
        componentes = []
        
        for v in range(self.num_vertices):
            if not visitado[v]:
                fila = deque([v])
                componente = []
                visitado[v] = True
                while fila:
                    u = fila.popleft()
                    componente.append(u)
                    vizinhos = (
                        [i for i, ligado in enumerate(self.matriz[u]) if ligado]
                        if self.representacao == "matriz"
                        else self.lista[u]
                    )
                    for w in vizinhos:
                        if not visitado[w]:
                            visitado[w] = True
                            fila.append(w)
                componentes.append(componente)

        with open(nome_arquivo, "w") as arq:
            arq.write("Componentes Conexos:\n\n")
            for i, c in enumerate(componentes, 1):
                arq.write(f"Componente {i}: {[v+1 for v in c]}\n")
            arq.write(f"\nTotal de componentes: {len(componentes)}\n")

        return componentes

    # ======= Medição de tempo e memória (opcional) =======
    def medir_bfs(self, inicio=0):
        inicio_tempo = time.time()
        self.busca_largura(inicio, "/dev/null")
        return time.time() - inicio_tempo

    # ======= Estimativas / utilitários adicionais =======
    def estimate_memory_mb(self):
        """Estimativa teórica (MB) de memória para cada representação.
        Matriz: n*n bytes (assumindo 1 byte por entrada).
        Lista: 2*m * 4 bytes (assumindo int32 por vizinho).
        Retorna (matriz_mb, lista_mb).
        """
        n = self.num_vertices
        m = self.num_arestas
        matriz_bytes = n * n  # 1 byte por entrada (teórico)
        lista_bytes = max(0, 2 * m * 4)  # 4 bytes por inteiro (teórico)
        mb = 1024 * 1024
        return matriz_bytes / mb, lista_bytes / mb

    def degree_stats(self):
        """Retorna (max_deg, min_deg, degrees_list)."""
        degrees = [self.grau(v) for v in range(self.num_vertices)]
        return max(degrees), min(degrees), degrees

    def _bfs_levels(self, inicio):
        """BFS interna que retorna lista de níveis (nivel[v] = distância ou -1)."""
        n = self.num_vertices
        nivel = [-1] * n
        visitado = [False] * n
        fila = deque([inicio])
        visitado[inicio] = True
        nivel[inicio] = 0
        while fila:
            v = fila.popleft()
            vizinhos = (
                [i for i, ligado in enumerate(self.matriz[v]) if ligado]
                if self.representacao == "matriz"
                else self.lista[v]
            )
            for u in vizinhos:
                if not visitado[u]:
                    visitado[u] = True
                    nivel[u] = nivel[v] + 1
                    fila.append(u)
        return nivel

    def diameter_by_bfs(self):
        """Computa o diâmetro do grafo aplicando BFS a partir de todos os vértices.
        Retorna (diameter, vertex_with_max_distance).
        Aviso: O(n*(n+m)) — caro para grafos grandes.
        """
        best = 0
        best_v = 0
        for v in range(self.num_vertices):
            levels = self._bfs_levels(v)
            maxlvl = max([lv for lv in levels if lv is not None and lv >= 0] or [0])
            if maxlvl > best:
                best = maxlvl
                best_v = v
        return best, best_v
