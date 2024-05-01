def calculate_feels_like(temperature, humidity, wind_speed):
    if temperature >= 27:
        feels_like = (-8.784694 + 1.61139411 * temperature + 2.33854900 * humidity
                      - 0.14611605 * temperature * humidity - 0.012308094 * temperature ** 2
                      - 0.016424827 * humidity ** 2 + 0.0022117323 * temperature ** 2 * humidity
                      + 0.00072546 * temperature * humidity ** 2 - 0.000003582 * temperature ** 3)
    elif temperature <= 10 and wind_speed > 4.8:
        feels_like = (13.12 + 0.6215 * temperature - 11.37 * wind_speed ** 0.16
                      + 0.3965 * temperature * wind_speed ** 0.16)
    else:
        feels_like = temperature

    return round(feels_like, 2)  # Round to two decimal places
