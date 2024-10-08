import struct
import os

FILENAME = "data.bin"

def add_record(record_id, name, price, category, stock_status):
    with open(FILENAME, 'ab') as f:
        f.write(struct.pack('I20sf20s10s', record_id, name.encode('utf-8'), price, category.encode('utf-8'), stock_status.encode('utf-8')))

def display_records():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sf20s10s'))
            if not record:
                break
            record_id, name, price, category, stock_status = struct.unpack('I20sf20s10s', record)
            print(f"ID: {record_id}, Name: {name.decode('utf-8').strip()}, Price: {price:.2f}, Category: {category.decode('utf-8').strip()}, Stock Status: {stock_status.decode('utf-8').strip()}")

def retrieve_records(search_value):
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    found = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sf20s10s'))
            if not record:
                break
            
            record_id, name, price, category, stock_status = struct.unpack('I20sf20s10s', record)
            
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
            stock_status = stock_status.decode('utf-8').strip('\x00')
                        
            if str(record_id) == search_value or name.lower() == search_value.lower():
                print(f"Match found: ID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Stock Status: {stock_status}")
                found = True
                break
    
    if not found:
        print("No matching records found.")

def update_record(record_id, new_name, new_price, new_category, new_stock_status):
    records = []
    updated = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sf20s10s'))
            if not record:
                break
            rec_id, name, price, category, stock_status = struct.unpack('I20sf20s10s', record)
            if rec_id == record_id:
                records.append((record_id, new_name.encode('utf-8'), new_price, new_category.encode('utf-8'), new_stock_status.encode('utf-8')))
                updated = True
            else:
                records.append((rec_id, name, price, category, stock_status))
    
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack('I20sf20s10s', *rec))

    if updated:
        print("Data has been updated!")
    else:
        print("No matching record")

def delete_record(record_id):
    records = []
    deleted = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sf20s10s'))
            if not record:
                break
            rec_id, name, price, category, stock_status = struct.unpack('I20sf20s10s', record)
            if rec_id != record_id:
                records.append((rec_id, name, price, category, stock_status))
            else:
                deleted = True
    
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack('I20sf20s10s', *rec))

    if deleted:
        print("Data has been deleted!")
    else:
        print("No matching record")

def create_report():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    report_lines = []
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(struct.calcsize('I20sf20s10s'))
            if not record:
                break
            record_id, name, price, category, stock_status = struct.unpack('I20sf20s10s', record)
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
            stock_status = stock_status.decode('utf-8').strip('\x00')
            line = f"ID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Stock Status: {stock_status}"
            report_lines.append(line)
    
    with open("report.txt", 'w', encoding='utf-8') as report_file:
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
            name = input("Please enter name: ")
            price = float(input("Please enter price: "))
            category = input("Please enter category: ")
            stock_status = input("Please enter stock status (In Stock / Out of Stock): ")
            add_record(record_id, name, price, category, stock_status)
        
        elif choice == '2':
            display_records()
        
        elif choice == '3':
            search_value = input("Please enter ID or name to search: ")
            retrieve_records(search_value)
        
        elif choice == '4':
            record_id = int(input("Please enter the ID you want to update: "))
            new_name = input("Please enter new name: ")
            new_price = float(input("Please enter new price: "))
            new_category = input("Please enter new category: ")
            new_stock_status = input("Please enter new stock status (In Stock / Out Stock): ")
            update_record(record_id, new_name, new_price, new_category, new_stock_status)
        
        elif choice == '5':
            record_id = int(input("Please enter the ID you want to delete: "))
            delete_record(record_id)
        
        elif choice == '6':
            create_report()
        
        elif choice == '7':
            print("Closing the program")
            break
        
        else:
            print("Invalid option")

menu()
