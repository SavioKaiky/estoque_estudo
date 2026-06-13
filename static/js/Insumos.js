/**
 * Mostra ou esconde o campo "Valor total da compra"
 * dependendo se o tipo selecionado é "entrada" ou "saida".
 */
function toggleValorTotal() {
    const tipoSelect = document.getElementById("tipo");
    const valorInput = document.getElementById("valor_total");

    if (!tipoSelect || !valorInput) return;

    if (tipoSelect.value === "entrada") {
        valorInput.style.display = "block";
        valorInput.required = true;
    } else {
        valorInput.style.display = "none";
        valorInput.required = false;
        valorInput.value = "";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const tipoSelect = document.getElementById("tipo");

    if (tipoSelect) {
        toggleValorTotal();
        tipoSelect.addEventListener("change", toggleValorTotal);
    }
});