$(document).ready(function() {
    let indice = 0; // índice de la sección inicial

    // Función para actualizar el carrusel según el tamaño de la pantalla
    function actualizarCarrusel() {
        const anchoPantalla = $(window).width();
        let seccionesVisibles = (anchoPantalla <= 425) ? 1 : 2; // 1 sección en móviles pequeños, 2 en pantallas mayores a 425px

        // Hacemos un desplazamiento del contenedor hacia la posición adecuada
        $(".contenedor").css("transform", "translateX(-" + (indice * (100 / seccionesVisibles)) + "%)");
    }

    // Al hacer clic en "Siguiente"
    $("#siguiente").click(function() {
        const anchoPantalla = $(window).width();
        let seccionesVisibles = (anchoPantalla <= 425) ? 1 : 2; // Determinar el número de secciones visibles

        // Calculamos cuántas veces podemos movernos según las secciones visibles
        if ((anchoPantalla <= 425 && indice < 5) || (anchoPantalla > 425 && indice < 3)) {
            indice++;
            actualizarCarrusel();
        }
    });

    // Al hacer clic en "Anterior"
    $("#anterior").click(function() {
        if (indice > 0) {
            indice--;
            actualizarCarrusel();
        }
    });

    // Inicializar el carrusel al cargar la página
    actualizarCarrusel();
    
    // Si el tamaño de la pantalla cambia, actualizar la visualización
    $(window).resize(function() {
        actualizarCarrusel();
    });
});