import csv
import os

def menu(username="@prof-rossetti", products_count=50):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Resets list to default.
    Please select an operation: """ # end of multi- line string. also using string interpolation
    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            #print(row["name"], row["price"])
            products.append(dict(row))
    return(products)
    #TODO: open the file and populate the products list with product dictionaries
    return products

def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    #print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    #TODO: open the file and write a list of dictionaries. each dict should represent a product.
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id","name","aisle","department","price"])
        writer.writeheader() # uses fieldnames set above
        # writer.writerow({"city": "New York", "name": "Yankees"})
        # writer.writerow({"city": "New York", "name": "Mets"})
        # writer.writerow({"city": "Boston", "name": "Red Sox"})
        # writer.writerow({"city": "New Haven", "name": "Ravens"})
        for p in products:
            writer.writerow(p)

def auto_incremented_id(products):
    all_ids = [int(p["id"]) for p in products]
    max_id = max(all_ids)
    next_id = max_id + 1
    return next_id

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print('''
    ----------------------------------------------------
    RESETTING DEFAULTS:
    ----------------------------------------------------
    ''')
    products = read_products_from_file(from_filename)
    print(len(products))
    write_products_to_file(filename, products)

# def enlarge(my_number):
#     return my_number * 100

list_product = '''
----------------------------------------------------
LISTING NEW PRODUCTS:
----------------------------------------------------
'''
show_product = '''
----------------------------------------------------
SHOWING A PRODUCT:
----------------------------------------------------
'''
create_product = '''
----------------------------------------------------
CREATING A NEW PRODUCT:
----------------------------------------------------
'''
update_product = '''
----------------------------------------------------
UPDATING A PRODUCT:
----------------------------------------------------
'''
destroy_product = '''
----------------------------------------------------
DESTROYING A PRODUCT:
----------------------------------------------------
'''

def run():
    # First, read products from file...
    products = read_products_from_file()
    product_ids = [p["id"] for p in products]
    print("----------------------------------------------------")
    print("INVENTORY MANAGEMENT APPLICATION")
    print("----------------------------------------------------")
    print ("There are " + str(len(products)) + " products in the database")

    my_menu = menu(username="@jnt303", products_count=len(products))
    #print(my_menu) #TODO instead of printing, capture user input
    while True:
        try:
            op_select = input(my_menu)
            op_select = op_select.title()
            if op_select == "List":
                print(list_product)
                for p in products:
                    print("#" + p["id"] + ": " + p["name"])
                break
            elif op_select == "Show":
                prod_id = input("Please input the product's 'id': ")
                if prod_id not in product_ids:
                    print("I'm sorry. Product not found.")
                    break
                matching_products = [p for p in products if int(p["id"]) == int(prod_id)]
                matching_product = matching_products[0]
                print(show_product)
                print(matching_product)
                break

            elif op_select == "Create":
                new_id = auto_incremented_id(products)
                new_name = input("Please input the product's 'name': ")
                new_aisle = input("Please input the product's 'aisle': ")
                new_dept = input("Please input the product's 'department': ")
                new_price = input("Please input the product's 'price': ")
                print(create_product)
                new_product = {
                    "id": new_id,
                    "name": new_name,
                    "aisle": new_aisle,
                    "department": new_dept,
                    "price": new_price
                }
                #print(new_product)
                products.append(new_product)
                print(new_product)
                break

            elif op_select == "Update":
                prod_id = input("Please input the product's 'id': ")
                if prod_id not in product_ids:
                    print("I'm sorry. Product not found.")
                    break
                matching_products = [p for p in products if int(p["id"]) == int(prod_id)]
                matching_product = matching_products[0]
                new_name = input("Please input the product's new 'name': ")
                matching_product["name"] = new_name
                new_aisle = input("Please input the product's new 'aisle': ")
                matching_product["aisle"] = new_aisle
                new_dept = input("Please input the product's new 'department': ")
                matching_product["department"] = new_dept
                new_price = input("Please input the product's new 'price': ")
                matching_product["price"] = new_price
                print(update_product)
                print(matching_product)
                break

            elif op_select == "Destroy":
                prod_id = input("Please input the product's 'id': ")
                matching_products = [p for p in products if int(p["id"]) == int(prod_id)]
                if prod_id not in product_ids:
                    print("I'm sorry. Product not found.")
                    break
                matching_product = matching_products[0]
                del products[products.index(matching_product)]
                print(destroy_product)
                break
            elif op_select == "Exit":
                break
            elif op_select == "Reset":
                reset_products_file()

            else:
                print("Unrecognized Operation. Please choose one of: 'List', 'Show', 'Create', 'Update', 'Destroy'")
                continue

        except ValueError:
            print("I'm sorry. Product not found.")
            break
                # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
                #TODO: handle selected operation

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)

# only prompt the user for input if this script is run from the command-line
# this allows us to import and test this application's component functions
if __name__ == "__main__": #just means if this script is being run from the command line
    run() #whatever is here will be invoked from the command line
