$(document).ready(function() {
    let indice = 0; // índice de la sección inicial

    function actualizarCarrusel() {
        // Hacemos un desplazamiento del contenedor hacia la posición adecuada
        $(".contenedor").css("transform", "translateX(-" + (indice * 50) + "%)");
    }

    $("#siguiente").click(function() {
        if (indice < 3) { // solo hay 6 secciones, por lo que el índice máximo es 3
            indice++;
            actualizarCarrusel();
        }
    });

    $("#anterior").click(function() {
        if (indice > 0) {
            indice--;
            actualizarCarrusel();
        }
    });

});
