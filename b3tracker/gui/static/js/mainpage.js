// Função para preencher selects
const populateSelect = (selectElement) => {
    $.ajax({
        url: "/api/tickers",
        method: "GET",
        dataType: "json",
        success: (data) => {
            
            // const selectElement = $("#ticker-select-1");

            selectElement.empty();

            $.each(data, (index, option) => {
                let optionElement = $("<option></option>")
                    .val(option) 
                    .text(option);
                selectElement.append(optionElement);
            });
        },
        error: (xhr, status, error) => {
            console.error("Error fetching data:", error);
        }
    });
}

$(document).ready(() => {
    $("#get-history").click(() => {

        const email = $("#email-input").val();
        
        const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; //Validar se o texto tem formato de email mesmo

        if (emailRe.test(email)) {
            $.ajax({
                url: `/api/trackers?email=${email}`,
                type: "GET",
                success: (response) => {
                    
                    // $("#fill-email-div").hide();
                    // $("#tracker-history-table").show();
                    
                    $("#price-history").html("");

                    response.quotes.forEach((item) => {
                        $("#price-history").append(
                            `
                            <tr>
                                <td>${item.requester_email}</td>
                                <td>${item.ticker_code}</td>
                                <td>${item.quote_price}</td>
                                <td>${item.task_id}</td>
                            </tr>
                            `
                        );
                    });
                },
                error: (xhr, status, error) => {
                    console.error(`Ocorreu um erro: ${status} ${error}`);
                }
            });
        } else {
            alert("Por favor, insira um endereço de e-mail válido.");
        }
    });

    populateSelect($("#ticker-select-1"));
    
});

$("#add-select-btn").click(() => {

    const formGroupCount = $(".form-group").length;

    const newFormGroupId = `select-form-group-${formGroupCount + 1}`;
    const newFormGroup = $(`
        <div class="form-group" id="${newFormGroupId}">
            <select name="ticker-select-${formGroupCount + 1}" id="ticker-select-${formGroupCount + 1}" form="track-data"></select>
            
            <label for="min-value-${formGroupCount + 1}">Valor Mínimo:</label>
            <input type="number" id="min-value-${formGroupCount + 1}" name="min-value-${formGroupCount + 1}" min="1" max="999">
            
            <label for="max-value-${formGroupCount + 1}">Valor Máximo:</label>
            <input type="number" id="max-value-${formGroupCount + 1}" name="max-value-${formGroupCount + 1}" min="1" max="999">
    
            <label for="frequency-${formGroupCount + 1}">Periodicidade (em minutos):</label>
            <input type="number" id="frequency-${formGroupCount + 1}" name="frequency-${formGroupCount + 1}" min="1" max="60">
        </div>
    `);

    // console.log("Elemento criado: ", newFormGroup)

    $("#ticker-form-fields").append(newFormGroup);

    populateSelect(newFormGroup.find("select"));
});