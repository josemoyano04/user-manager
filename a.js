const API_URL = "http://127.0.0.1:8000" //Modificar con URL de la API desplegada para uso en produccion
const ENDPOINT = "/user/me"
fetch(`${API_URL}${ENDPOINT}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
        user: {
            full_name: "example",
            username: "example",
            email: "user@example.com",
            password: "example"
        }
    })
})
.then(response => response.json())
.then(data => {
    console.log('Success:', data);
})
.catch((error) => {
    console.error('Error:', error);
});