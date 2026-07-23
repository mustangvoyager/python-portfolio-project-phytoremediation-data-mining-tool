import sys, requests
from datetime import datetime
from pathlib import Path
import lib
import time

# Pull in user selection for discrete search or search based on file/list
selection = "A"
while selection.lower() not in ["m", "s"]:
#    print(selection)
    selection = input("Search for single (s/S) or multiple species (m/M): ")

# Prompt user for species name iff single-s selected
if selection.lower() == "s":
    spec_name = input("Enter a species name directly (Do not enclose in quotes.): ")

# Prompt user for specific search criteria. Persist if value is out of bounds. 
print("Choose a search criteria - that which wish to be ANDed with each species...")
print("----------------------------------------")
print("1: phytoremediation")
print("2: rhizodegradation OR phytoextraction OR phytostabilization")
print("3: hydrocarbon OR PAH OR petroleum OR metal OR contaminant")
print("3a: hydrocarbon OR PAH OR petroleum OR metal OR contaminant OR pfas")
print("4: root exudate OR rhizosphere OR degradation")
print("5: pfas OR perfluoro* OR polyfluoro*")
print("6: fluorocarbons[Mesh] OR pfas[tiab] OR perfluoro*[tiab] OR polyfluoro*[tiab]")
print("----------------------------------------")
search_crit = input("Enter an integer, or \'3a\', in order to choose a search criteria: ")
while search_crit not in ["1", "2", "3", "4", "3a", "5", "6"]:
    search_crit = input("Enter a legitamate choice option - 1, 2, 3, 3a, 4, 5 or 6: ")
if search_crit == "3a":
    search_crit = "30"
search_crit = int(search_crit)

# If multiple species was selected - m - then create a python list 
if selection.lower() == "m":
    file_path = Path("species_list.txt")
    with open(file_path, "r") as file:
        species_list = [line.strip() for line in file if line.strip()]
#    print(species_list)
    print("Number of Returns by Species:  (these figures also appearing in your output report)")
    
    # Prepare report. Overwrite existing text file if necessary.
    now = datetime.now()
    # Format as YYYY-MM-DD HH:MM:SS
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Insert dummy spec_name in order to get usable search_crit_txt 
    spec_name = "spec_name"
    term, search_crit_txt = lib.assemble_term(spec_name, search_crit)
    output_file_name = "evidenceCollection_2/abstracts.txt"
    file_path = Path(output_file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w") as file:
        file.write("--- Abstracts for the species listed below, ---")
        file.write("\n--- based on the following search criteria: ---")

        file.write("\n*species name* ")
        file.write(search_crit_txt)
        file.write("  <-- Search ")
        if search_crit == 30:
            file.write("3a")
        else:
            file.write(str(search_crit))
        file.write(" specified by user.")

        file.write("\nTimestamp: ")
        file.write(timestamp)
        file.write("\n\n")
        file.write("        - - - - - - - - - - - - - - - - - - - - - - \
- - - - - - - - - - - - - - - - - - - - - - \n\n\n")

# NCBI Search:
# Defining the correct NCBI ESearch endpoint. This is the 1st of the 
# four parts for conducting an NCBI search.
search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

# For the 4th part of the NCBI search below.
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# If single species query - s - then execute search and prepare report. 
if selection.lower() == "s":
    term, search_crit_txt = lib.assemble_term(spec_name, search_crit)
    if search_crit == 30:
        search_crit = "3a"

    # Create a parameters dictionary for query logic and API settings. The 
    # requests library will then safely format and encode this information.
    # This is the 2nd of four steps for an NCBI search.
    search_params = {
        "db": "pubmed",
        "term": term,
        "retmode": "json",
        "usehistory": "y",
        "retmax": 999
    }

    # The 3rd step of the four step NCBI search:
    # Sending the request to NCBI with attached parameters. 
    response = requests.get(search_url, params=search_params)

    # The last of the 4 steps:
    # Parse and inspect the JSON data, execute the fetch, and assemble the report.
    if response.status_code == 200:
        data = response.json()
        # Safely extract IDs if they exist in the response
        id_list = data.get("esearchresult", {}).get("idlist", [])
#        print("Found unique IDs:", id_list)

        # Extract the WebEnv string and query_key safely
        my_webenv = data["esearchresult"]["webenv"]
        my_querykey = data["esearchresult"]["querykey"]
        
        fetch_params = {
            "db": "pubmed",
            "query_key": my_querykey,
            "WebEnv": my_webenv,
            "rettype": "abstract",
            "retmode": "text"
        }
        
        fetch_response = requests.get(fetch_url, params=fetch_params)

        # Technically, this is the end of the NCBI search/fetch operation, and 
        # the beginning of the report assembly

        # Get current date and time
        now = datetime.now()
        # Format as YYYY-MM-DD HH:MM:SS
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        output_file_name = "evidenceCollection_2/abstracts.txt"
        file_path = Path(output_file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as file:
            file.write("\n--- Fetched Abstracts for ---")
            file.write("\nSPECIES NAME: ")
            file.write(spec_name)

            file.write("\nSearch Criteria: ")
            file.write(spec_name)
            file.write(search_crit_txt)
            file.write("  <-- Search ")
            file.write(str(search_crit))
            file.write(" selected by user.")

            file.write("\nTimestamp: ")
            file.write(timestamp)
            file.write("\n\n")

#            return_count = f"The number of returns for {spec_name} = {str(len(id_list))}\n\n\n\n"
            return_count = f"\tThere are  {str(len(id_list))}  returns for this query\
... as printed below:\n\n\n"
            file.write(return_count)

            print("\nNumber of returns: " + str(len(id_list)) + "\t   See output report." + "\n")

            if "<ERROR>Empty result - nothing to do</ERROR>" in fetch_response.text:
                file.write("Direct evidence is absent based on your search criteria.")
                file.write("\nTry searching accepted synonyms and then genus-level evidence, and")
                file.write("\nthen label the Match_Level clearly.")
            else:
                file.write(fetch_response.text)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# If "multiple" was chosen then search via list, and continue building the report. 
if selection.lower() == "m":
    start_time = time.perf_counter()
    for species_name in species_list:
        term, search_crit_txt = lib.assemble_term(species_name, search_crit)

        # Create parameters dictionary for query logic and API settings
        search_params = {
            "db": "pubmed",
            "term": term,
            "retmode": "json",
            "usehistory": "y",
            "retmax": 999
        }

        # Send the request to NCBI 
        response = requests.get(search_url, params=search_params)

        # Parse the JSON data, execute the fetch, and add to the report
        if response.status_code == 200:
            data = response.json()
            # Safely extract IDs if they exist in the response
            id_list = data.get("esearchresult", {}).get("idlist", [])

            # Extract the WebEnv string and query_key safely
            my_webenv = data["esearchresult"]["webenv"]
            my_querykey = data["esearchresult"]["querykey"]
            
            fetch_params = {
                "db": "pubmed",
                "query_key": my_querykey,
                "WebEnv": my_webenv,
                "rettype": "abstract",
                "retmode": "text"
            }

            # Final step of NCBI search/fetch operation
            fetch_response = requests.get(fetch_url, params=fetch_params)

            # Append to report

            # Get current date and time
#            now = datetime.now()
            # Format as YYYY-MM-DD HH:MM:SS
#            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
#            output_file_name = "evidenceCollection_2/abstracts.txt"
#            file_path = Path(output_file_name)
#            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "a") as file:
                file.write("SPECIES NAME: ")
                file.write(species_name)
                file.write("\n")

                num_species_returned = len(id_list)
                file.write("Number of returns: ")
                file.write(str(num_species_returned))
                file.write("\n\n")

                if "<ERROR>Empty result - nothing to do</ERROR>" in fetch_response.text:
                    file.write("Direct evidence is absent based on your search criteria.")
                    file.write("\nTry searching accepted synonyms and then genus-level evidence, and")
                    file.write("\nthen label the Match_Level clearly.")
                else:
                    file.write(fetch_response.text)

                file.write("\n\n")
                file.write("The number of returns for ")
                file.write(species_name)
                file.write(" was equal to ")
                file.write(str(num_species_returned))
                file.write(".")
                file.write("\n\n*********************************************************************************")
                file.write("\n*********************************************************************************\n\n")

                print("\t" + species_name + "\t" + str(num_species_returned))

        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    end_time = time.perf_counter()

    # Calculate elapsed time
    elapsed_time = end_time - start_time

    print("\n--- Execution Summary ---")
    print(f"Data collection complete.")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    # (Useful for longer durations)
#    mins, secs = divmod(elapsed_total, 60)
#    print(f"Elapsed time: {int(mins)}m {secs:.1f}s")
