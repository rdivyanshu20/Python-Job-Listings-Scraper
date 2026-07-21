import requests
from bs4 import BeautifulSoup
import csv

def scrape_fake_jobs():
    # 1. Fetch the webpage
    url = "https://realpython.github.io/fake-jobs/"
    print(f"Fetching data from {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return

    # 2. Parse the HTML
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 3. Find all job containers
    # The site uses the Bulma CSS framework, where each job is wrapped in a "card" class
    job_cards = soup.find_all("div", class_="card")
    
    jobs_data = []
    
    # 4. Extract data from each card
    for card in job_cards:
        # Safely extract title
        title_element = card.find("h2", class_="title")
        title = title_element.text.strip() if title_element else "N/A"
        
        # Safely extract company
        company_element = card.find("h3", class_="company")
        company = company_element.text.strip() if company_element else "N/A"
        
        # Safely extract location
        location_element = card.find("p", class_="location")
        location = location_element.text.strip() if location_element else "N/A"
        
        # Safely extract job detail URL
        # The card footer contains two links: "Learn" and "Apply". We want the "Apply" link.
        detail_url = "N/A"
        links = card.find_all("a", class_="card-footer-item")
        for link in links:
            if link.text.strip() == "Apply":
                detail_url = link.get("href")
                break
                
        # Append as a row for our CSV
        jobs_data.append([title, company, location, detail_url])
        
    # 5. Save the results to a CSV file
    csv_filename = "fake_python_jobs.csv"
    
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(["Job Title", "Company Name", "Location", "Job Detail URL"])
            
            # Write the job data
            writer.writerows(jobs_data)
            
        print(f"Success! {len(jobs_data)} job postings have been saved to '{csv_filename}'.")
        
    except IOError as e:
        print(f"Error saving to CSV: {e}")

if __name__ == "__main__":
    scrape_fake_jobs()