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
from services.parser_service import ParserService
from services.cases_buckets import CasesBucketsService 
from services.schema_service import SchemaService


def main():        
    command = ParserService.get_command()
    try:
        clear_screen()
        
        if command == 'info':
            schemaService = SchemaService()
            schemaService.execute_info()

        if command == 'fake':
            casesBucketsLogsService = CasesBucketsService()
            casesBucketsLogsService.execute_fake_rows()

        if command == 'truncate':
            casesBucketsLogsService = CasesBucketsService()
            casesBucketsLogsService.execute_truncate()

        if command == 'recreate':
            schemaService = SchemaService()
            schemaService.execute_recreate()
            
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
