
document.getElementById('authorizeButton').addEventListener('click', () => {
    var apiInputValue = document.getElementById('apiInput').value;
    
    fetch('http://localhost:5000/authorize', {
        method: 'GET',
        headers: {
            'X-API-KEY': apiInputValue
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to authorize: ' + response.statusText);
        }
        return response.text();
    })
    .then(data => {
        console.log('Response:', data);
        alert('Authorized Successfully!');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Authorization Failed!');
    });
});
