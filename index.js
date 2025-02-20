document.addEventListener("DOMContentLoaded", function() {
    const showAddFormButton = document.getElementById('showAddFormButton');
    const addFormContainer = document.getElementById('addFormContainer');
    const editFormContainer = document.getElementById('editFormContainer');

    if (showAddFormButton) {
        showAddFormButton.addEventListener('click', function() {
            addFormContainer.style.display = addFormContainer.style.display === 'none' ? 'block' : 'none';
            showAddFormButton.style.display = 'none';
        });
    }

    function showEditForm(data) {
        const editForm = document.getElementById('editForm');
        for (const key in data) {
            if (editForm[key]) {
                editForm[key].value = data[key];
            }
        }
        editFormContainer.style.display = 'block';
        showAddFormButton.style.display = 'none';
    }

    document.querySelectorAll('a[href="#edit"]').forEach(editLink => {
        editLink.addEventListener('click', function(event) {
            event.preventDefault();
            const row = this.closest('tr');
            const data = {};
            row.querySelectorAll('td').forEach((cell, index) => {
                const header = row.closest('table').querySelectorAll('th')[index].innerText.toLowerCase().replace(' ', '_');
                data[header] = cell.innerText;
            });
            showEditForm(data);
        });
    });
});

function hideForm(formId) {
    document.getElementById(formId).style.display = 'none';
    const showAddFormButton = document.getElementById('showAddFormButton');
    if (showAddFormButton) {
        showAddFormButton.style.display = 'block';
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