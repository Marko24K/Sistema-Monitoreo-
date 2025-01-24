document.addEventListener('DOMContentLoaded', function () {
    const contenedorImagen = document.getElementById('imagen-contenedor');
    const imagenActual = contenedorImagen.querySelector('#imagen-actual'); // Obtenemos la imagen actual

    // Función para actualizar dinámicamente la imagen
    function actualizarImagen(src) {
        if (imagenActual) {
            imagenActual.src = src; // Actualizamos el `src` de la imagen existente
        } else {
            const img = document.createElement('img'); // Creamos una nueva imagen si no existe
            img.id = 'imagen-actual';
            img.src = src;
            img.classList.add('img-fluid');
            contenedorImagen.appendChild(img);
        }
    }

    // (Opcional) Llamar a actualizarImagen si necesitas cambiar dinámicamente la imagen
    // Ejemplo: actualizarImagen('/static/img/otra_imagen.png');
});
