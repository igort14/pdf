// Selecionar os elementos do DOM
const form = document.getElementById("pdf-form");
const resultDiv = document.getElementById("result");

// Adicionar evento ao formulário
form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Impedir envio padrão do formulário

    const formData = new FormData(form); // Capturar os dados do formulário

    // Exibir mensagem de processamento
    resultDiv.innerHTML = "<p>Processando o arquivo... Por favor, aguarde.</p>";

    try {
        // Enviar os dados para o backend
        const response = await fetch("/process-pdf", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            // Exibir o link para download do PDF gerado
            resultDiv.innerHTML = `
                <p>PDF gerado com sucesso!</p>
                <a href="/${data.pdf}" target="_blank" style="color: blue; text-decoration: underline;">Clique aqui para baixar o PDF</a>
            `;
        } else {
            // Exibir mensagem de erro
            resultDiv.innerHTML = `<p style="color: red;">Erro: ${data.error}</p>`;
        }
    } catch (error) {
        // Exibir erro geral
        resultDiv.innerHTML = `<p style="color: red;">Erro ao processar o PDF: ${error.message}</p>`;
    }
});
