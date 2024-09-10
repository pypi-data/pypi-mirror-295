import os
import configparser

class Config():

    # Database configuration
    db_user: str = None 
    db_password: str = None 
    db_host: str = None 
    db_database: str = None 
    db_raise_on_warnings: str = None

    root_dir: str = None

    def read(self, config_path: str):
        parser = configparser.ConfigParser()

        if not os.path.isfile(config_path):
            raise  FileNotFoundError(f"The config file '{config_path}' does not exist.")
                    
        parser.read(config_path)
        self.root_dir = os.path.dirname(os.path.dirname( os.path.dirname(__file__) ))

        # database configurations
        self.db_user = parser.get('DATABASE', 'db_user')
        self.db_password = parser.get('DATABASE', 'db_password')
        self.db_host = parser.get('DATABASE', 'db_host')
        self.db_database = parser.get('DATABASE', 'db_database')


        # security_log
        self.fc_num_workers = int(parser.get('FAKE_CASES', 'num_workers'))
        self.fc_batch_size  = int(parser.get('FAKE_CASES', 'batch_size'))
        self.fc_buffer_size = int(parser.get('FAKE_CASES', 'buffer_size'))
        self.fc_goal        = int(parser.get('FAKE_CASES', 'goal'))

config = Config()