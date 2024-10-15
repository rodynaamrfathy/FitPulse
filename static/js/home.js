window.onload = function () {
    // Get chart data from the Flask view (injected via Jinja2 templating)
    const waterIntake = {{ chart_data['water_intake'] }};
    const totalWaterGoal = {{ chart_data['total_water_goal'] }};
    const remainingWater = totalWaterGoal - waterIntake;

    var chart = new CanvasJS.Chart("waterIntakeChart", {
        title: {
            text: "Water Intake Progress"
        },
        data: [{
            type: "doughnut",
            dataPoints: [
                { y: waterIntake, indexLabel: "Water Intake (ml)" },
                { y: remainingWater, indexLabel: "Remaining (ml)" }
            ]
        }]
    });
    
    chart.render();
};