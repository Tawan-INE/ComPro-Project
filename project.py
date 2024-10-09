import struct
import os

FILENAME = "data.bin"
RECORD_FORMAT = 'I20sf20s10s'
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

def add_record(record_id, name, price, category, stock_status):
    with open(FILENAME, 'ab') as f:
        f.write(struct.pack(RECORD_FORMAT, record_id, name.encode('utf-8'), price, category.encode('utf-8'), stock_status.encode('utf-8')))

def display_records():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return

    print("\n" + "-" * 50)
    print("Current Records:")
    print("-" * 50)

    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            record_id, name, price, category, stock_status = struct.unpack(RECORD_FORMAT, record)
            print(f"ID: {record_id}, Name: {name.decode('utf-8').strip()}, Price: {price:.2f}, Category: {category.decode('utf-8').strip()}, Stock Status: {stock_status.decode('utf-8').strip()}")
    print("-" * 50)

def retrieve_records(search_value):
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    found = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            
            record_id, name, price, category, stock_status = struct.unpack(RECORD_FORMAT, record)
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
            stock_status = stock_status.decode('utf-8').strip('\x00')
                        
            if str(record_id) == search_value or name.lower() == search_value.lower():
                print("\n" + "-" * 50)
                print(f"Match found: ID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Stock Status: {stock_status}")
                print("-" * 50)
                found = True
                break
    
    if not found:
        print("\nNo matching records found.")

def update_record(record_id, new_name, new_price, new_category, new_stock_status):
    records = []
    updated = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            rec_id, name, price, category, stock_status = struct.unpack(RECORD_FORMAT, record)
            if rec_id == record_id:
                records.append((record_id, new_name.encode('utf-8'), new_price, new_category.encode('utf-8'), new_stock_status.encode('utf-8')))
                updated = True
            else:
                records.append((rec_id, name, price, category, stock_status))
    
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack(RECORD_FORMAT, *rec))

    print("\n" + "-" * 50)
    if updated:
        print("Data has been updated!") 
    else:
        print("No matching record found.")
    print("-" * 50)

def delete_record(record_id):
    records = []
    deleted = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            rec_id, name, price, category, stock_status = struct.unpack(RECORD_FORMAT, record)
            if rec_id != record_id:
                records.append((rec_id, name, price, category, stock_status))
            else:
                deleted = True
    
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack(RECORD_FORMAT, *rec))

    print("\n" + "-" * 50)
    if deleted:
        print("Data has been deleted!")
    else:
        print("No matching record found.")
    print("-" * 50)

def create_report():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    report_lines = []
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            record_id, name, price, category, stock_status = struct.unpack(RECORD_FORMAT, record)
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
            stock_status = stock_status.decode('utf-8').strip('\x00')
            line = f"ID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Stock Status: {stock_status}"
            report_lines.append(line)
    
    with open("report.txt", 'w', encoding='utf-8') as report_file:
        report_file.write("\n".join(report_lines))
    
    print("\n" + "-" * 50)
    print("Report saved to report.txt")
    print("-" * 50)

def main():
    while True:
        print("\n" + "=" * 50)
        print("   Convenience Store Management Program")
        print("=" * 50)
        print("1. Add new data")
        print("2. Display all data")
        print("3. Retrieve specific data")
        print("4. Update data")
        print("5. Delete data")
        print("6. Create report")
        print("7. Exit program")
        
        choice = int(input("Please choose an option (1-7): "))

        if choice == 1:
            record_id = int(input("Please enter ID: "))
            name = input("Please enter name: ")
            price = float(input("Please enter price: "))
            category = input("Please enter category: ")
            stock_status = input("Please enter stock status (In Stock / Out of Stock): ")
            add_record(record_id, name, price, category, stock_status)
        
        elif choice == 2:
            display_records()
        
        elif choice == 3:
            search_value = input("Please enter ID or name to search: ")
            retrieve_records(search_value)
        
        elif choice == 4:
            try:
                record_id = int(input("Please enter the ID you want to update: "))
                new_name = input("Please enter new name: ")
                new_price = float(input("Please enter new price: "))
                new_category = input("Please enter new category: ")
                new_stock_status = input("Please enter new stock status (In Stock / Out Stock): ")
                update_record(record_id, new_name, new_price, new_category, new_stock_status)
            except ValueError:
                print("Invalid input. Please enter the correct data type.")
        
        elif choice == 5:
            try:
                record_id = int(input("Please enter the ID you want to delete: "))
                delete_record(record_id)
            except ValueError:
                print("Invalid input. Please enter a valid ID.")
        
        elif choice == 6:
            create_report()
        
        elif choice == 7: 
            print("Closing the program")
            break
        
        else:
            print("Invalid option")

main()
