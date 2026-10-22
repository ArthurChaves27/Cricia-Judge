from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from judge import avaliar_codigo  # Importa o seu robô avaliador!
from pydantic import BaseModel

app = FastAPI()

# Configuração de CORS: Permite que o seu site HTML converse com este servidor Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # No MVP, aceitamos requisições de qualquer lugar
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define o formato do pacote que o JavaScript vai enviar
class SubmissaoAluno(BaseModel):
    codigo_aluno: str

# O Gabarito do Professor (Em um projeto real, viria do Banco de Dados)
CODIGO_PROFESSOR = """
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
"""
# As entradas secretas para os testes
ENTRADAS = ["5\n3", "10\n10", "100\n-50"]

# Criando a Rota (A "porta" que o JavaScript vai bater)
@app.post("/api/submeter")
def receber_submissao(submissao: SubmissaoAluno):
    print("Recebi um código do aluno! Avaliando...")
    
    # Chama o nosso juiz passando o código que veio da web, o gabarito e os testes
    resultado = avaliar_codigo(submissao.codigo_aluno, CODIGO_PROFESSOR, ENTRADAS)
    
    # Devolve o resultado de volta para o JavaScript
    return resultado
