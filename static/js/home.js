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
                        label: 'Steps',
                        data: [data.Steps.current], // Display steps current values
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Calories Burned',
                        data: [data.Calories.current], // Display calories current values
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
        const pieCtx = document.getElementById('waterChart').getContext('2d');
        const pieChart = new Chart(pieCtx, {
            type: 'pie',
            data: {
                datasets: [{
                    data: [data.WaterInTake.current, data.WaterInTake.goal - data.WaterInTake.current],
                    backgroundColor: ['#246CD0', '#302F2F'], 
                    borderRadius: [30, 20],
                    borderWidth: 0
                }]
            }
        });

        // Pie chart for calories intake
        const pieCtx2 = document.getElementById('CaloriesChart').getContext('2d');
        const pieChart2 = new Chart(pieCtx2, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [data.Calories.current, data.Calories.goal - data.Calories.current],
                    backgroundColor: ['#E8471C', '#302F2F'],
                    borderRadius: [30, 20],
                    borderWidth: 0
                }]
            }
        });

        // Pie chart for carbs intake
        const pieCtx3 = document.getElementById('CarbsChart').getContext('2d');
        const pieChart3 = new Chart(pieCtx3, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [data.Carbs.current, data.Carbs.goal - data.Carbs.current],
                    backgroundColor: ['#FF8500', '#302F2F'], 
                    borderRadius: [30, 20],
                    borderWidth: 0
                }]
            }
        });

        // Pie chart for protein intake
        const pieCtx4 = document.getElementById('ProtienChart').getContext('2d');
        const pieChart4 = new Chart(pieCtx4, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [data.Protein.current, data.Protein.goal - data.Protein.current],
                    backgroundColor: ['#13103B', '#302F2F'], 
                    borderRadius: [30, 20],
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
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ amount: amount }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Handle success, maybe update the UI with the new water intake amount
            alert('Water intake updated successfully!');
        } else {
            alert('Failed to update water intake.');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

