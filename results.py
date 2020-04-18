from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup
import pdfkit

start = 1601001
end = 1601270

html = '''<!DOCTYPE html>
<html>
<head>
<style>

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

td, th {
  border: 1px solid #dddddd;
  text-align: center;
  padding: 8px;
}

</style>
</head>
<body>

<table>
  <tr>
    <th>Roll Number</th>
    <th>Name</th>
    <th>GPA</th>
    <th>CGPA</th>
  </tr>'''

endhtml = '''</table>

</body>
</html>
'''

firefox_path = r'C:\Users\MohanRamM\selenium\drivers\geckodriver.exe'

firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

options = FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(executable_path=firefox_path, firefox_profile=firefox_profile, options=options)

driver.get("http://coe1.srec.ac.in")

print("{:^10s} | {:^30s} | {:^5s} | {:^5s} | ".format("RollNo","Name","GPA","CGPA"))

for rollnumber in range(start, end+1):
    rollnumber = str(rollnumber)
    driver.find_element_by_name("regno").send_keys(rollnumber)
    driver.find_element_by_name("Enter").click()

    htmlsource = driver.page_source
    soup = BeautifulSoup(htmlsource, features="html.parser")

    tables = soup.findChildren("table")

    nametable = tables[1]
    row = nametable.findChildren('tr')[1]
    name = row.findChildren('td')[1].string

    if name is not None:
        gpatable = tables[3]
        gparow = gpatable.findChildren('tr')[1]
        gpa = gparow.findChildren('td')[0].string
        if gpa.strip()=="":
            gpa = "NA"
        cgpa = gparow.findChildren('td')[1].string
        if cgpa.strip()=="":
            cgpa = "NA"
        print("{:^10s} | {:<30s} | {:^5s} | {:^5s} | ".format(rollnumber, name, gpa, cgpa))
        html_element = '''<tr>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
            <td>{}</td>
        </tr>
        '''.format(rollnumber, name, gpa, cgpa)
        html += html_element
    
    driver.find_element_by_name("Enter").click()

html += endhtml
pdfkit.from_string(html, 'results.pdf', options={'quiet': ''})

driver.quit()