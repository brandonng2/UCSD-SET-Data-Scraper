# UCSD-SET-Data-Scraper
After the discontinuation of [UCSD CAPEs](https://cape.ucsd.edu/) in Spring 2023, course evaluations have transitioned to [UCSD SET](https://set.ucsd.edu/). This project aims to scrape the data from the UCSD SET webpage, compiling course evaluations and reports from Fall 2023 and onwards and exporting them as a CSV file.

This scraper utilizes Selenium WebDriver to automate the login process and data retrieval from the UCSD SET website. As UCSD SET is a campus service available only to UCSD students, a valid TritonLink account is required. Additionally, DUO Mobile authentication is needed to complete the login process.

Other requirements for running the web scraper include Python, Google Chrome browser, and the following Python libraries:

- selenium
- webdriver_manager
- beautifulsoup4
- pandas

Disclaimer: This project is intended for individuals working on data science or personal app projects who require well-formatted data regarding UCSD course evaluation data. By providing a single dataset containing all necessary course evaluation data, this script allows project creators to focus on data cleaning and analysis instead of the data scraping process.

# Installation & Usage
  
**Step 1:** Clone the repository 
```
git clone <SSH Key or web URL>
```
**Step 2:** Install the necessary dependencies by navigating to the project directory and running the following command:
```
pip install -r requirements.txt
```
or 
```
pip install selenium webdriver_manager beautifulsoup4 pandas
```
**Step 3:** Run the script by excuting the following line:
```
python3 scraper.py
```
**Step 4:** Enter your TritonLink username and password, and complete the DUO Mobile authentication.

# Output
The script generates a CSV file named sets_data.csv containing the scraped SET data with the following columns:

- Instructor: The name of the instructor teaching the course.
- Course: The name of the course.
- Term: The quarter in which the course was offered.
- Enrolled/Response Rate: The number of students enrolled and the response rate in percentages.
- Avg Grade Received: The average GPA and letter grade received by students.
- Avg Hours Worked: The average number of hours students worked on the course.
- Student Learning: Evaluation of student learning experiences out of 5.
- Course Structure: Assessment of how the course is structured out of 5.
- Class Environment: Evaluation of the class environment out of 5. 
