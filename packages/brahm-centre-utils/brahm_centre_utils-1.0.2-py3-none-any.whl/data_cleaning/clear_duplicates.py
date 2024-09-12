from common import are_names_similar
# Duplicate Function. 
# Group by Postal Code -> In each group, merge the members again based on Postal Code (Outer merge to get all the combinations) 
# --> Filter out those rows that meets the duplicate conditions
def find_duplicates_within_group(group):
    # Reset index to keep track of the original row indices
    group = group.reset_index(drop=True)
    group['index'] = group.index
    
    # Get all the merged combinations of the group
    merged = group.merge(group, how='outer', on='Postal_Code__c')

    # Check if 'Client_NRIC__c_x' and 'Client_NRIC__c_y' exist in the DataFrame
    if 'Client_NRIC__c_x' in merged.columns and 'Client_NRIC__c_y' in merged.columns:
        nric_condition = merged['Client_NRIC__c_x'] == merged['Client_NRIC__c_y']
    else:
        nric_condition = False

    # Check if 'Mobile_Number__c_x' and 'Mobile_Number__c_y' exist in the DataFrame
    if 'Mobile_Number__c_x' in merged.columns and 'Mobile_Number__c_y' in merged.columns:
        mobile_condition = merged['Mobile_Number__c_x'] == merged['Mobile_Number__c_y']
    else:
        mobile_condition = False

    # Apply the mask to identify duplicates
    mask = (
        (
            merged.apply(lambda row: are_names_similar(row['Name_x'], row['Name_y']), axis=1) &
            (merged['Gender__c_x'] == merged['Gender__c_y']) &
            (
                (merged['Birth_Year__c_x'] == merged['Birth_Year__c_y']) | 
                mobile_condition
            )
        ) | 
        nric_condition
    ) & (merged.index_x < merged.index_y)

    return merged[mask]

def find_contact_duplicates(df):
    return df.groupby('Postal_Code__c').apply(find_duplicates_within_group).reset_index(drop=True)