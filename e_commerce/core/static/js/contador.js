var quantidadeElemento = document.getElementById('quantidade');
var quantidade = 0;

function incrementar() {
    quantidade++;
    atualizarQuantidade();
}

function decrementar() {
    if (quantidade > 0) {
        quantidade--;
        atualizarQuantidade();
    }
}

function atualizarQuantidade() {
    quantidadeElemento.textContent = quantidade;
}

document.getElementById('incrementar').addEventListener('click', incrementar);
document.getElementById('decrementar').addEventListener('click', decrementar);
