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
