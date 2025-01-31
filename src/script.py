import requests       # Imports the requests library to handle HTTP requests
import datetime       # Imports the datetime module to work with dates
import csv            # Imports the csv module to handle CSV file operations

# Define the date range dynamically
end_date = datetime.date.today()  # Get today's date dynamically
start_date = end_date - datetime.timedelta(days=30)  # Go back 30 days from today

# Your API key for authenticating with the Datafiniti API
API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkbWg2Z214eTk3bm9kb2U2ZGgwYWw2bXczaGV1MG53bSIsImlzcyI6ImRhdGFmaW5pdGkuY28ifQ.IhiLBQOyVcWLs-DkOSyYjlSrvYyWINxuKm6n25sq12DDSVlaxcTj8-dVPTWUaucVIF7OUeBQO2WU6NcqtS33vHq2-FVGi1_33fAw_scgarqRe6JL0KUNQHXfT8nWBF_7o7maRUEMiazKhAyi-p5reljhlmxJv-vzCi9Y3dyrw7T2cXlcu5E9vH-Ndnh7wLGeTIrdXCapn0kJ9SIMK35J8R_AMNBpboEvA6SiEVUDD4RqiCJ7Up6bLULMuMxIVQua5Cl_00IVme2GQUqGaTHjxT5LK0QWcOyB5G0QFcjWPfn-AcNYgT1f-KDdaqMalVDdWyboVriIyigeNieIrvGRFbMbUkzx2sNeQfckneodDQsuGpjczk2OOTm4_W5jQRQgjTH3FzeotPsNksUbB-t7hbbaPHkej29PxHG-NvCVR_Py0hCJIrrBQVhmeOwcloEksq-TH_N5zZE7ncIxGavJT2r-ScGNpRsnpMZU69RMjMxRmkAzkGrudjpfLWAioPzkhAPmhz5_WJdZDms8IurpJe-C9PGM-31u-2CrwQeuSBvyM5IPeY5OrikHU9xglrrf1sy0fcNCWMMuSCtxrImDEhPfReNE9793AQs89O0UlBzOlAHcftheEUfzjB51VZva6msm2rKh63JSmLLQtHov2myG-3a-3JwRUJLvClXWk_g"

# Open the CSV file 'nho_transactions.csv' in write mode
# 'newline=""' ensures that no extra blank lines are added on some platforms
with open('nho_transactions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)  # Create a CSV writer object
    writer.writerow(['Date', 'Number of NHO Transactions'])  # Write the header row to the CSV file

    # Initialize the current_date variable to start_date
    current_date = start_date
    
    # Loop through each day from start_date to end_date
    while current_date <= end_date:
        # Format the current_date as a string in 'YYYY-MM-DD' format for the API query
        query_date = current_date.strftime('%Y-%m-%d')
        print(f"Fetching data for {query_date}...")  # Inform the user which date is being processed

        # Construct the query payload for the API request
        # This query filters transactions based on:
        # - saleDate equal to query_date
        # - ownerType is 'Individual'
        # - buyerFirstName is present (non-empty)
        # - type is 'NHO' (Non-Household Owner)
        query = {
            "query": f'{{transactions.saleDate:[{query_date} TO {query_date}] AND transactions.ownerType:Individual AND transactions.buyerFirstName:* AND transactions.type:NHO}}'
        }

        # Define the HTTP headers for the API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",  # Bearer token for authentication
            "Content-Type": "application/json"       # Specify that the request body is JSON
        }

        # Send a POST request to the Datafiniti API with the query and headers
        response = requests.post(
            'https://api.datafiniti.co/v4/properties/search',  # API endpoint
            json=query,                                        # JSON payload containing the query
            headers=headers                                    # HTTP headers
        )

        # Check if the API request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON response from the API
            data = response.json()
            # Extract the number of records found; default to 0 if 'num_found' key is missing
            num_found = data.get('num_found', 0)
            print(f"Number of records found for {query_date}: {num_found}")  # Output the result
        else:
            # If the request was not successful, print an error message with status code and response text
            print(f"Error for {query_date}: {response.status_code} - {response.text}")
            num_found = 0  # Set number of records found to 0 in case of error

        # Write the date and number of transactions to the CSV file
        writer.writerow([query_date, num_found])

        # Move to the next day by adding one day to current_date
        current_date += datetime.timedelta(days=1)

# After processing all dates, inform the user that the CSV file has been generated
print("Spreadsheet generated successfully. Check 'nho_transactions.csv'.")
