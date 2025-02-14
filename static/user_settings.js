function editUser() {
    const username = document.getElementById("newUsername").value.trim();
    const messageElement = document.getElementById("editUserMessage");

    fetch("/user/settings/edit", {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({username})
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            messageElement.innerHTML = `<span class="text-danger">${data.error}</span>`;
        } else {
            messageElement.innerHTML = `<span class="text-success">${data.message}</span>`;
            document.getElementById("editUserForm").reset();
            setTimeout(() => window.location.reload(), 2000);
        }
    })
    .catch(error => {
        messageElement.innerHTML = `<span class="text-danger">Błąd serwera: ${error.message}</span>`;
    });
}