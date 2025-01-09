/*
function ajustarTermometro(temperatura) {
  // Si la temperatura no se pasa como argumento, se obtiene del input como valor predeterminado
  if (isNaN(temperatura)) {
    temperatura = parseInt(document.getElementById('temperatura').value);
  }

  const nivel = document.getElementById('nivel');
  const valor = document.getElementById('valor');

  // Limita la temperatura entre -25 y 50
  let altura = Math.min(Math.max(temperatura, -25), 50);

  // Mapea la temperatura entre -25 y 50 a un porcentaje entre 0% y 100%
  let alturaPorcentaje = ((altura + 25) / 75) * 100;
  alturaPorcentaje = Math.min(Math.max(alturaPorcentaje, 0), 100); // Asegura que esté entre 0% y 100%

  // Ajusta la altura del nivel del termómetro
  nivel.style.height = `${alturaPorcentaje}%`;

  // Ajustar color según la temperatura
  if (temperatura < 15) {
    nivel.style.backgroundColor = 'blue'; // Frío
  } else if (temperatura >= 15 && temperatura <= 30) {
    nivel.style.backgroundColor = 'yellow'; // Moderado
  } else {
    nivel.style.backgroundColor = 'red'; // Caluroso
  }

  // Actualizar el valor mostrado de la temperatura
  valor.textContent = `Temperatura: ${temperatura}°C`;
}
*/
let temperaturaActual = null; // Variable global para almacenar la temperatura actual

function ajustarTermometro(temperatura) {
  // Si la temperatura no se pasa como argumento, se obtiene del input como valor predeterminado
  if (isNaN(temperatura)) {
    temperatura = parseInt(document.getElementById('temperatura').value);
  }

  // Comprobamos si la temperatura ha cambiado
  if (temperatura !== temperaturaActual) {
    temperaturaActual = temperatura; // Actualizamos la temperatura actual

    const nivel = document.getElementById('nivel');
    const valor = document.getElementById('valor');

    // Limita la temperatura entre -25 y 50
    let altura = Math.min(Math.max(temperatura, -25), 50);

    // Mapea la temperatura entre -25 y 50 a un porcentaje entre 0% y 100%
    let alturaPorcentaje = ((altura + 25) / 75) * 100;
    alturaPorcentaje = Math.min(Math.max(alturaPorcentaje, 0), 100); // Asegura que esté entre 0% y 100%

    // Ajusta la altura del nivel del termómetro
    nivel.style.height = `${alturaPorcentaje}%`;

    // Ajustar color según la temperatura
    if (temperatura < 15) {
      nivel.style.backgroundColor = 'blue'; // Frío
    } else if (temperatura >= 15 && temperatura <= 30) {
      nivel.style.backgroundColor = 'yellow'; // Moderado
    } else {
      nivel.style.backgroundColor = 'red'; // Caluroso
    }

    // Actualizar el valor mostrado de la temperatura
    valor.textContent = `Temperatura: ${temperatura}°C`;
  }
}

