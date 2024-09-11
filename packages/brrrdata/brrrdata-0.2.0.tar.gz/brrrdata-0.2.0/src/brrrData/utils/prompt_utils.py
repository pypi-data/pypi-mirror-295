import inquirer

def select_columns_to_ignore(columns):
    # Skapa en multiselect prompt för att välja kolumner att ignorera
    questions = [
        inquirer.Checkbox('ignored_columns',
                          message="Välj kolumner att ignorera",
                          choices=columns)
    ]
    # Visa prompten och få de valda kolumnerna
    answers = inquirer.prompt(questions)

    if answers:
        return answers['ignored_columns']
    else:
        print("Inga kolumner valdes att ignorera.")
        return []

