$(document).ready(function(){
    $('#get-history').click(function(){
        $.ajax({
            url: '/api/trackers',
            type: 'GET',
            success: function(response) {
                $('#data-container').html('');
                response.quotes.forEach(function(item) {
                    $('#price-history').append(
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
            error: function(xhr, status, error) {
                console.error(`Ocorreu um erro: ${status} ${error}`);
            }
        });
    });
});