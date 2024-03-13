import kiribot
import configparser
import pathlib

TMP_FILES = [pathlib.Path("./tmpsongs")]
VERIFY_FILES = [pathlib.Path("./apicalls"), pathlib.Path("./images"), 
                pathlib.Path("./localbot"), pathlib.Path("./kiribot.py"),
                pathlib.Path("./configuration.ini")]

class SystemConfiguration:
    
    @staticmethod
    def verify_files() -> bool:
        total_amount_of_tmp_files = len(TMP_FILES)
        
        for current, tmp_file in enumerate(TMP_FILES):
            print(f"Verifying File Integrity... ({current}/{total_amount_of_tmp_files})")

            if not tmp_file.exists():
                print(f"Failed to Verify File Integrity. One of the files are missing {tmp_file.name()}")
                return False
            
        print("Finished.")
            
        return True
    
    @staticmethod
    def clear_tmp_folders():
        total_amount_of_tmp_files = len(TMP_FILES)
        
        for current, tmp_file in enumerate(TMP_FILES):
            print(f"Clearing Temporary Files [{tmp_file}]... ({current}/{total_amount_of_tmp_files})")

            if tmp_file.is_dir():
                for file in tmp_file.iterdir():
                    print(f"Clearing File {file}")
                    file.unlink()

        print("Finished.")

def run_bot():

    try:
        print("Initiating Program")

        if SystemConfiguration.verify_files():
            SystemConfiguration.clear_tmp_folders()

            config = configparser.ConfigParser()
            config.read(pathlib.Path("configuration.ini"))
            bot_token = config.get('Discord-Bot', 'BotToken')
            bot = kiribot.KiriBot(bot_token)
    except Exception as e:
        print(f"Unable to Start Bot. Error: {e}")


if __name__ == "__main__":
    run_bot()