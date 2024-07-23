function CelsiusToFahrenheit(celsius) {
    return celsius * 1.8 + 32;
}

function FahrenheitToCelsius(fahrenheit) {
    return (fahrenheit - 32) / 1.8;
}

function toggleUnits() {
    const currentUnits = document.getElementById('currentUnits');
    const feelsLikeElement = document.querySelector('.feels-like h2');

    if (!currentUnits || !feelsLikeElement) {
        console.error('Error: Elements not found or null values detected.');
        return;
    }

    currentUnits.innerText = currentUnits.innerText.includes('Metric') ? 'Current Units: Imperial' : 'Current Units: Metric';
    localStorage.setItem('selectedUnits', currentUnits.innerText.includes('Metric') ? 'metric' : 'imperial');

    const feelsValue = parseInt(feelsLikeElement.textContent); // Parse the feels like value

    if (!isNaN(feelsValue)) {
        if (currentUnits.innerText === 'Current Units: Metric') {
            // Switch to Imperial Units
            const fahrenheit = CelsiusToFahrenheit(feelsValue);
            feelsLikeElement.textContent = Math.round(fahrenheit) + " °F";
        } else {
            // Switch back to Metric Units
            const celsius = FahrenheitToCelsius(feelsValue);
            feelsLikeElement.textContent = Math.round(celsius) + " °C";
        }
    } else {
        console.error('Error: Invalid temperature value detected.');
    }
}
