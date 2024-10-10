import struct
import os

FILENAME = "data.bin"
RECORD_FORMAT = 'I20sf20si'
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)

def add_record(record_id, name, price, category, quantity):
    try:
        with open(FILENAME, 'ab') as f:
            f.write(struct.pack(RECORD_FORMAT, record_id, name.encode('utf-8'), price, category.encode('utf-8'), quantity))
        
        print("\n" + "-" * 50)
        print(f"Data added successfully!\nID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Quantity: {quantity}")
        print("-" * 50)

    except Exception as e:
        print("\n" + "-" * 50)
        print(f"Failed to add Data: {str(e)}")
        print("-" * 50)

def display_records():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return

    print("\n" + "-" * 70)
    print("{:<10} {:<20} {:<10} {:<15} {:<10}".format("ID", "Name", "Price", "Category", "Quantity"))
    print("-" * 70)

    records = []

    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            record_id, name, price, category, quantity = struct.unpack(RECORD_FORMAT, record)
            records.append((record_id, name, price, category, quantity))

    records.sort(key=lambda x: x[0])

    for record_id, name, price, category, quantity in records:
        print("{:<10} {:<20} {:<10.2f} {:<15} {:<10}".format(
            record_id, 
            name.decode('utf-8').strip('\x00'), 
            price, 
            category.decode('utf-8').strip('\x00'), 
            quantity
        ))
    
    print("-" * 70)

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
            
            record_id, name, price, category, quantity = struct.unpack(RECORD_FORMAT, record)
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
                        
            if str(record_id) == search_value or name.lower() == search_value.lower():
                print("\n" + "-" * 50)
                print(f"Match found: ID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Quantity: {quantity}")
                print("-" * 50)
                found = True
                break
    
    if not found:
        print("\nNo matching records found.")

def update_record(record_id):
    records = []
    updated = False
    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            rec_id, name, price, category, quantity = struct.unpack(RECORD_FORMAT, record)
            if rec_id == record_id:
                print("Choose the field to update:")
                print("1. Name")
                print("2. Price")
                print("3. Category")
                print("4. Quantity")
                choice = int(input("Enter your choice (1-4): "))
                if choice == 1:
                    new_name = input("Enter new name: ")
                    records.append((rec_id, new_name.encode('utf-8'), price, category, quantity))
                elif choice == 2:
                    new_price = float(input("Enter new price: "))
                    records.append((rec_id, name, new_price, category, quantity))
                elif choice == 3:
                    new_category = input("Enter new category: ")
                    records.append((rec_id, name, price, new_category.encode('utf-8'), quantity))
                elif choice == 4:
                    new_quantity = int(input("Enter new quantity: "))
                    records.append((rec_id, name, price, category, new_quantity))
                updated = True
            else:
                records.append((rec_id, name, price, category, quantity))
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
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
            rec_id, name, price, category, quantity = struct.unpack(RECORD_FORMAT, record)
            if rec_id != record_id:
                records.append((rec_id, name, price, category, quantity))
            else:
                deleted = True
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')
    with open(FILENAME, 'wb') as f:
        for rec in records:
            f.write(struct.pack(RECORD_FORMAT, *rec))

    print("\n" + "-" * 50)
    if deleted:
        print(f"Data has been deleted!\nID: {record_id}, Name: {name}, Price: {price:.2f}, Category: {category}, Quantity: {quantity}")
    else:
        print("No matching record found.")
    print("-" * 50)

def create_report():
    if not os.path.exists(FILENAME):
        print("Data file not found")
        return
    
    report_lines = []
    records = {}

    with open(FILENAME, 'rb') as f:
        while True:
            record = f.read(RECORD_SIZE)
            if not record:
                break
            record_id, name, price, category, quantity = struct.unpack(RECORD_FORMAT, record)
            name = name.decode('utf-8').strip('\x00')
            category = category.decode('utf-8').strip('\x00')

            if category not in records:
                records[category] = []
            records[category].append((record_id, name, price, quantity))
    
    total_price_all = 0
    total_quantity_all = 0
    total_quantity_in_stock_all = 0
    total_categories = len(records)

    for category, items in records.items():
        total_price = 0
        total_quantity_in_stock = 0
        total_quantity_category = len(items)

        report_lines.append(f"\n หมวดหมู่: {category}")
        report_lines.append("-" * 60)
        report_lines.append("{:<10} {:<25} {:<10} {:<10}".format("ID", "Name", "Price", "Quantity"))
        report_lines.append("-" * 60)
        
        for record_id, name, price, quantity in items:
            report_lines.append("{:<10} {:<25} {:<10.2f} {:<10}".format(record_id, name, price, quantity))
            total_price += price * quantity
            total_quantity_in_stock += quantity
        
        report_lines.append("-" * 60)
        report_lines.append(f"ราคารวม: {total_price:.2f}, จำนวนสินค้าทั้งหมดในหมวดหมู่: {total_quantity_category}")
        report_lines.append(f"จำนวนของสินค้าที่มีอยู่ในสต็อก: {total_quantity_in_stock}")
        report_lines.append("=" * 60)

        total_price_all += total_price
        total_quantity_all += total_quantity_category
        total_quantity_in_stock_all += total_quantity_in_stock

    report_lines.append("\nสรุปรวมทั้งหมด")
    report_lines.append("-" * 60)
    report_lines.append(f"ราคารวมทั้งหมด: {total_price_all:.2f}")
    report_lines.append(f"จำนวนสินค้าทั้งหมด: {total_quantity_all}")
    report_lines.append(f"จำนวนหมวดหมู่ทั้งหมด: {total_categories}")
    report_lines.append("-" * 60)
    report_lines.append("\n")

    with open("report.txt", 'w', encoding='utf-8') as report_file:
        for line in report_lines:
            report_file.write(line + "\n")
    
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
        
        try:
            choice = int(input("Please choose an option (1-7): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")

        if choice == 1:
            record_id = int(input("Please enter ID: "))
            name = input("Please enter name: ")
            price = float(input("Please enter price: "))
            category = input("Please enter category: ")
            quantity = int(input("Please enter quantity: "))
            add_record(record_id, name, price, category, quantity)
        
        elif choice == 2:
            display_records()
        
        elif choice == 3:
            search_value = input("Please enter ID or name to search: ")
            retrieve_records(search_value)
        
        elif choice == 4:
            try:
                record_id = int(input("Please enter the ID you want to update: "))
                update_record(record_id)
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
            user_input = input("Please confirm to Exit the Program (y / n): ").lower()
            if user_input == 'y':
                print("Exiting the program")
                break
            elif user_input == 'n':
                print("Returning the program")
                continue
            else:
                print("Invalid input, please enter 'y' for yes or 'n' for no.")
                continue

main()