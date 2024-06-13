import textwrap

def menu():
   menu = """\n
   =================== MENU ===================
   [1]- Criar Conta
   [2]- Depositar
   [3]- Sacar 
   [4]- Listar Conta 
   [5]- Extrato
   [6]- Criar Usuario
   [7]- Sair
   =================== ---- ===================
   => """
   return input(textwrap.dedent(menu))   

def criarConta(agencia, numeroConta, usuarios):
    cpf = input("Informe o CPF(Somente numero apenas): ")  
    usuario = filtrarCPF(cpf, usuarios)    
    
    if usuario:
        print("=====Conta Criada Com Sucesso! ====")
        return {"agencia": agencia, "numeroConta": numeroConta, "usuario": usuario}
    else:
        opcao = input("Usuario não cadastrado, deseja cadastrar o usuario?\n[1]-Sim\n[2]-Não: ")
        if opcao == "1":
            criarUsuario(usuarios)
        else:
            print("Usuario Não cadastrado")

 
def listaContas(contas,saldo):
      for conta in contas:
          linha = f"""\
          Agência:{conta['agencia']} 
          Conta: {conta['numeroConta']}
          Titular: {conta['usuario']['nome']}
          Saldo: {saldo}
          """
          print("=" * 100)
          print(textwrap.dedent(linha))        
def depositar(saldo,deposito,extrato,/) :
      
      if deposito > 0:
            print("Valor depositado com sucesso")
            saldo += deposito
            print("Seu saldo agora é: R$" + str(saldo))
            extrato += f"Deposito: R$ {deposito:.2f} \n"
      else:
            print("Operação invalida! O valor informado é invalido")      
      
      return saldo, extrato

def sacar(*,saldo,valorSacado,extrato,limite,numero_saque,limite_saque) :  

         
        
      excedeu_saldo = valorSacado > saldo
        
      excedeu_limite = valorSacado > limite
        
      excedeu_saques = numero_saque >= limite_saque
      if excedeu_saldo:
           print("Saldo insuficiente ")
           
      elif excedeu_limite:
           print("Erro ao realizar o saque. O valor do saque excedeu o limite da conta")
      elif excedeu_saques:
           print("Operação falhou, Numero maximo de saque excedido")
           
      elif valorSacado >0:
           saldo-=valorSacado
           extrato += f"Saque: R$ {valorSacado:.2f}\n"
           numero_saque += 1
           print("Seu saldo atual é: R$ " + str(saldo))
      else:
           print("Operação invalida! O valor informado é invalido")  
           
      return saldo, extrato
   
   
   
def exibirExtrato(saldo, /, *, extrato):   
      print("\n====================== EXTRATO ======================")
      print("Não foram realizada movimentações. " if not extrato else extrato)
      print(f"Saldo: R$ {saldo:.2f}") 
      
def criarUsuario(usuarios):
      cpf = input("Informe o CPF(Somente numero apenas): ")  
      usuario = filtrarCPF(cpf, usuarios)    
      if usuario:
         print("\n Usuario já cadastrado no sistema com esse CPF!")
         return
      nome =  input("Informe o Seu Nome e Sobrenome: ")
      dataNascimento = input("Informe a data de nascimento no formato(D-M-AAAA): ")
      endereco = input ("Informe o seu endereço completo (Rua, num- bairro-cidade/estado): ")
      usuarios.append({"nome": nome,"dataNascimento": dataNascimento,"cpf":cpf,"endereco":endereco})
      print("Usuario Cadastrado com sucesso !")
  
  
  
def filtrarCPF(cpf,usuarios):
      usuarioFiltrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
      return usuarioFiltrados[0] if usuarioFiltrados else None
         
def main():
   AGENCIA = "0001"
   saldo = 0
   limite = 500
   extrato = ""
   numero_saque = 0
   LIMITE_SAQUE = 3
   usuarios = []  # Inicialize a lista de usuários aqui
   contas = []

   while True:
      opcao = menu()
      if opcao == "1": #criar conta 
         numeroConta = len(contas) + 1
         conta = criarConta(AGENCIA,numeroConta,usuarios)
           
         if conta:
            contas.append(conta)
         
      elif opcao == "2": #depositar
         deposito = float(input("Digite qual é o valor que deseja depositar:"))
         saldo, extrato = depositar(saldo,deposito,extrato)
            

         
      elif opcao == "3": #sacar
         valorSacado = float(input("Digite qual é o valor que voce deseja sacar: "))
         saldo, extrato = sacar(
            saldo= saldo,
            valorSacado= valorSacado,
            extrato= extrato,
            limite= limite,
            numero_saque= numero_saque,
            limite_saque= LIMITE_SAQUE,
         )

      elif opcao == "4": #listar conta
            listaContas(contas,saldo)
      elif opcao == "5": #exibir extrato
            exibirExtrato(saldo,extrato=extrato)
      elif opcao == "6": #exibir criar usuario
             criarUsuario(usuarios)
      elif opcao == "7":
         print("Saindo") 
         break         
      else:
         print("Opção invalida");         


main()
