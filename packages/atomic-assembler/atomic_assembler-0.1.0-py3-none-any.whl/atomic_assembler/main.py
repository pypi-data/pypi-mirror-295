import logging
import sys
import shutil
import os

from atomic_assembler.app import AtomicAssembler

# Set up logging
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def reset_tools_folder():
    """
    Remove the 'tools' folder if it exists, then create an empty 'tools' folder.
    """
    tools_path = os.path.join(os.getcwd(), "tools")

    # Remove existing 'tools' folder
    if os.path.exists(tools_path):
        try:
            shutil.rmtree(tools_path)
            logger.info("Successfully removed the existing 'tools' folder.")
        except Exception as e:
            logger.error(f"Failed to remove the 'tools' folder: {str(e)}")
            return

    # Create new empty 'tools' folder
    try:
        os.mkdir(tools_path)
        logger.info("Successfully created an empty 'tools' folder.")
    except Exception as e:
        logger.error(f"Failed to create the 'tools' folder: {str(e)}")


def main():
    """Main function to run the CLI tool."""
    reset_tools_folder()
    app = AtomicAssembler()
    app.run()


if __name__ == "__main__":
    main()  # Call the main function
