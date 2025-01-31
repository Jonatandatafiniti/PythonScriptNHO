import requests
import datetime
import csv

# Define the date range dynamically
end_date = datetime.date.today()  # Get today's date dynamically
start_date = end_date - datetime.timedelta(days=30)  # Go back 30 days from today

# Your API key for authenticating with the Datafiniti API (Replace with your actual API key)
API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkbWg2Z214eTk3bm9kb2U2ZGgwYWw2bXczaGV1MG53bSIsImlzcyI6ImRhdGFmaW5pdGkuY28ifQ.IhiLBQOyVcWLs-DkOSyYjlSrvYyWINxuKm6n25sq12DDSVlaxcTj8-dVPTWUaucVIF7OUeBQO2WU6NcqtS33vHq2-FVGi1_33fAw_scgarqRe6JL0KUNQHXfT8nWBF_7o7maRUEMiazKhAyi-p5reljhlmxJv-vzCi9Y3dyrw7T2cXlcu5E9vH-Ndnh7wLGeTIrdXCapn0kJ9SIMK35J8R_AMNBpboEvA6SiEVUDD4RqiCJ7Up6bLULMuMxIVQua5Cl_00IVme2GQUqGaTHjxT5LK0QWcOyB5G0QFcjWPfn-AcNYgT1f-KDdaqMalVDdWyboVriIyigeNieIrvGRFbMbUkzx2sNeQfckneodDQsuGpjczk2OOTm4_W5jQRQgjTH3FzeotPsNksUbB-t7hbbaPHkej29PxHG-NvCVR_Py0hCJIrrBQVhmeOwcloEksq-TH_N5zZE7ncIxGavJT2r-ScGNpRsnpMZU69RMjMxRmkAzkGrudjpfLWAioPzkhAPmhz5_WJdZDms8IurpJe-C9PGM-31u-2CrwQeuSBvyM5IPeY5OrikHU9xglrrf1sy0fcNCWMMuSCtxrImDEhPfReNE9793AQs89O0UlBzOlAHcftheEUfzjB51VZva6msm2rKh63JSmLLQtHov2myG-3a-3JwRUJLvClXWk_g"

# Initialize total transactions count
total_transactions = 0  

# Open the CSV file 'nho_transactions.csv' in write mode
with open('nho_transactions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)  # Create a CSV writer object
    writer.writerow(['Date', 'Number of NHO Transactions'])  # Write the header row to the CSV file

    # Initialize the current_date variable to start_date
    current_date = start_date

    # Loop through each day from start_date to end_date
    while current_date <= end_date:
        query_date = current_date.strftime('%Y-%m-%d')
        print(f"Fetching data for {query_date}...")  # Inform the user which date is being processed

        query = {
            "query": f'{{transactions.saleDate:[{query_date} TO {query_date}] AND transactions.ownerType:Individual AND transactions.buyerFirstName:* AND transactions.type:NHO}}'
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            'https://api.datafiniti.co/v4/properties/search',
            json=query,
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            num_found = data.get('num_found', 0)
            print(f"Number of records found for {query_date}: {num_found}")
        else:
            print(f"Error for {query_date}: {response.status_code} - {response.text}")
            num_found = 0  

        # Write the date and number of transactions to the CSV file
        writer.writerow([query_date, num_found])

        # Add to total transactions count
        total_transactions += num_found  

        # Move to the next day
        current_date += datetime.timedelta(days=1)

    # Write a well-formatted summary row at the end of the file
    writer.writerow(["==================", "============"])
    writer.writerow(["TOTAL TRANSACTIONS", total_transactions])
    writer.writerow(["==================", "============"])

# After processing all dates, inform the user that the CSV file has been generated
print("\n" + "=" * 50)  # Add separator line
print(f"Spreadsheet generated successfully. Check 'nho_transactions.csv'.")
print("=" * 50)
print("\n📊 FINAL SUMMARY 📊")
print("=" * 50)
print(f"✅ TOTAL NHO TRANSACTIONS: {total_transactions} ✅")
print("=" * 50)
