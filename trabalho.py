import csv
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_visualizar_precos():
    limpar_tela()
    print("="*55)
    print(f"{'TABELA DE PREÇOS OFICIAL - IMOBILIÁRIA R.M':^55}")
    print("="*55)
    print(f"{'TIPO DE IMÓVEL':<25} | {'PREÇO BASE':<15}")
    print("-" * 55)
    print(f"{'1. Apartamento':<25} | R$ 700,00")
    print(f"{'2. Casa':<25} | R$ 900,00")
    print(f"{'3. Estúdio':<25} | R$ 1.200,00")
    print("-" * 55)
    print("REGRAS DE ADICIONAIS:")
    print("  • Apto com 2 quartos: + R$ 200,00")
    print("  • Casa com 2 quartos: + R$ 250,00")
    print("  • Vaga Garagem (Apto/Casa): + R$ 300,00")
    print("  • Vaga Estúdio: R$ 250,00 (2 vagas) + R$ 60,00 p/ extra")
    print("\nDESCONTOS E TAXAS:")
    print("  • Apto sem crianças: 5% de desconto no aluguel")
    print("  • Taxa de Contrato: R$ 2.000,00 (Parcelado em até 5x)")
    print("="*55)
    input("\nPressione ENTER para voltar...")

def menu_gerar_orcamento():
    limpar_tela()
    try:
        print("-" * 50)
        print(f"{'GERADOR DE ORÇAMENTO':^50}")
        print("-" * 50)

        # 1. Escolha do Tipo (Regra A)
        tipo = int(input("\nEscolha o tipo (1-Apto, 2-Casa, 3-Estúdio): "))
        aluguel_base = {1: 700.0, 2: 900.0, 3: 1200.0}.get(tipo, 0)
        
        if aluguel_base == 0:
            print("Tipo inválido!"); input(); return

        # 2. Quartos (Regras C e D)
        if tipo in [1, 2]:
            q = int(input("Quantidade de quartos (1 ou 2): "))
            if q == 2:
                aluguel_base += 200.0 if tipo == 1 else 250.0
            elif q != 1:
                print("Opção de quartos inválida para o desafio."); input(); return
        
        # 3. Desconto Criança (Regra G - Apenas Apartamento)
        if tipo == 1:
            crianca = input("Possui crianças residindo? (s/n): ").lower()
            if crianca == 'n':
                aluguel_base *= 0.95 # Aplica 5% de desconto

        # 4. Vaga de Garagem (Regras E e F)
        if input("Deseja incluir vaga de garagem? (s/n): ").lower() == 's':
            if tipo == 3: # Regra do Estúdio
                qtd_vagas = int(input("Quantas vagas totais desejadas? "))
                # R$ 250 pelas primeiras 2, R$ 60 por cada uma acima de 2
                aluguel_base += 250.0
                if qtd_vagas > 2:
                    aluguel_base += (qtd_vagas - 2) * 60.0
            else: # Regra Casa/Apto
                aluguel_base += 300.0

        # 5. Valor do Contrato (Regra B e H - Máximo de 5 vezes)
        print("\nO contrato imobiliário custa R$ 2.000,00.")
        parc_c = int(input("Parcelar o contrato em quantas vezes (1 a 5)? "))
        
        if not (1 <= parc_c <= 5):
            print("\n[ERRO] O desafio exige parcelamento em no máximo 5 vezes."); input(); return
            
        val_parc_c = 2000.0 / parc_c

        # 6. Apresentação do valor mensal (Regra H)
        print("\n" + "="*40)
        print(f"VALOR MENSAL DO ALUGUEL: R$ {aluguel_base:.2f}")
        print(f"VALOR DA PARCELA CONTRATO: {parc_c}x de R$ {val_parc_c:.2f}")
        print("="*40)

        # 7. Geração do Arquivo CSV com 12 parcelas (Regra I)
        diretorio = os.path.dirname(os.path.abspath(__file__))
        nome_arquivo = os.path.join(diretorio, 'orcamento_rm.csv')

        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as f:
            escritor = csv.writer(f, delimiter=',')
            
            # Cabeçalho formatado para leitura visual
            escritor.writerow([f"{'PARCELA':<12}", f"{'ALUGUEL':<15}", f"{'CONTRATO':<15}", f"{'TOTAL MENSAL':<15}"])
            escritor.writerow(["-"*10, "-"*14, "-"*14, "-"*14])

            for i in range(1, 13):
                # A parcela do contrato só existe até o limite escolhido (máximo 5)
                p_atual = val_parc_c if i <= parc_c else 0.0
                total_mes = aluguel_base + p_atual
                
                linha = [
                    f"Mes {i:02d}:",
                    f"R$ {aluguel_base:>10.2f}  ",
                    f"R$ {p_atual:>10.2f}  ",
                    f"R$ {total_mes:>10.2f}  "
                ]
                escritor.writerow(linha)

        print(f"\n✅ Arquivo CSV gerado com sucesso em:\n{nome_arquivo}")
        
    except ValueError:
        print("\n[ERRO] Digite apenas números para valores numéricos."); input()
    except Exception as e:
        print(f"\n[ERRO] Inesperado: {e}")
    
    input("\nPressione ENTER para voltar ao menu principal...")

# --- LOOP PRINCIPAL ---
while True:
    limpar_tela()
    print("="*40)
    print(f"{'SISTEMA IMOBILIÁRIA R.M':^40}")
    print("="*40)
    print("1. VISUALIZAR TABELA DE PREÇOS")
    print("2. GERAR NOVO ORÇAMENTO (CSV)")
    print("3. SAIR")
    print("-" * 40)
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == '1':
        menu_visualizar_precos()
    elif opcao == '2':
        menu_gerar_orcamento()
    elif opcao == '3':
        print("\nEncerrando sistema...")
        break
    else:
        print("\nOpção inválida!")
        import time
        time.sleep(1)