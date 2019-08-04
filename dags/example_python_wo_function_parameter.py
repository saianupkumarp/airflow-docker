#-------------------------------------- Chnage Log -------------------------------------------
__author__ = "Anup Kumar"
__copyright__ = "Copyright 2019"
__credits__ = ["Anup Kumar"]
__license__ = "Prop"
__version__ = "1.0.0"
__maintainer__ = "Anup Kumar"
__email__ = ""
__status__ = "Production"
#------------------------------------ Change Details ------------------------------------------
# 07/30/2019 - Anup Kumar - Example of simple dag with python operator without function paramters
#----------------------------------------------------------------------------------------------

import airflow
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

def hello_world():
    print ("Hello world Airflow")
    return

default_args = {
    'owner': 'Anup Kumar',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'email': [Variable.get("alert_email_to")], # This is a custom variable decreased in the airflow, change it as needed or add a variable in the airflow with key named "alert_email_to" and value of your choice 
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=10)
}

dag = DAG(
    'Example_dag_python_without_function_parameter',
    default_args=default_args,
    description='Example of simple dag with python operator without function paramters',
    schedule_interval='10 10 * * *',
)

start_task = DummyOperator(task_id="Start", dag=main_dag)
end_task = DummyOperator(task_id="End", dag=main_dag)

hello_world_task = PythonOperator(
                            task_id="Hello", 
                            python_callable=hello_world,
                            dag=dag
                        )

start_task >> hello_world_task >> end_task