# importing the libraries
import csv
import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':

    # URL that you to scrap
    url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'lxml')

    # Print the parsed data of HTML
    # print(soup.prettify())
    # Print data of specific HTML tags
    # print(soup.title)
    # print(soup.title.text)

    gdp_table = soup.find_all("table")

    # Get all the headings of lists
    heading = []
    for td in gdp_table[2].tbody.tr.find_all("td"):
        header = td.text.replace("\n", '').strip()
        heading.append(header)

    data = {}

    gdp_table_data = gdp_table[2].find_all("table")

    for i, heading in zip(range(0, len(gdp_table_data)), heading):

        tr_header = []
        for th in gdp_table_data[i].tbody.find_all("th"):
            tr_header.append(th.text.replace('\n', ''))

        table_data = []
        for tr in gdp_table_data[i].tbody.find_all("tr"):
            tr_rows = {}
            for td, th in zip(tr.find_all("td"),tr_header):
                tr_rows[th] = td.text.replace('\n', '').strip()
            table_data.append(tr_rows)

        # Put the data for the table with associated heading
        data[heading] = table_data

    # Export the data CSV
    for topic, table in data.items():
        # Creating CSB file for each table
        with open(f'{topic}.csv', 'w') as output_file:
            # Header for each table
            header = ["Country/Territory", "GDP(US$ M)"]
            # Writing headers to each table
            writer = csv.DictWriter(output_file, header)
            writer.writeheader()
            # Writing data CSV file
            for row in table:
                if row:
                    writer.writerow(row)

    print('Data exported to CSV files')




