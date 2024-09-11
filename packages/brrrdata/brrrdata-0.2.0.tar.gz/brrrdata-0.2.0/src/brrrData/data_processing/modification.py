import pandas as pd
from brrrData.file_selection import single_file_selector
from brrrData.utils.prompt_utils import select_columns_to_ignore
import inquirer

def modify_column_in_excel():
    filename = single_file_selector()
    if not filename:
        return

    try:
        # Läs in filen som DataFrame
        df = pd.read_excel(filename)

        # Få alla kolumnnamn
        all_columns = df.columns.tolist()

        # Låt användaren välja vilken kolumn som ska ändras
        column_to_modify = inquirer.list_input("Välj kolumn att ändra:", choices=all_columns)
        
        # Fråga användaren hur de vill ändra kolumnen
        modification_type = inquirer.list_input("Hur vill du ändra kolumnen?", 
                                                choices=["Lägg till text i slutet av varje värde", 
                                                         "Lägg till text i början av varje värde", 
                                                         "Ändra text (ange text att ersätta)"])

        if modification_type == "Lägg till text i slutet av varje värde":
            new_text = input("Skriv in den nya texten: ")
            df[column_to_modify] = df[column_to_modify].astype(str) + new_text

        elif modification_type == "Lägg till text i början av varje värde":
            new_text = input("Skriv in den nya texten: ")
            df[column_to_modify] = new_text + df[column_to_modify].astype(str)

        elif modification_type == "Ändra text (ange text att ersätta)":
            old_text = input("Skriv in texten som ska ersättas: ")
            new_text = input("Skriv in den nya texten: ")
            df[column_to_modify] = df[column_to_modify].astype(str).str.replace(old_text, new_text)

        # Fråga användaren om de vill spara resultatet i en ny fil eller uppdatera den befintliga
        save_choice = inquirer.list_input("Vill du spara resultatet i en ny fil eller uppdatera den befintliga?", 
                                          choices=["Spara i ny fil", "Uppdatera befintlig fil"])

        if save_choice == "Spara i ny fil":
            new_filename = input("Ange namnet på den nya filen (inklusive .xlsx): ")
            df.to_excel(new_filename, index=False)
            print(f"Ändringar har sparats i {new_filename}")

        else:
            df.to_excel(filename, index=False)
            print(f"Den befintliga filen {filename} har uppdaterats med ändringar")

        print(f"\nÄndringar har tillämpats på kolumnen '{column_to_modify}'.")

    except Exception as e:
        print(f"Ett fel uppstod: {e}")
