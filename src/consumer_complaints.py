import sys

def product_stats(firm_dict):
    """
    Parameters
    ----------
    firm_dict : dictionary
        DESCRIPTION.

    Returns
    -------
    unique_firm_count : dictionary
        DESCRIPTION.

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
    #complaints,unq_firms,hh_per_prod,output_file
    """
    Parameters
    ----------
    input_file : csv
        DESCRIPTION
    output_file: csv
        DESCRIPTION

    Returns
    -------
    None.
    """
    # Write the output file
    ### FOR TESTING
    # output_file = r'tests\my_test\output\report.csv'
    with open(output_file, 'w', encoding='UTF-8') as out_f:
        # Write header of the file
        out_f.write('product,year,total_complaints,total_companies,highest_percentage\n')
        
        for product_year in sorted(complaints.items()):
            prod_yr = product_year[0].split('--')
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
    Parameters
    ----------
    input_file : csv
        DESCRIPTION
    output_file: csv
        DESCRIPTION

    Returns
    -------
    None.

    """
    firms = dict()
    ### FOR TESTING
    # input_file = r'tests\my_test\input\complaints.csv'
    num_lines = 0
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
                    if str(dispute) not in ['Yes','No','N/A']:
                        comp_id='not yet'
                    int(comp_id)
                    break
                except:
                    record+= inp_f.readline()
            # we need something to split on, yet there can be commas and quotes
            # everywhere.
            semi_c_record = record.replace(",, ", "; ")
            semi_c_record = semi_c_record.replace(", ", "; ")
            semi_c_record = semi_c_record.replace('\xa0','')
            semi_c_record = semi_c_record.replace(',",', ';",')
            i=0
            while (i<5):
                semi_c_record = semi_c_record.replace(",,",",BREAK,")
                i+=1
            cl_record = semi_c_record.split(",")
                
            year = cl_record[0][:4]
            product = cl_record[1].lower().replace("; ",", ")
            company = cl_record[-11].lower().replace(";",",")

            if (company == 'inc.' or company == 'inc' or company == 'inc,'
                or company =='inc."' or company == 'inc"' or company == 'inc,"'):
                company = cl_record[-12].lower() +','+ company
            if (company == 'llc.' or company == 'llc' or company == 'llc,'
                or company =='llc."' or company == 'llc"' or company == 'llc,"'):
                company = cl_record[-12].lower() +','+ company

            complaint_id = cl_record[-1]
            key_record = product+'--'+year
            key_ = ''.join(key_record)
            
            # if complaint with product-year in complaints, then add 1
            # else create the instance and set it equal to 1
            if year!='' and product!='' and company!='':
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
            else:
                if record != ',,,,,,,,,,,,,,,,,\n' and record !='':
                    print('Error with Complaint ID:' +str(complaint_id))
                    print(company)
                else:
                    pass
            record = inp_f.readline()
            if company == 'â\xa0llc"':
                print(complaint_id)
            # Progress Report
            num_lines +=1
            if num_lines % 10**6 ==0:
                print('Number of records processed: '
                      +str(num_lines//10**6)+' million')
               
    print('All Records processed. Total of '
          +str(num_lines))
    complaints = product_stats(firms)
    write_output_file(complaints,output_file)
    print('Complete!')

if __name__ == '__main__':
    # Assign input and output files.
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # Call wrapper to execute
    compile_consumer_complaints(input_file,output_file)