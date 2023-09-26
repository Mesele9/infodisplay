![Front Desk Info app index page](https://github.com/Mesele9/infodisplay/blob/master/Web%20capture_26-9-2023_154644_192.168.1.200.jpeg?raw=true)

<p align="center">
  <img src="https://github.com/Mesele9/infodisplay/blob/master/Web%20capture_26-9-2023_154644_192.168.1.200.jpeg?raw=true" alt="Front Desk Info app index page" width="400">
</p>


# Front Desk Information App

InfoDisplay is a Django-based web application that provides real-time information about different cities. It fetches and displays data such as current time, weather, and daily exchange rates for a list of predefined cities.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)

## Features

- Real-time display of current time, weather, and exchange rates for multiple cities.
- Asynchronous data fetching using Celery to avoid blocking the main application.
- WebSocket integration for real-time updates.
- Data caching for improved performance.
- Django admin interface for managing cities and data models.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher installed.
- Django 4.2.5 installed.
- Redis server running (for Celery task queue and caching).

## Installation

    1. Clone the repository:

       git clone https://github.com/yourusername/infodisplay.git
       cd infodisplay

    2. Create and activate a virtual environment:

        python -m venv venv
        source venv/bin/activate

    3. Install the required Python packages:

        pip install -r requirements.txt

    4. Run migrations to set up the database:

        python manage.py migrate

    5. Create a superuser account (for Django admin access):

        python manage.py createsuperuser    

    6. Start the Django development server:

        python manage.py runserver

    7. Start Celery worker and Celey beat in two different terminals:

        Terminal 1:
            celery -A infodisplay beat -l INFO
    
        Terminal 2:
            celery -A infodisplay worker -l INFO

    8. Access the application at http://localhost:8000/ 

## Usage

- Log in to the Django admin interface at http://localhost:8000/admin/ to manage cities and data models.

- Visit the main application at http://localhost:8000/ to view real-time information for the predefined cities.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any inquiries or further information, please feel free to reach me:
- **Email** [Mesele Assefa] at (getmesy@gmail.com)
- **GitHub** [Mesele Assefa](https://github.com/Mesele9)
- **LinkedIn**: [Mesele Assefa](https://www.linkedin.com/in/mesele-assefa/)