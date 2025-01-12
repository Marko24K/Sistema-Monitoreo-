function mostrarImagen(inputElementId, contenedorElementId, imagenPredeterminada ='/static/img/img_parcela.png'){
    const inputImagen = document.getElementById(inputElementId);
    const contenedorImagen = document.getElementById(contenedorElementId);

    // Función para actualizar la imagen
    function actualizarImagen(src) {
        // Limpiar el contenedor antes de mostrar la nueva imagen
        contenedorImagen.innerHTML = '';  // Limpia el contenedor
        const img = document.createElement('img');
        img.src = src;
        contenedorImagen.appendChild(img);  // Agrega la nueva imagen al contenedor
    }

    // Mostrar la imagen predeterminada inicialmente
    actualizarImagen(imagenPredeterminada);

    // Escuchamos el cambio en el input de tipo file
    inputImagen.addEventListener('change', function(event) {
        const file = event.target.files[0];

        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Cuando el archivo es cargado, actualizamos el contenedor con la nueva imagen
                actualizarImagen(e.target.result);
            };
            reader.readAsDataURL(file);  // Leemos el archivo como DataURL
        } else {
            // Si no se selecciona una imagen, mostramos la imagen predeterminada
            actualizarImagen(imagenPredeterminada);
        }
    });
}

// Función de validación
function validarFormulario() {
    // Obtiene todos los campos de texto en el formulario
    const campos = [
        document.getElementById('validacion_01'),
        document.getElementById('validacion_02'),
        document.getElementById('validacion_Username'),
        document.getElementById('validacion_03')
    ];

    // Itera sobre cada campo para verificar si contiene espacios en blanco
    for (let i = 0; i < campos.length; i++) {
        let valor = campos[i].value.trim(); // Elimina espacios al principio y al final
        if (valor.includes(" ") || valor === "") {
            alert("Los campos no pueden contener espacios en blanco.");
            return false; // Detiene el envío del formulario
        }
    }

    // Si todos los campos son válidos, permite el envío del formulario
    return true;
}

// Llamamos a la función cuando se cargue la página
document.addEventListener('DOMContentLoaded', function() {
    mostrarImagen('input-imagen', 'imagen-contenedor');
});

