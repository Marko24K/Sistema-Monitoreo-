document.addEventListener("DOMContentLoaded", () => {
    let temperatureChart, humidityChart;
    const latestTemperatureElement = document.getElementById('latest-temperature');
    const latestHumidityElement = document.getElementById('latest-humidity');

    const tempRecentTableBody = document.querySelector('#temp-recent-table tbody');
    const humRecentTableBody = document.querySelector('#hum-recent-table tbody');

    initializeCharts();
    fetchData();
    setInterval(fetchData, 10000);  // Actualiza cada 10 segundos

    function initializeCharts() {
        const tempCtx = document.getElementById('temperatureChart').getContext('2d');
        const humidityCtx = document.getElementById('humidityChart').getContext('2d');

        temperatureChart = new Chart(tempCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Temperatura (°C)',
                    data: [],
                    borderColor: '#d9534f', 
                    backgroundColor: 'rgba(217, 83, 79, 0.2)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            tooltipFormat: 'DD/MM/YYYY HH:mm',
                            displayFormats: { hour: 'DD/MM HH:mm' }
                        },
                        title: { display: true, text: 'Fecha' }
                    },
                    y: {
                        beginAtZero: false,
                        title: { display: true, text: 'Temperatura (°C)' }
                    }
                }
            }
        });

        humidityChart = new Chart(humidityCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Humedad (%)',
                    data: [],
                    borderColor: '#003366', 
                    backgroundColor: 'rgba(0, 51, 102, 0.2)',
                    fill: true,
                    tension: 0.3
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'hour',
                            tooltipFormat: 'DD/MM/YYYY HH:mm',
                            displayFormats: { hour: 'DD/MM HH:mm' }
                        },
                        title: { display: true, text: 'Fecha' }
                    },
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Humedad (Hr)' }
                    }
                }
            }
        });
    }

    function fetchData() {
        const url = '/datos_recientes/'; // Aquí se hace la solicitud a la nueva vista
        
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la solicitud');
                }
                return response.json();
            })
            .then(data => {
                console.log("Datos recibidos:", data);  // Muestra los datos completos para depuración
                processData(data);
            })
            .catch(error => {
                console.error('Error al obtener los datos:', error);  // Muestra cualquier error
            });
    }

    function processData(data) {
        const temperatureData = data.temp_recent;  
        const humidityData = data.hum_recent;  

        updateLatestValues(data.latest_temperature, data.latest_humidity);
        updateStatistics(temperatureData, humidityData);
        updateCharts(temperatureData, humidityData);
        updateRecentTables(temperatureData, humidityData);
    }

    function updateLatestValues(tempData, humData) {
        const latestTemperature = tempData.length
            ? `${parseFloat(tempData[0].valor).toFixed(2)} °C`
            : '-- °C';
    
        latestTemperatureElement.textContent = latestTemperature;
        localStorage.setItem('latestTemperature', latestTemperature);
        
        const latestHumidity = humData.length
            ? `${parseFloat(humData[0].valor).toFixed(2)} Hr`
            : '-- Hr';
        latestHumidityElement.textContent = latestHumidity;
        localStorage.setItem('latestHumidity', latestHumidity);
    }

    function updateStatistics(tempData, humData) {
        const calculateStats = (data) => {
            if (!data.length) return { max: '--', maxDate: '--', min: '--', minDate: '--', avg: '--' };
            const values = data.map(item => parseFloat(item.valor));
            const maxIndex = values.indexOf(Math.max(...values));
            const minIndex = values.indexOf(Math.min(...values));
            const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);
            return {
                max: values[maxIndex].toFixed(2),
                maxDate: moment(data[maxIndex].fecha_registro).format('DD/MM/YYYY [a las] HH:mm'),
                min: values[minIndex].toFixed(2),
                minDate: moment(data[minIndex].fecha_registro).format('DD/MM/YYYY [a las] HH:mm'),
                avg: avg
            };
        };
    
        const tempStats = calculateStats(tempData);
        const humStats = calculateStats(humData);
    
        // Actualiza estadísticas de temperatura
        document.getElementById('temp-max').innerHTML = `${tempStats.max} °C`;
        document.getElementById('temp-max-date').innerHTML =`${tempStats.maxDate}`;
        document.getElementById('temp-min').innerHTML = `${tempStats.min} °C`;
        document.getElementById('temp-min-date').innerHTML =`${tempStats.minDate}`;
        document.getElementById('temp-avg').textContent = `${tempStats.avg} °C`;
    
        // Actualiza estadísticas de humedad
        document.getElementById('hum-max').innerHTML = `${humStats.max}Hr`;
        document.getElementById('hum-max-date').innerHTML = `${humStats.maxDate}`;
        document.getElementById('hum-min').innerHTML = `${humStats.min}Hr`;
        document.getElementById('hum-min-date').innerHTML = `${humStats.minDate}`;
        document.getElementById('hum-avg').textContent = `${humStats.avg} Hr`;
    }    

    function updateCharts(tempData, humData) {
        tempData.sort((a, b) => new Date(a.fecha_registro) - new Date(b.fecha_registro));
        humData.sort((a, b) => new Date(a.fecha_registro) - new Date(b.fecha_registro));

        temperatureChart.data.labels = tempData.map(row => moment(row.fecha_registro).format('YYYY-MM-DD HH:mm:ss'));
        temperatureChart.data.datasets[0].data = tempData.map(row => parseFloat(row.valor));
        temperatureChart.update();

        humidityChart.data.labels = humData.map(row => moment(row.fecha_registro).format('YYYY-MM-DD HH:mm:ss'));
        humidityChart.data.datasets[0].data = humData.map(row => parseFloat(row.valor));
        humidityChart.update();
    }

    function updateRecentTables(tempData, humData) {
        const recentTemp = tempData.slice(-10).reverse();
        tempRecentTableBody.innerHTML = recentTemp.length
            ? recentTemp.map(item => `
                <tr>
                    <td>${parseFloat(item.valor).toFixed(2)} °C</td>
                    <td>${moment(item.fecha_registro).format('DD/MM/YYYY HH:mm')}</td>
                    <td>${item.id_sensor.id_modelo_sensor.nombre_sensor || 'Desconocido'}</td>
                    <td>${item.id_sensor.id_sensor}</td>
                </tr>
            `).join('')
            : '<tr><td colspan="4">No hay datos disponibles.</td></tr>';

        const recentHum = humData.slice(-10).reverse();
        humRecentTableBody.innerHTML = recentHum.length
            ? recentHum.map(item => `
                <tr>
                    <td>${parseFloat(item.valor).toFixed(2)} Hr</td>
                    <td>${moment(item.fecha_registro).format('DD/MM/YYYY HH:mm')}</td>
                    <td>${item.id_sensor.id_modelo_sensor.nombre_sensor || 'Desconocido'}</td>
                    <td>${item.id_sensor.id_sensor}</td>
                </tr>
            `).join('')
            : '<tr><td colspan="4">No hay datos disponibles.</td></tr>';
    }
});
