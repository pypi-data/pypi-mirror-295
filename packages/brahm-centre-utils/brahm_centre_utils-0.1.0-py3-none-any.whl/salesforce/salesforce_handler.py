import pandas as pd
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_salesforce(query, sf):
    """
    Query Salesforce and return results as a flattened pandas DataFrame.
    
    :param query: SOQL query string
    :param sf: Salesforce object
    :return: pandas DataFrame with flattened records
    """
    try:
        result = sf.query_all(query)
        records = result['records']
        
        # Flatten all records
        flattened_records = [flatten_record(record) for record in records]
        
        # Convert to DataFrame
        df = pd.DataFrame(flattened_records)
        logger.info(f"Columns before renaming: {df.columns}")
        
        # Rename columns by removing the first part of the name before the first dot
        df.columns = [rename_columns(col) for col in df.columns]
        logger.info(f"Columns after renaming: {df.columns}")
        
        return df
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise

def flatten_record(record, parent_key='', sep='.'):
    """
    Flatten a nested dictionary into a single dictionary with dot-separated keys.
    
    :param record: Nested dictionary
    :param parent_key: String to prefix keys with
    :param sep: Separator to use between keys
    :return: Flattened dictionary
    """
    items = []
    for k, v in record.items():
        if k != 'attributes':
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_record(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    return dict(items)

def rename_columns(col_name):
    """
    Rename columns by removing the first part of the name before the first dot.
    
    :param col_name: Original column name
    :return: Renamed column name
    """
    if '.' in col_name:
        return col_name.split('.')[-1]
    return col_name

# Split the Id from the Salesforce URL
def get_Id_from_SF_URL(url):
    return url.split('/')[-2]

# Get SF picklist options
def get_picklist_options(object_name, field_name, sf):
    # Describe the object to get field metadata
    describe = sf.__getattr__(object_name).describe()
    
    # Find the field and get its picklist options
    for field in describe['fields']:
        if field['name'] == field_name:
            picklist_values = [option['value'] for option in field['picklistValues']]
            return picklist_values
    return None


