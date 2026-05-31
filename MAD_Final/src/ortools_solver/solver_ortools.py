import os
import time
import random
from ortools.linear_solver import pywraplp

# Leitura dos dados
def parse_file(file_path):
    """Lê o ficheiro e devolve uma lista de instâncias."""
    with open(file_path, 'r') as f:
        content = f.read().split()

    idx = 0
    num_instances = int(content[idx]); idx += 1
    instances = []

    for _ in range(num_instances):
        num_rects = int(content[idx]); idx += 1
        rectangles = []
        coord_to_id = {}
        next_id = 0

        for _ in range(num_rects):
            idx += 1                          
            n_verts = int(content[idx]); idx += 1
            verts = []
            for _ in range(n_verts):
                pt = (content[idx], content[idx + 1]); idx += 2
                if pt not in coord_to_id:
                    coord_to_id[pt] = next_id
                    next_id += 1
                verts.append(coord_to_id[pt])
            rectangles.append(verts)

        instances.append({
            'rectangles': rectangles,
            'num_vertices': next_id,
        })

    return instances

# Resolve uma instância
def solve_one(rectangles, num_vertices, required_indices=None):
    """Resolve o problema de vigilância usando o solver SCIP."""
    if required_indices is None:
        required_indices = range(len(rectangles))

    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = [solver.IntVar(0, 1, f'v_{i}') for i in range(num_vertices)]

    for i in required_indices:
        solver.Add(solver.Sum([x[v] for v in rectangles[i]]) >= 1)

    solver.Minimize(solver.Sum(x))

    t0 = time.perf_counter()
    status = solver.Solve()
    elapsed = time.perf_counter() - t0

    if status == pywraplp.Solver.OPTIMAL:
        guards = int(solver.Objective().Value())
        placed = [i for i in range(num_vertices) if x[i].solution_value() > 0.5]
        return guards, placed, elapsed
    else:
        return None, [], elapsed


# Experiência de cobertura total
def run_full_coverage(file_path):
    print(f"\n{'═'*60}")
    print(f"  COBERTURA TOTAL  —  {os.path.basename(file_path)}")
    print(f"{'═'*60}")
    print(f"{'Inst':>4}  {'Retâng':>6}  {'Vért':>5}  {'Guardas':>7}  {'Tempo (s)':>10}")
    print(f"{'─'*4}  {'─'*6}  {'─'*5}  {'─'*7}  {'─'*10}")

    instances = parse_file(file_path)
    for i, inst in enumerate(instances, 1):
        rects = inst['rectangles']
        nv    = inst['num_vertices']
        guards, _, t = solve_one(rects, nv)
        if guards is not None:
            print(f"{i:>4}  {len(rects):>6}  {nv:>5}  {guards:>7}  {t:>10.5f}")
        else:
            print(f"{i:>4}  {len(rects):>6}  {nv:>5}  {'N/A':>7}  {t:>10.5f}")


# Experiência de cobertura parcial
def run_subset_coverage(file_path, fractions=(1.0, 0.75, 0.50, 0.25), seed=42):
    """Resolve o problema para subconjuntos de retângulos."""
    print(f"\n{'═'*70}")
    print(f"  COBERTURA PARCIAL (Π' ⊂ Π)  —  {os.path.basename(file_path)}")
    print(f"{'═'*70}")
    print(f"{'Inst':>4}  {'|Π|':>4}  {chr(124)}Π'{chr(124)}  {'Frac':>5}  "
          f"{'Guardas':>7}  {'Redução':>7}  {'Tempo (s)':>10}")
    print(f"{'─'*4}  {'─'*4}  {'─'*5}  {'─'*5}  {'─'*7}  {'─'*7}  {'─'*10}")

    instances = parse_file(file_path)
    for i, inst in enumerate(instances, 1):
        rects = inst['rectangles']
        nv    = inst['num_vertices']
        nr    = len(rects)

        ref_guards, _, _ = solve_one(rects, nv)

        rng = random.Random(seed)
        all_indices = list(range(nr))

        for frac in fractions:
            k = max(1, round(nr * frac))

            if frac >= 1.0:
                required = all_indices
            else:
                required = sorted(rng.sample(all_indices, k))

            guards, _, t = solve_one(rects, nv, required_indices=required)

            if guards is not None and ref_guards is not None:
                reducao = f"{(1 - guards/ref_guards)*100:+.1f}%"
            else:
                reducao = "N/A"

            guards_str = str(guards) if guards is not None else "N/A"
            print(f"{i:>4}  {nr:>4}  {k:>5}  {frac:>5.0%}  "
                  f"{guards_str:>7}  {reducao:>7}  {t:>10.5f}")

        print()   # Linha em branco