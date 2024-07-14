# UCSD-SET-Data-Scraper
After the discontinuation of UCSD CAPEs in Spring 2023, course evaluations have transitioned to UCSD SET. This project aims to scrape data from the new UCSD SET webpage, compiling course evaluations and reports from Fall 2023 onward and exporting them as a CSV file.

The scraper utilizes Selenium WebDriver to automate the login process and data retrieval from the UCSD SET website. Since UCSD SET is a campus service available only to UCSD students, a valid TritonLink account is required to use this scraper along with DUO Mobile authentication.

To run the web scraper, you'll need Python, Google Chrome browser, and the following Python libraries:

- selenium
- webdriver_manager
- beautifulsoup4
- pandas

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
**Step 4:** Enter your TritonLink username and password
