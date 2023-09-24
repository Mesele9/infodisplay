from .models import City

def merge_time_and_weather_data(time_data, weather_data):
    merged_data = []

    # Create a dictionary to map 'city' to its corresponding 'weather' data
    weather_data_map = {entry['city']: entry for entry in weather_data}

    for entry in time_data:
        city = entry['city']
        weather_entry = weather_data_map.get(city, {})
        merged_entry = {
            'city': city,
            'current_date': entry['current_date'],
            'current_time': entry['current_time'],
            'temperature': weather_entry.get('temperature', ''),
            'description': weather_entry.get('description', ''),
            'icon': weather_entry.get('icon', ''),
        }
        merged_data.append(merged_entry)

    return merged_data


def get_template_column_width():
    total_cities = City.objects.all().count()
    if total_cities > 0:
        return 12 // total_cities
    else:
        return 12