document.addEventListener('DOMContentLoaded', function() {
    fetch('/data')
    .then(response => response.json())
    .then(data => {
        // Bar chart for steps and calories burned
        const ctx = document.getElementById('WorkoutChart').getContext('2d');
        const WorkoutChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday'], 
                datasets: [
                    {
                        label: 'Workouts',
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

        // Pie chart for waterChart intake
        const pieCtx = document.getElementById('waterChart').getContext('2d');
        const pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: data.WaterInTake.values,
                    borderRadius: [30, 20],
                    backgroundColor: ['#246CD0', '#302F2F'], 
                    borderWidth: 0
                }]
            }
        });

        // Pie chart for CaloriesChart intake
        const pieCtx2 = document.getElementById('CaloriesChart').getContext('2d');
        const pieChart2 = new Chart(pieCtx2, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: data.WaterInTake.values,
                    borderRadius: [30, 20],
                    backgroundColor: ['#E8471C', '#302F2F'],
                    borderWidth: 0
                }]
            }
        });

        // Pie chart for CarbsChart intake
        const pieCtx3 = document.getElementById('CarbsChart').getContext('2d');
        const pieChart3 = new Chart(pieCtx3, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: data.WaterInTake.values,
                    borderRadius: [30, 20],
                    backgroundColor: ['#FF8500', '#302F2F'], 
                    borderWidth: 0
                }]
            }
        });

        // Pie chart for ProtienChart intake
        const pieCtx4 = document.getElementById('ProtienChart').getContext('2d');
        const pieChart4 = new Chart(pieCtx4, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: data.WaterInTake.values,
                    borderRadius: [30, 20],
                    backgroundColor: ['#13103B', '#302F2F'], 
                    borderWidth: 0
                }]
            }
        });
       
    });
});

function updateWaterIntake(amount) {
    fetch('/update_water', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(response => response.json())
    .then(data => {
        // Update the UI to reflect the new water intake
        alert('Water intake updated!');
        location.reload();  // Reload to reflect the new intake
    })
    .catch(error => console.error('Error:', error));
}
