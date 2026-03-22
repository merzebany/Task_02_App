# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from functools import wraps
import requests
from flask_login import UserMixin

import os



# app = Flask(__name__)
app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/My_App')
# app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['JSON_AS_ASCII'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'



TELEGRAM_BOT_TOKEN = "8533540111:AAHeyCTOilpqxBF_-6jt44OnFiKA9I1rGe8"
TELEGRAM_CHAT_ID = "6878108547"


# Models

class User(UserMixin):
 
    def __init__(self, user_tuple):
        if not user_tuple:
            raise ValueError("User tuple is None")
       
        
        self.id = user_tuple[0]      # user_id
        self.username = user_tuple[1]
        self.password = user_tuple[2]
        self.role = user_tuple[3]
        self.full_name =user_tuple[4]
        
       


    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    try:
        # Convert session ID to int (critical!)
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        return None
    
    from DataBase import user_table
    user_v = user_table(user_id_int)
   
    return User(user_v)

    # return User.query.get(int(user_id))



# Role-based access decorators
def leader_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'leader':
            flash('Leader access required', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def member_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'member':
            flash('Member access required', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes


#**************************************************************************************************************
#*******************************     login   -   logout            ********************************************
#**************************************************************************************************************

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        from DataBase import user_check
        user_data = user_check(username)
       

        if not user_data:
          return "User not found", 401
    
    # Create User object
        user = User(user_data)
       
        # Simple auth - in production use hashed passwords
        if user.username.strip() == username.strip() and user.password.strip() == password.strip():
 
            hasattr(user, 'is_authenticated')
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            
            return redirect(url_for('dashboard'))
       
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    # return render_template('Test.html')
    #   now = datetime.utcnow()

      now = datetime.now().replace(microsecond=0)

      if current_user.role == 'leader':
        # Get all tasks created by this leader
          from DataBase import Task__assigned_by_CurrentUser
          Task_data = Task__assigned_by_CurrentUser (current_user.id)
          
          from DataBase import user_member
          members = user_member()

          from DataBase import Overdue_Tasks
          Overdue_Tasks_V = Overdue_Tasks(current_user.id,now)
          
        #   for task in Task_data:
        #      if task['current_deadline']:
        #       print(task['current_deadline'])
        #       Task_data['formatted_current_deadline'] = task['current_deadline'].strftime('%d %b, %Y at %I:%M %p')
        #      else:
        #       Task_data['formatted_current_deadline'] = 'No deadline'

          
          return render_template('leader_dashboard.html', tasks=Task_data, members=members,now=now , Overdue_Tasks_V=Overdue_Tasks_V)
      else:
          from DataBase import Task_assigned_to_CurrentUser
          Task_data = Task_assigned_to_CurrentUser(current_user.id)

          return render_template('member_tasks.html', tasks=Task_data, now=now )

#**************************************************************************************************************
#*******************************      assign-task        ******************************************************
#**************************************************************************************************************

@app.route('/assign-task', methods=['GET', 'POST'])
@login_required
@leader_required
def assign_task():

      from DataBase import user_member
      members = user_member()
      
      from DataBase import project_table
      projects = project_table()
      

      if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        assigned_to_id = request.form['assigned_to']
        assigned_by_id=current_user.id
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        original_end_date=end_date
        current_deadline = end_date
        status='pending'
        Project_id = request.form['Project_assigned']

  
        # Validate dates
        if end_date <= start_date:
            flash('End date must be after start date', 'danger')
            return render_template('assign_task.html', members=members)
        

        from DataBase import ADD_Task
        ADD_Task(title, description, assigned_to_id,assigned_by_id, start_date, original_end_date, current_deadline, status, datetime.now().replace(microsecond=0),Project_id)

        
        flash(f'Task "{title}" assigned successfully!', 'success')
        return redirect(url_for('dashboard'))
    
      return render_template('assign_task.html', members=members , projects = projects)




# ****************************************************************************************************************
# ****************************     edit task     ***************************************************************
# ****************************************************************************************************************


@app.route('/EditTask', methods=['GET', 'POST'])
@login_required
@leader_required
def EditTask():
  
  task_id = request.args.get('EE')
  



  from DataBase import Current_Task
  tasks = Current_Task(task_id) 
  
  from DataBase import user_member
  members = user_member()
 
  from DataBase import project_table
  projects = project_table()
  

  if request.method == 'POST':
        
        task_id_v = request.form['task_id']
        task_title = request.form['title']
        task_description = request.form['description']
        task_assigned_to_id = request.form['assigned_to']
        task_start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
        task_end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
        task_original_end_date= datetime.strptime(request.form['original_end_date'], '%Y-%m-%dT%H:%M')
        task_completed_at = request.form['completed_at']
        if task_completed_at:
            task_completed_at = datetime.strptime(request.form['completed_at'], '%Y-%m-%dT%H:%M')
        else:
            task_completed_at = None
        task_reson_for_delay = request.form['reason_for_delay']
        task_stuts = request.form['status']
        task_Dec = request.form ['Dec']  
        task_project = request.form['project']
        
        if task_project:
            task_project = request.form['project']
        else:
            task_project = None

        from DataBase import Edit_Task
        Edit_Task(task_id_v,task_title, task_description, task_assigned_to_id, task_start_date, task_end_date, task_original_end_date, task_completed_at, task_reson_for_delay,task_stuts,task_Dec,task_project)
  
        # Validate dates
        if task_end_date <= task_start_date:
            flash('End date must be after start date', 'danger')

        flash(f'Task "{task_title}" edited successfully!', 'success')
        return redirect(url_for('dashboard'))
  

  return render_template('edit_task.html', tasks=tasks ,members=members ,projects=projects)
# ****************************************************************************************************************


# ****************************************************************************************************************
# ****************************     delete task     ***************************************************************
# ****************************************************************************************************************


@app.route('/delete_task', methods = ['POST'])

@login_required
@leader_required

def delete_task():
 
  task_ID_01 = request.form.get('task_id')
  task_title = request.form.get('task_title')
  
  from DataBase import Delete_task
  Delete_task (task_ID_01)

  flash(f'Task "{task_title}" deleted successfully!', 'success')

  return redirect(url_for('dashboard'))

# ****************************************************************************************************************


# ****************************************************************************************************************
# ****************************     Add User     ******************************************************************
# ****************************************************************************************************************

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
@leader_required
def add_user():

 if request.method == 'POST':
     
        user_name = request.form['user_name']
        user_password = request.form['password']
        user_role = request.form['user_role']
        user_full_name = request.form['full_name']


        from DataBase import ADD_User
        ADD_User(user_name, user_password, user_role,user_full_name)

        flash(f'User "{user_full_name}" added successfully!', 'success')
        return redirect(url_for('Team_management'))

 return render_template('add_user.html')


# ****************************************************************************************************************
# ****************************     edit User     ******************************************************************
# ****************************************************************************************************************

@app.route('/EditUser', methods=['GET', 'POST'])
@login_required
@leader_required
def EditUser():
  
  user_id = request.args.get('EE')
  
  from DataBase import user_table
  users = user_table(user_id)

  if request.method == 'POST':
        
        user_id_v = request.form['user_id']
        user_name = request.form['user_name']
        user_password = request.form['password']
        user_role = request.form['user_role']
        user_full_name = request.form['full_name']

        from DataBase import Edit_User
        Edit_User(user_id_v,user_name, user_password, user_role,user_full_name)

        flash(f'User "{user_full_name}" edit successfully!', 'success')
        return redirect(url_for('Team_management'))

  return render_template('edit_user.html', users=users)


# ****************************************************************************************************************
# ****************************     delete User     ***************************************************************
# ****************************************************************************************************************


@app.route('/delete_user', methods = ['POST'])

@login_required
@leader_required

def delete_user():
 
  user_ID_01 = request.form.get('user_id')
  user_fullName = request.form.get('user_fullName')
  
  from DataBase import Delete_user
  Delete_user (user_ID_01)

  flash(f'User "{user_fullName}" deleted successfully!', 'success')

  return redirect(url_for('Team_management'))

# ****************************************************************************************************************



# ****************************************************************************************************************
# ****************************    Search data task filter by member    *******************************************
# ****************************************************************************************************************

@app.route('/Filter_Data_ByMember', methods=['GET', 'POST'])
@login_required
@leader_required
def Filter_Data_ByMember():

   Filter_by_member_v = request.args.get('TT')
#    now = datetime.utcnow()
   now = datetime.now().replace(microsecond=0)    
      
        # Get all tasks created by this leader
   from DataBase import Task__assigned_by_member
   Task_data = Task__assigned_by_member (Filter_by_member_v)

   from DataBase import user_member
   members = user_member()

   from DataBase import Overdue_Tasks
   Overdue_Tasks_V = Overdue_Tasks(current_user.id,now)

          
   return render_template('leader_dashboard.html', tasks=Task_data, members=members,now=now , Overdue_Tasks_V=Overdue_Tasks_V)
   
# ****************************************************************************************************************
# ****************************    Search data task     ***********************************************************
# ****************************************************************************************************************

@app.route('/Search_Data', methods=['GET', 'POST'])
@login_required
@leader_required
def Search_Fun():

   search_v = request.args.get('search_v')

   
   
#    now = datetime.utcnow()
   now = datetime.now().replace(microsecond=0)   
   if current_user.role == 'leader':
        
          from DataBase import Filter_task_assigned_by_id
          Filter_tasks_V = Filter_task_assigned_by_id(search_v,current_user.id)

          from DataBase import user_member
          members = user_member()

          from DataBase import Overdue_Tasks
          Overdue_Tasks_V = Overdue_Tasks(current_user.id,now)

          
          return render_template('leader_dashboard.html', tasks=Filter_tasks_V, members=members,now=now , Overdue_Tasks_V=Overdue_Tasks_V)
   else:
          from DataBase import Task_assigned_to_CurrentUser
          Task_data = Task_assigned_to_CurrentUser(current_user.id)

          return render_template('member_tasks.html', tasks=Task_data, now=now )
   
   
# ****************************************************************************************************************
# ****************************     Dec task update    ***************************************************************
# ****************************************************************************************************************


@app.route('/DecTask/<int:task_id>/<string:status>', methods=['GET', 'POST'])
@login_required
@leader_required
def DecTask(task_id, status):
  
#   task_id = request.args.get('EE')
  
 if status == 'completed' :
     from DataBase import Take_Dec_Task
     Take_Dec_Task(task_id)
     return redirect(url_for('dashboard'))
 
 else :
        
      flash(f'Task must be completed !', 'danger')
      
      return redirect(url_for('dashboard'))
    


# ****************************************************************************************************************
# ****************************     Dec task filter    ************************************************************
# ****************************************************************************************************************


@app.route('/Filter_Ok_Task', methods=['GET', 'POST'])
@login_required
@leader_required
def Filter_Ok_Task():


   now = datetime.now().replace(microsecond=0)
      
   if current_user.role == 'leader':
        # Get all tasks created by this leader
          from DataBase import Task__assigned_by_CurrentUser_Filter_Ok
          Task_data = Task__assigned_by_CurrentUser_Filter_Ok (current_user.id)

          from DataBase import user_member
          members = user_member()

          from DataBase import Overdue_Tasks_Filter_Ok
          Overdue_Tasks_V = Overdue_Tasks_Filter_Ok(current_user.id)


          return render_template('leader_dashboard.html', tasks=Task_data, members=members,now=now , Overdue_Tasks_V=Overdue_Tasks_V)
         
   return redirect(url_for('dashboard'))


# ****************************************************************************************************************
# ****************************    Team_Management     ************************************************************
# ****************************************************************************************************************


@app.route('/Team_Management', methods=['GET', 'POST'])
@login_required
@leader_required
def Team_management():
    #   return render_template('Test.html')

      from DataBase import all_user
      users = all_user()

      return render_template('Team.html', users=users)



# ****************************************************************************************************************
# ****************************    update              ************************************************************
# ****************************************************************************************************************


@app.route('/task/<int:task_id>/update', methods=['POST'])
@login_required
@member_required

def update_task(task_id):

    from DataBase import Current_Task
    task = Current_Task(task_id)
    
    # Verify this task belongs to the current member
    if task['assigned_to_id'] != current_user.id:
        flash('Unauthorized access', 'danger')
        return redirect(url_for('dashboard'))
    
    # Verify task isn't already completed
    if task['status'] == 'completed':
        flash('This task is already completed', 'warning')
        return redirect(url_for('dashboard'))
    
    action = request.form['action']


    if action == 'complete':
        
        status = 'completed'
        completed_at = datetime.now().replace(microsecond=0)
        requires_leader_attention = False
        
        from DataBase import update_Task_status
        update_Task_status(task_id, status, completed_at, requires_leader_attention)
        flash('Task marked as completed!', 'success') 

    elif action == 'delay':
        reason = request.form['reason']
        new_deadline_str = request.form['new_deadline']
        new_deadline = datetime.strptime(new_deadline_str, '%Y-%m-%dT%H:%M')
        
        # Validate new deadline
        if new_deadline <= datetime.now().replace(microsecond=0):
            flash('New deadline must be in the future', 'danger')
            return redirect(url_for('dashboard'))
        
        status = 'delayed'
        reason_for_delay = reason
        current_deadline = new_deadline
        requires_leader_attention = True  # Flag for leader notification

        from DataBase import update_Task_status_delay
        requires_leader_attention = False
        update_Task_status_delay(task_id,status,reason_for_delay, current_deadline, requires_leader_attention) 

        flash('Task deadline updated successfully!', 'success')
    
    
    return redirect(url_for('dashboard'))

# ****************************************************************************************************************
# ****************************    resolve              ***********************************************************
# ****************************************************************************************************************



@app.route('/task/<int:task_id>/resolve', methods=['POST'])
@login_required
@leader_required
def resolve_task(task_id):

    from DataBase import Current_Task
    task = Current_Task(task_id)
   
    # task = Task.query.get_or_404(task_id)
    
    # Verify this task was created by the current leader
    if task['assigned_by_id'] != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized access'}), 403
    
    action = request.form['action']
    
    if action == 'complete':
        status = 'completed'
        completed_at = datetime.now().replace(microsecond=0)
        
        requires_leader_attention = False
        
        from DataBase import update_Task_status
        update_Task_status(task_id, status, completed_at, requires_leader_attention)
         
    elif action == 'postpone':
        new_deadline_str = request.form['new_deadline']
        new_deadline = datetime.strptime(new_deadline_str, '%Y-%m-%dT%H:%M')
        
        if new_deadline <= datetime.now().replace(microsecond=0):
            return jsonify({'success': False, 'message': 'New deadline must be in the future'}), 400
        
        from DataBase import update_Task_status_postpone
        requires_leader_attention = False
        update_Task_status_postpone(task_id, new_deadline, requires_leader_attention) 

        
    
   
    return jsonify({'success': True})





# ****************************************************************************************************************
# ****************************           Project   ***************************************************************
# ****************************************************************************************************************


@app.route('/Projects', methods=['GET', 'POST'])
@login_required
@leader_required
def Projects():
    #   return render_template('Test.html')

      from DataBase import project_table
      Projects = project_table()
    

      return render_template('Projects.html', Projects=Projects)


# ****************************************************************************************************************
# ****************************     edit Project     **************************************************************
# ****************************************************************************************************************

@app.route('/EditProject', methods=['GET', 'POST'])
@login_required
@leader_required
def EditProject():
  
  project_id = request.args.get('EE')
  
  from DataBase import project_table_id
  Projects = project_table_id(project_id)

  if request.method == 'POST':
        
        project_id_v = request.form['project_id']
        project_name = request.form['project_name']
        project_group = request.form['project_group']

        from DataBase import Edit_Project
        Edit_Project(project_id_v, project_name, project_group)

        flash(f'Project "{project_name}" edit successfully!', 'success')
        return redirect(url_for('Projects'))

  return render_template('edit_project.html', projects=Projects)



# ****************************************************************************************************************


# ****************************************************************************************************************
# ****************************     delete Project     ***************************************************************
# ****************************************************************************************************************


@app.route('/delete_project', methods = ['POST'])

@login_required
@leader_required

def delete_project():
 
  project_ID_01 = request.form.get('project_id')
  project_name = request.form.get('project_name')
  
  from DataBase import Delete_Project
  Delete_Project (project_ID_01)

  flash(f'Project "{project_name}" deleted successfully!', 'success')

  return redirect(url_for('Projects'))

# ****************************************************************************************************************


# ****************************************************************************************************************
# ****************************     Add Project     ******************************************************************
# ****************************************************************************************************************

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
@leader_required
def add_project():

 if request.method == 'POST':
     
        project_name = request.form['project_name']
        project_group = request.form['project_group']


        from DataBase import Add_Project
        Add_Project(project_name, project_group)

        flash(f'Project "{project_name}" added successfully!', 'success')
        return redirect(url_for('Projects'))

 return render_template('add_project.html')


# ****************************************************************************************************************
# ****************************    Search data project     ***********************************************************
# ****************************************************************************************************************

@app.route('/Search_Data_project', methods=['GET', 'POST'])
@login_required
@leader_required
def Search_Projects():

   search_v = request.args.get('search_v')

   from DataBase import Search_Project
   Projects = Search_Project(search_v)
  
   return render_template('Projects.html', Projects=Projects)
   




# ****************************************************************************************************************
# ****************************   notification system massege    **************************************************
# ****************************************************************************************************************



# ****************************************************************************************************************
# ****************************************************************************************************************

@app.route('/api/overdue-tasks')
@login_required
# @leader_required
def get_overdue_tasks():

    now = datetime.now().replace(microsecond=0)


    success_count = 0
    error_details = []


    if current_user.role == 'leader' :
         from DataBase import Overdue_Tasks
         overdue_tasks = Overdue_Tasks(current_user.id, now)
         

    elif current_user.role == 'member' :
         from DataBase import Overdue_Tasks_Member
         overdue_tasks = Overdue_Tasks_Member(current_user.id, now)

    tasks_data = [{
    'id': task['task_id'],  # ← Use brackets instead of dot notation
    'title': task['title'],
    'assigned_to': task['assigned_to_fullname'],
    'current_deadline': task['current_deadline'].isoformat(),
    'original_deadline': task['original_end_date'].isoformat(),
    'reason_for_delay': task['reason_for_delay'],
    'description': task['description'],
    'projectname': task['project_name'],
    'status': task['status']
     } for task in overdue_tasks]
   

   
# ******************* sent telegram massege *******************

    for task in tasks_data:
      
      text = (
             f"اسم المشروع : {task['projectname']}\n"
             f"العنوان : {task['title']}\n"
             f"النشاط : {task['description']}\n"
             f"المسؤول : {task['assigned_to']}\n"
             f" تاريخ نهو النشاط : {task['current_deadline']}")

      url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'  # optional
        }
      response = requests.post(url, json=payload)

      if response.status_code == 200:
            success_count += 1
      else:
            error_details.append(response.text)

    
#  *********************************************************************

    return jsonify(tasks_data)

# ****************************************************************************************************************
# ***********************************  check-notifications  ******************************************************

@app.route('/api/check-notifications')
@login_required
def check_notifications():
    ## """Check if current user has notifications waiting"""

    if current_user.role == 'leader' :
         task_check_notifications_V1 = False
         from DataBase import task_check_notifications
         task_check_notifications_V = task_check_notifications (current_user.id)
         
         if task_check_notifications_V:
            task_check_notifications_V1 = True
    
            return jsonify({'has_notifications': task_check_notifications_V1})
         
    if current_user.role == 'member' :
         task_check_notifications_member_V1 = False
         from DataBase import task_check_notifications_member
         task_check_notifications_member_V = task_check_notifications_member (current_user.id)
         
         if task_check_notifications_member_V:
            task_check_notifications_member_V1 = True
    
            return jsonify({'has_notifications': task_check_notifications_member_V1})
         


    return jsonify({'has_notifications': False})


# ****************************************************************************************************************
# ****************************   telegram massege    ***********************************************************
# ****************************************************************************************************************



@app.route('/api/send-telegram', methods=['GET'])
@login_required
@leader_required

def send_telegram():

    now = datetime.now().replace(microsecond=0)

    success_count = 0
    error_details = []


    if current_user.role == 'leader' :
         from DataBase import Overdue_Tasks
         overdue_tasks = Overdue_Tasks(current_user.id, now)
         

    tasks_data = [{
    'id': task['task_id'],  # ← Use brackets instead of dot notation
    'title': task['title'],
    'assigned_to': task['assigned_to_fullname'],
    'current_deadline': task['current_deadline'].strftime('%b %d, %Y'),
    'original_deadline': task['original_end_date'].isoformat(),
    'reason_for_delay': task['reason_for_delay'],
    'description': task['description'],
    'projectname': task['project_name'],
    'status': task['status']
     } for task in overdue_tasks]
   

    # text=jsonify(tasks_data)
    for task in tasks_data:
      
      text = (
             f"اسم المشروع : {task['projectname']}\n"
             f"العنوان : {task['title']}\n"
             f"النشاط : {task['description']}\n"
             f"المسؤول : {task['assigned_to']}\n"
             f" تاريخ نهو النشاط : {task['current_deadline']}")

      url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'  # optional
        }
      response = requests.post(url, json=payload)

      if response.status_code == 200:
            success_count += 1
      else:
            error_details.append(response.text)
   
    
    # if response.status_code == 200:

    #     return jsonify({'status': 'sent'}), 200
    # else:
    #     return jsonify({'status': 'error', 'details': response.text}), 500

    # if response.status_code == 200:

    #      flash('Telegram massege was successfully send !', 'success')
    #      return  redirect(url_for('dashboard'))
    # else: 
    #      error_detail = {'details': response.text}
    #      flash(f'Telegram massege error : {error_detail} !', 'denger')
    #      return  redirect(url_for('dashboard'))
    
    
    if success_count == len(tasks_data):
        return jsonify({'status': 'success', 'message': 'Telegram messages sent!'}), 200
    else:
        return jsonify({'status': 'error', 'details': error_details}), 500
