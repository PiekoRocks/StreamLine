// Wait for the DOM to fully load
document.addEventListener("DOMContentLoaded", function() {
    // Show the add form when the button is clicked
    const showAddFormButton = document.getElementById('showAddFormButton');
    const addFormContainer = document.getElementById('addFormContainer');

    if (showAddFormButton && addFormContainer) {
        showAddFormButton.addEventListener('click', function() {
            addFormContainer.style.display = 'block';
            showAddFormButton.style.display = 'none';
        });
    }

    // Show the edit form when an edit button is clicked
    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(button => {
        button.addEventListener('click', function() {
            const id = this.getAttribute('data-id');
            const editFormContainer = document.getElementById('editFormContainer_' + id);
            if (editFormContainer) {
                editFormContainer.style.display = 'table-row';
            }
        });
    });

    // Animate the info section when it comes into view
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

    // Apply 3D effect to the about-container element
    const aboutContainer = document.querySelector(".about-container");

    document.addEventListener("mousemove", (e) => {
        rotateElement(e, aboutContainer);
    });

    function rotateElement(event, element) {
        // Get mouse position
        const x = event.clientX;
        const y = event.clientY;

        // Find the middle of the window
        const middleX = window.innerWidth / 2;
        const middleY = window.innerHeight / 2;

        // Calculate offset from the middle as a percentage
        const offsetX = ((x - middleX) / middleX) * 45;
        const offsetY = ((y - middleY) / middleY) * 45;

        // Set rotation based on mouse position
        element.style.setProperty("--rotateX", offsetX + "deg");
        element.style.setProperty("--rotateY", -1 * offsetY + "deg");
    }
});

// Hide the form and show the add button
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

// Show the edit form for a specific ID
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