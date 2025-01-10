function obtenerUltimaTemperatura() {
  // Intentamos obtener la temperatura más reciente desde localStorage
  const ultimaTemperatura = localStorage.getItem('latestTemperature');
  
  // Verificar si se ha encontrado un valor en localStorage
  console.log("Última temperatura obtenida desde localStorage:", ultimaTemperatura);
  
  // Si existe en localStorage, devolverla, de lo contrario, retornar un valor predeterminado
  if (ultimaTemperatura) {
    return parseInt(ultimaTemperatura);
  } else {
    return 0;  // Si no se encuentra ninguna temperatura almacenada, usar 0°C por defecto
  }
}

// Función para ajustar el termómetro usando la última temperatura registrada
function ajustarTermometro() { 
  // Obtener la última temperatura registrada desde localStorage
  let temperatura = obtenerUltimaTemperatura();

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
  valor.textContent = `${temperatura}°C`;

  // Guardar la temperatura actual en localStorage
  localStorage.setItem('latestTemperature', temperatura);
  console.log("Temperatura guardada en localStorage:", temperatura);
}

// Llamamos a la función para actualizar el termómetro cada 10 segundos
setInterval(function() {ajustarTermometro();}, 1);  // 10000 ms = 10 segundos

// Ajustar el termómetro al cargar la página con la última temperatura almacenada
window.addEventListener('load', function() {ajustarTermometro();});
