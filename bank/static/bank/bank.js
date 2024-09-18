document.addEventListener('DOMContentLoaded', function() {

    // check receiver name

    const receiverAccount = document.getElementById('transfer-receiver');
    const receiverName = document.getElementById('transfer-receiver-name');

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
});            