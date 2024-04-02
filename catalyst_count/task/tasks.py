from __future__ import absolute_import,unicode_literals
from task.models import Company
from celery import shared_task
import pandas as pd
@shared_task
def add(x,y):
    return x+y


# @shared_task
# def save_file(filepath):
#     # excel_data = pd.read_csv(filepath,nrows=5000)
#     excel_data = pd.read_csv(filepath)
#     instances = []
#     for index, row in excel_data.iterrows():
#         instance = Company(
#             name=row['name'],  
#             domain=row['domain'],
#             year_founded = row['year founded'],
#             size_range = row['industry'],
#             locality = row['size range'],
#             country = row['locality'],
#             linkedin_url = row['country'],
#             current_employee_estimate = row['current employee estimate'],
#             total_employee_estimate = row['total employee estimate'],
#         )
#         instances.append(instance)
#      # Bulk insert into the database
#     Company.objects.bulk_create(instances)
#     return "done"


@shared_task
def save_file(filepath):
    # Define chunk size (number of rows to read at a time)
    chunk_size = 5000
    
    # Initialize a list to hold instances
    instances = []
    
    # Iterate over the file in chunks and process each chunk
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        # Iterate over each row in the chunk
        for index, row in chunk.iterrows():
            # Create a Company instance for each row
            instance = Company(
                name=row['name'],  
                domain=row['domain'],
                year_founded=row['year founded'],
                size_range=row['industry'],
                locality=row['size range'],
                country=row['locality'],
                linkedin_url=row['country'],
                current_employee_estimate=row['current employee estimate'],
                total_employee_estimate=row['total employee estimate']
            )
            # Append the instance to the list
            instances.append(instance)
        
        # Bulk insert into the database after processing each chunk
        Company.objects.bulk_create(instances)
        
        # Clear the list for the next chunk
        instances = []

    # Insert remaining instances
    if instances:
        Company.objects.bulk_create(instances)
    
    return "done"