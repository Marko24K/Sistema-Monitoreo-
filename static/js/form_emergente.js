document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("overlay");
    const modalContainer = document.getElementById("modalContainer");
    const openModalButtons = document.querySelectorAll("[data-form-type]");

    window.loadModalContent = async (formType, idEspacio = '', idArduino = '') => {
        try {
            let url = `/modal/?form_type=${formType}`;
            
            if (formType === 'modelo_sensor') {
                if (!idArduino) {
                    console.error("El ID del Arduino es obligatorio para modelo_sensor.");
                    return;
                }
                url += `&id_arduino=${idArduino}`;
            }
            
            if (idEspacio) {
                url += `&id_espacio=${idEspacio}`;
            }
            
            const response = await fetch(url);
            if (response.ok) {
                const modalContent = await response.text();
                modalContainer.innerHTML = modalContent;
    
                const modal = modalContainer.querySelector(".modal");
                if (modal) {
                    modal.style.display = "block";
                    overlay.style.display = "block";
    
                    const closeModalButton = modal.querySelector("#closeModal");
                    if (closeModalButton) {
                        closeModalButton.addEventListener("click", closeModal);
                    }
                } else {
                    console.error("No se encontró el elemento modal dentro del contenido cargado.");
                }
            } else {
                console.error("No se pudo cargar el contenido del modal:", response.statusText);
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