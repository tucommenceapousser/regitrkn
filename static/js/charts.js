function initializeCharts(measurements) {
    const dates = measurements.map(m => new Date(m.date).toLocaleDateString());
    const weights = measurements.map(m => m.weight);

    const ctx = document.getElementById('weightChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dates.reverse(),
            datasets: [{
                label: 'Weight (kg)',
                data: weights.reverse(),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return value + ' kg';
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Weight: ${context.parsed.y} kg`;
                        }
                    }
                }
            }
        }
    });
}
