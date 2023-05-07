import requests
import csv
import sys
import re 

# checking command line arguments
if len(sys.argv) != 4:
    print("wrong number of arguments")
    sys.exit()
username = sys.argv[1]      #in arg 1 we put the LAU username
password = sys.argv[2]      #in arg 2 we put the password
department = sys.argv[3]    #Computer Sciences and Mathematiques department 

# log in to website
login_url = "https://myportal.lau.edu.lb/"  #login page
session = requests.Session() #Create a new object that allows us to maintain information about our session with the website across multiple requests.
#creating a dictionary
login_data = {"username": username, "password": password}
session.post(login_url, data=login_data)        #validate password and username 

#retrieve the web page that contains course information for the department and store the resulting HTML code in the page variable.
course_url = "https://soas.lau.edu.lb/academics/departments/computer-science-maths/"
page = session.get(course_url)      #we can re-use it later to extract info

# parse course information using regex
course_data = []    #empty list to store info for each course 
#finding the requirements from the web page: time, instructor, seats
for match in re.finditer(r'<tr>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>', page.text, re.DOTALL):
    time = match.group(1).strip()
    instructor = match.group(2).strip()
    seats = match.group(3).strip()
    course_data.append((time, instructor, seats))

# write data to CSV file
with open("course_offerings.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Time", "Instructor Name", "Remaining Seats"])
    for data in course_data:
        writer.writerow(data)
