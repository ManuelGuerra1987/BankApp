document.addEventListener('DOMContentLoaded', function() {

    // check receiver name

    const receiverAccount = document.getElementById('transfer-receiver');
    const receiverName = document.getElementById('transfer-receiver-name');

    if (receiverAccount && receiverName) {

        receiverAccount.addEventListener('input', () => {

            if (receiverAccount.value.length > 0) {

                fetch(`/get_name/${receiverAccount.value}`)
                .then(response => response.json())
                .then(data => {
                    if (data.name) {
                        receiverName.value = data.name;
                    } else {
                        receiverName.value = "Account not found";
                    }
                })    
                .catch(error => {
                    console.error('Error:', error);
                    receiverName.value = "Error retrieving name";
                });
            } else {
                receiverName.value = '';
            }
        });

    }
    // Eur rate

    const quoteButton = document.getElementById('eur_quote_button');
    const exchangeRateInput = document.getElementById('exchange_rate_hidden');

    if (quoteButton) {

    quoteButton.addEventListener('click', () => {
        fetch('https://api.exchangeratesapi.io/latest?access_key=cf0fd16b97736e34655275d658aa5731')
        .then(response => response.json())
        .then(data => {

            const rate = data.rates.USD;
            document.querySelector('#eur_quote').innerHTML = `EUR/USD: ${rate.toFixed(2)}`;
            exchangeRateInput.value = rate;
        })
        .catch(error => {console.log('Error:', error);

        });

    });
    }

    // Stocks price

    const stockQuoteButton = document.getElementById('stock-quote-button');

    if (stockQuoteButton) {

        const stockSymbol = document.getElementById('stock-symbol');
        const stockPrice = document.getElementById('stock-price');
        const stockPriceHidden = document.getElementById('stock-price-hidden');
        const stockAmount = document.getElementById('stock-amount');
        const stockShares = document.getElementById('stock-shares');

        stockQuoteButton.addEventListener('click', () => {

            fetch(`/get_stock_price/${stockSymbol.value}`)
            .then(response => response.json())
            .then(data => {
                stockPrice.value = data.price
                stockPriceHidden.value = data.price

                const price = parseFloat(stockPrice.value);
                const shares = parseFloat(stockShares.value);

                if (!isNaN(price) && !isNaN(shares)) {
                    stockAmount.value = (price * shares).toFixed(2);
                } else {
                    stockAmount.value = "";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                stockPrice.value = "Error retrieving name";
            });


        });    

        stockShares.addEventListener('input', () => {

            const price = parseFloat(stockPrice.value);
            const shares = parseFloat(stockShares.value);

            if (!isNaN(price) && !isNaN(shares)) {
                stockAmount.value = (price * shares).toFixed(2);
            } else {
                stockAmount.value = "";
            }
        });
       
    }        
});                    