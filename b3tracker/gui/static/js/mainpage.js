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

// Função para avaliar se o email está preenchido e é válido
const validateEmail = (email) => {
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; //Validar se o texto tem formato de email mesmo
    return emailRe.test(email)
}

// Função para validar se os valores de monitoramento fazem sentido
const validateTrackData = (minEl, maxEl, freq) => {
    const minRange = minEl >= 1 && minEl <= 999;
    const maxRange = maxEl >= 1 && maxEl <= 999;
    const freqRange = freq >= 1 && freq <= 60;
    const maxLogic = maxEl > minEl;
    return minRange && maxRange && freqRange && maxLogic;
}

/*
Buscar csrf token, foi necessário pois tomava 403 ao realizar o POST 
e o decorator do django para isso não estava funcionando 
*/
const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(() => {
    populateSelect($("#ticker-select-1"));
});

// Botão para buscar histórico de preços
$("#get-history").click(() => {

    const email = $("#email-input").val();

    if (validateEmail(email)) {
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

// Botão adicionar ativo
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
            
            <button id="start-track-${formGroupCount + 1}" class="btn btn-success">Iniciar</button>
            <button id="stop-track-${formGroupCount + 1}" class="btn btn-danger">Parar</button>

            <label for="track-id-${formGroupCount + 1}">ID:</label>
            <input id="track-id-${formGroupCount + 1}" class="form-control" name="track-id-${formGroupCount + 1}" type="text" placeholder="Aguardando início..." readonly />
        </div>
    `);

    // console.log("Elemento criado: ", newFormGroup)

    $("#ticker-form-fields").append(newFormGroup);

    populateSelect(newFormGroup.find("select"));
});

//Botões de iniciar
$("#track-data").on("click", "[id^=start-track-]", function(event) {
    event.preventDefault();
    
    const currButtonId = $(this).attr('id');
    const formNum = currButtonId[currButtonId.length - 1];
    
    const email = $("#email-input").val();
    const ticker = $(`#ticker-select-${formNum}`).val();
    const minEl = Number($(`#min-value-${formNum}`).val());
    const maxEl = Number($(`#max-value-${formNum}`).val());
    const freq = Number($(`#frequency-${formNum}`).val());

    if (validateTrackData(minEl, maxEl, freq) && validateEmail(email)) {
        //console.log("Funfou!", currButtonId, formNum, minEl, maxEl, freq, ticker);
        const payload = {
            "email": email,
            "order_data":{
                "ticker_code": ticker,
                "buy_limit": minEl,
                "sell_limit": maxEl,
                "frequency": freq,
            }
        }

        $.ajax({
            url: `/api/trackers`,
            type: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            contentType: "application/json",
            data: JSON.stringify(payload),
            success: (response) => {
                $(`#track-id-${formNum}`).val(response.task);
            },
            error: (xhr, status, error) => {
                console.error(`Ocorreu um erro: ${status} ${error}`);
            }
        });

    } else {
        // TODO: Trocar o alert por um modal mais bonito
        alert(`
            Insira valores válidos:
            * É necessário informar um email
            * Preço mínimo: 1 até 999
            * Preço máximo: 1 até 999
            * Periodicidade: 1 até 60
            * Preço máximo maior do que o mínimo
        `);
    }
});

//Botões de parar
$("#track-data").on("click", "[id^=stop-track-]", function(event) {
    event.preventDefault();
    
    const currButtonId = $(this).attr('id');
    const formNum = currButtonId[currButtonId.length - 1];
    const currTrackId = $(`#track-id-${formNum}`).val();

    $.ajax({
        url: `/api/trackers/${currTrackId}`,
        type: "PUT",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        success: (response) => {
            $(`#track-id-${formNum}`).val("");
            console.log(response.task, "Interrompido!")
        },
        error: (xhr, status, error) => {
            console.error(`Ocorreu um erro: ${status} ${error}`);
        }
    });
});