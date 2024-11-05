import tkinter as tk
from tkinter import ttk,simpledialog,messagebox,Label,Entry,Button,filedialog
from PIL import Image, ImageTk
import sqlite3


# Functionality Portion


totalPrice = 0

def connectandcreatetable():
# Connect to SQLite database
    conn = sqlite3.connect('gascylinder.db')
    cursor = conn.cursor()


# =======================================================================================
    # Creating tables
# =======================================================================================

    # -------------Inventory Table creation---------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        batch_no INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        purchase_price REAL NOT NULL,
        date_received DATE NOT NULL
        )
    ''')
    conn.commit()

    # -------------Sales Table creation--------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_item REAL NOT NULL,
            total_price REAL NOT NULL,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
connectandcreatetable()

# # ===================================================================================================
# # Below this line coding
# # ===================================================================================================

class CustomDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Enter Details")
        
        Label(self, text="Enter Quantity:", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=0, column=0, padx=10, pady=5)
        self.quantity_entry = Entry(self,font=('arial',15),bd=7,width=18)
        self.quantity_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self, text="Enter Price:", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=1, column=0, padx=10, pady=5)
        self.price_entry = Entry(self,font=('arial',15),bd=7,width=18)
        self.price_entry.grid(row=1, column=1, padx=10, pady=5)

        Button(self, text="Submit", command=self.on_submit, font=('arial', 12, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10).grid(row=2, columnspan=2, pady=10)

    def on_submit(self):
        self.quantity = self.quantity_entry.get()
        self.price = self.price_entry.get()
        self.destroy()

def extra_function_1(textArea,root):

    textArea.insert(1.0,'\t   ***Medical Store***\n\n')
    textArea.insert(tk.END,'\tContact # :0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
    textArea.insert(tk.END,'========================================\n')
    textArea.insert(tk.END,' Item \t     Unit \t  Quantity\t   Total \n')
    textArea.insert(tk.END,' Name \t     Price \t\t         Price \n')
    textArea.insert(tk.END,'========================================\n')

    dialog = CustomDialog(root) 
    root.wait_window(dialog)

    # query = "SELECT quantity FROM inventory WHERE item_name = ?"

    # conn = sqlite3.connect('gascylinder.db')
    # cursor = conn.cursor()
    # cursor.execute(query, (item,))
    # result = cursor.fetchone()

    # if result is not None: 
    #     priceofitem = result[0] 
    #     quantityofitem = result[1] 

    # else: 
    #     print("No matching record found.") # Handle the case where no record is found


    itemQuantity = dialog.quantity
    itemPrice = dialog.price
    print(itemPrice,itemQuantity)

# ===================================================================================================
# Inventory Management function
# ===================================================================================================

def extra_function_2(root):
    print("Button 2 clicked")

# def open_inventory_window():
    inventory_window = tk.Toplevel(root)
    inventory_window.title("Inventory Management")
    inventory_window.geometry("800x500")
    # center_window(inventory_window)

    headingLabel = tk.Label(inventory_window, text="Inventory Management", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
    headingLabel.pack(fill=tk.X, pady=5)

    # Project Details
    treeviewFrame = tk.Frame(inventory_window, background='gray20', bd=8, relief=tk.GROOVE)
    treeviewFrame.pack(fill=tk.X, pady=5)

    columns = ('#1', '#2', '#3', '#4', '#5', '#6')
    tree = ttk.Treeview(treeviewFrame, columns=columns, show='headings')
    tree.heading('#1', text='Sr')
    tree.heading('#2', text='Item Name')
    tree.heading('#3', text='Batch Number')
    tree.heading('#4', text='Quantity')
    tree.heading('#5', text='Purchased Price')
    tree.heading('#6', text='Purchased Date')

    # Setting column widths
    tree.column('#1', width=30)
    tree.column('#2', width=150)
    tree.column('#3', width=100)
    tree.column('#4', width=100)
    tree.column('#5', width=70)
    tree.column('#6', width=70)

    # Adding Vertical Scrollbar
    vsb = ttk.Scrollbar(treeviewFrame, orient="vertical", command=tree.yview)
    vsb.pack(side='right', fill='y')
    tree.configure(yscrollcommand=vsb.set)

    # Adding Horizontal Scrollbar
    hsb = ttk.Scrollbar(treeviewFrame, orient="horizontal", command=tree.xview)
    hsb.pack(side='bottom', fill='x')
    tree.configure(xscrollcommand=hsb.set)
    tree.pack(fill='both', expand=True)

    # Configure Treeview Style 
    style = ttk.Style() 
    style.configure("Treeview", rowheight=25) 
    style.configure("Treeview.Heading", font=('Calibri', 10,'bold')) 
    style.map('Treeview', background=[('selected', 'blue')])

    def clear_treeview():
        for item in tree.get_children():
            tree.delete(item)

    # Reading Data from DB and inserting into Treeview
    def readintotreeview():
        conn = sqlite3.connect('gascylinder.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory;")
        completeRow = cursor.fetchall()

        conn.close()

        clear_treeview()

        # projectsList.delete(0, tk.END)
        tree.tag_configure('low', background='red', foreground='white')
        for record in completeRow:
            # projectsList.insert(tk.END, f'{record[0]}')
            tag = "low" if record[4] < 10 else ""
            tree.insert('', 'end', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=(tag,))

    
    readintotreeview()


    # Add edit, delete, update buttons
    def edit_item():
        pass  # Add your logic here

    # def delete_item():
    #     pass  # Add your logic here
    def delete_item():
        selected_item = tree.selection()[0]  # Get selected item
        item_values = tree.item(selected_item, 'values')  # Get values of the selected item
        item_id = item_values[0]  # Assuming 'id' is the first value in the tuple

        conn = sqlite3.connect('gascylinder.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM inventory WHERE id = ?
        ''', (item_id,))
        conn.commit()
        conn.close()

        # tree.delete(selected_item)  # Remove the item from Treeview
        readintotreeview()
        # readitems()


    # def update_item():
    #     pass  # Add your logic here

    def update_item():
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')

        update_window = tk.Toplevel(inventory_window)
        update_window.title("Update Entry")
        update_window.geometry("450x420")

        headingLabel = tk.Label(update_window, text="Edit", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
        headingLabel.pack(fill=tk.X, pady=5)

        # Create form labels and entries
        editentryFrame = tk.Frame(update_window, background='gray20', bd=8, relief=tk.GROOVE)
        editentryFrame.pack(fill=tk.X, pady=5)

        tk.Label(editentryFrame, text="Item Name", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=0, column=0, padx=10, pady=5)
        item_name_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        item_name_entry.grid(row=0, column=1, padx=10, pady=5)
        item_name_entry.insert(0, values[1])

        tk.Label(editentryFrame, text="Batch No", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=1, column=0, padx=10, pady=5)
        batch_no_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        batch_no_entry.grid(row=1, column=1, padx=10, pady=5)
        batch_no_entry.insert(0, values[2])

        tk.Label(editentryFrame, text="Quantity", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=2, column=0, padx=10, pady=5)
        quantity_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)
        quantity_entry.insert(0, values[3])

        tk.Label(editentryFrame, text="Purchased Price", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=3, column=0, padx=10, pady=5)
        price_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        price_entry.grid(row=3, column=1, padx=10, pady=5)
        price_entry.insert(0, values[4])

        tk.Label(editentryFrame, text="Purchased Date", font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=4, column=0, padx=10, pady=5)
        purchaseddate_entry = tk.Entry(editentryFrame,font=('arial',15),bd=7,width=18)
        purchaseddate_entry.grid(row=4, column=1, padx=10, pady=5)
        purchaseddate_entry.insert(0, values[5])

        def save_changes():
            conn = sqlite3.connect('gascylinder.db')
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE inventory
                SET item_name=?, batch_no=?, quantity=?, purchase_price=?, date_received=?
                WHERE id=?
            ''', (item_name_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get(), purchaseddate_entry.get(), values[0]))
            conn.commit()
            conn.close()

            # Update Treeview
            # tree.item(selected_item, values=(values[0], med_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get()))
            readintotreeview()
            # readitems()
            update_window.destroy()

        tk.Button(editentryFrame, text="Save", font=('arial', 12, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10,command=save_changes).grid(row=5, column=0, columnspan=2, pady=10)

    inventorybuttonFrame = tk.Frame(inventory_window, background='gray20', bd=8, relief=tk.GROOVE)
    inventorybuttonFrame.pack(fill=tk.X, pady=5)

    # Buttons
    add_button = tk.Button(inventorybuttonFrame, text="New Entry", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=open_new_entry_window)
    add_button.pack(side='left')

    # edit_button = tk.Button(inventorybuttonFrame, text="Edit", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=edit_item)
    # edit_button.pack(side='left')

    delete_button = tk.Button(inventorybuttonFrame, text="Delete", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=delete_item)
    delete_button.pack(side='left')

    print_button = tk.Button(inventorybuttonFrame, text="Print", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=update_item)
    print_button.pack(side='right')

    update_button = tk.Button(inventorybuttonFrame, text="Update", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=update_item)
    update_button.pack(side='right')

def extra_function_3(root):
    # print("Button 3 clicked")
    # def open_new_entry_window():
    new_entry_window = tk.Toplevel(root)
    new_entry_window.title("New Entry")
    new_entry_window.geometry("550x450")
    # center_window(new_entry_window)

    headingLabel = tk.Label(new_entry_window, text="New Entry", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
    headingLabel.pack(fill=tk.X, pady=5)

    # Create form labels and entries
    newentryFrame = tk.Frame(new_entry_window, background='gray20', bd=8, relief=tk.GROOVE)
    newentryFrame.pack(fill=tk.X, pady=5)
    
    tk.Label(newentryFrame, text="Item Name",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=0, column=0, padx=10, pady=5)
    item_name_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
    item_name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(newentryFrame, text="Batch No",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=1, column=0, padx=10, pady=5)
    batch_no_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
    batch_no_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(newentryFrame, text="Quantity",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=2, column=0, padx=10, pady=5)
    quantity_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
    quantity_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(newentryFrame, text="Purchased Price",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=3, column=0, padx=10, pady=5)
    price_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
    price_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(newentryFrame, text="Purchased Date (YYYY-MM-DD)",font=('times new roman',15,'bold'),background='gray20',foreground='white').grid(row=4, column=0, padx=10, pady=5)
    purchaseddate_entry = tk.Entry(newentryFrame,font=('arial',15),bd=7,width=18)
    purchaseddate_entry.grid(row=4, column=1, padx=10, pady=5)

    

    # Function to insert data into database
    def add_entry():
        conn = sqlite3.connect('gascylinder.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (item_name,  batch_no, quantity, purchase_price, date_received)
            VALUES (?, ?, ?, ?, ?)
        ''', (item_name_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get(),  purchaseddate_entry.get()))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        # Insert new data into Treeview 
        # tree.insert('', 'end', values=(new_id, medicine_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get()))
        # readintotreeview() 
        # readitems()
        new_entry_window.destroy()

    # Add submit button
    submit_button = tk.Button(newentryFrame, text="Submit", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10,command=add_entry)
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)

def extra_function_4(index,images,buttons):
    print("Extra function 1 executed!")

def writeintotextarea():
    pass

def change_icon(index, images, icon_labels):
    file_path = filedialog.askopenfilename()
    if file_path:
        new_image = Image.open(file_path)
        new_image = new_image.resize((85, 85), Image.LANCZOS)
        new_photo = ImageTk.PhotoImage(new_image)
        
        images[index] = new_photo  # Update the stored image reference
        icon_labels[index].config(image=new_photo)
        icon_labels[index].image = new_photo  # Keep a reference to the new image

def extra_function():
    print("Extra function executed!")

def create_dashboard():
    root = tk.Tk()
    root.title("Colorful Dashboard")
    root.geometry("1000x600")

    # Head Frame
    up_frame = tk.Frame(root, bg='orange', height=50)
    up_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
    tk.Label(up_frame, text="ITTEFAQ TRADERS", font=('Helvetica', 24, 'bold'), bg='orange', fg='green').pack(pady=10)
    
    # Left Frame
    left_frame = tk.Frame(root, bg='lightblue', width=350)
    left_frame.grid(row=1, column=0, sticky='ns')
    scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    textArea = tk.Text(left_frame, bg='lightblue', height=30, width=50)
    textArea.pack()
    textArea.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=textArea.yview)

    # Right Frame
    right_frame = tk.Frame(root, bg='lightgray')
    right_frame.grid(row=1, column=1, sticky='nsew')

    # Adding a grid of image icons to the right frame
    image_paths = [
        "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/addicon.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG",
        "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG",
        "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg",
        "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/addicon.jpg", "C:/Users/sc/Client gas/color-dashboard/images/sales.JPG", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg"
    ]
    
    images = []
    icon_labels = []
    extra_functions = [extra_function_1, extra_function_2, extra_function_3, extra_function_4] # Add more functions as needed
    for index, image_path in enumerate(image_paths):
        row = index // 4
        col = index % 4
        try:
            image = Image.open(image_path)
            image = image.resize((85, 85), Image.LANCZOS)
            img = ImageTk.PhotoImage(image)
            images.append(img)  # Store the reference to avoid garbage collection

            # Create a frame to hold the icon and the small button
            frame = tk.Frame(right_frame, padx=5, pady=5)
            frame.grid(row=row, column=col)

            # Create the icon label
            icon_label = tk.Label(frame, image=img, compound='top')
            icon_label.grid(row=0, column=0)
            icon_label.bind("<Button-1>", lambda e, idx=index: change_icon(idx, images, icon_labels))
            icon_labels.append(icon_label)

            # Create the small button below the icon label
            if index < len(extra_functions):
                extra_button = tk.Button(frame, text="Extra Button", command=extra_functions[index])
            else:
                extra_button = tk.Button(frame, text="Extra Button", command=lambda: print(f"Extra function for index {index}"))
            extra_button.grid(row=1, column=0)

        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
    
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.mainloop()

create_dashboard()










# def create_dashboard():
#     root = tk.Tk()
#     root.title("Colorful Dashboard")
#     root.geometry("1000x600")

#     # head Frame
#     up_frame = tk.Frame(root, bg='orange', height=50)
#     up_frame.grid(row=0, column=0, columnspan=2, sticky='ew')
#     tk.Label(up_frame, text="ITTEFAQ TRADERS", font=('Helvetica', 24, 'bold'), bg='orange', fg='green').pack(pady=10)
    
#     # Left Frame
#     left_frame = tk.Frame(root, bg='lightblue', width=350)
#     left_frame.grid(row=1, column=0, sticky='ns')
#     scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL)
#     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
#     textArea = tk.Text(left_frame, bg='lightblue', height=30, width=50)
#     textArea.pack()
#     textArea.config(yscrollcommand=scrollbar.set)
#     scrollbar.config(command=textArea.yview)

#     # Right Frame
#     right_frame = tk.Frame(root, bg='lightgray')
#     right_frame.grid(row=1, column=1, sticky='nsew')

#     # Adding a grid of image buttons to the right frame
#     image_paths = [
#         "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/addicon.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG",
#         "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG", "C:/Users/sc/Client gas/color-dashboard/images/img.JPG",
#         "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg",
#         "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg", "C:/Users/sc/Client gas/color-dashboard/images/addicon.jpg", "C:/Users/sc/Client gas/color-dashboard/images/sales.JPG", "C:/Users/sc/Client gas/color-dashboard/images/invt.jpg"
#     ]
    
#     images = []
#     buttons =[]
#     for index, image_path in enumerate(image_paths):
#         row = index // 4
#         col = index % 4
#         try:
#             image = Image.open(image_path)
#             image = image.resize((85, 85), Image.LANCZOS)
#             img = ImageTk.PhotoImage(image)
#             images.append(img)  # Store the reference to avoid garbage collection

#             # Create a frame to hold the icon and the small button 
#             frame = tk.Frame(root, padx=5, pady=5) 
#             frame.grid(row=row, column=col)

#             # Create the icon button 
#             icon_button = tk.Button(frame, image=img, compound='top', font=('Arial', 10, 'bold')) 
#             icon_button.grid(row=0, column=0) .buttons.append(icon_button)

#             # Create the small button below the icon button 
#             change_button = tk.Button(frame, text="Change Icon", command=lambda idx=index: button_command_4(idx)) 
#             change_button.grid(row=1, column=0)

#             # if index == 0:
#             #     button.config(command=lambda: button_command_1(textArea,root))
#             #     # print("Command assigned to Button 1")

#             # elif index == 1:
#             #     button.config(command=lambda idx=index: button_command_2(root))
#             #     # print("Command assigned to Button 2")

#             # elif index == 2:
#             #     button.config(command=lambda idx=index: button_command_3(root))
#             #     # print("Command assigned to Button 14")
            
#             # elif index == 3:
#             #     button.config(command=lambda idx=index: button_command_4(index, images, buttons))
#             #     # print("Command assigned to Button 14")
                
#             # else:
#             #     # print('Other Button Clicked')
#             #     button.config(command=lambda row=row, col=col: print(f"Button {row*4+col+1} clicked"))

#             # button.grid(row=row, column=col, padx=10, pady=10)
#         except Exception as e:
#             print(f"Error loading image {image_path}: {e}")
#     root.grid_rowconfigure(1, weight=1) 
#     root.grid_columnconfigure(1, weight=1)
    
#     root.mainloop()

# create_dashboard()






# def center_window(window):
#     window.update_idletasks()
#     width = window.winfo_width()
#     height = window.winfo_height()
#     x = (window.winfo_screenwidth() // 2) - (width // 2)
#     y = (window.winfo_screenheight() // 2) - (height // 2)
#     window.geometry(f'{width}x{height}+{x}+{y}')


# def open_summary_view():

#     def clearsummary():
#         pass

#     def printsummary():
#         pass

#     summary_view_window = tk.Toplevel()
#     summary_view_window.title("Summary View")
#     summary_view_window.geometry("1000x500")
#     center_window(summary_view_window)

#     headingLabel = tk.Label(summary_view_window, text="Summary View", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
#     headingLabel.pack(fill=tk.X, pady=5)

#     treeviewFrame = tk.Frame(summary_view_window, background='gray20', bd=8, relief=tk.GROOVE)
#     treeviewFrame.pack(fill=tk.X, pady=5)

#     columns = ("item_name", "purchased_price", "sale_price", "sale_quantity", "total_sale_price", "average_sale_price", "profit_per_item", "total_profit")
#     tree = ttk.Treeview(treeviewFrame, columns=columns, show='headings')
#     tree.heading("item_name", text="Item Name")
#     tree.heading("purchased_price", text="Purchased Price")
#     tree.heading("sale_price", text="Sale Price")
#     tree.heading("sale_quantity", text="Sale Quantity")
#     tree.heading("total_sale_price", text="Total Sale Price")
#     tree.heading("average_sale_price", text="Average Sale Price")
#     tree.heading("profit_per_item", text="Profit Per Item")
#     tree.heading("total_profit", text="Total Profit")

#     tree.column("item_name", width=150)
#     tree.column("purchased_price", width=100)
#     tree.column("sale_price", width=100)
#     tree.column("sale_quantity", width=100)
#     tree.column("total_sale_price", width=120)
#     tree.column("average_sale_price", width=120)
#     tree.column("profit_per_item", width=120)
#     tree.column("total_profit", width=120)

#     # Adding Vertical Scrollbar
#     vsb = ttk.Scrollbar(treeviewFrame, orient="vertical", command=tree.yview)
#     vsb.pack(side='right', fill='y')
#     tree.configure(yscrollcommand=vsb.set)

#     # Adding Horizontal Scrollbar
#     hsb = ttk.Scrollbar(treeviewFrame, orient="horizontal", command=tree.xview)
#     hsb.pack(side='bottom', fill='x')
#     tree.configure(xscrollcommand=hsb.set)
#     tree.pack(fill='both', expand=True)

#     # Fetch and compare data
#     conn = sqlite3.connect('gascylinder.db')
#     cursor = conn.cursor()
#     query = '''
#         SELECT i.item_name, i.purchase_price,
#                (SELECT s.price_per_item FROM sales s WHERE s.item_name = i.item_name LIMIT 1) AS sale_price,
#                (SELECT SUM(s.quantity) FROM sales s WHERE s.item_name = i.item_name) AS sale_quantity,
#                (SELECT SUM(s.total_price) FROM sales s WHERE s.item_name = i.item_name) AS total_sale_price,
#                (SELECT AVG(s.price_per_item) FROM sales s WHERE s.item_name = i.item_name) AS average_sale_price,
#                ((SELECT AVG(s.price_per_item) FROM sales s WHERE s.item_name = i.item_name) - i.purchase_price) AS profit_per_item,
#                (((SELECT AVG(s.price_per_item) FROM sales s WHERE s.item_name = i.item_name) - i.purchase_price) * (SELECT SUM(s.quantity) FROM sales s WHERE s.item_name = i.item_name)) AS total_profit
#         FROM inventory i
#     '''
#     cursor.execute(query)
#     summary_data = cursor.fetchall()
#     conn.close()
#     # print(f"Fetched summary data: {summary_data}")

#     for record in summary_data:
#         tree.insert('', 'end', values=record)

#     # Configure Treeview Style
#     style = ttk.Style()
#     style.configure("Treeview", rowheight=25)
#     style.configure("Treeview.Heading", font=('Calibri', 10,'bold'))
#     style.map('Treeview', background=[('selected', 'blue')])

#     inventorybuttonFrame = tk.Frame(summary_view_window, background='gray20', bd=8, relief=tk.GROOVE)
#     inventorybuttonFrame.pack(fill=tk.X, pady=5)

#     # Buttons
    
#     delete_button = tk.Button(inventorybuttonFrame, text="Delete", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=clearsummary)
#     delete_button.pack(side='left')

#     print_button = tk.Button(inventorybuttonFrame, text="Print", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=printsummary)
#     print_button.pack(side='right')


# # ===================================================================================================
# # Sales Management function
# # ===================================================================================================

# def open_sales_window():

#     def open_sales_view():

#         def clear_treeview():
#             for item in tree.get_children():
#                 tree.delete(item)

#         def delete_item():
#             selected_item = tree.selection()[0]  # Get selected item
#             item_values = tree.item(selected_item, 'values')  # Get values of the selected item
#             item_id = item_values[0]  # Assuming 'id' is the first value in the tuple

#             conn = sqlite3.connect('gascylinder.db')
#             cursor = conn.cursor()
#             cursor.execute('''
#                 DELETE FROM sales WHERE sale_id = ?
#             ''', (item_id,))
#             conn.commit()
#             conn.close()
#             clear_treeview()

#             # tree.delete(selected_item)  # Remove the item from Treeview
#             readsales()
#             readitems()

#         def printsalesview():
#             pass

#         sales_view_window = tk.Toplevel()
#         sales_view_window.title("Sales Records")
#         sales_view_window.geometry("800x500")
#         center_window(sales_view_window)

#         headingLabel = tk.Label(sales_view_window, text="Sales Records", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
#         headingLabel.pack(fill=tk.X, pady=5)

#         treeviewFrame = tk.Frame(sales_view_window, background='gray20', bd=8, relief=tk.GROOVE)
#         treeviewFrame.pack(fill=tk.X, pady=5)

#         columns = ("sale_id", "item_name", "quantity", "price_per_item", "total_price", "sale_date")
#         tree = ttk.Treeview(treeviewFrame, columns=columns, show='headings')
#         tree.heading("sale_id", text="Sale ID")
#         tree.heading("item_name", text="Item Name")
#         tree.heading("quantity", text="Quantity")
#         tree.heading("price_per_item", text="Price per Item")
#         tree.heading("total_price", text="Total Price")
#         tree.heading("sale_date", text="Sale Date")

#         # Setting column widths
#         tree.column("sale_id", width=30)
#         tree.column("item_name", width=150)
#         tree.column("quantity", width=100)
#         tree.column("price_per_item", width=100)
#         tree.column("total_price", width=70)
#         tree.column("sale_date", width=70)

#         # Adding Vertical Scrollbar
#         vsb = ttk.Scrollbar(treeviewFrame, orient="vertical", command=tree.yview)
#         vsb.pack(side='right', fill='y')
#         tree.configure(yscrollcommand=vsb.set)

#         # Adding Horizontal Scrollbar
#         hsb = ttk.Scrollbar(treeviewFrame, orient="horizontal", command=tree.xview)
#         hsb.pack(side='bottom', fill='x')
#         tree.configure(xscrollcommand=hsb.set)
#         tree.pack(fill='both', expand=True)

        
#         # Configure Treeview Style
#         style = ttk.Style()
#         style.configure("Treeview", rowheight=25)
#         style.configure("Treeview.Heading", font=('Calibri', 10,'bold'))
#         style.map('Treeview', background=[('selected', 'blue')])

#         # Fetch sales data from the database
#         def readsales():

#             conn = sqlite3.connect('gascylinder.db')
#             cursor = conn.cursor()

#             cursor.execute("SELECT * FROM sales")
#             sales_data = cursor.fetchall()
#             conn.close()
#             # print(f"Fetched sales data: {sales_data}")

#             for sale in sales_data:
#                 tree.insert('', 'end', values=sale)

#             tree.pack(fill='both', expand=True)
        
#         readsales()


#         inventorybuttonFrame = tk.Frame(sales_view_window, background='gray20', bd=8, relief=tk.GROOVE)
#         inventorybuttonFrame.pack(fill=tk.X, pady=5)

#         # Buttons
        
#         delete_button = tk.Button(inventorybuttonFrame, text="Delete", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=delete_item)
#         delete_button.pack(side='left')

#         print_button = tk.Button(inventorybuttonFrame, text="Print", font=('arial', 16, 'bold'), background="gray20", foreground='white', bd=5, width=8, pady=10, command=printsalesview)
#         print_button.pack(side='right')




#         sales_view_window.mainloop()


#         # cursor.execute("SELECT * FROM sales")
#         # sales_data = cursor.fetchall()
#         # conn.close()
#         # print(f"Fetched sales data: {sales_data}")

        

#         # tree.pack(fill='both', expand=True)
#         # sales_view_window.mainloop()


#     def logout():
#         pass 
#         # root.destroy() 
#         # subprocess.run(["python", "registration.py"])


#     def print_bill():
#         if textArea.get(1.0,tk.END) == '\n':
#             messagebox.showerror('Error','Nothing to print')
#         else:
#             file= tempfile.mktemp('.txt')
#             open(file, 'w').write(textArea.get(1.0,tk.END))
#             os.startfile(file,'print')


#     def send_email():
#         pass

#     def clearAll():
#         pass
#         # global totalPrice
#         # totalPrice  = 0
#         # nameEntry.delete(0,tk.END)
#         # phoneEntry.delete(0, tk.END)
#         # billEntry.delete(0, tk.END)
#         # textArea.delete(1.0, tk.END)

#         # textArea.insert(1.0, '\t   ***Medical Store***\n\n')
#         # textArea.insert(tk.END,'\tContact # :0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
#         # textArea.insert(tk.END,'========================================\n')
#         # textArea.insert(tk.END,' Item \t     Unit \t  Quantity\t   Total \n')
#         # textArea.insert(tk.END,' Name \t     Price \t\t         Price \n')
#         # textArea.insert(tk.END,'========================================\n')

#     def total():
#         textArea.insert(tk.END, f'\n\nTotal Bill \t\t\t\t{totalPrice} Rs\n')
#         textArea.insert(tk.END, '----------------------------------------\n\n')
#         textArea.insert(tk.END, 'Developed by Django Softwate PVT\n')
#         textArea.insert(tk.END, 'Contact:92-311-5552866  Email:mansoorpay@gmail.com\n')



#     # Function to update Listbox based on search
#     def update_listbox(event):
#         search_term = search_entry.get()
#         results = fetch_data(search_term)
#         projectsList.delete(0, tk.END)
#         for result in results:
#             projectsList.insert(tk.END, result[0])

    
#     # Function to search and update Listbox
#     def fetch_data(search_term):

#         conn = sqlite3.connect('gascylinder.db')
#         cursor = conn.cursor()

#         cursor.execute("SELECT item_name FROM inventory WHERE item_name LIKE ?", ('%' + search_term + '%',))

#         results = cursor.fetchall()

#         conn.close()

#         return results


#     def readitems():
#         conn = sqlite3.connect('gascylinder.db')
#         cursor = conn.cursor()

#         cursor.execute("SELECT item_name FROM inventory;")
#         # tree.insert('', 'end', values=(new_id, medicine_name_entry.get(), expiry_entry.get(), batch_no_entry.get(), quantity_entry.get(), price_entry.get())) 
            
#         records = cursor.fetchall()

#         conn.close()

#         projectsList.delete(0, tk.END)
#         for record in records:
#             projectsList.insert(tk.END, f'{record[0]}')


#     def on_select(event):


#         global totalPrice
#         selectedIndex = projectsList.curselection()

#         if selectedIndex:
#             item = projectsList.get(selectedIndex)

#             # priceofitem = cursor.fetchone()[0]
#             # quantityofitem = cursor.fetchone()[1]

#             dialog = CustomDialog(sales_window)
#             sales_window.wait_window(dialog)

#             itemQuantity = dialog.quantity
#             itemPrice = dialog.price


#             # itemQuantity = simpledialog.askstring("Input", "Enter Quantity:", initialvalue="1", parent=sales_window)
#             if itemQuantity and itemPrice:
                
#                 remainingitemQuantity = quantityofitem - int(itemQuantity)

#                 cursor.execute('''
#                     UPDATE inventory
#                     SET quantity=? 
#                     WHERE item_name =?
#                 ''', (remainingitemQuantity, item))
#                 conn.commit()
#                 # conn.close()

#             # Do something with the entered string 
#                 # print("Entered string:", itemQuantity)
#                 totalitemPrice = int(itemQuantity) * int(itemPrice)
#                 totalPrice += totalitemPrice

#                 # Save the sale record 
#                 cursor.execute(''' 
#                     INSERT INTO sales (item_name, quantity, price_per_item, total_price, sale_date)
#                     VALUES (?, ?, ?, ?, datetime('now')) 
#                     ''', (item, int(itemQuantity), float(itemPrice), totalitemPrice))
#                 print(f"Inserted sale: {item}, {itemQuantity}, {itemPrice}, {totalitemPrice}")
#                 conn.commit()

#                 cursor.execute("SELECT * FROM sales") 
#                 sales_data = cursor.fetchall() 
#                 print(f"Data after insertion: {sales_data}")
#                 conn.close()

#             # totalPrice = totalPrice + int(itemPrice)
#                 textArea.insert(tk.END, f' {item}\t\t{itemPrice}\t{itemQuantity}\t{totalitemPrice}\n')
#             # print(f'Selected item is {item}')
#         else:
#             messagebox.INFO('Not Found','Unknown Error')


#     sales_window = tk.Toplevel(root)
#     sales_window.title("Sales Management")
#     sales_window.geometry("1200x600")
#     center_window(sales_window)

#     headingLabel = tk.Label(sales_window, text="Sales Management", font=('times new roman', 30, 'bold'), background='gray20', foreground='gold', bd=12, relief=tk.GROOVE)
#     headingLabel.pack(fill=tk.X, pady=5)

#     #Project Details
#     projectPanel = tk.Frame(sales_window,background='gray20')
#     projectPanel.pack(fill= tk.X,pady=5)


#     items_details_frame = tk.LabelFrame(projectPanel,text="Items",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=tk.GROOVE,background='gray20')
#     items_details_frame.grid(row=0,column=0,padx=50)

#     #Listbox
#     search_entry = tk.Entry(items_details_frame,  width=40,font=('arial',15),bd=7)
#     search_entry.bind("<KeyRelease>", update_listbox)
#     search_entry.grid(row=0,column=0,padx=5)
#     projectsList = tk.Listbox(items_details_frame,bd=5,font=('arial',15,),height=15,width=40,relief=tk.GROOVE)
#     projectsList.bind('<Return>',on_select)
#     projectsList.grid(row=1,column=0,padx=5)

#     #Bill Area
#     billFrame=tk.Frame(projectPanel,bd=8,relief=tk.GROOVE)
#     billFrame.grid(row=0,column=2,padx=50,pady = 5)
#     bill_details_frame = tk.Label(billFrame,text="Bill",font=('times new roman',15,'bold'),bd=8,relief=tk.GROOVE)
#     bill_details_frame.pack(fill=tk.X)
#     scrollbar=tk.Scrollbar(billFrame,orient=tk.VERTICAL)
#     scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
#     textArea = tk.Text(billFrame,height=25,width=40,yscrollcommand=scrollbar.set)
#     textArea.pack()
#     scrollbar.config(command=textArea.yview)
#     textArea.insert(1.0,'\t   ***Medical Store***\n\n')
#     textArea.insert(tk.END,'\tContact # :0311-5552866\n\tEmail:mansoorpay@gmail.com\n')
#     textArea.insert(tk.END,'========================================\n')
#     textArea.insert(tk.END,' Item \t     Unit \t  Quantity\t   Total \n')
#     textArea.insert(tk.END,' Name \t     Price \t\t         Price \n')
#     textArea.insert(tk.END,'========================================\n')
#     readitems()

#     #Bill menu frame

#     billmenuframe = tk.LabelFrame(projectPanel,text="Buttons",font=('times new roman',15,'bold'),foreground='gold',bd=8,relief=tk.GROOVE,background='gray20')
#     billmenuframe.grid(row=0,column=1,padx=20)

#     totalbutton=tk.Button(billmenuframe,text="Total",font=('arial',16,'bold'),background="gray20",
#                     foreground='white',bd=5,width=8,pady=10,command=total)
#     totalbutton.grid(row=0,column=0,pady=5,padx=10)

#     billbutton=tk.Button(billmenuframe,text="Sales View",font=('arial',16,'bold'),background="gray20",
#                             foreground='white',bd=5,width=8,pady=10, command=open_sales_view)
#     billbutton.grid(row=1,column=0,pady=5,padx=10)

#     emailbutton=tk.Button(billmenuframe,text="Email",font=('arial',16,'bold'),background="gray20",
#                     foreground='white',bd=5,width=8,pady=10,command=send_email)
#     emailbutton.grid(row=2,column=0,pady=5,padx=10)

#     printbutton=tk.Button(billmenuframe,text="Print",font=('arial',16,'bold'),background="gray20",
#                     foreground='white',bd=5,width=8,pady=10,command=print_bill)
#     printbutton.grid(row=3,column=0,pady=5,padx=10)

#     clearbutton=tk.Button(billmenuframe,text="Clear",font=('arial',16,'bold'),background="gray20",
#                     foreground='white',bd=5,width=8,pady=10,command=clearAll)
#     clearbutton.grid(row=4,column=0,pady=5,padx=10)
   

#     sales_window.mainloop()


# # ----------------------------------------------------------Main root Window---------------------------------------
# root = tk.Tk()
# root.title("Gas Cylinder Management System")
# root.geometry("800x600")
# root.configure(bg='gray20')
# center_window(root)

# # Dashboard Heading
# headingLabel = tk.Label(root, text="Gas Cylinder Management System", font=('Helvetica', 24, 'bold'), bg='gray20', fg='gold')
# headingLabel.pack(pady=20)

# # ----------------------------------------Inventory Overview Frame-----------------------------------------------------
# inventory_frame = tk.Frame(root, bg='gray25', bd=5, relief=tk.GROOVE)
# inventory_frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)

# inventory_label = tk.Label(inventory_frame, text="Inventory Overview", font=('Helvetica', 16, 'bold'), bg='gray25', fg='white')
# inventory_label.pack(pady=10)

# conn = sqlite3.connect('gascylinder.db')
# cursor = conn.cursor()
# cursor.execute("SELECT quantity FROM inventory")
# sales_data = cursor.fetchall()
# conn.close()
# # Extract the values from the tuple 
# total_quantity = sales_data[0][0]

# # Create separate labels 
# quantityLabel = tk.Label(inventory_frame, text=f'Remaining Stock = {total_quantity}', font=('Helvetica', 15 ), bg='gray25', fg='white') 
# quantityLabel.pack(pady=2)

# # ------------------------------------------Sales Summary Frame------------------------------------------------------
# sales_frame = tk.Frame(root, bg='gray25', bd=5, relief=tk.GROOVE)
# sales_frame.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.2)

# sales_label = tk.Label(sales_frame, text="Sales Summary", font=('Helvetica', 16, 'bold'), bg='gray25', fg='white')
# sales_label.pack(pady=10)
# conn = sqlite3.connect('gascylinder.db')
# cursor = conn.cursor()
# cursor.execute("SELECT SUM(quantity),SUM(total_price) FROM sales")
# sales_data = cursor.fetchall()
# conn.close()
# # Extract the values from the tuple 
# total_quantity, total_price = sales_data[0]

# # Create separate labels 
# quantityLabel = tk.Label(sales_frame, text=f'Total Quantity Sold = {total_quantity}', font=('Helvetica', 15 ), bg='gray25', fg='white') 
# quantityLabel.pack(pady=2) 
# priceLabel = tk.Label(sales_frame, text=f'Total Sales Price = {total_price}', font=('Helvetica', 15), bg='gray25', fg='white') 
# priceLabel.pack(pady=2)



# # --------------------------------------------------Purchase Records Frame-------------------------------------------
# purchase_frame = tk.Frame(root, bg='gray25', bd=5, relief=tk.GROOVE)
# purchase_frame.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

# purchase_label = tk.Label(purchase_frame, text="Purchase Records", font=('Helvetica', 16, 'bold'), bg='gray25', fg='white')
# purchase_label.pack(pady=10)

# conn = sqlite3.connect('gascylinder.db')
# cursor = conn.cursor()
# cursor.execute("SELECT SUM(quantity),SUM(purchase_price) FROM inventory")
# sales_data = cursor.fetchall()
# conn.close()
# # Extract the values from the tuple 
# total_quantity, total_price = sales_data[0]

# # Create separate labels 
# quantityLabel = tk.Label(purchase_frame, text=f'Total Quantity purchased = {total_quantity}', font=('Helvetica', 15 ), bg='gray25', fg='white') 
# quantityLabel.pack(pady=2) 
# priceLabel = tk.Label(purchase_frame, text=f'Total Purchased Price = {total_price}', font=('Helvetica', 15), bg='gray25', fg='white') 
# priceLabel.pack(pady=2)

# # Safety Alerts Frame
# alerts_frame = tk.Frame(root, bg='gray25', bd=5, relief=tk.GROOVE)
# alerts_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)

# alerts_label = tk.Label(alerts_frame, text="Safety Alerts", font=('Helvetica', 16, 'bold'), bg='gray25', fg='white')
# alerts_label.pack(pady=10)

# # Navigation Buttons
# button_frame = tk.Frame(root, bg='gray20')
# button_frame.pack(pady=20)

# inventory_button = tk.Button(button_frame, text="Manage Inventory", font=('Helvetica', 14), bg='gray30', fg='white', command=open_inventory_window)
# inventory_button.pack(side='left', padx=10)

# sales_button = tk.Button(button_frame, text="Record Sales", font=('Helvetica', 14), bg='gray30', fg='white', command=open_sales_window)
# sales_button.pack(side='left', padx=10)

# summary_button = tk.Button(button_frame, text="Summary", font=('Helvetica', 14), bg='gray30', fg='white', command=open_summary_view)
# summary_button.pack(side='left', padx=10)

# root.mainloop()
