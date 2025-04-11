document.addEventListener("DOMContentLoaded", function () {
    const inputNumero = document.getElementById("numero_processo");
    const avisoDiv = document.getElementById("alerta-processo");
  
    inputNumero.addEventListener("blur", function () {
      const numero = inputNumero.value.trim();
  
      if (numero.length < 5) {
        avisoDiv.innerHTML = "";
        avisoDiv.style.display = "none";
        return;
      }
  
      fetch(`/verificar_processo?numero_processo=${encodeURIComponent(numero)}`)
        .then(response => response.json())
        .then(data => {
          if (data.existe) {
            avisoDiv.innerHTML = `
              ⚠️ Este processo já está cadastrado.
              <a href="/atualizar_processo/${data.id}" class="btn-secondary" style="margin-top:0.5rem;display:inline-block;">Clique aqui para atualizá-lo</a>.
            `;
            avisoDiv.style.display = "block";
          } else {
            avisoDiv.innerHTML = "";
            avisoDiv.style.display = "none";
          }
        })
        .catch(err => {
          console.error("Erro ao validar o número do processo:", err);
          avisoDiv.innerHTML = "Erro na validação. Tente novamente.";
          avisoDiv.style.display = "block";
        });
    });
  });
  