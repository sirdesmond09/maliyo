import pandas as pd

def process_data(file):
    """ This is a helper function that takes in the file that was uploaded, reads it with pandas and cleans the data for saving into the db. """
    
    #read the file
    data = pd.read_csv(file)
    #
    data.fillna('', inplace=True)
    data.set_index('name', inplace=True)
    
    cols = ['name']
    cols.extend([k for k in data.columns])
    rows = []
    for row in data.itertuples():
        each_data = {}
        for i in range(len(cols)):
            each_data[cols[i]]=row[i]

        rows.append(each_data)
    return rows