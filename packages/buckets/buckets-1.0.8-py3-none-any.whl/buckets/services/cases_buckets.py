from datetime import datetime
import json
import threading
import time

from tqdm import tqdm
import concurrent.futures
import mysql.connector

from fake.console import move_cursor_to_line, print_n_lines_up, print_with_cursor_control
from fake.users import get_user_name
from fake.cases_rows import CasesRows
from fake.dates import get_HMS
from services.config_service import config

class CasesBucketsService(): 

    workers: [] # type: ignore
    count: int = 0
            
    def fmt_workers(workers):
        output = ''.join('O' if worker['running'] else ' ' for worker in workers)
        count = sum(worker['running'] for worker in workers)
        inserted = sum(worker['rows_inserted'] for worker in workers)
        return f"{output} {count:3} {inserted}"   


    def my_callback(self, future):
        worker_id = future.result()
        self.workers[worker_id]['running'] = False
        self.workers[worker_id]['count'] += 1  
        self.workers[worker_id]['rows_inserted'] += self.batch_size 
        #to do: increment by the real rows inserted

        
    def insert_rows(self, worker_id: int, query: str, data):

        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            cursor.executemany(query, data)
            cnx.commit()
        return worker_id
    
    # cases started functions
    
    def get_cases_started(self, data):
        cases_rows = []
        
        for r in data: 
            user_id  = self.get_started_user_id(r['tokens'] )
            requests = self.get_requests_from_requests(r['requests'] )
            request_tokens = self.get_request_tokens_from_tokens(r['tokens'] )
            tasks  = self.get_tasks_from_tokens(r['tokens'] )
            participants = self.get_participants_from_tokens(r['tokens'] )
            
            cases_rows.append( (
                user_id,
                r['case_number'], 
                r['case_title'], 
                r['case_status'],
                json.dumps( r['processes'] ), 
                json.dumps( requests ), 
                json.dumps( request_tokens ), 
                json.dumps( tasks ), 
                json.dumps( participants ), 
                datetime.now(), 
                datetime.now(), 
                None, 
                None, 
                'keyword1'
            ))
        return cases_rows
    
    def get_started_user_id(self, tokens):
        if len(tokens) < 1:
            print ("Error: tokens has 0 items. this should never happens")
                   
        return tokens[0]['user_id']
    
        
    def get_requests_from_requests(self, requests):
        # iterate requests
        result = []

        for r in requests:
            result.append({
                'id': r['id'],
                'name': r['name'],
                'parent_request_id': r['parent_request_id']
            })
            
        return result
    
        
    def get_request_tokens_from_tokens(self, tokens):
        # iterate tokens
        request_tokens = []

        for t in tokens:
            request_tokens.append({
                'id': t['id']
            })
        return request_tokens

    
    def get_tasks_from_tokens(self, tokens):
        # iterate tokens
        tasks = []
        seen_ids = set()  # Set to track seen element IDs

        for t in tokens:
            element_id = t['element_id']
            if element_id not in seen_ids:  # Check if the ID is already seen
                tasks.append({
                    'id': element_id,
                    'name': t['element_name']
                })
                seen_ids.add(element_id)  # Add the ID to the seen set

        return tasks
    
    def get_participants_from_tokens(self, tokens):
        # iterate tokens
        participants = []
        seen_ids = set()  # Set to track seen element IDs

        for t in tokens:
            user_id = t['user_id']
            if user_id not in seen_ids:  # Check if the ID is already seen
                participants.append({
                    'id': user_id,
                    'name': get_user_name(user_id)
                })
                seen_ids.add(user_id)  # Add the ID to the seen set

        return participants


    # cases participated functions
    def get_user_list(self, tokens):
        user_set = set()  # Use a set to store unique user_ids
        for t in tokens:
            user_set.add(t['user_id'])  # Add user_id to the set

        return list(user_set)  # Convert the set back to a list before returning
    
    
    def get_cases_participated(self, data):
        cases_rows = []

        for r in data: 
            user_list  = self.get_user_list(r['tokens'] )
            for user_id in user_list:
                requests = self.get_requests_from_requests(r['requests'] )
                request_tokens = self.get_request_tokens_from_tokens(r['tokens'] )
                tasks  = self.get_tasks_from_tokens(r['tokens'] )
                participants = self.get_participants_from_tokens(r['tokens'] )
                
                cases_rows.append( (
                    user_id,
                    r['case_number'], 
                    r['case_title'], 
                    r['case_status'],
                    json.dumps( r['processes'] ), 
                    json.dumps( requests ), 
                    json.dumps( request_tokens ), 
                    json.dumps( tasks ), 
                    json.dumps( participants ), 
                    datetime.now(), 
                    datetime.now(), 
                    None, 
                    None, 
                    'keyword1'
                ))

        return cases_rows
            

    def insert_case_started_rows(self, data):
        base_query = (
            "INSERT INTO cases_started "
            "(user_id, case_number, case_title, case_status, processes, requests, request_tokens, tasks, participants, created_at, initiated_at, completed_at, updated_at, keywords) "
            "VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s)"
        )

        cases_rows = self.get_cases_started(data)

             
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            cursor.executemany(base_query, cases_rows)
            cnx.commit()
    
    
    def insert_case_participated_rows(self, data):
        base_query = (
            "INSERT INTO cases_participated "
            "(user_id, case_number, case_title, case_status, processes, requests, request_tokens, tasks, participants, created_at, initiated_at, completed_at, updated_at, keywords) "
            "VALUES (%s, %s, %s, %s, %s,  %s, %s, %s, %s, %s,  %s, %s, %s, %s)"
        )

        cases_rows = self.get_cases_participated(data)
             
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            cursor.executemany(base_query, cases_rows)
            cnx.commit()
    
    
    def insert_case_rows(self, worker_id: int,  data):
        self.insert_case_started_rows(data)
        self.insert_case_participated_rows(data)
        return worker_id
    
    
    def show_table_count_all(self, table):
        print(f"Counting rows in {table}...")
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            query = (f"select count(*) from {table};")
            cursor.execute(query)
            # Fetch the count result
            count_result = cursor.fetchone()[0]
            
            # Close the cursor and connection
            cursor.close()
        print(f"\033[FRows in {table}: { count_result :,}          ")

        return count_result

    def show_count_all(self):
        self.show_table_count_all('case_numbers')
        self.show_table_count_all('cases_started')
        self.show_table_count_all('cases_participated')


    def setup_db_config(self):
        # Database configuration
        self.db_config = {
            'user': config.db_user,
            'password': config.db_password,
            'host': config.db_host,
            'database': config.db_database,
            'raise_on_warnings': True
        }

    def create_tqdms(self,):        
        main_pbar = tqdm(
            total=self.goal, 
            desc='Inserting fake rows',
            unit='K', 
            leave=True,
            position=0, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )
        
        buffer_pbar = tqdm(
            total=self.buffer_size, 
            desc='Buffer of fake rows', 
            leave=True,
            position=1, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} '
        )

        return main_pbar, buffer_pbar


    def create_fast_copy_tqdms(self,):        
        main_pbar = tqdm(
            total=self.goal, 
            desc='Rows  inserted',
            unit='K', 
            leave=True,
            position=0, 
            unit_scale=True, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]'
        )
        
        buffer_pbar = tqdm(
            total=self.buffer_size * 2, 
            desc='Buffer of rows', 
            leave=True,
            position=1, 
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} '
        )

        return main_pbar, buffer_pbar
    
    
    def initialize_workers(self):
        # Initialize the workers
        self.workers = [{'id': i, 'future': None, 'running': False, 'count': 0, 'rows_inserted': 0} for i in range(self.num_workers)]
        
        
    def execute_fake_rows(self):
        self.setup_db_config()

        # Number of workers and batch size
        self.num_workers = config.fc_num_workers
        self.batch_size = config.fc_batch_size
        self.buffer_size = config.fc_buffer_size
        self.goal = config.fc_goal

        print (f"Batch size: {self.batch_size}  num workers: {self.num_workers}  goal: {self.goal}")
        
        rows_at_start = self.show_table_count_all('cases_started')

        main_pbar, buffer_pbar = self.create_tqdms()

        casesRows = CasesRows()
        casesRows.set_last_case_number(rows_at_start)
        casesRows.set_last_token_id(1000)
        casesRows.set_last_request_id(100)
        casesRows.init_fake_rows(self.goal, self.batch_size, self.buffer_size, buffer_pbar)  

        self.initialize_workers()
        start_time = time.time()        

        # generate a batch in a separate thread
        #if self.count_sent < self.goal:
        thread = threading.Thread(target=casesRows.generate_batches_thread)
        thread.start()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            continue_loop = True

            while continue_loop:
                for worker_id, worker in enumerate(self.workers):
                    if not worker['running']:
                        batch_of_rows = casesRows.get_batch_of_rows()
                        if batch_of_rows is None:
                            continue_loop = False
                        else:
                            print_with_cursor_control (f"   batches_sent: {casesRows.count_sent:9,} ", 50, 9, 30)

                            worker['running'] = True
                            future = executor.submit(self.insert_case_rows, worker_id, batch_of_rows)
                            future.add_done_callback(self.my_callback)
                            worker['future'] = future 
                            main_pbar.update(self.batch_size)

        # wait until all workers completed
        while True:
            # Check if any workers are still running
            if any(worker['running'] for worker in self.workers):            
                time.sleep(1)
            else:
                break
            
        main_pbar.close()
        buffer_pbar.close()
        completed = sum(worker['rows_inserted'] for worker in self.workers)        
        
        move_cursor_to_line(15)
        print (f"Completed (Σ workers): {completed:9,}")


        end_time = time.time()
        execution_time = end_time - start_time
        rows_at_end = self.show_table_count_all('cases_started')
        print(f"  Total Rows inserted: { (rows_at_end - rows_at_start):9,}")
        print(f"     The process took: { get_HMS(execution_time)} to execute.")


    def truncate_table(self, table: str):
        print(f"Truncating table {table}...")
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            query = (f"truncate {table};")
            cursor.execute(query)
            # Close the cursor and connection
            cursor.close()
        print(f"\033[FTable {table}: truncated    \n")        

    def execute_truncate(self):
        self.setup_db_config()
        self.truncate_table('cases_started')
