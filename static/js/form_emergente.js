document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("overlay");
    const modalContainer = document.getElementById("modalContainer");
    const openModalButtons = document.querySelectorAll("[data-form-type]");

    const loadModalContent = async (formType) => {
        const response = await fetch(`/modal/?form_type=${formType}`);
        if (response.ok) {
            const modalContent = await response.text();
            modalContainer.innerHTML = modalContent;
            modalContainer.querySelector(".modal").style.display = "block";
            overlay.style.display = "block";

            const closeModalButton = modalContainer.querySelector("#closeModal");
            closeModalButton.addEventListener("click", closeModal);
        } else {
            console.error("No se pudo cargar el modal");
        }
    };

    openModalButtons.forEach(button => {
        button.addEventListener("click", () => {
            const formType = button.getAttribute("data-form-type");
            loadModalContent(formType);
        });
    });

    function closeModal() {
        modalContainer.innerHTML = "";
        overlay.style.display = "none";
        modalContainer.setAttribute("aria-hidden", "true");
        overlay.setAttribute("aria-hidden", "true");
    }
});
