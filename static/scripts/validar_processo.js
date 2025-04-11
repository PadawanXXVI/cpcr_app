// static/scripts/validar_processo.js

document.addEventListener("DOMContentLoaded", function () {
    const inputNumero = document.getElementById("numero_processo");
    const avisoDiv = document.getElementById("aviso_processo_existente");

    inputNumero.addEventListener("blur", function () {
        const numero = inputNumero.value.trim();

        if (numero.length === 0) {
            avisoDiv.innerHTML = "";
            return;
        }

        fetch(`/verificar_processo?numero=${encodeURIComponent(numero)}`)
            .then(response => response.json())
            .then(data => {
                if (data.existente) {
                    avisoDiv.innerHTML = `
                        <div class="alert">
                            Este processo já está cadastrado.
                            <a href="/atualizar_processo/${data.id}" class="btn-secondary">Atualizar agora</a>
                        </div>`;
                } else {
                    avisoDiv.innerHTML = "";
                }
            })
            .catch(err => {
                console.error("Erro na validação do processo:", err);
            });
    });
});
