import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizarTransacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionarConta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, sobrenome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.sobrenome = sobrenome
        self.cpf = cpf

    @property
    def fullName(self):
        return f"{self.nome} {self.sobrenome}"


class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def novaConta(cls, cliente, numero):
        return cls(cliente, numero)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeuSaldo = valor > saldo
        if excedeuSaldo:
            print("\nErro ao realizar o saque. Verifique o saldo e tente novamente.")
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso.")
            return True
        else:
            print("\nErro ao efetuar o saque. Informação inválida.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso.")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500, limite_saque=3):
        super().__init__(cliente, numero)  # Passando cliente como primeiro argumento
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque >= self.limite_saque
        if excedeu_limite:
            print("Erro ao realizar o saque. O valor do saque excedeu o limite da conta.")
        elif excedeu_saques:
            print("Operação falhou. Número máximo de saques excedido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
        Agência: {self.agencia}
        Conta: {self.numero}
        Titular: {self.cliente.fullName} 
        Saldo: {self.saldo}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionarTransacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionarTransacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionarTransacao(self)


def menu():
    menu = """
    =================== MENU ===================
    [1] Criar Conta
    [2] Depositar
    [3] Sacar
    [4] Listar Conta
    [5] Extrato
    [6] Criar Usuário
    [7] Sair
    =================== ---- ===================
    => """
    return input(textwrap.dedent(menu))


def filtrarCliente(cpf, clientes):
    clientesFiltrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientesFiltrados[0] if clientesFiltrados else None


def recuperarConta(cliente):
    if not cliente.contas:
        print("Usuário não possui conta.")
        return None
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)
    if not cliente:
        print("Cliente não cadastrado.")
        return
    valor = float(input("Informe o valor que deseja depositar: "))
    transacao = Deposito(valor)
    conta = recuperarConta(cliente)
    if not conta:
        return
    cliente.realizarTransacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)
    if not cliente:
        print("Cliente não cadastrado.")
        return
    valor = float(input("Informe o valor que deseja sacar: "))
    transacao = Saque(valor)
    conta = recuperarConta(cliente)
    if not conta:
        return
    cliente.realizarTransacao(conta, transacao)


def extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)
    if not cliente:
        print("Cliente não cadastrado.")
        return
    conta = recuperarConta(cliente)
    if not conta:
        return
    print("\n====================== EXTRATO DE MOVIMENTAÇÂO ======================")
    print(f"Titular da Conta: {conta.cliente.fullName}")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f}")
      
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("=====================================================")


def criarConta(numero, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrarCliente(cpf, clientes)
    
    if cliente:
        print("Usuário já cadastrado.")
        return
    
    print("Cliente não encontrado.")
    opcao = input("Deseja cadastrar o usuário?\n[1] - Sim\n[2] - Não\nOpção: ")
    if opcao == "1":
        criarUsuario(clientes)
        cliente = filtrarCliente(cpf, clientes)  # Atualiza o cliente após o cadastro
        if cliente:
            conta = ContaCorrente.novaConta(cliente, numero)
            contas.append(conta)
            cliente.adicionarConta(conta)
            print("\nConta cadastrada com sucesso.")
        else:
            print("\nErro ao cadastrar conta. Cliente não encontrado.")
    else:
        print("Usuário não cadastrado.")


def criarUsuario(clientes):
    cpf = input("Informe o seu CPF (somente números): ")
    cliente = filtrarCliente(cpf, clientes)
    if cliente:
        print("\nJá existe cliente com esse CPF.")
        return
    nome = input("Informe seu nome: ")
    sobrenome = input("Informe seu sobrenome: ")
    endereco = input("Informe seu endereço completo: ")
    nascimento = input("Informe sua data de nascimento (D/M/AAAA): ")
    novo_cliente = PessoaFisica(nome, sobrenome, nascimento, cpf, endereco)
    clientes.append(novo_cliente)
    print(f"\nUsuário {novo_cliente.fullName} criado com sucesso.")


def listarContas(contas):
    for conta in contas:
        print("=" * 50)
        print(conta)


def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()
        if opcao == "1":  # Criar conta
            numero = len(contas) + 1
            criarConta(numero, clientes, contas)
        
        elif opcao == "2":  # Depositar
            depositar(clientes)
        
        elif opcao == "3":  # Sacar
            sacar(clientes)
        
        elif opcao == "4":  # Listar conta
            listarContas(contas)
        
        elif opcao == "5":  # Exibir extrato
            extrato(clientes)
        
        elif opcao == "6":  # Criar usuário
            criarUsuario(clientes)
        
        elif opcao == "7":  # Sair
            print("Saindo...")
            break
        
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
