import argparse
import os
from grafo import Grafo

os.makedirs("resultados", exist_ok=True)

p = argparse.ArgumentParser()
p.add_argument("-i", "--input", default="entrada.txt", help="arquivo de entrada")
p.add_argument("-r", "--repr", choices=["lista", "matriz"], default="lista")
p.add_argument("-s", "--start", type=int, default=1, help="vértice inicial (1-based)")
p.add_argument("-a", "--actions", nargs="+", choices=["info","bfs","dfs","components"], default=["info","bfs","dfs","components"])
args = p.parse_args()

g = Grafo.ler_arquivo(args.input, representacao=args.repr)
if "info" in args.actions:
    g.salvar_info("resultados/info.txt")
if "bfs" in args.actions:
    g.busca_largura(args.start - 1, "resultados/bfs.txt")
if "dfs" in args.actions:
    g.busca_profundidade(args.start - 1, "resultados/dfs.txt")
if "components" in args.actions:
    g.componentes_conexos("resultados/componentes.txt")

print("Arquivos de saída gerados em resultados/")
