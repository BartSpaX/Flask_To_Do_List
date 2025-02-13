function assignTask() {
    const userId = document.getElementById("userSelect").value;
    const taskTitle = document.getElementById("taskTitle").value.trim();
    const messageElement = document.getElementById("message");

    if (!taskTitle) {
        messageElement.innerHTML = '<span class="text-danger">Treść zadania nie może być pusta.</span>';
        return;
    }

    fetch("/api/admin/assign-task", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, title: taskTitle })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            messageElement.innerHTML = `<span class="text-danger">${data.error}</span>`;
        } else {
            messageElement.innerHTML = `<span class="text-success">${data.message}</span>`;
            document.getElementById("taskTitle").value = ""; // Wyczyść pole po dodaniu
        }
    })
    .catch(error => {
        messageElement.innerHTML = `<span class="text-danger">Błąd serwera: ${error.message}</span>`;
    });
}

function manageUser() {
    const userId = document.getElementById("userSelect").value;
    if (userId) {
        window.location.href = `/admin/manage-users/user/${userId}`;
    }
}

function deleteUser() {
    const userId = document.getElementById("userSelect").value;
    if (!userId) {
        alert("Wybierz użytkownika do usunięcia!");
        return;
    }

    const confirmDelete = confirm("Czy na pewno chcesz usunąć tego użytkownika?");
    if (!confirmDelete) return;

    fetch(`/admin/manage-users/user/delete-user/${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);  // Wyświetlamy komunikat z Flask
        window.location.reload();  // Odświeżamy stronę po usunięciu użytkownika
    })
    .catch(error => alert("Błąd: " + error.message));
}

