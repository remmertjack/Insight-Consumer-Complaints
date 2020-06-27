"""
Project: Consumer Complaints
Author: Jack Remmert
Date: June 25th, 2020

The objective of this program is, given a comma separated input file of consumer
complaints (which contains information such as date, company, product, consumer
notes, company info such as zip code and state, status of complaint)
output an aggregated file that contains various stats for a 
product-year combination such as total number of complaints, number of unique
companies per proudct-year, and the highest percentage of complaints per
product-year.
    
"""

import sys

def read_and_clean_input_file(input_file):
    """
    This function reads the data from the input_file, cleans it, and creates a
    dictionary, firms, that contains every product-year combination as the key
    and an inner dictionary that consists of a company, as the inner key,
    and the total number of complaints against said company for the given
    product-year.
    
    In the cleaning stages, we clean for commas in any user comments or company
    names and turn them into semi-colon's. Then we split on the csv provided
    commas, extract the relevant data and load the data onto our firm dictionary.
    
    Parameters
    ----------
    input_file : csv
        Input file of data. See beginning of script for a summary.

    Returns
    -------
    firms : dictionary
        Contains a product-year key in the form of xxxx--YYYY and a nested 
        dictionary with a company key and total number of complaints filed
        against them for said product and year.
    num_lines : int
        Number of records processed.
    num_errors : int
        Number of Errors found.

    """
    firms = dict()
    ### FOR TESTING
    # input_file = r'input/complaints.csv'
    num_lines = 0
    num_errors = 0
    with open(input_file, 'r', encoding='UTF-8') as inp_f:
        record = inp_f.readline() # header 
        record = inp_f.readline()

        while len(record)>0:
            # if comment goes onto next line, grab the very next record, append
            # to current record
            while True:
                try:
                    comp_id = record.split(",")[-1].split('\n')[0]
                    dispute = record.split(",")[-2]
                    # some comments end in a 0-9 value, so look at previous
                    # value in Consumer Disputed? column, see if in the list
                    if str(dispute) not in ['Yes','No','N/A']:
                        comp_id='not yet'
                    int(comp_id)
                    break
                except:
                    record+= inp_f.readline()
            # we need something to split on, yet there can be commas and quotes
            # everywhere.
            semi_c_record = record.replace(",, ", "; ") # spelling mistakes
            # for all commas in record, but not as the csv, i.e. ,,
            semi_c_record = semi_c_record.replace(", ", "; ") 
            semi_c_record = semi_c_record.replace(',",', ';",')
            i=0
            while (i<2):
                # create our own BREAK for any missing values
                semi_c_record = semi_c_record.replace(",,",",BREAK,")
                i+=1
            cl_record = semi_c_record.split(",") # split on commas
                
            year = cl_record[0][:4]
            product = cl_record[1].lower().replace("; ",", ")
            company = cl_record[-11].lower().replace(";",",")
            # minor fixes if the above replacements did not catch a period or
            # double quote. Simply append the value in above location
            if (company == 'inc.' or company == 'inc' or company == 'inc,'
                or company =='inc."' or company == 'inc"' or company == 'inc,"'):
                company = cl_record[-12].lower() +','+ company
            if (company == 'llc.' or company == 'llc' or company == 'llc,'
                or company =='llc."' or company == 'llc"' or company == 'llc,"'):
                company = cl_record[-12].lower() +','+ company
            # if it ends a double quote and doesn't start with one, but the
            # previous object does, it must be a company with a comma in it
            if (company[-1] == '"' and company[0]!='"' and cl_record[-12][0]=='"'):
                company = cl_record[-12].lower() +','+ company

            complaint_id = cl_record[-1]
            key_record = product+'--'+year
            key_ = ''.join(key_record)
            
            # first check to see if company is blank or equal to 'break'
            if (company==' ' or company=='break'):
                # if record is empty, do nothing
                if record == ',,,,,,,,,,,,,,,,,\n' or record =='':
                    pass
                # else if record is not empty, then print an error
                else:
                    print('Error with Complaint ID: ' +str(complaint_id))
                    num_errors+=1
                
            else:
                # if complaint in firms, find the company, add 1
                if key_ in firms:
                    if company in firms[key_]:
                        firms[key_][company]+=int(1)
                 # if complaint in firms, but company is not, add company,
                 # init w/1
                    else:
                        firm_product_record = {company:1}
                        firms[key_].update(firm_product_record)   
                # if complaint not in firms, add complaint, add company,
                # init w/1
                else:
                    firm_record = {key_: {company:1} }
                    firms.update(firm_record)
                    
            # Progress Report
            num_lines +=1
            if num_lines % 10**6 ==0:
                print('Number of records processed: '
                      +str(num_lines//10**6)+' million')
            # read next line
            record = inp_f.readline()
                
    return firms, num_lines, num_errors

def product_stats(firm_dict):
    """
    This function takes in a dictionary, firm_dict, and calculates certain stats.
    These stats include the total number of complaints received for that product
    and year, total number of companies receiving at least one complaint for
    that product and year, and the highest percentage of total complaints
    filed against one company for that product and year.
    
    Parameters
    ----------
    firm_dict : dictionary
        Contains a product-year key in the form of xxxx--YYYY and a nested 
        dictionary with a company key and total number of complaints filed
        against them for said product and year.

    Returns
    -------
    complaints : dictionary
        Contains product-year key in the form of xxxx--YYYY and a list with the
        following elements:
            # total number of complaints
            # total number of companies receiving at least one complaint (uniqueness)
            # highest percentage
            # boolean of 1 or 0 if product-year key contains a double quote (")

    """
    complaints = dict()
    for product_year in firm_dict:
        # find total records for each product and year
        total = sum(firm_dict[product_year].values())
        # find unique records for each product and year
        unq_company_records = len(firm_dict[product_year])
        # find max percentage for each product and year
        mx = max(firm_dict[product_year].values())
        hh_per = int(round(mx/total * 100))
        # check if key contains quotes...they need to be removed before sorting
        if ('"' in product_year):
            include_quotes = 1
            product_year = product_year.replace('"','')
        else:
            include_quotes = 0
        
        complaints_record = {product_year:[total, unq_company_records, hh_per,include_quotes]}
        complaints.update(complaints_record)
        
    return complaints

def write_output_file(complaints, output_file):
    """
    This functions writes the aggregated data, complaints, to a csv file,
    output_file.
    
    Parameters
    ----------
    complaints : dictionary
        See product_stats complaints for definition.
        
    output_file: csv
        Output file of aggregated data. See beginning of script for example.

    Returns
    -------
    None.
    """
    # Write the output file
    ### FOR TESTING
    # output_file = r'output/report.csv'
    with open(output_file, 'w', encoding='UTF-8') as out_f:
        # Write header of the file
        # out_f.write('product,year,total_complaints,total_companies,highest_percentage\n')
        
        for product_year in sorted(complaints.items()):
            prod_yr = product_year[0].split('--')
            # put back the quotes for a given product, but only if they exist
            if (product_year[-1][-1] == 1):
                product = '"'+prod_yr[0]+ '"'
            else:
                product = prod_yr[0]
            line = (product+','+prod_yr[1]+','
                +str(product_year[-1][0]) +','+ str(product_year[-1][1])+','
                +str(product_year[-1][2]) + '\n')
            out_f.write(line)
           
def compile_consumer_complaints(input_file, output_file):
    """
    This is a wrapper function that executes all the steps to compile the 
    consumer complaints into a csv for the user.
    1. It reads and cleans the data with the read_and_clean_input_file
        function. This function, will print a progress report every million
        records.
    2. Print a summary with total number of records and the 
        number of errors, if they exist. 
    3. Calcuate the stats with the product_stats function.
    4. Write the compiled data to the output file.
    5. Print "Complete!" to let the user know the program has finished executing. 
    
    Parameters
    ----------
    input_file : csv
        Input file of data. See beginning of script for a summary.
        
    output_file: csv
        Output file of aggregated data. See beginning of script for example.

    Returns
    -------
    None.

    """
    firms, num_lines, num_errors = read_and_clean_input_file(input_file)
    if num_errors == 0:           
        print('All records processed. Total of '
              +str(num_lines)+' records. No errors found.')
    else:
        print('Records processed. Total of '+str(num_lines)+' records and '
              +str(num_errors)+' errors found.')
    complaints = product_stats(firms)
    write_output_file(complaints,output_file)
    print('Complete!')

if __name__ == '__main__':
    # Assign input and output files.
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # Call wrapper to execute
    compile_consumer_complaints(input_file,output_file)
