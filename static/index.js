document.addEventListener("DOMContentLoaded", function() {
    const showAddFormButton = document.getElementById('showAddFormButton');
    const addFormContainer = document.getElementById('addFormContainer');
    const editFormContainer = document.getElementById('editFormContainer');

    const hamburger = document.getElementById('hamburger');
    const navbar = document.getElementById('navbar');

    if (hamburger && navbar) {
        hamburger.addEventListener('click', function() {
            navbar.classList.toggle('active');
        });
    }
});

function hideForm(formId) {
    const formContainer = document.getElementById(formId);
    if (formContainer) {
        formContainer.style.display = 'none';
    }
    const showAddFormButton = document.getElementById('showAddFormButton');
    if (showAddFormButton) {
        showAddFormButton.style.display = 'block';
    }
}

function showEditForm(id) {
    const editRow = document.getElementById("editFormContainer_" + id);
    if (editRow) {
        editRow.style.display = "table-row";
        const formDiv = editRow.querySelector(".form-container");
        if (formDiv) {
            formDiv.classList.add("show");
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const infoSection = document.querySelector('.info');
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                infoSection.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    observer.observe(infoSection);
});