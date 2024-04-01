document.addEventListener("DOMContentLoaded", function(){
    document.getElementById('stockInp').addEventListener('keyup', function(){
        const val = document.getElementById('stockInp').value;
        if (val.length > 0){
            fetch("https://api.polygon.io/v3/reference/tickers?search="+ val +"&active=true&limit=5&apiKey=LnR21zv6euM7KmY_HafxN9XgwdnmltXE")
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json()

            })
            .then(data => {
                var stockSuggestions = document.getElementById("stockSuggestions");
                while (stockSuggestions.firstChild) {
                    stockSuggestions.removeChild(stockSuggestions.firstChild);
                  }
                  

                data['results'].forEach(element => {
                    var listItem = document.createElement("li");
                    listItem.textContent = element.ticker;
                    stockSuggestions.appendChild(listItem);

                });
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        }
        else{
            var stockSuggestions = document.getElementById("stockSuggestions");
            while (stockSuggestions.firstChild) {
                stockSuggestions.removeChild(stockSuggestions.firstChild);
              }

        }

        })
})