
__authors__ = 'Hannah and Mark'


'''
Script that allows you to extract files from Dropbox

USAGE:

From the terminal:

python3 extract_files.py <local_dir> <'/dbx_dir'>

local_dir is where you file(s) will be downloaded to, and
dbx_dir (should be in '/') is the specific dropbox folder
you are trying to download from
'''


# Flag that determines whether to save your slice of a csv file locally
# True = yes, False = no
SAVE_CSV_LOCALLY = True


import dropbox
import argparse
import pandas as pd
TOKEN = 'MmZG6Vu56DAAAAAAAAAAIfI849OOrLXuNbRnlDbY4EzsABoSSFUDc7-1XUsv2NsO'
dbx = dropbox.Dropbox(TOKEN)
dbx.users_get_current_account()

parser = argparse.ArgumentParser(description='Download all files from dropbox')
parser.add_argument('local_dir', nargs='?',
                    help='Local directory to store downloads')
parser.add_argument('dbx_dir', nargs='?',
                    help='Folder name in your Dropbox')



def main():
    args = parser.parse_args()

    def save_df_slice_locally():

        '''
        Find a csv file and take a slice of it (just example
        here for now) and write it locally to /slices dir as a
        csv file
        '''

        if local_file.endswith('.csv'):
            df = pd.read_csv(local_file)
            print('Head of df:  ', df.head(10))
            df[['petal width (cm)']].to_csv('./slices/slice_test.csv')

    def save_df_slice_as_variable():

        '''
        Find a csv file and take a slice of it (just example
        here for now) and save that as a variable for manipulating
        locally
        '''

        if local_file.endswith('.csv'):
            df = pd.read_csv(local_file)
            print('Head of df:  ', df.head(10))
            grouping = df.groupby('petal width (cm)')
            return grouping

    # Prints the dropbox folder you're downloading from
    for entry in dbx.files_list_folder('').entries:
        print('Dropbox folder:  ',entry.name)

    response = dbx.files_list_folder(args.dbx_dir)

    for file in response.entries:
        try:
            local_file = args.local_dir +'/'+ file.name

            if SAVE_CSV_LOCALLY == True:
                save_df_slice_locally()
            else:
                save_df_slice_as_variable()

            # Prints file(s) in dropbox folder you are downloading from and the...
            # ... local location it will be downloaded to
            print('Downloading: {} to {}'.format(file.path_display, local_file))
            dbx.files_download_to_file(local_file, file.path_display)


        except Exception as err:
            print("Failed to Download %s\n%s" % (file.name, err))
    print("Finished downloading")



if __name__ == '__main__':
    main()