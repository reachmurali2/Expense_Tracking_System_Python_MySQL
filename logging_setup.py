import logging                                                       # Imports Python’s logging module, which allows capturing logs for debugging and monitoring.

def setup_logger(name, log_file='server.log', level=logging.DEBUG):   # Defines a function to set up a logger.
                                                                      # - name: Logger name to differentiate logs. - log_file: Filename to store logs (default: 'server.log').
    # Create a custom logger                                          # - level: Logging level (default: DEBUG).
    logger = logging.getLogger(name)                                  # Creates a custom logger with the specified name. - If a logger with the same name exists, it reuses it.

    # Configure the custom logger
    logger.setLevel(level)                                            # Sets the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    file_handler = logging.FileHandler(log_file)                      # Creates a file handler to write logs into the specified file.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(message)s')  # Defines the log format: - %(asctime)s: Timestamp of the log event.     - %(name)s: Logger name.      - %(levelname)s: Log level (DEBUG, INFO, etc.).       - %(message)s: Log message.
    file_handler.setFormatter(formatter)                              # Applies the log format to the file handler.
    logger.addHandler(file_handler)                                   # Attaches the file handler to the logger so logs are written to the file.
    return logger                                                     # Returns the configured logger, allowing other files to use it.