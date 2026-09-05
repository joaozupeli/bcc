fetch("https://localhost:8000/",{
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        name: "John Doe",
        email: "john.doe@example.com"
    })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));


