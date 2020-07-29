from flask import Flask, request
import logging
import json
from authenticated import Auth
from db import Database

app = Flask(__name__)
logging.basicConfig(filename='CIE.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
logger.info('CIE app started.')
db = Database(logger)

# Endpoint returns employee's row from employee table, limit top 10 for super user
# Param required is employee authentication token
@app.route('/employees', methods=['GET'])
def get_employees():
    token = request.args.get('token')
    auth_enum = do_authentication(token)
    if auth_enum:
        logging.info("Employee list GET Request")
        results = get_employees(auth_enum)
        for option in results:
            print(option)
        return "Top 10 Employees"
    else:
        return "Connection Refused"

# Endpoint returns employee information as well as previous salary history
# Param required is employee number and employee authentication token
@app.route('/employees/<enum>', methods=['GET'])
def emp_history(enum):
    logging.info("Employee history GET Request for employee number {}".format(enum))
    token = request.args.get('token')
    if not token:
        logging.warning("Request denied, no authentication token provided.")
        return "Connection Refused"
    try:
        enum = int(enum)
    except Exception as e:
        logging.warning("Exception {}. Invalid employee number provided: {}".format(e, enum))
        return "Connection Refused"
    try:
        authenticated, auth_enum = do_authentication(token, enum)
        if authenticated:
            return emp_history_helper(auth_enum)
        else:
            return "Connection Refused"
    except Exception as e:
        logging.critical("Unexpected exception occurred {}".format(e))
        return "Unknown error. Connection Refused."

# Helper method for elegance, checks enum is valid and returns employee information and history for authenticated user
def emp_history_helper(enum):
    try:
        enum = int(enum)
    except Exception as e:
        logging.warning("Invalid employee number provided to helper method: {}.  Exception: {}".format(enum, e))
        raise e
    results = get_salary_history(enum)
    return results

# Returns employee information and history for a given employee
def get_salary_history(emp_no):
    logging.info('Query salary history for employee number {}'.format(emp_no))
    cursor, connection = db.connect_db()
    sql_employee = "SELECT `employees`.emp_no, first_name, last_name, dept_name, salary, `salaries`.from_date, `salaries`.to_date " \
                   "from employees, dept_emp, departments, salaries WHERE" \
                   "`employees`.emp_no = `dept_emp`.emp_no AND " \
                   "`dept_emp`.dept_no = `departments`.dept_no AND " \
                   "`employees`.emp_no = `salaries`.emp_no AND " \
                   " `employees`.emp_no = {}".format(emp_no)
    cursor.execute(sql_employee)
    results = list(cursor)
    db.close_db(cursor, connection)
    return results

# Returns employee information for a given employee, limit 10 for authenticated super user
def get_employees(enum):
    if enum == "*":
        pass
    else:
        try:
            enum = int(enum)
        except Exception as e:
            logging.warning("Exception {}. Invalid employee number provided: {}".format(e, enum))
            return "Connection Refused"
    cursor, connection = db.connect_db()
    if enum == "*":
        logging.info("Query employee list by super user, limit 10")
        sql = "SELECT * from employees LIMIT 10"
    else:
        logging.info("Query employee information of employee by employee {}".format(enum))
        sql = "SELECT * from employees where `employees`.emp_no={}".format(enum)
    cursor.execute(sql)
    results = list(cursor)
    db.close_db(cursor, connection)
    return results

# Compares token to list of authenticated tokens and returns the employee number or * for super user
def do_authentication(token, enum=""):
    if enum:
        try:
            auth_enum = Auth.tokens[token]
            if auth_enum == "*":
                logging.info("Authenticated request from super user.")
                return True, enum
            else:
                if enum != int(auth_enum):
                    logging.warning("Authentication failed for request")
                    return False, None
                else:
                    logging.info("Authentication succeeded for request")
                    return True, enum
        except Exception as e:
            logging.warning("Authentication failed unknown token request: {}".format(e))
            return False, None
    else:
        try:
            auth_enum = Auth.tokens[token]
            if auth_enum == "*":
                logging.info("Authenticated request from super user.")
                return "*"
            else:
                logging.info("Authentication succeeded for request")
                return auth_enum
        except Exception as e:
            logging.warning("Authentication failed unknown token request: {}".format(e))
            return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')