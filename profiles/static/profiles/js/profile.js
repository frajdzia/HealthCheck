//runs only when HTMl doc has finished loading
document.addEventListener("DOMContentLoaded", function () {
    const editButton = document.getElementById("editButton");
    const saveButton = document.getElementById("saveButton");
    const form = document.querySelector("form");
    const formFields = form.querySelectorAll("input, select, textarea");

    // save btn hidden here
    saveButton.style.display = "none";

    //handles 'edit' button being clicked
    editButton.addEventListener("click", () => {
        formFields.forEach((field) => {
            if (field.id !== "role") {
                field.disabled = false; // all other fields apart from role not disabled
            }
        });

        editButton.style.display = "none";
        saveButton.style.display = "inline-block";
    });

    //handles any accidental submits, ensures that if a form has been submitted without any changes then no change message will be displayed
    form.addEventListener("submit", (e) => {
        const isFormEnabled = Array.from(formFields).some((field) => !field.disabled && field.id !== "role");
        if (!isFormEnabled) {
            e.preventDefault();
        }
    });
});
