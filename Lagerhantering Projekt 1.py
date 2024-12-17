'''
FILNAMN.PY: En lagerhanterare som läser IT produkter och hanterar dem

__author__  = "Förnamn Efternamn"
__version__ = "1.0.0"
__email__   = "förnamn.efternamn@elev.ga.ntig.se"
'''

import csv  # Hantera CSV-filer
import os  # För systemfunktioner som att rensa skärmen
from time import sleep  # För att lägga in fördröjningar
from colorama import Fore, Style, init  # För färgad text i terminalen

# Initialisera Colorama
init(autoreset=True)  # Återställer färger automatiskt efter varje utskrift

def load_data(filename):  # Funktion för att ladda produktdata från en CSV-fil
    products = []  # Lista för att lagra produkter
    if not os.path.exists(filename):  # Kontrollera om filen finns
        print(Fore.RED + f"Databasen {filename} finns inte.")
        return products
    with open(filename, 'r') as file:  # Öppnar filen i läsläge
        reader = csv.DictReader(file)  # Läser CSV-filen som en ordlista
        for row in reader:  # Itererar genom varje rad i CSV-filen
            id = int(row['id'])  # Konverterar ID till ett heltal
            name = row['name']  # Hämtar produktnamnet
            desc = row['desc']  # Hämtar beskrivningen
            price = float(row['price'])  # Konverterar priset till flyttal
            quantity = int(row['quantity'])  # Konverterar mängden till heltal
            
            products.append({  # Lägger till en produkt som en ordlista
                "id": id,       
                "name": name,
                "desc": desc,
                "price": price,
                "quantity": quantity
            })
    return products  # Returnerar listan med produkter

def remove_product(products, id):  # Funktion för att ta bort en produkt
    temp_product = None  # Temporär variabel för att lagra produkten
    for product in products:  # Itererar genom produktlistan
        if product["id"] == id:  # Hittar produkten med matchande ID
            temp_product = product  # Sparar produkten
            break  # Avslutar loopen
    if temp_product:  # Om produkten hittades
        products.remove(temp_product)  # Tar bort produkten från listan
        return f"Produkt: {id} {temp_product['name']} har tagits bort"
    else:  # Om produkten inte hittades
        return f"Produkt med id {id} hittades inte"

def view_product(products, id):  # Funktion för att visa en specifik produkt
    for product in products:  # Itererar genom produktlistan
        if product["id"] == id:  # Hittar produkten med matchande ID
            return f"Visar produkt: {product['name']} - {product['desc']} - Pris: {product['price']} - Antal: {product['quantity']}"
    return "Produkten hittas inte"  # Om ingen produkt hittades

def view_products(products):  # Funktion för att visa alla produkter
    product_list = []  # Lista för att lagra produktinformation
    for index, product in enumerate(products, 1):  # Itererar genom produkterna med index
        product_info = f"{index}) (#{product['id']}) {product['name']} \t {product['desc']} \t {product['price']} SEK"
        product_list.append(product_info)  # Lägger till produktinformationen i listan
    
    return "\n".join(product_list)  # Returnerar produkterna som en formatterad sträng

def edit_product(product, name, desc, price, quantity):  # Funktion för att ändra en produkt
    product['name'] = name  # Uppdaterar namnet
    product['desc'] = desc  # Uppdaterar beskrivningen
    product['price'] = price  # Uppdaterar priset
    product['quantity'] = quantity  # Uppdaterar mängden
    return f"Ändrade produkt med id #{product['id']}"

def add_product(products, name, desc, price, quantity):  # Funktion för att lägga till en ny produkt
    max_id = max(products, key=lambda x: x['id'], default={"id": 0})  # Hittar det högsta ID:t i listan, standard är 0
    id_value = max_id['id']  # Hämtar ID-värdet
    id = id_value + 1  # Genererar ett nytt ID
    products.append({  # Lägger till den nya produkten i listan
        "id": id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    })
    return f"Lade till produkt: {id} - {name}"

def show_menu():  # Funktion för att visa huvudmenyn
    os.system('cls' if os.name == 'nt' else 'clear')  # Rensar skärmen
    print(Fore.MAGENTA + Style.BRIGHT + "Välkommen till produktmanagement-systemet!\n")
    print(Fore.CYAN + "Välj ett alternativ:")
    print(Fore.RED + "(V)isa alla produkter")
    print(Fore.RED + "(L)ägg till en produkt")
    print(Fore.RED + "(Ä)ndra en produkt")
    print(Fore.RED + "(T)a bort en produkt")
    print(Fore.RED + "(A)vsluta\n")

def main():  # Huvudfunktion för att köra programmet
    products = load_data('db_products.csv')  # Ladda data från CSV-fil
    while True:  # Oändlig loop för menyval
        show_menu()  # Visar huvudmenyn
        choice = input("Ditt val: ").strip()  # Hämtar användarens val

        if choice == 'V'.lower():  # Visa alla produkter
            os.system('cls' if os.name == 'nt' else 'clear')
            print(view_products(products))
            input("\nTryck Enter för att återvända till menyn.")

        elif choice == 'L'.lower():  # Lägg till produkt
            os.system('cls' if os.name == 'nt' else 'clear')
            print(view_products(products))
            name = input(Fore.MAGENTA + "Namn på produkt: ")
            desc = input("Beskrivning: ")
            try:
                    price = float(input("Pris: "))
                    return price
            except ValueError:
                        print("Ogiltig inmatning. Vänligen ange ett giltigt nummer.")
            try:
                    quantity = int(input("Antal: "))
                    return quantity
            except ValueError:
                        print("Ogiltig inmatning. Vänligen ange ett giltigt nummer.")
            print(add_product(products, name, desc, price, quantity))
            sleep(1)  # Fördröjning innan återgång till menyn

        elif choice == 'Ä'.lower():  # Ändra produkt
            os.system('cls' if os.name == 'nt' else 'clear')
            print(view_products(products))
            id = int(input("Ange produktens ID som du vill ändra: "))
            product = next((p for p in products if p['id'] == id), None)  # Hitta produkt med matchande ID
            if product:
                print(f"Ändrar produkt med id #{id}: {product['name']}")
                name = input("Nytt namn: ")
                desc = input("Ny beskrivning: ")
                price = float(input("Nytt pris: "))
                quantity = int(input("Nytt antal: "))
                print(edit_product(product, name, desc, price, quantity))
            else:
                print(Fore.RED + "Produkten med detta ID finns inte.")
            sleep(1)

        elif choice == 'T'.lower():  # Ta bort produkt
            os.system('cls' if os.name == 'nt' else 'clear')
            print(view_products(products))
            id = int(input("Ange produktens ID som du vill ta bort: "))
            print(remove_product(products, id))
            sleep(1)

        elif choice == 'A'.lower():  # Avsluta programmet
            os.system('cls' if os.name == 'nt' else 'clear')
            # Spara ändringar till CSV 
            with open('db_products.csv', mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
                writer.writeheader()  # Skriver rubrikerna till CSV-filen
                writer.writerows(products)  # Skriver alla produkter till filen
            print(Fore.GREEN + "Data har sparats framgångsrikt.")
            break

        else:  # Hantera ogiltiga val
            print(Fore.RED + "Ogiltigt val, försök igen.")
            sleep(1)

if __name__ == '__main__':
    main() 
