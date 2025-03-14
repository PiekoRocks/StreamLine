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

const pre = document.querySelector("pre");

document.addEventListener("mousemove", (e) => {
  rotateElement(e, pre);
});

function rotateElement(event, element) {
  // get mouse position
  const x = event.clientX;
  const y = event.clientY;
  // console.log(x, y)

  // find the middle
  const middleX = window.innerWidth / 2;
  const middleY = window.innerHeight / 2;
  // console.log(middleX, middleY)

  // get offset from middle as a percentage
  // and tone it down a little
  const offsetX = ((x - middleX) / middleX) * 45;
  const offsetY = ((y - middleY) / middleY) * 45;
  // console.log(offsetX, offsetY);

  // set rotation
  element.style.setProperty("--rotateX", offsetX + "deg");
  element.style.setProperty("--rotateY", -1 * offsetY + "deg");
}
