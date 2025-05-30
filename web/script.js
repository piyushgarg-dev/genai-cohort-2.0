function addTodo() {
  const input = document.getElementById("todo-input");
  const value = input.value.trim();
  if (value === "") return;
  const ul = document.getElementById("todo-list");
  const li = document.createElement("li");
  li.textContent = value;
  ul.appendChild(li);
  input.value = "";
  input.focus();
}
document.getElementById("todo-input").addEventListener("keyup", function(event) {
  if (event.key === "Enter") {
    addTodo();
  }
});
