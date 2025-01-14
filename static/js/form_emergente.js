document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("overlay");
    const modalContainer = document.getElementById("modalContainer");
    const openModalButtons = document.querySelectorAll("[data-form-type]");

    // Función para cargar un formulario dinámico
    const loadModalContent = async (formType) => {
        try {
            const response = await fetch(`/modal/?form_type=${formType}`);
            if (response.ok) {
                const modalContent = await response.text();
                modalContainer.innerHTML = modalContent;

                // Mostrar el modal y el fondo
                modalContainer.querySelector(".modal").style.display = "block";
                overlay.style.display = "block";
                modalContainer.setAttribute("aria-hidden", "false");
                overlay.setAttribute("aria-hidden", "false");

                // Cerrar el modal
                const closeModalButton = modalContainer.querySelector("#closeModal");
                if (closeModalButton) {
                    closeModalButton.addEventListener("click", closeModal);
                }
            } else {
                modalContainer.innerHTML = "<p>Error al cargar el formulario. Intenta nuevamente.</p>";
            }
        } catch (error) {
            console.error("Error al cargar el modal:", error);
            modalContainer.innerHTML = "<p>Ocurrió un error. Intenta nuevamente más tarde.</p>";
        }
    };

    // Asociar eventos a los botones para cargar el formulario correspondiente
    openModalButtons.forEach(button => {
        button.addEventListener("click", () => {
            const formType = button.getAttribute("data-form-type");
            loadModalContent(formType);
        });
    });

    // Función para cerrar el modal
    function closeModal() {
        modalContainer.innerHTML = "";
        overlay.style.display = "none";
        modalContainer.setAttribute("aria-hidden", "true");
        overlay.setAttribute("aria-hidden", "true");
    }
});
