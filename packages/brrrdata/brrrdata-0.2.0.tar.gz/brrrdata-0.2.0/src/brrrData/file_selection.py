import os
import inquirer

def multi_file_selector():
    # Lista alla filer i den nuvarande mappen
    files_in_current_directory = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Skapa en fråga för att välja filer
    questions = [
        inquirer.Checkbox('selected_files',
                          message="Välj filer från nuvarande mapp",
                          choices=files_in_current_directory)
    ]
    
    # Visa prompten och få de valda filerna
    answers = inquirer.prompt(questions)
    
    # Skriv ut de valda filerna
    if answers:
        selected_files = answers['selected_files']
        print("Valda filer:", selected_files)
    else:
        print("Inga filer valdes.")

def single_file_selector():
    # Lista alla filer i den nuvarande mappen
    files_in_current_directory = [f for f in os.listdir('.') if os.path.isfile(f)]
    # Skapa en fråga för att välja en fil
    questions = [
        inquirer.List('selected_file',
                      message="Välj en fil från nuvarande mapp",
                      choices=files_in_current_directory)
    ]
    # Visa prompten och få den valda filen
    answers = inquirer.prompt(questions)
    # Skriv ut den valda filen
    if answers:
        selected_file = answers['selected_file']
        print("Vald fil:", selected_file)
        return selected_file
    else:
        print("Ingen fil valdes.")
