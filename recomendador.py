import os, re
import pandas as pd

# df = pd.DataFrame('TMDb_updated.csv')

BOLD = '\033[1m'
DICT_COLOURS = {'Film': '\033[38;2;255;43;053m', 'Series': '\033[38;2;70;100;228m'}
END = '\033[m'
FILE_NAME = 'imdb.csv'

QUESTIONS = {
    'Type': 'Series|Film',
    'Genre': 'Mystery|Action|Drama|Thriller|CrimeSci-Fi|Sport|Comedy|Animation|Horror|Romance|Fantasy|Crime',
    'Date': '(1922-2022)',
    'Certificate': 'PG-16|R|TV-14|TV-MA|PG'
}

def extract(file_name) -> pd.DataFrame:
    """
    Get the DataFrame from a .csv file file name
    """
    df = pd.read_csv(file_name, sep=',')
    return df

def get_desired(df: pd.DataFrame, wants: dict, rate = False) -> list[list]:
    """
    Returns a list with sublists containing the index of the line and the corresponding number of
    ocurrences based on the filters apllied by the user input (wants)

    If rate == True, it ads the rate of the movie to the number of ocurrences so it can be ordered later
    """
    desired = []

    for i in range(len(df)):
        counter = 0
        for w in wants:
            if len(re.findall('\w',wants[w])):
                for ocurrence in re.findall(wants[w],str(df[w].iloc[i])): counter += 2
        if counter > 0: desired.append([i,counter])
    
    rate = True if (desired != [] and input('Order by Imdb rate? (Y/N): ') == 'Y') else False
    clear()
    
    if rate:
        for movie in desired:
            rate = df['Rate'].iloc[movie[0]]
            if rate != 'No Rate': movie[1] *= float(rate)

    return desired

def transform(df: pd.DataFrame, wants: dict) -> list:
    """
    Return a list of the indexed of the filtered movies ordered from higher to lower relation
    """
    #Get the desired
    desired = get_desired(df,wants)

    #Order the desired by the second index
    desired.sort(key=lambda x: x[1], reverse=True)

    return [movie[0] for movie in desired]

def show_results(df: pd.DataFrame, keyindexes: list, give=True, pages=10):
    
    l = len(keyindexes)
    print(f'{BOLD}RESULTADOS DEL RECOMENDADOR:{END}\n')
    lenpage = (len(keyindexes)//pages) + 1

    a, b, page = 0, lenpage, 1
    while give and page <= pages:

        perline = 1
        for i in keyindexes[a:b]:
            only_name = df['Name'].iloc[i] if len(df['Name'].iloc[i]) < 50 else (df['Name'].iloc[i][:45] + '...')
            name = DICT_COLOURS[df['Type'].iloc[i]] + only_name + END
            print(name, end=" "*(51-len(only_name))) if perline < 3 else print(name)
            perline = (perline + 1) if perline < 3 else 1

        if b < l and input('\nMore results?(Y/N): ') == 'Y':
            a += lenpage
            b += lenpage
            page += 1
            print()
        else: give = False

    if page >= pages: print(f'{BOLD}NO MORE RESULTS{END}')

def load(df: pd.DataFrame, keyindexes: list, save=False):
    """
    Shows all results based on keyindexes

    If save == True, if saves the resultin movie names in a .txt file named "desired_movies"
    """
    show_results(df, keyindexes, pages=20) if keyindexes != [] else print(f'{BOLD}NO RESULTS FOR YOUR SEARCH{END}') 
    
    if save:
        with open('desired_movies.txt','w') as file:
            for i in keyindexes: file.write(df['Name'].iloc[i] + '\n')

def clear():
    """Clears the terminal"""
    os.system('cls')

def title():
    print(f'\t\t\t{BOLD}RECOMENDADOR DE PELÍCULAS Y SERIES DE IMDB{END}\n')

def leyend():
    print(f'*NOTE*: Select as many as wanted on each field using {BOLD}|{END} as separator\n')
    for q in QUESTIONS:
        print(f'{BOLD}{q}{END}: {QUESTIONS[q]}')
    print()

def get_wants() -> dict:
    """
    Returns a dictionary with the desired filters based on user input
    """
    wants = {}

    for q in QUESTIONS:
        title()
        leyend()
        wants[q] = (input(f'Search for {BOLD}{q}{END}: '))
        clear()
    
    return wants

if __name__ == '__main__':

    clear()
    wants = get_wants()

    df = extract(FILE_NAME)
    keyindexes = transform(df, wants)
    load(df,keyindexes)