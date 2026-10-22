// 1. Variável global para armazenar o código do aluno em tempo real
let codigoAtualDoAluno = "";

// 2. O evento que você descobriu! Ele intercepta as mensagens do Iframe
window.onmessage = function (e) {
    // Verifica se a mensagem contém dados de linguagem (vem do OneCompiler)
    if (e.data && e.data.language) {
        // A estrutura do OneCompiler geralmente envia o código dentro de "files"
        if (e.data.files && e.data.files.length > 0) {
            codigoAtualDoAluno = e.data.files[0].content;
        }
    }
};

// 3. Configuração do Botão e Modal
const botaoSubmeter = document.getElementById('btn-submeter');
const modal = document.getElementById('feedback-modal');
const feedbackTitulo = document.getElementById('feedback-titulo');
const feedbackMensagem = document.getElementById('feedback-mensagem');

botaoSubmeter.addEventListener('click', processarSubmissao);

// 4. A função que envia o código interceptado
// ... (mantenha a parte de cima do arquivo igual) ...

// 4. A função que envia o código pela rede para o Python
async function processarSubmissao() {
    if (codigoAtualDoAluno.trim() === "") {
        alert("O código está vazio ou o editor ainda está carregando!");
        return;
    }

    abrirModal("Processando...", "Enviando seu código para o Juiz em Python.");

    try {
        // Envia o código para o nosso servidor FastAPI
        const resposta = await fetch("http://localhost:8000/api/submeter", {
            method: "POST", // Método de envio de dados
            headers: {
                "Content-Type": "application/json"
            },
            // Empacota o código capturado do OneCompiler
            body: JSON.stringify({ codigo_aluno: codigoAtualDoAluno }) 
        });

        // Recebe a resposta (O dicionário que o juiz.py gerou)
        const resultado = await resposta.json();
        
        // Exibe o resultado real na tela!
        exibirResultadoFinal(resultado.sucesso, resultado.mensagem);

    } catch (erro) {
        exibirResultadoFinal(false, "❌ Erro de conexão! O servidor Python está rodando?");
        console.error(erro);
    }
}

// ... (mantenha o abrirModal e fecharModal igual) ...

// Atualizamos a função para mostrar a mensagem exata que o Python gerou


// Funções Auxiliares Visuais
function abrirModal(titulo, mensagem) {
    feedbackTitulo.innerText = titulo;
    feedbackMensagem.innerText = mensagem;
    modal.style.display = 'flex';
}

function fecharModal() {
    modal.style.display = 'none';
}

function exibirResultadoFinal(sucesso, mensagemDoPython) {
    if (sucesso) {
        feedbackTitulo.innerText = "✅ Sucesso! Nota 10";
        feedbackTitulo.style.color = "#28a745";
    } else {
        feedbackTitulo.innerText = "❌ Falha na Submissão";
        feedbackTitulo.style.color = "#dc3545";
    }
    // Mostra a mensagem detalhada (os erros de sintaxe ou a saída errada)
    feedbackMensagem.innerText = mensagemDoPython;
}
