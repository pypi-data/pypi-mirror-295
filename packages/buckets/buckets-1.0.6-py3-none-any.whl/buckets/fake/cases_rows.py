# Define the events and their probabilities
from datetime import datetime
import json
import os
import random
from collections import deque
import re
import sys
import threading
import time
from faker import Faker
from tqdm import tqdm

from fake.console import print_with_cursor_control
from fake.dates import get_case_dates, get_working_past_date
from fake.users import generate_user_id_normal

class CasesRows:
    _instance = None
    buffer = deque()
    batch_size = 0
    buffer_size = 0
    goal = 0
    count_generated = 0
    count_sent = 0
    buffer_pbar = None
    last_read_row = None       # Track the last read row or the beggining of the limit range
    last_delivered_row = None  # Track the last delivered row
    last_processed_row = None  # Track the last processed row
    reading_a_batch = False     # a semaphore to allow only one thread to read from database
    goal_row = 0
             
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CasesRows, cls).__new__(cls)
        return cls._instance


    def init(self, goal, batch_size: int, buffer_size: int, pbar: tqdm):
        self.goal = goal
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        self.buffer_pbar = pbar

    
    def init_fake_rows(self, goal, batch_size: int, buffer_size: int, pbar: tqdm):
        self.init(goal, batch_size, buffer_size, pbar)

        # Create a Faker instance
        self.fake = Faker()

        # set buffer
        self.buffer = deque(maxlen=self.buffer_size)
        for _ in range( int (self.buffer_size )):
            self.generate_a_batch()
           
    def set_last_case_number(self, last_case_number):
        self.last_case_number = last_case_number

    def get_next_case_number(self):
        self.last_case_number = self.last_case_number + 1
        return self.last_case_number

    def set_last_token_id(self, last_case_number):
        self.last_token_id = last_case_number

    def get_next_token_id(self):
        self.last_token_id = self.last_token_id + 1
        return self.last_token_id

    def set_last_request_id(self, last_request_id):
        self.last_request_id = last_request_id

    def get_next_request_id(self):
        self.last_request_id = self.last_request_id + 1
        return self.last_request_id

    def get_last_delivered_row(self):
        return self.last_delivered_row

    def get_last_processed_row(self):
        return self.last_processed_row

    def set_last_delivered_row(self, row):
        self.last_delivered_row = row

    def set_last_processed_row(self, row):
        self.last_processed_row = row

                
    def generate_a_batch(self):
        # generate one batch of fake rows and push into the queue
        # update the counters to make it available
        
        if self.count_generated >= self.goal: 
            return None
        
        this_batch_size = self.batch_size

        if self.count_generated + self.batch_size > self.goal:
            this_batch_size = max(0, self.goal - self.count_generated)
            
        batch = [self.generate_simple_case() for _ in range(this_batch_size)]
        
        self.count_generated += this_batch_size
        self.buffer.append(batch)
        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        
        #dump_object_to_file(batch, True)
        print_with_cursor_control (f"cases generated: {self.count_generated:9,} ", 50, 8, 30)


    def get_batch_of_rows(self):
        # get the next available batch from the queue, 
        # if not available batch, waits until it is generated
        # do not wait, if no more batches to generate and return None
        # and then update the counters. 

        if not self.buffer and self.count_generated < self.goal :
            iterations = 0
            while self.count_generated < self.goal and len(self.buffer) == 0:
                #print_with_cursor_control (f"len self.buffer: {len(self.buffer):3,} iterations: {iterations}  ", 50, 13, 30)
                #print_with_cursor_control (f"self.count_generated {self.count_generated} < self.goal {self.goal}  ", 50, 14, 30)
                time.sleep(1.1) # wait 0.1 second until the the buffer refills
                iterations = iterations + 1

        # get a batch and update counters
        if self.buffer:
            batch = self.buffer.popleft()
        else:
            return None
 
        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.count_sent += 1

        return batch

    def generate_batches_thread(self):
        # generate a batches in a separate thread
        
        # if all batchs were sent, just return
        if self.count_generated >= self.goal:
            return 
        
        continue_thread = True
        index = 0 
        while continue_thread:
            # wait until the buffer needs to be generated
            while len(self.buffer) >= self.buffer_size:
                time.sleep(0.5) # wait 0.5 second until previous batch is generated

            if self.count_generated + self.batch_size <= self.goal:
                self.generate_a_batch()

            continue_thread = self.count_generated + self.batch_size <= self.goal
            # print_with_cursor_control (f" continue_thread: {continue_thread}  {index} ", 50, 12, 30)
            index =+ 1


    def get_batch_of_read_rows(self):
        # get the next available batch from the queue of read rows, 
        # if not available batch, waits until it is readed
        # do not wait, if reach the goal and return None
        # and then update the counters. 
        if not self.buffer and self.last_read_row < self.goal_row :
            while not self.buffer :
                time.sleep(0.1) # wait 0.1 second until the the buffer refills
                #print ("wait\n")
                    
        # return None if no more batches
        if not self.buffer:
            self.buffer_pbar.n = 0
            self.buffer_pbar.refresh() 
            return None 
            
        # get a batch and update counters
        batch = self.buffer.popleft()

        # read the next batch in a separate thread
        if self.last_read_row < self.goal_row and self.reading_a_batch == False:
            len_buffer = 0 if self.buffer is None else len(self.buffer)
            # start the thread when buffer is less of 50% of capacity
            if len_buffer < self.buffer_size:
                thread = threading.Thread(target=self.read_a_batch)
                thread.start()

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.last_delivered_row += len(batch)

        #print (f"\033[1A         {self.last_delivered_row} {self.goal}     \033[1B", end='') 
        #tqdm.write (f"   {self.last_delivered_row} {self.goal}  ", end='') 
        return batch
    

    def read_a_batch(self):
        # read a batch from database, executes only one tread, no parallelism
        self.reading_a_batch = True
        
        # Logic to read the next batch of rows from the table
        time.sleep(0.5)
        this_buffer_size = self.buffer_size
        pending_rows = self.goal_row - self.last_read_row 
        if  pending_rows < self.buffer_size * self.batch_size:
            this_buffer_size, last_batch_size = divmod (pending_rows, self.batch_size)

        for i in range(this_buffer_size):
            batch = []
            for i in range(self.batch_size):
                batch.append ( {"n":i*100, "data": "ABC"} )
            
            self.buffer.append(batch)                
        
        self.last_read_row += this_buffer_size * self.batch_size
        
        if this_buffer_size != self.buffer_size:
            last_batch = []
            for i in range(last_batch_size):
                last_batch.append ( {"n":i*100, "data": "last"} )
            
            self.buffer.append(last_batch)                
            self.last_read_row += 1 * last_batch_size

        self.buffer_pbar.n = len(self.buffer)
        self.buffer_pbar.refresh() 
        self.reading_a_batch = False
        
        
    def get_random_status(self):
        return random.choice(["in_progress", "completed"])

    def get_random_process_id(self):
        return random.choice([23])

   
    def get_random_travel_processes(self):
        processes = random.choice([
            [
                {'id': 23, 'name': 'Business Travel'}
            ], 
            [
                {'id': 23, 'name': 'Business Travel'},
                {'id': 25, 'name': 'Subprocess Business Travel'}
            ], 
            [
                {'id': 23, 'name': 'Business Travel'},
                {'id': 24, 'name': 'Parallel of Travel'},
                {'id': 25, 'name': 'Subprocess of Business Travel'}
            ]
        ])
        return processes

    # process_requests   `status` enum('DRAFT','ACTIVE','COMPLETED','ERROR','CANCELED') COLLATE utf8mb4_unicode_ci NOT NULL,
    # process_request_tokens  `status` enum('ACTIVE','FAILING','COMPLETED','CLOSED','EVENT_CATCH','TRIGGERED','INCOMING') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'ACTIVE',
 
    def get_random_travel_tokens(self, processes: any, case_title: str, case_number: int, case_created_at: datetime):

        # assign id for the requests of this case
        requests = []
        for process in processes:
            requests.append({
                'id' : self.get_next_request_id(),
                'process_id': process['id'],
                'parent_request_id': 0 if process['id'] == processes[0]['id'] else processes[0]['id'], # todo: improve 
                'status': 'ACTIVE', #DRAFT','ACTIVE','COMPLETED','ERROR','CANCELED'
                'name': f"{ process['name'] } {self.last_request_id}", 
                'case_title' : case_title,
                'case_number' : case_number
            })
            
        
        bpmn_tasks = [
            { "task_id": "node_12345", "task_name": "Request Travel Approval" },
            { "task_id": "node_67890", "task_name": "Book Flights" },
            { "task_id": "node_23456", "task_name": "Reserve Accommodation" },
            { "task_id": "node_78901", "task_name": "Arrange Ground Transportation" },
            { "task_id": "node_34567", "task_name": "Prepare Travel Itinerary" },
            { "task_id": "node_89012", "task_name": "Submit Expense Report" },
            { "task_id": "node_45678", "task_name": "Review Travel Policies" },
            { "task_id": "node_90123", "task_name": "Notify Team of Travel Plans" },
            { "task_id": "node_56789", "task_name": "Conduct Pre-Travel Briefing" },
            { "task_id": "node_11223", "task_name": "Collect Feedback Post-Travel" }
        ]
        
        # assign default user for these tasks for this case
        for bpmn_task in bpmn_tasks:
            bpmn_task['user_id'] = generate_user_id_normal(5000) 


        # create an array of tokens  (process_request_tokens)  
        tokens = []    
        current_request = requests[0]
        
        tokens_len = random.randint(1, len(processes) * 10)
        current_case_date = case_created_at  # use this variable to maintain some logic in dates, every task is after this one.
            
        for _ in range(0, tokens_len):
            task = random.choice(bpmn_tasks)
            tokens.append({
                'id': self.get_next_token_id(), 
                'user_id' : random.choice( [task['user_id'], generate_user_id_normal(5000) ]),
                'process_id': current_request['process_id'],     
                'process_request_id': current_request['id'],     
                'element_id' : task['task_id'],
                'element_name' : task['task_name'],
                'status' : '?',
                'created_at' : current_request,
                'initiated_at' : '?',
                'updated_at' : '?',
                'completed_at' : '?',
            })
        
            # algorithm to select in which process/subprocess will be next request
            # the algoritm started with the main process
            is_main_process = current_request['process_id'] == requests[0]['process_id']
        
            if not is_main_process or random.random() > 0.3:
                random_index = random.randint(0, len(requests) - 1)
                current_request = requests[random_index]
                
        # todo: complete some request_tokens
        # todo: add dats in fashionable way
        return requests, tokens

    def get_travel_data(self, case_number: int, case_created_at: datetime):
        city = self.fake.city()
        country = self.fake.country()

        case_title = f'Travel to {city} in {country}'
        processes = self.get_random_travel_processes()
        requests, tokens = self.get_random_travel_tokens(processes, case_title, case_number, case_created_at)

        
        return case_title, processes, requests, tokens
        
    # generate a fake Case
    def generate_simple_case(self):
        case_number = self.get_next_case_number() 
        case_status = self.get_random_status() 
        main_process_id = self.get_random_process_id() 
        case_created_at = get_working_past_date(1000, 1)

        simple_case = {}
        simple_case['case_number']  = case_number 
        simple_case['case_status']  = case_status 

        if main_process_id == 23:
            case_title, processes, requests, tokens = self.get_travel_data(case_number, case_created_at) 
        
            simple_case['case_title']   = case_title
            simple_case['processes']    = processes
            simple_case['requests']     = requests
            simple_case['tokens']       = tokens
            
        
        #user_id = generate_user_id_normal(5000)  
        #simple_case['user_id']   = user_id
        
        created_at, initiated_at, completed_at, updated_at = get_case_dates(case_status)
        simple_case['created_at']   = case_created_at
        simple_case['initiated_at'] = initiated_at
        simple_case['completed_at'] = completed_at
        simple_case['updated_at']   = updated_at
        return simple_case

