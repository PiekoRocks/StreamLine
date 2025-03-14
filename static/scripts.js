document.addEventListener("DOMContentLoaded", function () {
    const showAddFormButton = document.getElementById("showAddFormButton");
    const addFormContainer = document.getElementById("addFormContainer");

    if (showAddFormButton && addFormContainer) {
        showAddFormButton.addEventListener("click", function () {
            addFormContainer.style.display = "block";
        });
    } else {
        console.error("🚨 Missing 'showAddFormButton' or 'addFormContainer'.");
    }
});

function hideForm(id) {
    const formContainer = document.getElementById(id);
    if (formContainer) {
        formContainer.style.display = "none";
        const form = formContainer.querySelector("form");
        if (form) {
            form.reset();
        }
    }
}

function showEditForm(id) {
    const editRow = document.getElementById("editFormContainer_" + id);
    if (editRow) {
        editRow.style.display = "table-row";
        const formDiv = editRow.querySelector(".form-container");
        if (formDiv) {
            formDiv.style.display = "block";
        }
    }
}