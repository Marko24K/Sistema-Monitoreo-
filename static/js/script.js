document.addEventListener("DOMContentLoaded", () => {
    let temperatureChart, humidityChart;
    const latestTemperatureElement = document.getElementById('latest-temperature');
    const latestHumidityElement = document.getElementById('latest-humidity');

    const tempRecentTableBody = document.querySelector('#temp-recent-table tbody');
    const humRecentTableBody = document.querySelector('#hum-recent-table tbody');

    initializeCharts();
    fetchData();
    setInterval(fetchData, 10000); 

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
                        title: { display: true, text: 'Humedad (%)' }
                    }
                }
            }
        });
    }

    function fetchData() {
        const url = 'datos_recibidos.php';

        fetch(url)
            .then(response => response.json())
            .then(data => processData(data))
            .catch(error => console.error('Error al obtener los datos:', error));
    }

    function processData(data) {
        const temperatureData = data.filter(row => row.nombre_tipo_dato === 'Temperatura');
        const humidityData = data.filter(row => row.nombre_tipo_dato === 'Humedad');

        updateLatestValues(temperatureData, humidityData);
        updateStatistics(temperatureData, humidityData);
        updateCharts(temperatureData, humidityData);
        updateRecentTables(temperatureData, humidityData);
    }

    function updateLatestValues(tempData, humData) {
        latestTemperatureElement.textContent = tempData.length
            ? `${parseFloat(tempData[tempData.length - 1].valor).toFixed(2)} °C`
            : '-- °C';

        latestHumidityElement.textContent = humData.length
            ? `${parseFloat(humData[humData.length - 1].valor).toFixed(2)} %`
            : '-- %';
    }

    function updateStatistics(tempData, humData) {
        const calculateStats = (data, unit) => {
            if (!data.length) return { max: '--', min: '--', avg: '--' };
            const values = data.map(item => parseFloat(item.valor));
            const max = Math.max(...values).toFixed(2);
            const min = Math.min(...values).toFixed(2);
            const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(2);
            return { max, min, avg };
        };

        const tempStats = calculateStats(tempData, '°C');
        const humStats = calculateStats(humData, '%');

        document.getElementById('temp-max').textContent = tempStats.max !== '--' ? `${tempStats.max} °C` : '-- °C';
        document.getElementById('temp-min').textContent = tempStats.min !== '--' ? `${tempStats.min} °C` : '-- °C';
        document.getElementById('temp-avg').textContent = tempStats.avg !== '--' ? `${tempStats.avg} °C` : '-- °C';

        document.getElementById('hum-max').textContent = humStats.max !== '--' ? `${humStats.max} %` : '-- %';
        document.getElementById('hum-min').textContent = humStats.min !== '--' ? `${humStats.min} %` : '-- %';
        document.getElementById('hum-avg').textContent = humStats.avg !== '--' ? `${humStats.avg} %` : '-- %';
    }

    function updateCharts(tempData, humData) {
        tempData.sort((a, b) => new Date(a.fecha) - new Date(b.fecha));
        humData.sort((a, b) => new Date(a.fecha) - new Date(b.fecha));

        temperatureChart.data.labels = tempData.map(row => moment(row.fecha).toDate());
        temperatureChart.data.datasets[0].data = tempData.map(row => parseFloat(row.valor));
        temperatureChart.update();

        humidityChart.data.labels = humData.map(row => moment(row.fecha).toDate());
        humidityChart.data.datasets[0].data = humData.map(row => parseFloat(row.valor));
        humidityChart.update();
    }

    function updateRecentTables(tempData, humData) {
        const recentTemp = tempData.slice(-10).reverse();
        tempRecentTableBody.innerHTML = recentTemp.length
            ? recentTemp.map(item => `
                <tr>
                    <td>${parseFloat(item.valor).toFixed(2)} °C</td>
                    <td>${moment(item.fecha).format('DD/MM/YYYY HH:mm')}</td>
                    <td>${item.nombre_sensor}</td>
                </tr>
            `).join('')
            : '<tr><td colspan="3">No hay datos disponibles.</td></tr>';

        const recentHum = humData.slice(-10).reverse();
        humRecentTableBody.innerHTML = recentHum.length
            ? recentHum.map(item => `
                <tr>
                    <td>${parseFloat(item.valor).toFixed(2)} %</td>
                    <td>${moment(item.fecha).format('DD/MM/YYYY HH:mm')}</td>
                    <td>${item.nombre_sensor}</td>
                </tr>
            `).join('')
            : '<tr><td colspan="3">No hay datos disponibles.</td></tr>';
    }
});
