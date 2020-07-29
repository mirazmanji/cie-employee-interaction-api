# Customer Interaction Ecosystem

Application programming interface that allows users to access employee information.

 - Get basic employee information
 - Get employee information plus salary history
 
 ### TODOS
 
 - Convert list into JSON object to complete request response
 - Unit test cases of authenticated output
 - Refactor authentication into seperate module
 - Create an html template to post json response to frontend
 
 # USAGE
 
 - Run app.py and navigate to localhost (0.0.0.0) port 5000.
 - /employee GET endpoint for employee data
 - /employee/employeeNumber for employee data and salary info
 - Connect to database from docker: MySQL Employee database 
   repository: https://hub.docker.com/r/genschsa/mysql-employees/

 # NOTE
 
 - Endpoint returns string confirmation and not JSON object as per TODO.