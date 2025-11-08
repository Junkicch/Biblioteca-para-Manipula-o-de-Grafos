import argparse
import os
from grafo import Grafo

def unique_filename(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    i = 1
    while True:
        new_path = f"{base}_{i}{ext}"
        if not os.path.exists(new_path):
            return new_path
        i += 1

def main():
    p = argparse.ArgumentParser(description="Runner para Grafo")
    p.add_argument("-i","--input", required=True, help="arquivo de entrada (edge list)")
    p.add_argument("-r","--repr", choices=["lista","matriz"], default="lista")
    p.add_argument("-a","--actions", nargs="+", choices=["info","bfs","dfs","components","memory","degree","diameter","time"], default=["info"])
    p.add_argument("-s","--start", type=int, default=1, help="vértice inicial (1-based)")
    args = p.parse_args()

    resultados_dir = os.path.join(os.path.dirname(args.input) or ".", "resultados")
    os.makedirs(resultados_dir, exist_ok=True)

    g = Grafo.ler_arquivo(args.input, representacao=args.repr)
    base = os.path.splitext(os.path.basename(args.input))[0]

    if "info" in args.actions:
        out = os.path.join(resultados_dir, f"{base}_info.txt")
        out = unique_filename(out)
        g.salvar_info(out)
        print("info ->", out)

    if "bfs" in args.actions:
        out = os.path.join(resultados_dir, f"{base}_bfs.txt")
        out = unique_filename(out)
        g.busca_largura(args.start - 1, out)
        print("bfs ->", out)

    if "dfs" in args.actions:
        out = os.path.join(resultados_dir, f"{base}_dfs.txt")
        out = unique_filename(out)
        g.busca_profundidade(args.start - 1, out)
        print("dfs ->", out)

    if "components" in args.actions:
        out = os.path.join(resultados_dir, f"{base}_components.txt")
        out = unique_filename(out)
        g.componentes_conexos(out)
        print("components ->", out)

    if "memory" in args.actions:
        mat_mb, lst_mb = g.estimate_memory_mb()
        print(f"estimativa memória (MB) -> matriz: {mat_mb:.3f}, lista: {lst_mb:.3f}")

    if "degree" in args.actions:
        mx, mn, _ = g.degree_stats()
        print("grau max:", mx, "grau min:", mn)

    if "diameter" in args.actions:
        d, v = g.diameter_by_bfs()
        print("diâmetro (BFS all):", d, "vértice:", v+1)

    if "time" in args.actions:
        t = g.medir_bfs(args.start - 1)
        print("tempo BFS (s):", round(t,3))

if __name__ == "__main__":
    main()
