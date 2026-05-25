import time

def parse_instance(file_path):
    """Lê a instância utilizando o mesmo parser da Estudante 2."""
    try:
        with open(file_path, 'r') as f:
            n_inst = int(f.readline().strip())
            num_rects = int(f.readline().strip())
            
            rectangles = []
            coord_to_id = {}
            next_id = 0
            
            for _ in range(num_rects):
                line = f.readline().split()
                if not line: break
                # Formato: ID N_VERT X1 Y1 X2 Y2...
                coords = line[2:]
                current_rect = []
                for i in range(0, len(coords), 2):
                    pt = (coords[i], coords[i+1])
                    if pt not in coord_to_id:
                        coord_to_id[pt] = next_id
                        next_id += 1
                    current_rect.append(coord_to_id[pt])
                rectangles.append(current_rect)
            return rectangles, next_id
    except Exception as e:
        print(f"Erro na leitura: {e}")
        return None, None

def solve_greedy(rectangles, num_vars):
    """
    Resolve o problema usando uma heurística Greedy:
    A cada passo, escolhe o vértice que cobre o maior número de retângulos ainda não vigiados.
    """
    # 1. Mapeamento Inverso: Para cada vértice, guardar os índices dos retângulos que ele cobre
    vertex_to_rects = {i: set() for i in range(num_vars)}
    for rect_idx, rect in enumerate(rectangles):
        for v in rect:
            vertex_to_rects[v].add(rect_idx)
            
    # 2. Inicializar o conjunto de retângulos que ainda precisam de cobertura
    uncovered_rects = set(range(len(rectangles)))
    
    guards_placed = []
    
    # 3. Ciclo Greedy
    while uncovered_rects:
        best_vertex = None
        max_covered_count = 0
        best_vertex_coverage = set()
        
        # Procurar o vértice que cobre mais retângulos não vigiados
        for v in range(num_vars):
            # Interseção entre o que o vértice vê e o que ainda falta cobrir
            covered_by_v = vertex_to_rects[v].intersection(uncovered_rects)
            
            if len(covered_by_v) > max_covered_count:
                max_covered_count = len(covered_by_v)
                best_vertex = v
                best_vertex_coverage = covered_by_v
                
        # Adicionar o melhor vértice à solução
        guards_placed.append(best_vertex)
        
        # Remover os retângulos que este novo guarda cobre da lista de "não vigiados"
        uncovered_rects -= best_vertex_coverage
        
    return guards_placed

if __name__ == "__main__":
    # Define o ficheiro a testar
    # target_file = '../../data/examples/step50'
    target_file = '../../data/examples/parts40'
    
    print(f"--- A processar com Algoritmo Greedy: {target_file} ---")
    rects, n_vars = parse_instance(target_file)
    
    if rects:
        print(f"Dados: {len(rects)} retângulos, {n_vars} vértices únicos.")
        
        start_time = time.time()
        
        # Executar a estratégia Greedy
        solution = solve_greedy(rects, n_vars)
        
        total_time = time.time() - start_time
        
        print(f"\n--- RESUMO GREEDY ---")
        print(f"Total de guardas colocados: {len(solution)}")
        # print(f"IDs dos guardas: {solution}") # Descomenta se quiseres ver exatamente onde estão
        print(f"Tempo decorrido: {total_time:.5f}s")