import pandas as pd
from file_selection import single_file_selector
from utils.prompt_utils import select_columns_to_ignore
import inquirer

def sort_excel_rows():
    filename = single_file_selector()
    if not filename:
        return
    
    try:
        # Läs in filen som DataFrame
        df = pd.read_excel(filename)
        
        # Få alla kolumnnamn
        all_columns = df.columns.tolist()
        
        # Låt användaren välja vilken kolumn som ska sorteras
        sort_column = inquirer.list_input("Välj kolumn att sortera på:", choices=all_columns)
        
        # Fråga användaren om sorteringsordning
        sort_order = inquirer.list_input("Välj sorteringsordning:", 
                                         choices=["Stigande", "Fallande"])
        
        # Sortera DataFrame
        ascending = True if sort_order == "Stigande" else False
        df_sorted = df.sort_values(by=sort_column, ascending=ascending)
        
        # Fråga användaren om de vill spara resultatet i en ny fil eller uppdatera den befintliga
        save_choice = inquirer.list_input("Vill du spara resultatet i en ny fil eller uppdatera den befintliga?", 
                                          choices=["Spara i ny fil", "Uppdatera befintlig fil"])
        
        if save_choice == "Spara i ny fil":
            new_filename = input("Ange namnet på den nya filen (inklusive .xlsx): ")
            df_sorted.to_excel(new_filename, index=False)
            print(f"Sorterad data har sparats i {new_filename}")
        else:
            df_sorted.to_excel(filename, index=False)
            print(f"Den befintliga filen {filename} har uppdaterats med sorterad data")
        
        print(f"\nSortering slutförd. Raderna sorterades efter kolumnen '{sort_column}' i {sort_order.lower()} ordning.")
        
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
