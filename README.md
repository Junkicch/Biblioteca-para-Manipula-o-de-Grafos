# Biblioteca-para-Manipulação-de-Grafos

- Para iniciar:
    -python main.py -i as_graph.txt -r lista -a info bfs components -s 1
    -python main.py -i collaboration_graph.txt -r lista -a info bfs components -s 1

- O objetivo deste trabalho é projetar e desenvolver uma biblioteca para manipular grafos. A biblioteca deverá ser capaz de representar grafos assim como implementar um conjunto de algoritmos em grafos. Sendo que a biblioteca deve tem ar seguintes funcionalidades:
    - Entrada: A biblioteca deve ser capaz de ler um grafo de um arquivo texto. O formato do grafo no arquivo será o seguinte: a primeira linha informa o número de vértices do grafo. Cada linha subsequente informa as arestas.
    - Saída: A biblioteca deve ser capaz de gerar um arquivo texto com as seguintes informações sobre o grafo: número de vértices, número de arestas, grau de cada vértice.
    - Representação de grafos: A biblioteca deve ser capaz de representar grafos utilizando tanto uma matriz de adjacência, quanto uma lista de adjacência. O usuário da biblioteca (programa que irá usá-la) poderá escolher a representação a ser utilizada.
    -  Busca em grafos: largura e profundidade. A biblioteca deve ser capaz de percorrer o grafo utilizando busca em largura e busca em profundidade. O vértice inicial será dado pelo usuário da biblioteca. A respectiva árvore de busca deve ser gerada assim como o nível de cada vértice na árvore (nível da raiz é zero). Estas informações devem ser impressas em um arquivo. Para descrever a árvore gerada, basta informar o pai de cada vértice e seu nível no arquivo de saída.
    - Componentes conexos: A biblioteca deve ser capaz descobrir os componentes conexos de um grafo. O número de componentes conexas, assim como o tamanho (em vértices) de cada componente e a lista de vértices pertencentes à componente.

- Há dois grafos de exemplo para o teste e verficação das funcionalidades, ao final do processo, será criado um novo diretório com os arquivos de texto de resultado.