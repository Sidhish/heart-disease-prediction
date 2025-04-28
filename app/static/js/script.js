document.getElementById('predictionForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if(data.status === 'success') {
            resultDiv.innerHTML = `
                <h3>${data.prediction}</h3>
                <p>Based on your input:</p>
                <pre>${JSON.stringify(data.details, null, 2)}</pre>
            `;
        } else {
            resultDiv.innerHTML = `<p class="error">Error: ${data.message}</p>`;
        }
    });
});