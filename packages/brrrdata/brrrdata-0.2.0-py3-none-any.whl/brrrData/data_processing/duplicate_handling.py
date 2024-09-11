import pandas as pd
import inquirer
from brrrData.file_selection import single_file_selector
from brrrData.utils.prompt_utils import select_columns_to_ignore

from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style


def list_duplicates_in_excel():
    filename = single_file_selector()
    if not filename:
        return
    
    try:
        df = pd.read_excel(filename)
        total_rows = len(df)
        
        all_columns = df.columns.tolist()
        ignored_columns = select_columns_to_ignore(all_columns)
        columns_to_consider = [col for col in all_columns if col not in ignored_columns]
        
        df_duplicates = df[df.duplicated(subset=columns_to_consider, keep=False)]
        df_duplicates = df_duplicates.sort_values(by=columns_to_consider)
        
        duplicate_rows = len(df_duplicates)
        
        print(f"\nStatistik:")
        print(f"Totalt antal rader i filen: {total_rows}")
        print(f"Antal dubblett-rader i filen: {duplicate_rows}")
        print(f"Procent av rader som är dubbletter: {(duplicate_rows / total_rows * 100):.2f}%")
        
        if duplicate_rows > 0:
            save_choice = inquirer.confirm("Vill du spara dubletterna till en ny fil? (Ja/Nej): ")
            if save_choice:
                new_filename = input("Vad ska den nya filen med dubbletter heta? (inklusive .xlsx): ")
                df_duplicates.to_excel(new_filename, index=False)
                print(f"Dubbletter har listats och sparats i {new_filename}.")
            else:
                print("\nDubbletter:")
                
                # Interactive view of duplicates
                def create_table_text():
                    header = ' | '.join(df_duplicates.columns)
                    rows = [' | '.join(map(str, row)) for row in df_duplicates.values]
                    return [header] + rows

                table_text = create_table_text()
                current_row = 0

                def get_formatted_text():
                    return [(('class:header ' if i == 0 else '') + 
                             ('class:current ' if i == current_row else ''), 
                             line + '\n') for i, line in enumerate(table_text)]

                kb = KeyBindings()

                @kb.add('q')
                def _(event):
                    event.app.exit()

                @kb.add('down')
                def _(event):
                    nonlocal current_row
                    if current_row < len(table_text) - 1:
                        current_row += 1

                @kb.add('up')
                def _(event):
                    nonlocal current_row
                    if current_row > 0:
                        current_row -= 1

                style = Style.from_dict({
                    'header': 'bold reverse',
                    'current': 'reverse',
                })

                layout = Layout(HSplit([
                    Window(FormattedTextControl(get_formatted_text)),
                    Window(height=1, content=FormattedTextControl(
                        [('class:bottom-toolbar', ' Använd piltangenterna för att navigera. Tryck "q" för att avsluta.')]
                    )),
                ]))

                app = Application(layout=layout, key_bindings=kb, full_screen=True, style=style)
                app.run()
                print(f"\nStatistik:")
                print(f"Totalt antal rader i filen: {total_rows}")
                print(f"Antal dubblett-rader i filen: {duplicate_rows}")
                print(f"Procent av rader som är dubbletter: {(duplicate_rows / total_rows * 100):.2f}%")

        else:
            print("Inga dubbletter hittades i filen.")
        
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def remove_duplicate_rows_in_excel():
    filename = single_file_selector()
    if not filename:
        return
    new_filename = input("vad ska den nya filen heta?")
    save_removed_filename = input("Vill du spara de borttagna raderna i en separat fil? \n (Skriv 'Y'/'N')")

    # Välj vilken typ av dubbletter som ska tas bort
    remove_option = input("Vill du (1) ta bort alla dubletter helt eller (2) behålla en unik rad? (Skriv '1' eller '2') ")
    try:
        df = pd.read_excel(filename)

        # Få alla kolumnnamn
        all_columns = df.columns.tolist()

        # Låt användaren välja vilka kolumner som ska ignoreras
        ignored_columns = select_columns_to_ignore(all_columns)

        # Välj alla kolumner utom de som ska ignoreras
        columns_to_consider = [col for col in all_columns if col not in ignored_columns]

        # Antal rader innan dubbletter tas bort
        original_row_count = len(df)

        if remove_option == '1':
            # Ta bort alla dubbletter helt
            df_unika = df.drop_duplicates(subset=columns_to_consider, keep=False)
            # Hitta de borttagna raderna
            df_removed = df[~df.index.isin(df_unika.index)]
        elif remove_option == '2':
            # Ta bort dubbletter men behåll en unik rad
            df_unika = df.drop_duplicates(subset=columns_to_consider, keep='first')
            # Hitta de borttagna raderna
            df_removed = df[~df.index.isin(df_unika.index)]
        else:
            print("Ogiltigt alternativ, avslutar.")
            return

        new_row_count = len(df_unika)
        removed_rows = original_row_count - new_row_count

        df_unika.to_excel(new_filename, index=False)

        # Spara de borttagna raderna om användaren önskar
        if save_removed_filename.lower() == 'y' or save_removed_filename.lower() == "ja":
            removed_filename = input("Vad ska filen med borttagna rader heta?")
            df_removed.to_excel(removed_filename, index=False)
            print(f"Borttagna rader har sparats i {removed_filename}")

          # Skriv ut statistik om ändringarna
        print(f"Dubbletter har tagits bort och en ny fil har sparats.")
        print(f"Totalt antal rader i ursprunglig fil: {original_row_count}")
        print(f"Totalt antal rader i nya filen: {new_row_count}")
        print(f"Antal rader som togs bort: {removed_rows}")

    except exception as e:
        print(e)

    print("dubbletter har tagits bort och en ny fil har sparats.")



def save_duplicate_rows_only():
    filename = single_file_selector()
    if not filename:
        return
    new_filename = input("Vad ska den nya filen heta?")
    try:
        df = pd.read_excel(filename)

        # Få alla kolumnnamn
        all_columns = df.columns.tolist()

        # Låt användaren välja vilka kolumner som ska ignoreras
        ignored_columns = select_columns_to_ignore(all_columns)

        # Välj alla kolumner utom de som ska ignoreras
        columns_to_consider = [col for col in all_columns if col not in ignored_columns]

        # Antal rader innan dubbletter tas bort
        original_row_count = len(df)
        
        # Hitta dubbletter baserat på de specificerade kolumnerna
        df_duplicates = df[df.duplicated(subset=columns_to_consider, keep=False)]
        
        new_row_count = len(df_duplicates)
        removed_rows = original_row_count - new_row_count

        df_duplicates.to_excel(new_filename, index=False)

        # Skriv ut statistik om ändringarna
        print(f"Endast dubbletter har sparats i den nya filen.")
        print(f"Totalt antal rader i ursprunglig fil: {original_row_count}")
        print(f"Totalt antal rader i nya filen: {new_row_count}")
        print(f"Antal rader som är dubbletter: {new_row_count}")

    except Exception as e:
        print(e)

    print("Endast dubbletter har sparats i den nya filen.")
