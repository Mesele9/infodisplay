var socket = new WebSocket('ws://localhost:8000/ws/display/');

    socket.onopen = function(event) {
        console.log("WebSocket connection opened:", event);
    };

    socket.onmessage = function(event) {

        var dataArray = JSON.parse(event.data);
        console.log('WebSocket message received', dataArray);

        // Loop through the array of data
        dataArray.forEach(function(data) {
            // Check the source property to determine the data type
            switch (data.source) {
                case 'time':    
                    var timeElement = document.getElementById('time-' + data.city);
                    if (timeElement) {
                        timeElement.innerText = data.current_time;
                    }
                    break;

                case 'weather':    
                    var temperatureElement = document.getElementById('temperature-' + data.city);
                    var descriptionElement = document.getElementById('description-' + data.city);

                    if (temperatureElement && descriptionElement) {
                        temperatureElement.innerText = data.temperature + '° C';
                        descriptionElement.innerText = data.description;
                    }
                    break;

                case 'exchange':
                    // Handle exchange rate data
                    // Update exchange rate elements as needed
                    break;

                default:
                    // Handle other data types, if any
                    break;
            }
        });
    };

    socket.onclose = function(event) {
        console.log("WebSocket connection closed:", event);
    };