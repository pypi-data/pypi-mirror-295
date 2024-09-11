import argparse
from configparser import NoSectionError
from services.config_service import config

class ParserService(): 

    def get_command(*args, **kwargs):
        parser = argparse.ArgumentParser(
            description='Database utils for buckets.  This tools helps to populate and create tables related to My Cases improvements'
        )
        parser.add_argument(
            'command', 
            type=str, 
            help="Command to execute 'fake', 'truncate' "
        )
        
        parser.add_argument(
            '--config-path', 
            type=str, 
            help='Path to the config file', default='buckets.ini'
        )

        args = parser.parse_args()
        
        command = args.command    
        config.read(args.config_path)
            
        return command