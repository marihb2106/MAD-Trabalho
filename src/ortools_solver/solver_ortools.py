import sys
import os
from ortools.linear_solver import pywraplp

def solve_instances(file_path):
    if not os.path.exists(file_path):
        print(f"Erro: Ficheiro {file_path} não encontrado.")
        return

    with open(file_path, 'r') as f:
        content = f.read().split()
    
    if not content:
        return

    idx = 0
    num_instances = int(content[idx])
    idx += 1
    
    print(f"A processar {num_instances} instâncias de: {file_path}\n")

    for inst in range(1, num_instances + 1):
        num_rects = int(content[idx])
        idx += 1
        
        rectangles = []
        coord_to_id = {}
        next_id = 0
        
        # 1. Parsing da Instância
        for _ in range(num_rects):
            rect_id = content[idx]
            n_verts = int(content[idx + 1])
            idx += 2
            
            current_rect_vars = []
            for _ in range(n_verts):
                x = content[idx]
                y = content[idx + 1]
                point = (x, y)
                idx += 2
                
                # Mapeamento para ID único (Vértice Único)
                if point not in coord_to_id:
                    coord_to_id[point] = next_id
                    next_id += 1
                current_rect_vars.append(coord_to_id[point])
            rectangles.append(current_rect_vars)

        # 2. Modelação com OR-Tools (SCIP)
        solver = pywraplp.Solver.CreateSolver('SCIP')
        # Variáveis binárias para cada vértice único
        x = [solver.IntVar(0, 1, f'v_{i}') for i in range(next_id)]
        
        # Restrições: Pelo menos um guarda por retângulo
        for rect_verts in rectangles:
            solver.Add(solver.Sum([x[v] for v in rect_verts]) >= 1)
        
        # Objetivo: Minimizar o número de guardas
        solver.Minimize(solver.Sum(x))
        
        status = solver.Solve()

        # 3. Output de Resultados
        if status == pywraplp.Solver.OPTIMAL:
            print(f"Instância {inst}: Mínimo de guardas = {int(solver.Objective().Value())}")
        else:
            print(f"Instância {inst}: Não foi encontrada solução ótima.")

if __name__ == "__main__":
    solve_instances('../../data/examples/parts40')
    solve_instances('../../data/examples/step50')