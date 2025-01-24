document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("overlay");
    const modalContainer = document.getElementById("modalContainer");
    const openModalButtons = document.querySelectorAll("[data-form-type]");

    // Cargar contenido del modal por AJAX
    const loadModalContent = async (formType, idEspacio) => {
        try {
            // Si es un formulario de división de espacio, agregamos el id_espacio
            const response = await fetch(`/modal/?form_type=${formType}&id_espacio=${idEspacio || ''}`);
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
        } catch (error) {
            console.error("Error al cargar el modal:", error);
        }
    };

    // Escuchar el clic en los botones con data-form-type
    openModalButtons.forEach(button => {
        button.addEventListener("click", (e) => {
            e.preventDefault();  // Evitar la acción predeterminada (la redirección)
            
            const formType = button.getAttribute("data-form-type");
            const idEspacio = button.getAttribute("data-id-espacio");

            loadModalContent(formType, idEspacio);
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