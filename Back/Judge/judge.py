import os
import subprocess
import tempfile


def compilar_cpp(codigo_fonte):
    """
    Salva o código C++ em um arquivo .cpp e tenta compilar usando o g++.
    Retorna se deu certo, o erro (se houver), e os caminhos dos arquivos gerados.
    """
    # 1. Cria o arquivo .cpp temporário
    with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False, encoding='utf-8') as f:
        f.write(codigo_fonte)
        arq_cpp = f.name

    # 2. Define o nome do executável gerado
    arq_exe = arq_cpp[:-4] # Tira o ".cpp" do nome
    if os.name == 'nt':    # Se for Windows, adiciona .exe
        arq_exe += '.exe'
    else:
        arq_exe += '.out'  # Se for Linux/Mac

    # 3. Roda o comando do compilador: g++ arquivo.cpp -o arquivo.exe
    proc = subprocess.run(
        ['g++', arq_cpp, '-o', arq_exe], 
        check=False, capture_output=True, 
        text=True
    )

    # Se o returncode for diferente de 0, significa que deu Erro de Compilação (Syntax Error)
    if proc.returncode != 0:
        return False, proc.stderr, arq_cpp, None

    return True, "", arq_cpp, arq_exe

def avaliar_codigo(codigo_aluno, codigo_professor, casos_de_teste):
    """
    Avalia a submissão do aluno comparando com o gabarito do professor (em C++).
    """
    # Variáveis para podermos apagar os arquivos depois
    cpp_prof = exe_prof = cpp_aluno = exe_aluno = None

    resultado_final = {
        "sucesso": True, 
        "mensagem": "✅ Parabéns! Seu código passou em todos os testes.", 
        "testes_passados": 0
    }

    try:
        # --- 1. COMPILAR O GABARITO DO PROFESSOR ---
        sucesso_prof, erro_prof, cpp_prof, exe_prof = compilar_cpp(codigo_professor)
        if not sucesso_prof:
            return {"sucesso": False, "mensagem": "❌ Erro no código do Professor!\n" + erro_prof, "testes_passados": 0}

        # --- 2. COMPILAR O CÓDIGO DO ALUNO ---
        sucesso_aluno, erro_aluno, cpp_aluno, exe_aluno = compilar_cpp(codigo_aluno)
        if not sucesso_aluno:
            # Erro de compilação clássico (ex: esqueceu o ponto e vírgula ;)
            return {"sucesso": False, "mensagem": "❌ Erro de Compilação:\n" + erro_aluno, "testes_passados": 0}

        # --- 3. EXECUTAR OS TESTES ---
        for indice, entrada in enumerate(casos_de_teste):
            
            # Roda o executável do professor
            proc_prof = subprocess.run(
                [exe_prof], input=entrada, text=True, capture_output=True, timeout=2
            )
            saida_esperada = proc_prof.stdout.strip()

            # Roda o executável do aluno
            proc_aluno = subprocess.run(
                [exe_aluno], input=entrada, text=True, capture_output=True, timeout=2
            )
            saida_aluno = proc_aluno.stdout.strip()

            # Compara as saídas
            if saida_aluno != saida_esperada:
                resultado_final = {
                    "sucesso": False,
                    "mensagem": f"❌ Falha no Teste {indice + 1}.\nEntrada:\n{entrada}\n\nSaída Esperada:\n{saida_esperada}\n\nSua Saída:\n{saida_aluno}",
                    "testes_passados": indice
                }
                break

            resultado_final["testes_passados"] += 1

    except subprocess.TimeoutExpired:
         resultado_final = {
             "sucesso": False, 
             "mensagem": "⏳ Tempo limite excedido (Possível loop infinito ou pedindo dados a mais).", 
             "testes_passados": resultado_final.get("testes_passados", 0)
         }
    finally:
        # --- 4. FAXINA (Apaga os .cpp e os executáveis) ---
        arquivos_para_apagar = [cpp_prof, exe_prof, cpp_aluno, exe_aluno]
        for arq in arquivos_para_apagar:
            if arq and os.path.exists(arq):
                try:
                    os.remove(arq)
                except Exception:
                    pass # Ignora erros de arquivo trancado pelo Windows

    return resultado_final

# ==========================================
# ÁREA DE TESTE EM C++
# ==========================================
if __name__ == "__main__":
    codigo_do_professor = """
    #include <iostream>
    using namespace std;
    int main() {
        int a, b;
        cin >> a >> b;
        cout << a + b << endl;
        return 0;
    }
    """

    codigo_do_aluno_certo = """
    #include <iostream>
    using namespace std;
    int main() {
        int num1, num2;
        cin >> num1 >> num2;
        int soma = num1 + num2;
        cout << soma << endl;
        return 0;
    }
    """

    codigo_do_aluno_sem_ponto_e_virgula = """
    #include <iostream>
    using namespace std;
    int main() {
        int a, b
        cin >> a >> b;
        cout << a + b << endl;
        return 0;
    }
    """

    entradas_secretas = ["5\n3", "10\n10"]

    print("--- TESTANDO ALUNO CERTO ---")
    res1 = avaliar_codigo(codigo_do_aluno_certo, codigo_do_professor, entradas_secretas)
    print(res1['mensagem'])

    print("\n--- TESTANDO ALUNO COM ERRO DE SINTAXE ---")
    res2 = avaliar_codigo(codigo_do_aluno_sem_ponto_e_virgula, codigo_do_professor, entradas_secretas)
    print(res2['mensagem'])
