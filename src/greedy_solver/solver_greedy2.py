import time

def parse_instance(file_path):
    """(Copia a mesma função parse_instance do outro ficheiro aqui)"""
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

def solve_greedy_removal(rectangles, num_vars):
    """
    Estratégia Greedy por Remoção:
    1. Começa com todos os guardas ativos.
    2. Remove iterativamente o guarda "mais redundante".
    """
    # 1. Estruturas de dados iniciais
    active_guards = set(range(num_vars))
    
    # vertex_to_rects: que retângulos o vértice V vê?
    vertex_to_rects = {i: set() for i in range(num_vars)}
    
    # rect_coverage_count: quantos guardas estão a vigiar o retângulo R neste momento?
    rect_coverage_count = {r: 0 for r in range(len(rectangles))}
    
    for rect_idx, rect in enumerate(rectangles):
        for v in rect:
            vertex_to_rects[v].add(rect_idx)
            rect_coverage_count[rect_idx] += 1
            
    # 2. Ciclo de Remoção
    changed = True
    while changed:
        changed = False
        best_guard_to_remove = None
        max_redundancy = -1
        
        # Avaliar cada guarda que ainda está ativo
        for g in active_guards:
            can_remove = True
            
            # Verificar se podemos remover o guarda 'g'
            # (Só podemos se todos os retângulos que ele vê tiverem > 1 guarda atual)
            for r in vertex_to_rects[g]:
                if rect_coverage_count[r] <= 1:
                    can_remove = False
                    break
            
            if can_remove:
                # Se podemos remover, calculamos o quão "redundante" ele é.
                # Exemplo de heurística: somar as coberturas atuais dos retângulos que ele vê.
                redundancy_score = sum(rect_coverage_count[r] for r in vertex_to_rects[g])
                
                if redundancy_score > max_redundancy:
                    max_redundancy = redundancy_score
                    best_guard_to_remove = g
                    
        # Se encontrámos um guarda que pode ser removido, removemos o melhor
        if best_guard_to_remove is not None:
            active_guards.remove(best_guard_to_remove)
            
            # Atualizar a contagem de vigilância dos retângulos afetados
            for r in vertex_to_rects[best_guard_to_remove]:
                rect_coverage_count[r] -= 1
                
            changed = True # Continuar o ciclo
            
    return list(active_guards)

if __name__ == "__main__":
    # target_file = '../../data/examples/step50'
    target_file = '../../data/examples/parts40'
    
    print(f"--- A processar com Greedy por Remoção: {target_file} ---")
    rects, n_vars = parse_instance(target_file)
    
    if rects:
        start_time = time.time()
        solution = solve_greedy_removal(rects, n_vars)
        total_time = time.time() - start_time
        
        print(f"\n--- RESUMO GREEDY REMOÇÃO ---")
        print(f"Total de guardas mantidos: {len(solution)}")
        print(f"Tempo decorrido: {total_time:.5f}s")