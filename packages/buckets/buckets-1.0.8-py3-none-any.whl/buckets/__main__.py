import argparse
from configparser import NoSectionError
import os
import sys
import traceback

import mysql.connector

# Add this directory to sys.path
package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__) ))
sys.path.insert(0, package_dir)

from fake.console import clear_screen, move_cursor_to_line
from services.config_service import config
from services.cases_buckets import CasesBucketsService 


def main():        
    parser = argparse.ArgumentParser(description='Database utils for buckets.  This tools helps to populate and create tables related to My Cases improvements')
    parser.add_argument('command', type=str, help="Command to execute 'fake', 'truncate' ")
    parser.add_argument('--config-path', type=str, help='Path to the config file', default='buckets.ini')

    args = parser.parse_args()
    command = args.command
    
    try:
        clear_screen()
        
        config.read(args.config_path)
        
        casesBucketsLogsService = CasesBucketsService()
        
        if command == 'fake':
            casesBucketsLogsService.execute_fake_rows()

        if command == 'truncate':
            casesBucketsLogsService.execute_truncate()
            
    except (mysql.connector.errors.DatabaseError, FileNotFoundError, NoSectionError) as dbe: 
        #move_cursor_to_line(20)
        print(dbe)
        return    
    except Exception as e: 
        #move_cursor_to_line(20)
        print( e)
        print(f"Exception class: {type(e).__name__}")
        traceback.print_exc()
    finally:
        #move_cursor_to_line(20)
        pass

        
main()
