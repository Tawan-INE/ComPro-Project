import struct
import os

FILENAME = "data.bin"

def add_record(record_id, name, price, quantity, category):
    with open(FILENAME, 'ab') as f:
        f.write(struct.pack('I20sfI15s', record_id, name.encode('utf-8'), price, quantity, category.encode('utf-8')))

def display_records():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sfI15s'))
            if not record:
                break
            record_id, name, price, quantity, category = struct.unpack('I20sfI15s', record)
            print(f"ID: {record_id}, Name: {name.decode('utf-8').strip()}, Price: {price}, Quantity: {quantity}, Category: {category.decode('utf-8').strip()}")

def retrieve_records(search_value):
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    found = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sfI15s'))
            if not record:
                break
            record_id, name, price, quantity, category = struct.unpack('I20sfI15s', record)
            if str(record_id) == search_value or name.decode('utf-8').strip() == search_value:
                print(f"ID: {record_id}, Name: {name.decode('utf-8').strip()}, Price: {price}, Quantity: {quantity}, Category: {category.decode('utf-8').strip()}")
                found = True
                
    if not found:
        print("No matching records found.")

def update_record(record_id, new_name, new_price, new_quantity, new_category):
    records = []
    updated = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sfI15s'))
            if not record:
                break
            rec_id, name, price, quantity, category = struct.unpack('I20sfI15s', record)
            if rec_id == record_id:
                records.append((record_id, new_name.encode('utf-8'), new_price, new_quantity, new_category.encode('utf-8')))
                updated = True
            else:
                records.append((rec_id, name, price, quantity, category))
    
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack('I20sfI15s', *rec))

    if updated:
        print("Data has been updated successfully")
    else:
        print("No matching record found for update")

def delete_record(record_id):
    records = []
    deleted = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sfI15s'))
            if not record:
                break
            rec_id, name, price, quantity, category = struct.unpack('I20sfI15s', record)
            if rec_id != record_id:
                records.append((rec_id, name, price, quantity, category))
            else:
                deleted = True
    
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack('I20sfI15s', *rec))

    if deleted:
        print("Data has been deleted successfully")
    else:
        print("No matching record found for deletion")

def create_report():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    report_lines = []
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sfI15s'))
            if not record:
                break
            record_id, name, price, quantity, category = struct.unpack('I20sfI15s', record)
            line = f"ID: {record_id}, Name: {name.decode('utf-8').strip()}, Price: {price}, Quantity: {quantity}, Category: {category.decode('utf-8').strip()}"
            report_lines.append(line)
    
    # Display report on console
    print("\n----- Report -----")
    for line in report_lines:
        print(line)

    # Save report to a text file
    with open("report.txt", 'w') as report_file:
        report_file.write("\n".join(report_lines))
    
    print("Report saved to report.txt")

def menu():
    while True:
        print("\nBinary Data Management Program")
        print("1. Add new data")
        print("2. Display all data")
        print("3. Retrieve specific data")
        print("4. Update data")
        print("5. Delete data")
        print("6. Create report")
        print("7. Exit program")
        choice = input("Please choose an option (1-7): ")

        if choice == '1':
            record_id = int(input("Please enter ID: "))
            name = input("Please enter name (up to 20 characters): ")
            price = float(input("Please enter price: "))
            quantity = int(input("Please enter quantity: "))
            category = input("Please enter category (up to 15 characters): ")
            add_record(record_id, name[:20], price, quantity, category[:15])
        elif choice == '2':
            display_records()
        elif choice == '3':
            search_value = input("Please enter ID or name to search: ")
            retrieve_records(search_value)
        elif choice == '4':
            record_id = int(input("Please enter the ID you want to update: "))
            new_name = input("Please enter new name: ")
            new_price = float(input("Please enter new price: "))
            new_quantity = int(input("Please enter new quantity: "))
            new_category = input("Please enter new category: ")
            update_record(record_id, new_name[:20], new_price, new_quantity, new_category[:15])
        elif choice == '5':
            record_id = int(input("Please enter the ID you want to delete: "))
            delete_record(record_id)
        elif choice == '6':
            create_report()
        elif choice == '7':
            print("Closing the program safely")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    menu()
