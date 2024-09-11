import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import builtins

class SlackLogger:
    def __init__(self, token, channel):
        self.token = token
        self.channel = channel
        self.client = WebClient(token=self.token)

    def send_message(self, text):
        """Sends a message to the specified Slack channel."""
        try:
            response = self.client.chat_postMessage(channel=self.channel, text=text)
            if not response.get("ok"):
                print(f"Failed to send message: {response}")
        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")

    class SlackLoggerHandler(logging.Handler):
        def __init__(self, slack_logger):
            super().__init__()
            self.slack_logger = slack_logger

        def emit(self, record):
            log_entry = self.format(record)
            self.slack_logger.send_message(log_entry)

    @staticmethod
    def redirect_print_to_logger(logger):
        """Redirects print statements to the specified logger."""
        def print_to_logger(*args, **kwargs):
            message = " ".join(str(arg) for arg in args)
            logger.info(message)
        builtins.print = print_to_logger

    @classmethod
    def create_logger(cls, slack_token='xoxb-7424459969442-7456034210037-EMCjbI9oi1xTszU1iUh4tLFH', slack_channel='C07DYFK5SE8', redirect_print=True):
        """Creates a logger that sends log messages to a Slack channel.

        Args:
            slack_token (str): The Slack API token for authentication.
            slack_channel (str): The Slack channel ID to send messages to.
            redirect_print (bool): Whether to redirect print statements to the logger.

        Returns:
            logging.Logger: Configured logger instance with Slack handler.
        """
        # Initialize SlackLogger and SlackLoggerHandler
        slack_logger = cls(slack_token, slack_channel)
        slack_handler = cls.SlackLoggerHandler(slack_logger)

        # Create a logger and attach the custom Slack handler
        logger = logging.getLogger('SlackLogger')
        logger.setLevel(logging.INFO)  # Set the logging level
        logger.addHandler(slack_handler)

        # Set a basic format for the log messages
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        slack_handler.setFormatter(formatter)

        # Automatically redirect print statements if specified
        if redirect_print:
            cls.redirect_print_to_logger(logger)

        return logger