import subprocess
import tempfile
import os

def avaliar_codigo(codigo_aluno, codigo_professor, casos_de_teste):
    """
    Recebe os dois códigos, roda contra as entradas (casos_de_teste)
    e compara os resultados.
    """
    # 1. Cria arquivos temporários para guardar os códigos (.py)
    # Usamos delete=False provisoriamente para o Windows não bloquear o arquivo
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f_aluno:
        f_aluno.write(codigo_aluno)
        arq_aluno = f_aluno.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f_prof:
        f_prof.write(codigo_professor)
        arq_prof = f_prof.name

    resultado_final = {
        "sucesso": True, 
        "mensagem": "✅ Parabéns! Seu código passou em todos os testes.", 
        "testes_passados": 0
    }

    try:
        # 2. Testa cada entrada da nossa lista de casos de teste
        for indice, entrada in enumerate(casos_de_teste):
            
            # --- EXECUÇÃO DO PROFESSOR (GABARITO) ---
            proc_prof = subprocess.run(
                ['python', arq_prof],  # Comando no terminal: python script_prof.py
                input=entrada,         # Injeta a entrada atual
                text=True,             # Trata a entrada e saída como texto (String)
                capture_output=True,   # Captura o print gerado
                timeout=2              # Se demorar mais de 2 segundos, cancela (evita loop infinito)
            )
            # Removemos espaços em branco desnecessários no final do print
            saida_esperada = proc_prof.stdout.strip()

            # --- EXECUÇÃO DO ALUNO ---
            proc_aluno = subprocess.run(
                ['python', arq_aluno],
                input=entrada,
                text=True,
                capture_output=True,
                timeout=2
            )
            saida_aluno = proc_aluno.stdout.strip()
            erro_aluno = proc_aluno.stderr.strip() # Captura erros de sintaxe (ex: NameError)

            # 3. Análise dos Resultados
            
            # A) O código do aluno "quebrou" (Erro de sintaxe, lógica, etc)
            if erro_aluno:
                resultado_final = {
                    "sucesso": False,
                    "mensagem": f"❌ Erro no código (Teste {indice + 1}):\n{erro_aluno}",
                    "testes_passados": indice
                }
                break # Para a execução na hora, não testa o resto

            # B) O código rodou, mas a resposta é diferente da sua
            if saida_aluno != saida_esperada:
                resultado_final = {
                    "sucesso": False,
                    "mensagem": f"❌ Falha no Teste {indice + 1}.\nEntrada dada:\n{entrada}\n\nSaída Esperada:\n{saida_esperada}\n\nSua Saída:\n{saida_aluno}",
                    "testes_passados": indice
                }
                break # Para a execução, o aluno errou

            # Se chegou até aqui, passou neste teste específico
            resultado_final["testes_passados"] += 1

    except subprocess.TimeoutExpired:
         # Captura se o aluno fez um "while True" infinito
         resultado_final = {
             "sucesso": False, 
             "mensagem": "⏳ Tempo limite excedido (Possível loop infinito).", 
             "testes_passados": resultado_final["testes_passados"]
         }
    finally:
        # 4. Limpeza: Apaga os arquivos temporários do computador para não lotar o disco
        if os.path.exists(arq_aluno):
            os.remove(arq_aluno)
        if os.path.exists(arq_prof):
            os.remove(arq_prof)

    return resultado_final


# ==========================================
# ÁREA DE TESTE DO SCRIPT (Para você rodar agora!)
# ==========================================
if __name__ == "__main__":
    # O Gabarito que você (professor) escreveu
    codigo_do_professor = """
num1 = int(input())
num2 = int(input())
print(num1 + num2)
"""

    # O Código que o aluno mandou lá do Frontend
    codigo_do_aluno_certo = """
a = int(input())
b = int(input())
soma = a + b
print(soma)
"""

    codigo_do_aluno_errado = """
a = int(input())
b = int(input())
print(a * b)  # Aluno multiplicou em vez de somar!
"""

    # As entradas que o Python vai jogar invisivelmente para os dois códigos (cada item é um teste)
    entradas_secretas = [
        "5\n3",   # Teste 1: Vai injetar o 5 e depois o 3
        "10\n10", # Teste 2: Vai injetar o 10 e depois o 10
        "-2\n5"   # Teste 3: Vai injetar o -2 e depois o 5
    ]

    print("--- TESTANDO ALUNO CERTO ---")
    resultado1 = avaliar_codigo(codigo_do_aluno_certo, codigo_do_professor, entradas_secretas)
    print(resultado1['mensagem'])

    print("\n--- TESTANDO ALUNO ERRADO ---")
    resultado2 = avaliar_codigo(codigo_do_aluno_errado, codigo_do_professor, entradas_secretas)
    print(resultado2['mensagem'])
