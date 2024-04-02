import os
from django.conf import settings
import pandas as pd
import json
from task.tasks import save_file



def filter_data(file_path,filters):
    filtered_data = []
    chunk_reader = pd.read_csv(file_path,chunksize=10,nrows=7000)
    total_rows_processed = 0

    for chunk_df in chunk_reader:
        # Create a copy of the chunk DataFrame
        filtered_df = chunk_df.copy()
        filter_conditions = pd.Series(False, index=filtered_df.index)  # Initialize with False values
        
        # Apply filters on the chunk
        for col, value in filters.items():
            if value:
                # Perform case-insensitive substring matching for string columns
                if filtered_df[col].dtype == 'O':  # 'O' represents object (string) dtype
                    filter_conditions |= filtered_df[col].str.contains(value, case=False)
                else:
                    filter_conditions |= (filtered_df[col] == value)
        
        # Apply the filter conditions and convert the filtered DataFrame to a list of dictionaries
        filtered_chunk = filtered_df[filter_conditions]
        for _, row in filtered_chunk.iterrows():
            row = row.where(pd.notnull(row), None)
            filtered_data.append(row.to_dict())
            total_rows_processed += 1

            # Check if we have processed 500 rows
            if total_rows_processed >= 500:
                return filtered_data

    return filtered_data


def handle_uploaded_file(uploaded_file):
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_file', uploaded_file.name)
        
        # Validate file path
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        
        with open(file_path, 'wb+') as destination:
            # Write chunks to the destination file
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        print("File uploaded successfully")
        save = save_file.delay(str(file_path))
        # Return the file path if upload is successful
    except Exception as e:
        # Handle any exceptions that may occur during the file upload process
        print("Error uploading file:", e)
        return None