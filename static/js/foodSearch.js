document.getElementById('searchButton').addEventListener('click', function() {
    const foodName = document.getElementById('foodSearch').value;
    const apiKey = 'MA5SryEx9s1s84qOXC1yuc2nzQQTgEGw2YHAaKP5'; // Replace with your USDA FoodData Central API key
    const url = `https://api.nal.usda.gov/fdc/v1/foods/search?query=${encodeURIComponent(foodName)}&api_key=${apiKey}`;

    // Fetch data from the USDA FoodData Central API
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.foods && data.foods.length > 0) {
                displayResults(data.foods);
            } else {
                document.getElementById('searchResults').innerHTML = '<p>No results found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            document.getElementById('searchResults').innerHTML = '<p>There was an error fetching the data.</p>';
        });
});

function displayResults(foods) {
    const resultsDiv = document.getElementById('searchResults');
    resultsDiv.innerHTML = ''; // Clear previous results

    foods.forEach(food => {
        const foodItem = document.createElement('div');
        foodItem.className = 'result-item';
        foodItem.innerHTML = `
            <h4>${food.description}</h4>
            <p>Calories: ${getCalories(food)}</p>
        `;
        resultsDiv.appendChild(foodItem);
    });
}

function getCalories(food) {
    // Get the 'Energy' nutrient which represents calories
    const energyNutrient = food.foodNutrients.find(nutrient => nutrient.nutrientName === 'Energy' || nutrient.nutrientName === 'Calories');
    return energyNutrient ? `${energyNutrient.value} ${energyNutrient.unitName}` : 'N/A'; // Display calories and unit, or 'N/A' if not available
}