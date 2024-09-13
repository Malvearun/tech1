import os  # Imports the os module to work with environment variables
import logging  # Imports logging to handle logging within the application
from flask import Flask, request, render_template  # Imports necessary Flask components
from datadog import initialize, statsd  # Imports Datadog initialization and statsd for metrics

# Initialize the Flask application
app = Flask(__name__)  # Creates a Flask application instance

# Initialize Datadog with API key and App key from environment variables
options = {
    'api_key': os.getenv('DD_API_KEY'),  # Fetches the Datadog API key from environment variables
    'app_key': os.getenv('DD_APP_KEY')   # Fetches the Datadog App key from environment variables
}
initialize(**options)  # Initializes Datadog with the provided API and App keys

# Setup custom logging handler for Datadog
class DatadogHandler(logging.Handler):  # Defines a custom logging handler for Datadog
    def emit(self, record):  # Function to process log entries
        log_entry = self.format(record)  # Formats the log entry
        statsd.increment('flask_app.logs', tags=[f"level:{record.levelname.lower()}", f"message:{log_entry}"])  
        # Sends a log event to Datadog with log level and message as tags
        # Optional: Also write the log entry to a local file for debugging or tracking
        with open('/app/prime_number.log', 'a') as f:  # Opens a log file in append mode
            f.write(f"{log_entry}\n")  # Writes the formatted log entry to the file

# Set up the Datadog handler for logging
datadog_handler = DatadogHandler()  # Creates an instance of the custom DatadogHandler
datadog_handler.setLevel(logging.DEBUG)  # Sets the logging level to DEBUG (logs all levels)

# Define the log format (timestamp, logger name, log level, and message)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  
# Creates a formatter that specifies the log format
datadog_handler.setFormatter(formatter)  # Associates the formatter with the Datadog handler

# Add the Datadog logging handler to the Flask app's logger
app.logger.addHandler(datadog_handler)  # Adds the custom Datadog handler to the app's logger

# Function to check if a number is prime
def is_prime(n):  # Defines the function that checks if a number is prime
    """Return True if n is a prime number, otherwise False."""  # Docstring explaining the function
    if n <= 1:  # Numbers less than or equal to 1 are not prime
        return False  # Returns False for non-prime numbers
    if n == 2:  # Special case where 2 is the only even prime number
        return True  # Returns True for the prime number 2
    if n % 2 == 0:  # All other even numbers are not prime
        return False  # Returns False for non-prime even numbers
    max_divisor = int(n**0.5) + 1  # Calculate the square root of the number (max divisor)
    for d in range(3, max_divisor, 2):  # Only check odd divisors greater than 2
        if n % d == 0:  # If n is divisible by any number, it's not prime
            return False  # Returns False if a divisor is found
    return True  # Returns True if the number is prime

# Define the main route for the application
@app.route('/', methods=['GET', 'POST'])  # Sets up the route for the root URL with GET and POST methods
def index():  # Defines the index function for the root route
    result = None  # Initializes result to None (no result yet)
    app.logger.debug("Debug log: Entering the index route.")  # Logs a debug message when entering the route

    if request.method == 'POST':  # Checks if the request is a POST
        try:
            number = int(request.form['number'])  # Converts the form input (number) to an integer
            result = is_prime(number)  # Calls the is_prime function to check if the number is prime
            result_text = f"{number} is {'a prime' if result else 'not a prime'} number."
            # Constructs a result message indicating if the number is prime or not
            
            # Log the result with different log levels
            app.logger.info(result_text)  # Logs the result message at the INFO level
            app.logger.debug(f"Debug log: The number {number} was processed.")  # Logs detailed debug info
            app.logger.warning(f"Warning log: Processing of the number {number} completed.")  # Logs a warning
            
            # Send a custom metric to Datadog tracking the number of prime number requests
            statsd.increment('prime_number.requests', tags=['number:{}'.format(number)])  
            # Tracks the prime number request count in Datadog, with the number as a tag
            
            return render_template('index.html', result=result_text)  # Renders the result on the webpage
        except ValueError:  # Handles the case where input is not a valid number
            error_message = "Invalid input. Please enter a valid number."  # Sets an error message
            app.logger.error(error_message)  # Logs the error at the ERROR level
            return render_template('index.html', result=error_message)  # Displays the error message

    # Log an informational message when the index page is accessed via GET
    app.logger.info("Info log: GET request made to the index route.")  # Logs an INFO message when accessed via GET
    
    return render_template('index.html', result=result)  # Renders the index page without a result (GET request)

# Define a route for generating a critical log entry
@app.route('/critical', methods=['GET'])  # Defines a route to simulate a critical log event
def critical():  # Defines the function for the /critical route
    app.logger.critical("Critical log: This is a critical log entry.")  # Logs a critical message for testing
    return "Critical log entry created!"  # Returns a simple message to the user

# Start the Flask application on host 0.0.0.0 and port 8083
if __name__ == '__main__':  # Runs the app only if this script is executed directly
    app.run(host='0.0.0.0', port=8083, debug=True)  # Starts the Flask app on port 8083 with debug mode enabled
