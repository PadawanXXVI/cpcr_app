document.addEventListener("DOMContentLoaded", function () {
  const inputNumero = document.getElementById("numero_processo");
  const alertaDiv = document.getElementById("alerta-processo");

  inputNumero.addEventListener("blur", function () {
    const numero = inputNumero.value.trim();
    alertaDiv.innerHTML = "";
    alertaDiv.style.display = "none";

    if (numero.length === 0) return;

    fetch("/verificar_processo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ numero_processo: numero }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.status === "existe") {
          const numeroFormatado = numero.replace(
            /^(\d{5})(\d{8})\/(\d{4})-(\d{2})$/,
            "$1-$2/$3-$4"
          );

          alertaDiv.innerHTML = `
            ⚠️ O processo <strong>${numeroFormatado}</strong> já está cadastrado.<br>
            <a href="/atualizar_processo/${data.id}" class="btn-destaque">→ Atualizar agora</a>
          `;
          alertaDiv.style.display = "block";
        } else if (data.status === "disponivel") {
          alertaDiv.innerHTML = "✅ Número de processo disponível.";
          alertaDiv.style.color = "green";
          alertaDiv.style.display = "block";
        }
      })
      .catch((err) => {
        console.error("Erro ao verificar processo:", err);
        alertaDiv.innerHTML = "⚠️ Erro ao validar número do processo.";
        alertaDiv.style.display = "block";
      });
  });

  // Extra: esconde o alerta ao digitar um novo número
  inputNumero.addEventListener("input", function () {
    alertaDiv.innerHTML = "";
    alertaDiv.style.display = "none";
    alertaDiv.style.color = "red"; // reset cor
  });
});
