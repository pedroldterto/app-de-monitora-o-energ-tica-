import os
import json

dados_arquivo = "dados_usuarios.json"

# Salva o arquivo
def salvar_dados(usuarios):
    dados = [
       {"nome": u.nome, "dispositivos": u.dispositivos}
        for u in usuarios
    ]
    with open(dados_arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

# Carrega o arquivo
def carregar_dados():
    
    # Cria um arquivo caso ele não exista
    if not os.path.exists(dados_arquivo):
        return [Usuario("Thor", salvar=False), Usuario("Pedro lucas", salvar=False), Usuario("João Henrique", salvar=False), Usuario("Rafael de Brito", salvar=False)]

    with open(dados_arquivo, "r", encoding="utf-8") as f:
        dados = json.load(f)

    usuarios = []
    for item in dados:
        u = Usuario(item["nome"], salvar=False)
        u.dispositivos = item.get("dispositivos", [])
        usuarios.append(u)
    return usuarios


# Representa um usuário com nome e lista de dispositivos
class Usuario:
    # Inicializa o usuário e salva no arquivo se for um novo cadastro
    def __init__(self, nome, salvar=True):
        self.nome = nome
        self.dispositivos = []
        if salvar:
            salvar_dados(GerenciadorSistema.usuarios + [self])

    # Solicita dados ao usuário e adiciona um novo dispositivo à sua lista
    def cadastrar_dispositivo(self):
        print(f"\n--- Cadastrando dispositivo para {self.nome} ---")
        nome = input("Nome do dispositivo de geração: ")
        try:
            energia = float(input("Energia gerada atual (em kWh): "))
        except ValueError:
            print("Valor de energia inválido! Definido como 0.0")
            energia = 0.0

        self.dispositivos.append({"nome": nome, "energia": energia})
        salvar_dados(GerenciadorSistema.usuarios)
        print(f"Dispositivo '{nome}' cadastrado com sucesso para {self.nome}!")

    # Exibe todos os dispositivos cadastrados para este usuário
    def listar_dispositivos(self):
        print(f"\nDispositivos de {self.nome}:")
        if not self.dispositivos:
            print("Nenhum dispositivo cadastrado.")
            return
        for i, disp in enumerate(self.dispositivos, start=1):
            print(f"{i}. {disp['nome']} - Geração: {disp['energia']} kWh")

    # Permite alterar o nome ou a energia de um dispositivo existente
    def atualizar_dispositivo(self):
        self.listar_dispositivos()
        if not self.dispositivos:
            return
        try:
            indice = int(input("Digite o número do dispositivo que deseja atualizar: ")) - 1
            if 0 <= indice < len(self.dispositivos):
                novo_nome = input(f"Novo nome para '{self.dispositivos[indice]['nome']}' (Enter para manter): ")
                nova_energia_str = input(f"Nova geração em kWh (Enter para manter): ")

                if novo_nome:
                    self.dispositivos[indice]["nome"] = novo_nome
                if nova_energia_str:
                    self.dispositivos[indice]["energia"] = float(nova_energia_str)

                salvar_dados(GerenciadorSistema.usuarios)
                print("Dispositivo atualizado com sucesso!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida. Operação cancelada.")

    # Remove um dispositivo da lista do usuário pelo número exibido
    def deletar_dispositivo(self):
        self.listar_dispositivos()
        if not self.dispositivos:
            return
        try:
            indice = int(input("Digite o número do dispositivo que deseja excluir: ")) - 1
            if 0 <= indice < len(self.dispositivos):
                removido = self.dispositivos.pop(indice)
                salvar_dados(GerenciadorSistema.usuarios)
                print(f"Dispositivo '{removido['nome']}' excluído com sucesso!")
            else:
                print("Número inválido.")
        except ValueError:
            print("Entrada inválida.")

    # Soma e exibe a energia gerada por todos os dispositivos do usuário
    def total_energia(self):
        if not self.dispositivos:
            print(f"{self.nome} não tem energia gerada acumulada.")
            return
        total = sum(disp["energia"] for disp in self.dispositivos)
        print(f"Geração total do mês de {self.nome}: {total:.2f} kWh")

# Gerencia a lista global de usuários do sistema
class GerenciadorSistema:
    usuarios = [] 

    # Lê o nome e adiciona um novo usuário à lista, salvando em seguida
    @classmethod
    def cadastrar_usuario(cls):
        nome = input("Digite o nome do novo usuário: ")
        if nome:
            novo = Usuario(nome, salvar=False)
            cls.usuarios.append(novo)
            salvar_dados(cls.usuarios)
            print(f"Usuário '{nome}' cadastrado com sucesso!")

    # Imprime todos os usuários cadastrados com seus índices
    @classmethod
    def listar_usuarios(cls):
        print("\nUsuários cadastrados no sistema:")
        for i, user in enumerate(cls.usuarios, start=1):
            print(f"{i}. {user.nome}")

    # Percorre todos os usuários e exibe dispositivos e energia de cada um
    @classmethod
    def rodar_para_todos(cls):
        if not cls.usuarios:
            print("Nenhum usuário cadastrado no sistema.")
            return

        print("\n=========================================")
        print(" EXECUTANDO ROTINA PARA TODOS OS USUÁRIOS")
        print("=========================================")
        for user in cls.usuarios:
            print(f"\n>>> Lendo dados de: {user.nome.upper()} <<<")
            user.listar_dispositivos()
            user.total_energia()
        print("\n=========================================")

# Exibe o menu principal e direciona para as funções corretas
def menu():
    GerenciadorSistema.usuarios = carregar_dados()
    print(f"[Sistema] {len(GerenciadorSistema.usuarios)} usuário(s) carregado(s) de '{dados_arquivo}'.")

    opcao = 0
    while opcao != 8:
        print("\n=== SISTEMA CENTRAL ===")
        print("1 - Cadastrar Usuário")
        print("2 - Listar Usuários")
        print("3 - Gerenciar Dispositivos de um Usuário")
        print("7 - Rodar Relatório de Energia para Cada Usuário")
        print("8 - Sair")

        try:
            opcao = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Por favor, digite um número válido.")
            continue

        if opcao == 1:
            GerenciadorSistema.cadastrar_usuario()

        elif opcao == 2:
            GerenciadorSistema.listar_usuarios()

        elif opcao == 3:
            GerenciadorSistema.listar_usuarios()
            try:
                escolha = int(input("Escolha o número do usuário para gerenciar os dispositivos: ")) - 1
                if 0 <= escolha < len(GerenciadorSistema.usuarios):
                    usuario_atual = GerenciadorSistema.usuarios[escolha]

                    sub_opcao = 0
                    while sub_opcao != 6:
                        print(f"\n--- Gerenciando Dispositivos de: {usuario_atual.nome} ---")
                        print("1 - Cadastrar Dispositivo")
                        print("2 - Listar Dispositivos")
                        print("3 - Atualizar Dispositivo")
                        print("4 - Deletar Dispositivo")
                        print("5 - Total de Energia do Mês")
                        print("6 - Voltar ao Menu Principal")

                        try:
                            sub_opcao = int(input("Digite a opção: "))
                        except ValueError:
                            print("Opção inválida.")
                            continue

                        if sub_opcao == 1:   usuario_atual.cadastrar_dispositivo()
                        elif sub_opcao == 2: usuario_atual.listar_dispositivos()
                        elif sub_opcao == 3: usuario_atual.atualizar_dispositivo()
                        elif sub_opcao == 4: usuario_atual.deletar_dispositivo()
                        elif sub_opcao == 5: usuario_atual.total_energia()
                else:
                    print("Número de usuário inválido.")
            except ValueError:
                print("Entrada inválida.")

        elif opcao == 7:
            GerenciadorSistema.rodar_para_todos()

        elif opcao == 8:
            print("Encerrando o sistema de energia. Até logo!")

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()  
