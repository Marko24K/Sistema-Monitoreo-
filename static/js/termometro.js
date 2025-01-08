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
function ajustarTermometro(temperatura) {
  let tempValue = parseFloat(temperatura);
  const nivel = document.getElementById('nivel');
  const valor = document.getElementById('valor');

  // Verificar si el valor es numérico
  if (isNaN(tempValue)) {
    tempValue = 20; // Valor por defecto si no es un número válido
  }

  // Limitar la temperatura entre -25 y 50 grados
  let altura = Math.min(Math.max(tempValue, -25), 50);
  
  // Mapear la temperatura al rango del termómetro (0% a 100%)
  let alturaPorcentaje = ((altura + 25) / 75) * 100;
  alturaPorcentaje = Math.min(Math.max(alturaPorcentaje, 0), 100); // Asegurarse de que esté entre 0% y 100%

  // Actualizar la altura del nivel en el termómetro
  nivel.style.height = `${alturaPorcentaje}%`;

  // Cambiar el color del nivel basado en la temperatura
  if (tempValue < 15) {
      nivel.style.backgroundColor = 'blue'; // Frío
  } else if (tempValue >= 15 && tempValue <= 30) {
      nivel.style.backgroundColor = 'yellow'; // Moderado
  } else {
      nivel.style.backgroundColor = 'red'; // Caluroso
  }

  // Actualizar el valor de la temperatura en el texto
  valor.textContent = `Temperatura: ${tempValue}°C`;
}

// Función para obtener la temperatura de un servidor (AJAX)
function obtenerTemperatura() {
  fetch('/obtener_temperatura/')  // Cambia esta URL a tu endpoint real
      .then(response => response.json())
      .then(data => {
          console.log('Datos recibidos:', data);  // Depuración: Verifica qué datos se están recibiendo
          if (data.temperatura != undefined) {
              ajustarTermometro(data.temperatura);
          } else {
              console.error('Temperatura no disponible');
          }
      })
      .catch(error => {
          console.error('Error al obtener la temperatura:', error);
      });
}

// Llamada inicial al cargar la página
window.onload = function() {
  obtenerTemperatura();  // Llamada inicial para cargar el valor
  setInterval(obtenerTemperatura, 5000);  // Actualización cada 5 segundos
};


