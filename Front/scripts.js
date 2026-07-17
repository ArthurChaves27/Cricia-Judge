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
function processarSubmissao() {
    if (codigoAtualDoAluno.trim() === "") {
        alert("O código está vazio ou o editor ainda está carregando!");
        return;
    }

    abrirModal("Processando...", "Enviando seu código para o Juiz em Python.");

    console.log("Código capturado silenciosamente que irá para o Python:");
    console.log(codigoAtualDoAluno);

    // Simulando o tempo de resposta do servidor Python
    setTimeout(function() {
        exibirResultadoFinal(true); 
    }, 2000);
}

// Funções Auxiliares Visuais
function abrirModal(titulo, mensagem) {
    feedbackTitulo.innerText = titulo;
    feedbackMensagem.innerText = mensagem;
    modal.style.display = 'flex';
}

function fecharModal() {
    modal.style.display = 'none';
}

function exibirResultadoFinal(sucesso) {
    if (sucesso) {
        feedbackTitulo.innerText = "✅ Sucesso! Nota 10";
        feedbackTitulo.style.color = "#28a745";
        feedbackMensagem.innerText = "Parabéns! Seu código passou em todos os casos de teste.";
    }
}

