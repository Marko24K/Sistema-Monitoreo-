document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("overlay");
    const modalContainer = document.getElementById("modalContainer");
    const openModalButton = document.getElementById("openModal");
    const openModelo_sensor_Button = document.getElementById("openmodelo_sensor"); // Nuevo botón para el formulario de contacto
    //const openModelo_sensor_Button = document.getElementById(" ID_del_boton_donde_esta");
    
    // Función para cargar un formulario
    const loadModalContent = async (formType) => {
        const response = await fetch(`/modal/?form_type=${formType}`);
        if (response.ok) {
            const modalContent = await response.text();
            modalContainer.innerHTML = modalContent;

            // Mostrar el modal y fondo
            modalContainer.querySelector(".modal").style.display = "block";
            overlay.style.display = "block";

            // Añadir eventos de cierre
            const closeModalButton = modalContainer.querySelector("#closeModal");
            closeModalButton.addEventListener("click", closeModal);

            // Evitar que el clic en el fondo cierre el modal
            overlay.addEventListener("click", () => {
                alert("El fondo no cierra el modal. Usa el botón de cerrar.");
            });

            const modalForm = modalContainer.querySelector("#modalForm");
            modalForm.addEventListener("submit", (event) => {
                event.preventDefault(); // Evitar el envío real del formulario
                alert("Formulario enviado con éxito");
                closeModal();
            });
        } else {
            console.error("Error al cargar el modal");
        }
    }

    // Cargar el formulario cuando se hace clic en el botón correspondiente
    openModalButton.addEventListener("click", () => loadModalContent('form1'));  // Cargar formulario 1
    openModelo_sensor_Button.addEventListener("click", () => loadModalContent('form2'));  // Cargar formulario de contacto
    //openModelo_sensor_Button.addEventListener("click", () => loadModalContent('form3'));

    // Función para cerrar el modal
    function closeModal() {
        modalContainer.innerHTML = "";
        overlay.style.display = "none";
    }
});

