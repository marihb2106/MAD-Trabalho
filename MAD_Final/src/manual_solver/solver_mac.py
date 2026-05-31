import sys
import time

# Aumentar o limite de recursão para instâncias maiores
sys.setrecursionlimit(10000)

class MACSolver:
    """
    Classe que resolve o problema de vigilância de retângulos usando 
    Maintaining Arc-Consistency (MAC) com Generalized Arc Consistency (GAC).
    """
    def __init__(self, rectangles, num_vars):
        self.rectangles = rectangles
        self.num_vars = num_vars
        self.best_solution = num_vars + 1 # Inicializar com valor alto
        self.nodes_count = 0
        self.start_time = time.time()
        
        # --- HEURÍSTICA DE ORDENAÇÃO DE VARIÁVEIS ---
        # Contamos em quantos retângulos cada vértice aparece (Grau)
        degree_map = [0] * num_vars
        for r in rectangles:
            for v in r:
                degree_map[v] += 1
        
        # Escolhemos os vértices que cobrem mais retângulos primeiro
        self.order = sorted(range(num_vars), key=lambda x: degree_map[x], reverse=True)
        self.domains = [None] * num_vars

    def gac_consistency(self, domains, current_count):
        """
        Implementação do algoritmo de consistência para restrições n-árias.
        Deduze valores obrigatórios para podar a árvore de procura.
        """
        changed = True
        new_count = current_count
        while changed:
            changed = False
            for rect in self.rectangles:
                # Filtrar vértices que ainda podem ser guardas (não são 0)
                candidates = [v for v in rect if domains[v] != 0]
                
                # Se um retângulo ficar sem candidatos, a solução é impossível
                if not candidates:
                    return False, domains, new_count
                
                # Se sobrar apenas um candidato, ele TEM de ser 1 (Guarda)
                if len(candidates) == 1:
                    v = candidates[0]
                    if domains[v] is None:
                        domains[v] = 1
                        new_count += 1
                        changed = True
        return True, domains, new_count

    def solve(self, order_idx=0, current_guards=0):
        """Executa a busca por Backtracking com poda."""
        self.nodes_count += 1
        
        # Print de progresso a cada 100.000 nós explorados
        if self.nodes_count % 100000 == 0:
            elapsed = time.time() - self.start_time
            print(f"... [Busca] Nós: {self.nodes_count} | Melhor atual: {self.best_solution} | Tempo: {elapsed:.1f}s", flush=True)

        # PODA: Se o custo atual já é pior que o melhor encontrado, pára
        if current_guards >= self.best_solution:
            return

        # SUCESSO: Todas as variáveis foram decididas
        if order_idx == self.num_vars:
            if current_guards < self.best_solution:
                self.best_solution = current_guards
                print(f"\n*** NOVA MELHOR SOLUÇÃO ENCONTRADA: {self.best_solution} guardas ***")
            return

        # Selecionar variável seguindo a heurística
        var_idx = self.order[order_idx]

        # Se o GAC já decidiu esta variável, saltamos para a próxima
        if self.domains[var_idx] is not None:
            self.solve(order_idx + 1, current_guards)
            return

        # Tentar valores: 0 (sem guarda) primeiro para minimizar o custo rápido
        for val in [0, 1]:
            backup = list(self.domains)
            self.domains[var_idx] = val
            
            # Cálculo do custo local
            new_val_count = current_guards + (1 if val == 1 else 0)
            
            # Chamar propagação de restrições (MAC)
            consistent, propagated_domains, final_count = self.gac_consistency(list(self.domains), new_val_count)
            
            if consistent:
                old_state = self.domains
                self.domains = propagated_domains
                self.solve(order_idx + 1, final_count)
                self.domains = old_state
            
            self.domains = backup

def parse_instance(file_path):
    """Lê a primeira instância de um ficheiro de dados da professora."""
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

if __name__ == "__main__":
    # Define o ficheiro a testar
    target_file = '../../data/examples/step50'
    
    print(f"--- A processar: {target_file} ---")
    rects, n_vars = parse_instance(target_file)
    
    if rects:
        solver = MACSolver(rects, n_vars)
        print(f"Dados: {len(rects)} retângulos, {n_vars} vértices únicos.")
        print("Iniciando Procura (Heurística: Maior Grau)...\n")
        
        try:
            solver.solve()
        except KeyboardInterrupt:
            print("\nProcura interrompida pelo utilizador.")
        
        total_time = time.time() - solver.start_time
        print(f"\n--- RESUMO ---")
        print(f"Melhor solução encontrada: {solver.best_solution} guardas")
        print(f"Nós explorados: {solver.nodes_count}")
        print(f"Tempo decorrido: {total_time:.2f}s")