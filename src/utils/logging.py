import logging

def setup_logger():
    logging.basicConfig(
        filename="chatbot.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s"
    )
    return logging.getLogger("chatbot")

logger = setup_logger()
