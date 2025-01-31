/*
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
*/
$(document).ready(function() {
    // Función para inicializar gráficos dinámicamente
    $("canvas[id^='chart-']").each(function() {
        let ctx = this.getContext('2d');
        let labels = JSON.parse(this.getAttribute('data-labels'));
        let values = JSON.parse(this.getAttribute('data-values'));

        new Chart(ctx, {
            type: 'line', // Tipo de gráfico (puede ser 'line', 'bar', 'pie', etc.)
            data: {
                labels: labels,
                datasets: [{
                    label: 'Valor',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });

    // Código del carrusel (sin cambios)
    let indice = 0; // Índice de la sección inicial
    function actualizarCarrusel() {
        const anchoPantalla = $(window).width();
        let seccionesVisibles = (anchoPantalla <= 425) ? 1 : 2;
        $(".contenedor").css("transform", "translateX(-" + (indice * (100 / seccionesVisibles)) + "%)");
    }
    $("#siguiente").click(function() {
        const anchoPantalla = $(window).width();
        let seccionesVisibles = (anchoPantalla <= 425) ? 1 : 2;
        if ((anchoPantalla <= 425 && indice < 5) || (anchoPantalla > 425 && indice < 3)) {
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
    actualizarCarrusel();
    $(window).resize(actualizarCarrusel);
});
