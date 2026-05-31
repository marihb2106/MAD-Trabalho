import time

def parse_instance(file_path):
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

def solve_dp(rectangles, num_vars, limit_rects=15):
    """
    Avaliação de Programação Dinâmica usando Bitmask.
    limit_rects: Para evitar a explosão combinatória (2^N estados),
    resolvemos apenas um subconjunto do problema para provar o conceito.
    """

    target_rects = min(len(rectangles), limit_rects)
    
    vertex_masks = [0] * num_vars
    for rect_idx in range(target_rects):
        for v in rectangles[rect_idx]:
            vertex_masks[v] |= (1 << rect_idx)
            
    target_mask = (1 << target_rects) - 1 
    
    INF = float('inf')
    dp = [INF] * (target_mask + 1)
    
    # estado base: 0 guardas para cobrir 0 retângulos
    dp[0] = 0
    
    for mask in range(target_mask + 1):
        if dp[mask] == INF:
            continue 
            
        for v_mask in vertex_masks:
            if v_mask == 0: continue 
            
            next_mask = mask | v_mask
            
            if dp[mask] + 1 < dp[next_mask]:
                dp[next_mask] = dp[mask] + 1
                
    return dp[target_mask], target_rects

if __name__ == "__main__":
    # target_file = '../../data/examples/step50'
    target_file = '../../data/examples/parts40'

    print(f"--- A processar Programação Dinâmica: {target_file} ---")
    rects, n_vars = parse_instance(target_file)
    
    if rects:
        # testar cobrir apenas os primeiros 18 retângulos do ficheiro
        limite = 18
        
        start_time = time.time()
        min_guards, rects_processed = solve_dp(rects, n_vars, limit_rects=limite)
        total_time = time.time() - start_time
        
        print(f"\n--- RESUMO DA PROGRAMAÇÃO DINÂMICA ---")
        print(f"Retângulos processados: {rects_processed} (de {len(rects)})")
        print(f"Número mínimo (ótimo) de guardas: {min_guards}")
        print(f"Tempo decorrido: {total_time:.5f}s")