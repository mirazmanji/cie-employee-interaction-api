# Customer Interaction Ecosystem

Application programming interface that allows users to access employee information.

 - Get basic employee information
 - Get employee information plus salary history
 
 ### TODOS
 
 - Unit test cases of authenticated output
 - Refactor authentication into seperate module
 - Create an html template to post json response to frontend
 
 ### USAGE
 
 - pip install --upgrade -r requirements.txt
 - Run app.py and navigate to localhost (0.0.0.0) port 5000.
 - /employee GET endpoint for employee data
 - /employee/employeeNumber for employee data and salary info
 - add ?token= argument to url for authenticated get request
 - Connect to database from docker: MySQL Employee database 
   repository: https://hub.docker.com/r/genschsa/mysql-employees/

 ### NOTE
 
 - Endpoint returns JSON with employee ID as key, and SQL list result as value.