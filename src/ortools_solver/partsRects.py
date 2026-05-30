from ortools.linear_solver import pywraplp

def solve_partRects():
    # Cria o solver MIP
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variáveis de decisão
    x = {}
    for i in range(1,9):
        x[i] = solver.IntVar(0, 1, f'x_{i}')
    
    # Restrições
    solver.Add(x[8] >= 1)
    solver.Add(x[8]+x[7] >= 1)
    solver.Add(x[7]+x[6]+x[4]+x[5] >= 1)
    solver.Add(x[7]+x[6]+x[8] >= 1)
    solver.Add(x[3]+x[4] >= 1)
    solver.Add(x[2]+x[1] >= 1)
    solver.Add(x[5]+x[4]+x[3]+x[2] >= 1)
    solver.Add(x[5]+x[6] >= 1)
    solver.Add(x[1]+x[3]+x[2] >= 1)
    solver.Add(x[1] >= 1)
    
    # Objetivo: minimizar o custo
    objective = solver.Objective()
    for i in range(1,9):
        objective.SetCoefficient(x[i],1)
    objective.SetMinimization()

    # Resolver
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print("Custo ótimo:", objective.Value())
        for i in range(1,9):
            if x[i].solution_value() > 0.5:
                print(f'Guarda no nó {i}')
    else:
        print("Nenhuma solução ótima encontrada.")

solve_partRects()