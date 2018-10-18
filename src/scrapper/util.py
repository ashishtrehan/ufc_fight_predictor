import pandas as pd
import traceback





def name_cleaner(x):
    if not pd.isnull(x):
        try:
            x = str(x)
        except:
            x = x.encode('ascii','ignore')
        x = x.strip()
        x = x.replace('  ',' ')
        x = x.replace(r'=-','')
    return x


def name_standardizer():
    fighters_df = pd.read_csv(r'../data/fighters.csv',low_memory=False)
    del fighters_df['Last Name'] #only for use when filling out spreadsheet


    #iterate through each fighter to create dict
    fighter_name_standardization_dict = {}
    for i in range(0,fighters_df.shape[0]):
        myfighter_row = fighters_df.iloc[i]
        myfighter_row = myfighter_row.dropna()

        myfighter = myfighter_row['Fighter']
        myfighter_alternatives = list(myfighter_row.drop('Fighter').values)

        for myalternative in myfighter_alternatives:
            try:
                fighter_name_standardization_dict.update({myalternative:myfighter})
            except:
                #i forsee errors where doubling of alternate names breaks dict
                print (myfighter, myalternative)
                print (str(traceback.format_exc()))
                pass

    return fighter_name_standardization_dict

def replace_if_in_dict(parm,mydict):
    if not pd.isnull(parm) and parm in list(mydict.keys()):
        parm = mydict[parm]
    return parm