import os
import subprocess

# Obtém a contagem de commits do repositório atual
def get_commit_count():
    try:
        commit_count = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD'])
        return commit_count.strip().decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Erro ao contar commits: {e}")
        return None

# Atualiza o valor de BUILD_NUMBER no arquivo .env
def update_env_file(build_number):
    env_file = ".env"
    new_lines = []

    # Lê o conteúdo atual do arquivo .env e atualiza ou adiciona BUILD_NUMBER
    if os.path.exists(env_file):
        with open(env_file, "r") as file:
            lines = file.readlines()
            build_number_updated = False
            for line in lines:
                if line.startswith("BUILD_NUMBER="):
                    new_lines.append(f"BUILD_NUMBER={build_number}\n")
                    build_number_updated = True
                else:
                    new_lines.append(line)

            if not build_number_updated:
                new_lines.append(f"BUILD_NUMBER={build_number}\n")
    else:
        new_lines = [f"BUILD_NUMBER={build_number}\n"]

    # Escreve o novo conteúdo no arquivo .env
    with open(env_file, "w") as file:
        file.writelines(new_lines)

if __name__ == "__main__":
    commit_count = get_commit_count()
    if commit_count:
        update_env_file(commit_count)
        print(f"BUILD_NUMBER atualizado para: {commit_count}")
    else:
        print("Erro ao obter o número de commits.")