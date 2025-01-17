// Función para obtener un valor almacenado en localStorage o un predeterminado
function obtenerValor(key, defaultValue) {
  const valor = localStorage.getItem(key);
  const numero = parseInt(valor, 10);
  return isNaN(numero) ? defaultValue : numero;
}

// Función para actualizar un indicador (genérico para temperatura/humedad)
function ajustarIndicador(tipo, valorActual, config) {
  const { idNivel, idValor, limites, colores } = config;
  const nivel = document.getElementById(idNivel);
  const valor = document.getElementById(idValor);

  // Limita el valor al rango definido
  const valorLimitado = Math.min(Math.max(valorActual, limites.min), limites.max);

  // Mapea el valor a un porcentaje
  const porcentaje = ((valorLimitado - limites.min) / (limites.max - limites.min)) * 100;

  // Ajusta la altura del indicador
  nivel.style.height = `${porcentaje}%`;

  // Determina el color del indicador basado en el valor
  if (valorLimitado < colores.umbralBajo) {
    nivel.style.backgroundColor = colores.bajo;
  } else if (valorLimitado <= colores.umbralAlto) {
    nivel.style.backgroundColor = colores.moderado;
  } else {
    nivel.style.backgroundColor = colores.alto;
  }

  // Actualiza el texto mostrado
  valor.textContent = `${valorActual}${tipo === 'temperatura' ? '°C' : '%'}`;

  // Guarda el valor actualizado en localStorage
  localStorage.setItem(`latest${tipo.charAt(0).toUpperCase() + tipo.slice(1)}`, valorActual);

  console.log(`${tipo.charAt(0).toUpperCase() + tipo.slice(1)} guardado en localStorage:`, valorActual);
}

// Función para ajustar el termómetro
function ajustarTermometro() {
  const temperatura = obtenerValor('latestTemperature', 0);
  ajustarIndicador('temperatura', temperatura, {
    idNivel: 'nivel',
    idValor: 'valor',
    limites: { min: -25, max: 50 },
    colores: { bajo: 'blue', moderado: 'green', alto: 'red', umbralBajo: 15, umbralAlto: 26 },
  });
}

// Función para ajustar el indicador de humedad
function ajustarIndicadorHumedad() {
  const humedad = obtenerValor('latestHumidity', 50);
  ajustarIndicador('humedad', humedad, {
    idNivel: 'nivelHumedad',
    idValor: 'valorHumedad',
    limites: { min: 0, max: 100 },
    colores: { bajo: 'yellow', moderado: 'blue', alto: 'purple', umbralBajo: 30, umbralAlto: 60 },
  });
}

// Configurar actualizaciones automáticas cada 1 segundos
setInterval(ajustarTermometro, 1000);
setInterval(ajustarIndicadorHumedad, 1000);

// Ajustar indicadores al cargar la página
window.addEventListener('load', ajustarTermometro);
window.addEventListener('load', ajustarIndicadorHumedad);
