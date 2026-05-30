import os

def gerar_factos_prolog(file_path, output_path):
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

    with open(output_path, 'w') as out:
        out.write(f"% Factos gerados automaticamente a partir de {os.path.basename(file_path)}\n")
        out.write(":- dynamic retangulo/3, num_vars/2.\n\n")

        for inst in range(1, num_instances + 1):
            num_rects = int(content[idx])
            idx += 1
            
            coord_to_id = {}
            next_id = 1 
            
            for _ in range(num_rects):
                rect_id = int(content[idx])
                n_verts = int(content[idx + 1])
                idx += 2
                
                current_rect_vars = []
                for _ in range(n_verts):
                    x = int(content[idx])
                    y = int(content[idx + 1])
                    point = (x, y)
                    idx += 2
                    
                    if point not in coord_to_id:
                        coord_to_id[point] = next_id
                        next_id += 1
                    current_rect_vars.append(coord_to_id[point])
                
                # Escreve o facto Prolog: retangulo(ID_Instancia, ID_Retangulo, [Lista_de_Vertices]).
                verts_str = "[" + ", ".join(map(str, current_rect_vars)) + "]"
                out.write(f"retangulo({inst}, {rect_id}, {verts_str}).\n")
            
            # Guarda o número total de vértices únicos para sabermos quantas variáveis criar
            out.write(f"num_vars({inst}, {next_id - 1}).\n\n")

if __name__ == '__main__':
    # Caminhos relativos tendo em conta que o script corre em src/prolog_solver/
    gerar_factos_prolog('../../data/examples/parts40', 'dados_parts40.pl')
    gerar_factos_prolog('../../data/examples/step50', 'dados_step50.pl')
    print(" Ficheiros .pl gerados.")