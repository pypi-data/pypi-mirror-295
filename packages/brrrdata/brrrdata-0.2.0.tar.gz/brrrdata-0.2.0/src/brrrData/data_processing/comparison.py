import pandas as pd
from brrrData.file_selection import single_file_selector
from brrrData.utils.prompt_utils import select_columns_to_ignore
import inquirer

def compare_columns_in_files_and_save():
    # Välj den första filen
    file1 = single_file_selector()
    if not file1:
        return
    
    # Välj den andra filen
    file2 = single_file_selector()
    if not file2:
        return
    
    # Läs in filerna som DataFrames
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    
    # Välj en kolumn från första filen
    column1 = inquirer.list_input("Välj kolumn från första filen:", choices=df1.columns.tolist())
    
    # Välj en kolumn från andra filen
    column2 = inquirer.list_input("Välj kolumn från andra filen:", choices=df2.columns.tolist())
    
    # Hitta gemensamma värden
    common_values = set(df1[column1]) & set(df2[column2])
    
    # Räkna statistik
    total_rows1 = len(df1)
    total_rows2 = len(df2)
    unique_rows1 = len(df1[column1].unique())
    unique_rows2 = len(df2[column2].unique())
    common_count = len(common_values)
    
    # Skriv ut statistik
    print(f"\nStatistik:")
    print(f"Totalt antal rader i fil 1: {total_rows1}")
    print(f"Totalt antal rader i fil 2: {total_rows2}")
    print(f"Antal unika värden i kolumn '{column1}' från fil 1: {unique_rows1}")
    print(f"Antal unika värden i kolumn '{column2}' från fil 2: {unique_rows2}")
    print(f"Antal värden som finns i båda filerna: {common_count}")
    
    if common_count > 0:
        save_common = inquirer.confirm("Vill du spara de gemensamma värdena till en ny fil? (Ja/Nej): ")
        if save_common:
            new_filename = input("Ange namnet på den nya filen (inklusive .xlsx): ")
            common_df = pd.DataFrame({'Gemensamma värden': list(common_values)})
            common_df.to_excel(new_filename, index=False)
            print(f"Gemensamma värden har sparats till {new_filename}.")
        else:
            print("\nGemensamma värden:")
            for value in common_values:
                print(value)
    
    print(f"\nTotalt antal värden som finns i båda filerna: {common_count}")
