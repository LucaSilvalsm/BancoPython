menu = """
[1]- Depositar
[2]- Sacar
[3]- Extrato 
[4]- Sair 

=> """
saldo = 0
limite = 500
extrato = ""
numero_saque = 0
LIMITE_SAQUE = 3

while True:
    opcao = input(menu)
    if opcao == "1":
        deposito = float(input("Digite qual é o valor que deseja depositar:"))
        if deposito > 0:
            print("Valor depositado com sucesso")
            saldo += deposito
            print("Seu saldo agora é: R$" + str(saldo))
            extrato += f"Deposito: R$ {deposito:.2f} \n"
        else:
           print("Operação invalida! O valor informado é invalido")          
           
        
    elif opcao == "2":
        valorSacado = float(input("Digite qual é o valor que voce deseja sacar: "))
        excedeu_saldo = valorSacado > saldo
        
        excedeu_limite = valorSacado > limite
        
        excedeu_saques = numero_saque >= LIMITE_SAQUE
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
         

        
    elif opcao == "3":
        print("\n====================== EXTRATO ======================")
        print("Não foram realizada movimentações. " if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")

    elif opcao == "4":
         print("Saindo") 
         break  
    else:
      print("Opção invalida");         


        
         
         
        


