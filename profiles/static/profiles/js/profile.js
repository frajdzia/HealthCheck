document.addEventListener("DOMContentLoaded", function () {
    const editButton = document.getElementById("editButton");
    const saveButton = document.getElementById("saveButton");
    const formFields = document.querySelectorAll("input, select");

    formFields.forEach((field) => {
        if (field.id !== "role") {
            field.disabled = true;
        }
    });

    if (editButton) {
        editButton.addEventListener("click", () => {
            formFields.forEach((field) => {
                if (field.id !== "role") {
                    field.disabled = false;
                }
            });

            editButton.style.display = "none";
            saveButton.disabled = false;
            saveButton.style.display = "inline-block";
        });
    }
});
