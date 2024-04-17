console.log('Script loaded successfully');

document.addEventListener('DOMContentLoaded', function(){
    document.getElementById('fetchQuote').addEventListener('click', function(event) {
        event.preventDefault(); 

        fetch('/quotes?') 
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                document.getElementById('quote').textContent = data.quote;
            })
            .catch(error => {
                console.error('Error fetching quote:', error);
            });
    });

    document.getElementById('fetchAuthor').addEventListener('click', function(event) {
        event.preventDefault(); 

        const authorName = document.getElementById('query').value;
        fetch('/quotes?author=${authorName}') 
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                document.getElementById('quote').textContent = data.quote;
            })
            .catch(error => {
                console.error('Error fetching quote:', error);
            });
    });
});
