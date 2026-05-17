import sys
import time

# Aumentar o limite para evitar erros em árvores de procura profundas
sys.setrecursionlimit(10000)

class MACSolver:
    """
    Solver manual que utiliza Backtracking + MAC (Maintaining Arc-Consistency).
    O objetivo é minimizar o número de guardas nos vértices dos retângulos.
    """
    def __init__(self, rectangles, num_vars):
        self.rectangles = rectangles
        self.num_vars = num_vars
        self.best_solution = num_vars + 1
        self.nodes_count = 0
        self.start_time = time.time()
        
        # HEURÍSTICA DE ORDENAÇÃO: Vértices que pertencem a mais retângulos primeiro
        degree_map = [0] * num_vars
        for r in rectangles:
            for v in r:
                degree_map[v] += 1
        self.order = sorted(range(num_vars), key=lambda x: degree_map[x], reverse=True)
        
        # Domínios: None (aberto), 0 (sem guarda), 1 (com guarda)
        self.domains = [None] * num_vars

    def gac_consistency(self, domains, current_count):
        """
        GAC (Generalized Arc Consistency): Deduze guardas obrigatórios.
        Se um retângulo só tem um vértice disponível, esse vértice tem de ser 1.
        """
        changed = True
        new_count = current_count
        while changed:
            changed = False
            for rect in self.rectangles:
                # Candidatos são vértices que não foram fixados em 0
                candidates = [v for v in rect if domains[v] != 0]
                
                if not candidates: # Inconsistência: retângulo sem guarda possível
                    return False, domains, new_count
                
                if len(candidates) == 1: # Propagação: guarda obrigatório
                    v = candidates[0]
                    if domains[v] is None:
                        domains[v] = 1
                        new_count += 1
                        changed = True
        return True, domains, new_count

    def solve(self, order_idx=0, current_guards=0):
        self.nodes_count += 1
        
        # Log de progresso a cada 200.000 nós
        if self.nodes_count % 200000 == 0:
            elapsed = time.time() - self.start_time
            print(f"... [Processando] Nós: {self.nodes_count} | Melhor: {self.best_solution} | Tempo: {elapsed:.1f}s", flush=True)

        # PODA: Se já gastámos mais que a melhor solução, cortamos o ramo
        if current_guards >= self.best_solution:
            return

        # FIM DA PROCURA: Todas as variáveis atribuídas
        if order_idx == self.num_vars:
            if current_guards < self.best_solution:
                self.best_solution = current_guards
                print(f"\n*** SUCESSO: Nova melhor solução: {self.best_solution} guardas ***")
            return

        var_idx = self.order[order_idx]

        if self.domains[var_idx] is not None:
            self.solve(order_idx + 1, current_guards)
            return

        # HEURÍSTICA DE VALOR: Tentar 0 primeiro para minimizar guardas
        for val in [0, 1]:
            backup = list(self.domains)
            self.domains[var_idx] = val
            new_val_count = current_guards + (1 if val == 1 else 0)
            
            # Executar MAC (Manter Consistência)
            consistent, propagated, final_count = self.gac_consistency(list(self.domains), new_val_count)
            
            if consistent:
                old_state = self.domains
                self.domains = propagated
                self.solve(order_idx + 1, final_count)
                self.domains = old_state
            
            self.domains = backup

def solve_parts40_instances(file_path, start_at=1, limit=3):
    """Lê e resolve um intervalo de instâncias do ficheiro parts40."""
    print(f"--- A ler ficheiro: {file_path} ---")
    try:
        with open(file_path, 'r') as f:
            content = f.read().split()
        
        idx = 0
        total_instances = int(content[idx]); idx += 1
        
        for inst_idx in range(1, total_instances + 1):
            num_rects = int(content[idx]); idx += 1
            rectangles = []
            coord_to_id = {}
            next_id = 0
            
            for _ in range(num_rects):
                idx += 1 # Pular ID do retângulo
                n_verts = int(content[idx]); idx += 1
                current_rect = []
                for _ in range(n_verts):
                    pt = (content[idx], content[idx+1]); idx += 2
                    if pt not in coord_to_id:
                        coord_to_id[pt] = next_id
                        next_id += 1
                    current_rect.append(coord_to_id[pt])
                rectangles.append(current_rect)

            # Resolver apenas se estiver dentro do intervalo que pediste
            if start_at <= inst_idx < start_at + limit:
                print(f"\n>>> A resolver Instância {inst_idx} ({next_id} variáveis) <<<")
                solver = MACSolver(rectangles, next_id)
                try:
                    solver.solve()
                except KeyboardInterrupt:
                    print("\nInterrompido. Passando à próxima...")
                
                print(f"Instância {inst_idx} Finalizada. Melhor: {solver.best_solution}")

    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    # Caminho para o ficheiro parts40
    file = '../../data/examples/parts40'
    
    # Resolve as instâncias 1, 2 e 3 (podes mudar o limite para resolver mais à noite)
    solve_parts40_instances(file, start_at=1, limit=3)