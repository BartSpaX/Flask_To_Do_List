document.addEventListener("DOMContentLoaded", () => {
    loadTasks();

    document.getElementById("taskForm").addEventListener("submit", function(event) {
        event.preventDefault();  // Zapobiega przeładowaniu strony
        addTask();
    });
});

// Pobieranie zadań z REST API i wyświetlanie ich w HTML
function loadTasks() {
    fetch("/api/tasks")
        .then(response => response.json())
        .then(tasks => {
            const tasksList = document.getElementById("tasksList");
            const completedTasksList = document.getElementById("completedTasksList");

            tasksList.innerHTML = "";
            completedTasksList.innerHTML = "";

            tasks.forEach(task => {
                const listItem = document.createElement("li");
                listItem.className = "list-group-item d-flex justify-content-between align-items-center";
                listItem.innerHTML = `
                    ${task.done ? `<s>${task.title}</s>` : task.title}
                    <div>
                        <button class="btn btn-${task.done ? "warning" : "success"} btn-sm" onclick="toggleTask(${task.id}, ${!task.done})">
                            ${task.done ? "↺" : "✓"}
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="deleteTask(${task.id})">✗</button>
                    </div>
                `;

                if (task.done) {
                    completedTasksList.appendChild(listItem);
                } else {
                    tasksList.appendChild(listItem);
                }
            });
        })
        .catch(error => console.error("Błąd pobierania zadań:", error));
}

// Dodawanie nowego zadania
function addTask() {
    const taskInput = document.getElementById("taskInput");
    const taskTitle = taskInput.value.trim();

    if (!taskTitle) {
        alert("Nie możesz dodać pustego zadania!");
        return;
    }

    fetch("/api/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: taskTitle })
    })
    .then(response => response.json())
    .then(() => {
        taskInput.value = "";  // Czyścimy pole po dodaniu
        loadTasks();  // Odświeżamy listę
    })
    .catch(error => console.error("Błąd dodawania zadania:", error));
}

// Oznaczanie zadania jako ukończone / przywracanie
function toggleTask(taskId, status) {
    fetch(`/api/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ done: status })
    })
    .then(() => loadTasks())
    .catch(error => console.error("Błąd zmiany statusu zadania:", error));
}

// Usuwanie zadania
function deleteTask(taskId) {
    fetch(`/api/tasks/${taskId}`, { method: "DELETE" })
    .then(() => loadTasks())
    .catch(error => console.error("Błąd usuwania zadania:", error));
}
