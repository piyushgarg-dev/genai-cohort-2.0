
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("todo-input");
    const addBtn = document.getElementById("add-btn");
    const list = document.getElementById("todo-list");

    function addTask() {
        const task = input.value.trim();
        if (task === "") return;
        const li = document.createElement("li");
        li.innerHTML =
            `<span>${task}</span> <button class="delete-btn">&#10005;</button>`;
        list.appendChild(li);
        input.value = "";
    }

    addBtn.addEventListener("click", addTask);
    input.addEventListener("keydown", e => {
        if (e.key === "Enter") addTask();
    });
    list.addEventListener("click", e => {
        if (e.target.classList.contains("delete-btn")) {
            e.target.parentElement.remove();
        }
    });
});

