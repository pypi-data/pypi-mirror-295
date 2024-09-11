from services.config_service import config
import mysql.connector

class SchemaService(): 

    def setup_db_config(self):
        
        # Database configuration
        self.db_config = {
            'user': config.db_user,
            'password': config.db_password,
            'host': config.db_host,
            'database': config.db_database,
            'raise_on_warnings': False
        }
        
    def drop_table(self, table: str):
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            try:
                query = (f"drop table if exists {table};")
                print (query)
                cursor.execute(query)
                cnx.commit()
            except Exception as e:
                print (e)
                
            cursor.close()
        print(f"\033[FTable {table}: dropped                \n")        

    def execute_query(self, query: str):
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            cursor.execute(query)
            cnx.commit()
            cursor.close()
            
        query_first_line = ""    
        for line in query.splitlines():
            if query_first_line != "":
                continue
            if line.strip():  # Check if the line is not empty or only spaces
                query_first_line = line.strip()  # Return the first non-empty line, stripped of leading/trailing spaces
                
        print(f"\033[FQuery executed: {query_first_line}\n")        

    def create_table_pointers(self):
        query = """        
CREATE TABLE `case_pointers` (
  `id` varchar(20) NOT NULL,
  `counter` int unsigned DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
        self.execute_query(query)
        query = "insert into case_pointers values ('case_number', 1000, NOW(), NOW()); "
        self.execute_query(query)
        query = "insert into case_pointers values ('request_number', 1000, NOW(), NOW()); "
        self.execute_query(query)
        query = "insert into case_pointers values ('token_number', 1000, NOW(), NOW()); "
        self.execute_query(query)


    def create_table_cases_started(self):
        query = """        
CREATE TABLE cases_started (
  `case_number` int unsigned,
  `user_id` int unsigned,
  `case_title`  varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `case_status` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `processes` JSON NOT NULL,
  `requests` JSON NOT NULL,
  `request_tokens` JSON NOT NULL,
  `tasks` JSON NOT NULL,
  `participants` JSON NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `initiated_at` timestamp NULL DEFAULT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `keywords` TEXT COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`case_number`),
  KEY (`user_id`,`case_status`,`created_at`),
  KEY (`user_id`,`case_status`,`updated_at`),
  FULLTEXT KEY `case_title` (`case_title`),
  FULLTEXT KEY `keywords` (`keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
        self.execute_query(query)

          
    def create_table_cases_participated(self):
        query = """        
CREATE TABLE cases_participated (
  `user_id` int unsigned ,
  `case_number` int unsigned,
  `case_title`  varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `case_status` varchar(20) COLLATE utf8_unicode_ci NOT NULL,
  `processes` JSON NOT NULL,
  `requests` JSON NOT NULL,
  `request_tokens` JSON NOT NULL,
  `tasks` JSON NOT NULL,
  `participants` JSON NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `initiated_at` timestamp NULL DEFAULT NULL,
  `completed_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `keywords` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`user_id`, `case_number`),
  KEY `idx_user_status_created` (`user_id`,`case_status`,`created_at`),
  KEY `idx_user_status_completed` (`user_id`,`case_status`,`completed_at`),
  FULLTEXT KEY `case_title` (`case_title`),
  FULLTEXT KEY `keywords` (`keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""
        self.execute_query(query)


    def execute_recreate(self):
        self.setup_db_config()
        self.drop_table('case_pointers')
        self.drop_table('cases_started')
        self.drop_table('cases_participated')
        self.create_table_pointers()
        self.create_table_cases_started()
        self.create_table_cases_participated()


    def execute_info(self):
        self.setup_db_config()
        rows_at_start = self.show_table_count_all('cases_started')
        rows_at_start = self.show_table_count_all('cases_participated')
        self.show_table_pointers()
        print ("\n\n\n\n")

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

    def show_table_pointers(self):
        with mysql.connector.connect(**self.db_config) as cnx:
            cursor = cnx.cursor()
            query = (f"select * from case_pointers;")
            cursor.execute(query)
            # Fetch the count result
            result = cursor.fetchall()
            
            # Close the cursor and connection
            cursor.close()
        for r in result:
            print(f"{r[0]:20}: { r[1]:,} ")

    