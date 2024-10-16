document.addEventListener('DOMContentLoaded', function() {
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Bar chart for steps and calories burned
        const ctx = document.getElementById('salesChart').getContext('2d');
        const salesChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'], 
                datasets: [
                    {
                        label: 'Steps',
                        data: data.Steps, // Update to match new data
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Calories Burned',
                        data: data['calories burned'], // Update to match new data
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        // Pie chart for water intake
        const pieCtx = document.getElementById('pieChart').getContext('2d');
        const pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: data.WaterInTake.values, // Use values from WaterInTake
                    backgroundColor: ['#36A2EB', '#f0f0f0'], // Adjust as needed
                    hoverBackgroundColor: ['#FF6384', '#36A2EB']
                }]
            }
        });

        // Second pie chart (example)
        const ctx2 = document.getElementById('pieChart2').getContext('2d'); // Change to new ID
        const pieChart2 = new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: ['Label1', 'Label2', 'Label3'], // Update labels as necessary
                datasets: [{
                    data: [10, 20, 30], // Update data as necessary
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                },
            }
        });
    });
});

function updateIntake(amount) {
    // Logic to update the user's water intake
    console.log(`Added ${amount} ml of water.`);
    // You can also update the displayed water intake and chart data here
}
