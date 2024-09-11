import logging
import time
import psutil  # For memory usage logging

def setup_logging(level=logging.INFO, log_file=None):
    """
    Setup logging configuration for the library. 
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if log_file:
        logging.basicConfig(level=level, format=log_format, filename=log_file, filemode='a')
    else:
        logging.basicConfig(level=level, format=log_format)

    logger = logging.getLogger(__name__)
    logger.info("Logging setup complete.")

def set_logging_level(level):
    """
    Set the logging level dynamically during runtime.
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    logger.info(f"Logging level set to {logging.getLevelName(level)}")

def log_to_file(log_file):
    """
    Add a file handler to log messages to a specified file.
    """
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    
    logger.info(f"Started logging to file: {log_file}")

def disable_logging():
    """
    Disable logging completely.
    """
    logging.disable(logging.CRITICAL)

def log_custom_message(level, message):
    """
    Log a custom message at the specified log level.
    
    Parameters:
    level : int
        The logging level (e.g., logging.INFO, logging.WARNING, logging.ERROR).
    message : str
        The custom message to log.
    
    Returns:
    None
    """
    logger = logging.getLogger()
    logger.log(level, message)

def log_timed_event(start_time, event_name="Event"):
    """
    Log the time taken for a specific event or function to complete.
    
    Parameters:
    start_time : float
        The start time of the event (from time.time()).
    event_name : str, optional
        Name of the event or function being timed.
    
    Returns:
    None
    """
    end_time = time.time()
    elapsed_time = end_time - start_time
    logger = logging.getLogger()
    logger.info(f"{event_name} completed in {elapsed_time:.2f} seconds")

def log_memory_usage():
    """
    Log the current memory usage of the system.
    
    Returns:
    None
    """
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 ** 2  # Convert to MB
    logger = logging.getLogger()
    logger.info(f"Current memory usage: {memory_usage:.2f} MB")

def log_dataframe_shape(df, message="DataFrame shape logged"):
    """
    Log the shape of a DataFrame at a given point in processing.
    
    Parameters:
    df : pd.DataFrame
        The DataFrame whose shape is to be logged.
    message : str, optional
        A custom message to accompany the DataFrame shape log.
    
    Returns:
    None
    """
    logger = logging.getLogger()
    logger.info(f"{message}: {df.shape}")
    
def enable_console_logging():
    """
    Enable logging output to the console.
    """
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)
    logger.info("Console logging enabled.")

def disable_console_logging():
    """
    Disable logging output to the console.
    """
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.StreamHandler):
            logger.removeHandler(handler)
    logger.info("Console logging disabled.")
