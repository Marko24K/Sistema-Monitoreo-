document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#dataTable tbody"); // Selecciona el cuerpo de la tabla

    // Realiza una solicitud al endpoint '/get_data/' para obtener los datos
    fetch("/get_data/")
        .then(response => response.json()) // Convierte la respuesta JSON a un objeto JavaScript
        .then(data => {
            // Itera sobre los datos recibidos y genera filas en la tabla
            data.forEach(item => {
                const row = document.createElement("tr"); // Crea una nueva fila
                row.innerHTML = `
                    <th>${item.id_divicion_Parcela}</th> <!-- agregar para el ID divicion parcela -->
                    <th>${item.id_parcela}</th> <!-- agregar para el ID parcela -->
                    <th>${item.tipo_division}</th> <!-- agregar para el tipo division -->
                    <th>${item.Identificador}</th> <!-- agregar para la Identificacion -->
                    <th>${item.codigoQR}</th> <!-- agregar para el QR -->
                `;
                tableBody.appendChild(row); // Agrega la fila al cuerpo de la tabla
            });
        })
        .catch(error => console.error("Error fetching data:", error)); // Muestra un error si falla la solicitud
});
