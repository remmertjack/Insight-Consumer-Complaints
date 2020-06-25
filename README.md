# Insight Data Engineering: Consumer Complaints Challenge
******

This GitHub repository contains my solution for the Fall 2020 Insight Data Engineering Fellowship [coding challenge](https://github.com/insightdatascience/consumer_complaints).

## Problem and Objective
The federal government provides a way for consumers to file complaints against companies regarding different financial products, such as payment problems with a credit card or debt collection tactics. This challenge will be about identifying the number of complaints filed and how they're spread across different companies.

Thus, given a comma separated file of consumer complaints (which contains information such as date recieved, company, product, consumer notes, company info such as zip code and state, status of complaint), output an aggregated file that contains various stats for a product-year combination such as total number of complaints, number of unique companies per proudct-year, and the highest percentage of complaints per product-year.

For example, the script within will create a csv in the following format:
```
"credit reporting, credit repair services, or other personal consumer reports",2019,3,2,67
"credit reporting, credit repair services, or other personal consumer reports",2020,1,1,100
debt collection,2019,1,1,100
```

For more informaiton on the data, [click here](https://cfpb.github.io/api/ccdb/fields.html).

## Process
The `consumer_complaints.py` script takes an input and output file path and then executes a wrapper function, `compile_consumer_complaints`.

This wrapper function, first reads the input file line by line, cleans the data by removing excess commas and quotes and replacing them with semi-colons, and then creates a dictionary containing each product-year combination and an inner dictionary containting a company and the number of complaints filed against them for said product-year. The program will print a *Progress Report* for every million lines and once more  when the program has finished reading every record.

Next, the `product_stats` function runs, executed within `compile_consumer_complaints`, to compile the statistics mentioned above and creates a dictionary containing the product-year combination and the required stats.  This is performed with a *for loop* over each product-year combination and sums the total number of complaints, counts the total number of unique companies per proudct-year using the length of said inner dictionary, and finds the highest percentage of complaints per product-year by taking the maxium value, dividng by the sum of total complaints, and rounded as required.

Finally, the `write_output_file` function, executed within `compile_consumer_complaints`, writes the data to a csv given the output file. First, it builds the line using 
string concatenation based on the output from `product_stats` and then it writes it to said file.

For more comments on each individual function, please see the code itself.

## Instructions
To execute the script, move to the main directory of the project and run the following in the terminal:
```
python3.7 ./src/consumer_complaints.py ./input/complaints.csv ./output/report.csv
```
The last two arguments should be input and output files, respectively.

### Ways to improve
1. Implement logging to print errors for a Complaint Id directly to a file rather than the printing to the console itself.
1. Implement timeouts in while loops in case of column removal. Currently the script will continue to read lines until the last object in the line is an integer and the second to last object either `'Yes', 'No', or 'N/A'` from the Consumer Dispute? column, which has been depreciated since April 24th, 2017.

### Additional comments
Due to the large file size of the test complaints provided, that file has been omitted from this repository. That file can be found [here](http://files.consumerfinance.gov/ccdb/complaints.csv.zip) if so desired.

This program was created in `python3.7.6` to be exact with the `sys` package.

### Questions?
Please feel free to email me at remmertjack@gmail.com

