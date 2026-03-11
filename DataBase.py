
# import pypyodbc
# import pyodbc
import pymssql
import json
import pyodbc

# Define your connection parameters
server = '41.38.197.252'  # e.g., 'localhost' or '41.38.197.252' 'DESKTOP-LMBLE4G\MERZOSQLEXPRESS'
database = 'Task_App'
username = 'merzo'    # Use None if using Windows Authentication
password = 'merzo1976'     # Use None if using Windows Authentication

# Create the connection string
# connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection_string = f'SERVER={server}; user={username}; password={password};database={database}'

# Connect to the database

try:  
    # db = pyodbc.connect(connection_string)
    
    # db = pymssql.connect(server='MERZ\MYDATABASE', user='merzo', password='merzo1976', database='Task_App')

    # **********************************************************************************************************
    # **********************pymssql*************************
   # server=r'41.38.197.252'
   # db = pymssql.connect(
   # server=server,
   # user='merzo',
   # password='merzo1976',
   # database='Task_App',
   # charset='UTF-8'    # ← Correct for pymssql
               
   #   )

   # print("Connection successful!")
   
   # cr = db.cursor()

   # def commit_and_close():
    
   #    db.commit() 
   #    db.close()
      
# # **********************pymssql*************************
# # **********************************************************************************************************

# # **********************************************************************************************************
# # **********************pyodbcsql*************************

   db = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=41.38.197.252;'  #    MERZ\\MYDATABASE
        'DATABASE=Task_App;'
        'UID=merzo;'
        'PWD=merzo1976;'
        'CHARSET=UTF8;'
    )


   print("Connection successful!")
   
   cr = db.cursor()

   def commit_and_close():
    
      db.commit() 
      db.close()



# **********************************************************************************************************
# ********************************  user by user id         ************************************************
# **********************************************************************************************************

   def user_table(user_id):
    
      cr.execute(f"SELECT user_id, username, password, role, full_name FROM [user] WHERE user_id = ?", (user_id,))
      
      return  cr.fetchone()
    

# **********************************************************************************************************
# ********************************   user by user username           ***************************************
# **********************************************************************************************************

   def user_check(user_name):    #user_name
     
      cr.execute(f"select user_id, username, password, role, full_name from [user] where username ='{user_name}'")  # where username ='{user_name}'
      return  cr.fetchone()
   

# **********************************************************************************************************
# ********************************  All User For Team mangment          ***************************************
# **********************************************************************************************************

   def all_user():    
     
      cr.execute(f"select user_id, username, password, role, full_name from [user]")  
      return  cr.fetchall()


# **********************************************************************************************************
# ********************************  Delete Emp  Data *******************************************************
# **********************************************************************************************************

   def Delete_user(user_id):
      
      cr.execute(f"delete from [user] where user_id = ?", (user_id,))
      db.commit()


# **********************************************************************************************************


# **********************************************************************************************************
# ********************************  Delete task   *******************************************************
# **********************************************************************************************************

   def Delete_task(task_id):
      
      cr.execute(f"delete from [task] where task_id = ?", (task_id,))
      db.commit()


# **********************************************************************************************************

    
# # **********************************************************************************************************
# # ********************************  Task filter assigned_by_id  ********************************************
# # **********************************************************************************************************

   def Task__assigned_by_CurrentUser (current_user_id):    #user_name
     
    #   cr.execute(f"select * from [task] where assigned_by_id ='{current_user_id}' ORDER BY current_deadline ")  
    #   return  cr.fetchall()
      
      cr.execute(f"select * from [Task_View] where assigned_by_id ='{current_user_id}' and Dec = 0 ORDER BY current_deadline ")  
      return  cr.fetchall()
   
# # **********************************************************************************************************
# # ********************************  Task filter assigned_by_id  and dec ok *********************************
# # **********************************************************************************************************

   def Task__assigned_by_CurrentUser_Filter_Ok (current_user_id):    #user_name
     
    #   cr.execute(f"select * from [task] where assigned_by_id ='{current_user_id}' ORDER BY current_deadline ")  
    #   return  cr.fetchall()
      
      cr.execute(f"select * from [Task_View] where assigned_by_id ='{current_user_id}' and Dec = 1 ORDER BY current_deadline ")  
      return  cr.fetchall()
   
# # **********************************************************************************************************
# # ********************************  Task filter assigned_by_id_and Dely  ********************************************
# # **********************************************************************************************************

   def Task_Dlay (current_user_id,now):    #user_name
     
    #   cr.execute(f"select * from [task] where assigned_by_id ='{current_user_id}' ORDER BY current_deadline ")  
    #   return  cr.fetchall()
      
      cr.execute(f"select * from [Task_View] where assigned_by_id = ? and current_deadline < ? and Dec = 0  ORDER BY current_deadline ", (current_user_id,))  
      return  cr.fetchall()
   


# # **********************************************************************************************************
# # ********************************  Task filter assigned_to_id  ********************************************
# # **********************************************************************************************************

   def Task_assigned_to_CurrentUser (current_user_id):    #user_name
     
    #   cr.execute(f"select * from [task] where assigned_to_id ='{current_user_id}' ORDER BY current_deadline ")  
    #   return  cr.fetchall()
     
      cr.execute(f"select * from [Task_View] where assigned_to_id = ? and Dec = 0 ORDER BY current_deadline ", (current_user_id,))  
      return  cr.fetchall()


# **********************************************************************************************************
# ********************************  Search in Data Task in assigned_by_id *********************************************************
# **********************************************************************************************************


   def Filter_task_assigned_by_id(Search_V_01,current_user_id):

      cr.execute(f"select * from Task_View where assigned_by_id = ? and Dec = 0 and ( title LIKE  '%' + ? + '%' or description LIKE  '%' + ? + '%' or project_name LIKE  '%' + ? + '%')  ORDER BY title ", (current_user_id, Search_V_01, Search_V_01, Search_V_01))
      return  cr.fetchall()
    
# **********************************************************************************************************

# # **********************************************************************************************************
# # ********************************  Task  overdue_tasks  FOR LEADER        ********************************************
# # **********************************************************************************************************

   def Overdue_Tasks (ssigned_by_id,now):    
     
      cr.execute(f"select * from [Task_View] where assigned_by_id = ? and Dec = 0 and (current_deadline < ? or requires_leader_attention = 1) and status <> 'completed'", (ssigned_by_id, now))
   
      return  cr.fetchall()

# # **********************************************************************************************************
# # ********************************  Task  overdue_tasks  FOR LEADER  for Dec 1      ********************************************
# # **********************************************************************************************************

   def Overdue_Tasks_Filter_Ok (ssigned_by_id):    
     
      cr.execute(f"select * from [Task_View] where assigned_by_id = ? and Dec = 1  and status <> 'completed'", (ssigned_by_id))
   
      return  cr.fetchall()
   
# # **********************************************************************************************************
# # ********************************  Task  overdue_tasks  FOR MEMBER       ********************************************
# # **********************************************************************************************************

   def Overdue_Tasks_Member (assigned_to_id,now):    
     
      cr.execute(f"select * from [Task_View] where assigned_to_id = ? and Dec = 0 and (current_deadline < ? or requires_leader_attention = 1) and status <> 'completed'", (assigned_to_id, now))
      
      return  cr.fetchall()
   
# # **********************************************************************************************************
# # ********************************  Task filter by task_Id  ********************************************
# # **********************************************************************************************************

   def Task_by_TaskId (task_id):    #user_name
     
 
      cr.execute(f"select * from [Task_View] where task_id = ? ", (task_id,))  
      return  cr.fetchone()



# # **********************************************************************************************************

# **********************************************************************************************************
# ********************************  Search in Data Task filter by memeber *********************************************************
# **********************************************************************************************************


   def Task__assigned_by_member(Filter_by_member_v ):

      cr.execute(f"select * from Task_View where assigned_to_id = ? and Dec = 0  ORDER BY current_deadline ", (Filter_by_member_v))
      return  cr.fetchall()
   

# # **********************************************************************************************************
# # ********************************  user filter by member   *****************************************************
# # **********************************************************************************************************

   def user_member():   
     
      cr.execute(f"select * from [user] where role='member'")  # where username ='{user_name}'
      return  cr.fetchall()

# **********************************************************************************************************
# ********************************   task check_notifications  leader         ***************************************
# **********************************************************************************************************

   def  task_check_notifications (user_id):    
     
     cr.execute(f"SELECT COUNT(task_id) AS no_task  FROM [Task_View] WHERE  (assigned_by_id = ?) and Dec = 0 and (requires_leader_attention = 1) AND (status <> 'completed')", user_id)
     
     return  cr.fetchone()
    

# **********************************************************************************************************
# ********************************   task check_notifications  member     **********************************
# **********************************************************************************************************

   def  task_check_notifications_member (user_id):    
     
     cr.execute(f"SELECT COUNT(task_id) AS no_task  FROM [Task_View] WHERE  (assigned_to_id = ?) AND (requires_leader_attention = 1) AND (status <> 'completed')", user_id)
     
     return  cr.fetchone()
   
# **********************************************************************************************************
# ********************************  ADD Task  Data *********************************************************
# **********************************************************************************************************

   def ADD_Task(title, description, assigned_to_id,assigned_by_id, start_date, original_end_date, current_deadline, status, created_at,Project_id):
               

    #  cr.execute(f"insert into [task] (title, description, assigned_to_id,assigned_by_id, start_date, original_end_date, current_deadline, status, created_at) values('{title}', '{description}', '{assigned_to_id}', '{assigned_by_id}', '{start_date}', '{original_end_date}', '{current_deadline}', '{status}', '{created_at}')")
    #  db.commit()

     cr.execute("""
            INSERT INTO [task] (
                title, description, assigned_to_id, assigned_by_id, 
                start_date, original_end_date, current_deadline, status, created_at,task_project_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, title, description, assigned_to_id, assigned_by_id, 
           start_date, original_end_date, current_deadline, status, created_at,Project_id)
     
     db.commit() 
       
# **********************************************************************************************************


# **********************************************************************************************************
# ********************************  ADD new user **********************************************************
# **********************************************************************************************************

   def ADD_User( user_name, user_password, user_role,user_full_name ):
               

     cr.execute("""
            INSERT INTO [user] (
                username, password, role, full_name
            ) VALUES (?, ?, ?, ?)
        """, user_name, user_password, user_role, user_full_name)
     
     db.commit() 
       
# **********************************************************************************************************

# **********************************************************************************************************
# ********************************  Updata user  Data                      *********************************
# **********************************************************************************************************

 
   def Edit_User(user_id ,user_name, user_password, user_role,user_full_name):

     cr.execute("""
            UPDATE [user] 
            SET   username = ?, 
                  password = ?, 
                  role = ?, 
                  full_name = ? 
            WHERE user_id = ?
        """, (
            user_name, 
            user_password,  
            user_role,
            user_full_name,
            user_id
        ))
    
    
     db.commit()
                
   
# # **********************************************************************************************************
# # ********************************  Task filter task_id         ********************************************
# # **********************************************************************************************************

   def Current_Task (Task_id):    
     
      cr.execute(f"select * from [Task_View] where task_id = ? ", (Task_id,))  
      return  cr.fetchone()
   


# **********************************************************************************************************
# ********************************  Updata Task  Data for complete ststus  *********************************
# **********************************************************************************************************

 
   def update_Task_status(task_id, status, completed_at, requires_leader_attention):

    #  cr.execute(f"UPDATE [task] SET status ='{status}', completed_at ='{completed_at}', requires_leader_attention ='{requires_leader_attention}'  where task_id = '{task_id}'")
     cr.execute("""
            UPDATE [task] 
            SET   status = ?, 
                  completed_at = ?, 
                  requires_leader_attention = ? 
            WHERE task_id = ?
        """, (
            status, 
            completed_at,  
            requires_leader_attention, 
            task_id
        ))
    
    
     db.commit()
      


# **********************************************************************************************************
# ********************************  Updata Task  Data for postpone ststus  ************************************
# **********************************************************************************************************

 
   def update_Task_status_postpone(task_id, new_deadline, requires_leader_attention):

    #  cr.execute(f"UPDATE [task] SET current_deadline ='{new_deadline}', requires_leader_attention ='{requires_leader_attention}'  where task_id = '{task_id}'")
    
     cr.execute("""
            UPDATE [task] 
            SET   current_deadline = ?, 
                  requires_leader_attention = ?
            WHERE task_id = ?
        """, (
            new_deadline, 
            requires_leader_attention,
            task_id
        ))
     
     
     
     db.commit()
      

# **********************************************************************************************************
# ********************************  Updata Task  Data for delay ststus  ************************************
# **********************************************************************************************************

 
   def update_Task_status_delay(task_id,status,reason_for_delay, current_deadline, requires_leader_attention):

    #  cr.execute(f"UPDATE [task] SET status ='{status}', reason_for_delay ='{reason_for_delay}', current_deadline ='{current_deadline}', requires_leader_attention ='{requires_leader_attention}'  where task_id = '{task_id}'")
     
     cr.execute("""
            UPDATE [task] 
            SET   status = ?, 
                  reason_for_delay = ?, 
                  current_deadline = ?,
                  requires_leader_attention = ?
            WHERE task_id = ?
        """, (
            status, 
            reason_for_delay,
            current_deadline,  
            requires_leader_attention, 
            task_id
        ))
     
     db.commit()



# **********************************************************************************************************
# ********************************  Updata Task  Dec  ************************************
# **********************************************************************************************************

 
   def Take_Dec_Task(task_id):

    #  cr.execute(f"UPDATE [task] SET status ='{status}', reason_for_delay ='{reason_for_delay}', current_deadline ='{current_deadline}', requires_leader_attention ='{requires_leader_attention}'  where task_id = '{task_id}'")
     
     cr.execute("""
            UPDATE [task] 
            SET   Dec = 1 
            WHERE task_id = ?
        """, (
            task_id
        ))
     
     db.commit()



# **********************************************************************************************************
# ********************************  Updata task  Data                      *********************************
# **********************************************************************************************************

 
   def Edit_Task(task_id, task_title, task_description, task_assigned_to_id, task_start_date, task_end_date, task_original_end_date, task_completed_at, task_reason_for_delay,task_status,task_Dec,task_project):

     cr.execute("""
            UPDATE [task] 
            SET   title = ?, 
                  description = ?, 
                  assigned_to_id = ?, 
                  start_date = ?, 
                  original_end_date = ?, 
                  current_deadline = ?, 
                  completed_at = ?, 
                  reason_for_delay = ?,
                  status = ?,
                  Dec = ?,
                  task_project_id = ?
            WHERE task_id = ?
        """, (
            task_title,
            task_description,
            task_assigned_to_id,
            task_start_date,
            task_original_end_date,
            task_end_date,
            task_completed_at,
            task_reason_for_delay,
            task_status,
            task_Dec,
            task_project,
            task_id
        ))
    
    
     db.commit()
                
# **********************************************************************************************************

# **********************************************************************************************************
# ********************************  All project        ***************************************
# **********************************************************************************************************

   def project_table():    
     
      cr.execute(f"select project_id, project_name, project_group  from [Project_Table]")  
      return  cr.fetchall()

# **********************************************************************************************************
# ********************************  All project by id        ***************************************
# **********************************************************************************************************

   def project_table_id(project_id):    
     
      cr.execute(f"select project_id, project_name, project_group  from [Project_Table] where project_id = ?", (project_id,))
      return  cr.fetchone()
# **********************************************************************************************************
# ********************************  Delete Project   *******************************************************
# **********************************************************************************************************

   def Delete_Project(project_id):
      
      cr.execute(f"delete from [Project_Table] where project_id = ?", (project_id,))
      db.commit()

# **********************************************************************************************************
# ********************************  ADD Project **********************************************************
# **********************************************************************************************************

   def Add_Project(project_name, project_group):
      
      cr.execute(f"INSERT INTO [Project_Table] (project_name, project_group) VALUES (?, ?)", (project_name, project_group))
      db.commit()


# **********************************************************************************************************
# ********************************  Updata Project  Data                      *********************************
# **********************************************************************************************************

 
   def Edit_Project(project_id, project_name, project_group):

     cr.execute("""
            UPDATE [Project_Table] 
            SET   project_name = ?, 
                  project_group = ? 
            WHERE project_id = ?
        """, (
            project_name, 
            project_group,  
            project_id
        ))
    
    
     db.commit()






except Exception as e:
    print("Error connecting to the database:", e)

# Don't forget to close the connection when done
finally:
    if 'connection' in locals():
        commit_and_close()
