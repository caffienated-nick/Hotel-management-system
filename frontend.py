import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import backend 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import seaborn as sns

#creating the sql tables
backend.create_table1()
backend.create_table2()
backend.create_table3()
backend.create_combined_table()  
# Initialize the main window
widthh = ctk.CTk().winfo_screenwidth()
heightt = ctk.CTk().winfo_screenheight()
window = ctk.CTk()
window.title("Hotel Management System")
window.after(0, lambda: window.wm_state('zoomed'))
window.iconbitmap('icons\\a-simple_-clean_-square-app-icon-for-hotel-management-with-a-grey-base-theme_-no-3D-effects-or-gradi.ico')

# Set up the main tab view
tabview = ctk.CTkTabview(master=window, segmented_button_fg_color="#242323", height=heightt-100, width=widthh-100)
tabview.pack(padx=20, pady=10)
tabview.add("Dashboard")
tabview.add("Rooms")
tabview.add("Food Menu")

custom_font = ("Segoe UI", 30, 'bold')  # Increased font size
tabview._segmented_button.configure(font=("Segoe UI", 24, 'bold'))

# Frame for room assignment inputs (left side)
vertical_frame = ctk.CTkScrollableFrame(master=tabview.tab("Rooms"), width=(widthh // 2) - 50, height=heightt, fg_color="#383838", corner_radius=10)
vertical_frame.pack(padx=10, pady=10, side="left")

# Frame for room buttons (right side, above status frame)
button_frame = ctk.CTkFrame(master=tabview.tab("Rooms"), fg_color="#383838", corner_radius=10)
button_frame.pack(padx=10, pady=10, side="top")

# Status frame at the bottom of button_frame
status_frame = ctk.CTkFrame(master=tabview.tab("Rooms"), width=600, height=400, fg_color="#383838", corner_radius=10)
status_frame.pack(padx=10, pady=(5, 10), side="top", anchor="n")

# Room button dictionary
buttons = {}
labels = []
entries = []
cart_items = []
adhaar_container = None  # Container for dynamically added Adhaar entry fields
current_room = None  # To keep track of the currently selected room

if current_room == None:
        label1 = ctk.CTkLabel(vertical_frame, text="Please select a room", font=("Segoe UI", 30, 'bold'), anchor='center')
        label1.pack(pady=260)       
room_names = [
        "A1", "B1", "C1", "D1", "E1",
        "A2", "B2", "C2", "D2", "E2",
        "A3", "B3", "C3", "D3", "E3",
        "A4", "B4", "C4", "D4", "E4",
        "A5", "B5", "C5", "D5", "E5"
    ]     
def create_room_buttons():
    """Function to create room buttons."""
    global buttons
    for idx, room_name in enumerate(room_names):
        row = idx // 5
        col = idx % 5
        buttons[room_name] = ctk.CTkButton(
            master=button_frame, 
            text=room_name, 
            width=60, 
            height=60,
            fg_color="green", 
            text_color="black",
            hover_color='#016e03',
            command=lambda b=room_name: page_decider(b)
        )
        buttons[room_name].grid(row=row, column=col, padx=5, pady=5)
def page_decider(room_name):
    global current_room
    current_room = room_name
    if buttons[room_name].cget('fg_color') == 'green':
        show_room_assignment_form(room_name)
        room_status(room_name)
    elif buttons[room_name].cget('fg_color') == 'red':
        show_invoice_page(room_name)
        room_status(room_name)
    else: 
        for widget in vertical_frame.winfo_children():
         widget.destroy()
        underservice = ctk.CTkLabel(vertical_frame, text="~:ROOM IS UNDER SERVICE-PLEASE TRY LATER:~", font=("Segoe UI", 30, 'bold'), anchor='center')
        underservice.pack(pady=260)
        room_status(room_name)
def create_adhaar_fields(container, number_of_people):
    """Function to dynamically create Adhaar number fields based on the number of people."""
    global adhaar_container
    # Clear any existing Adhaar fields
    for widget in adhaar_container.winfo_children():
        widget.destroy()
    adhaar_font = ("Segoe UI", 16)  # Increased font size for Adhaar fields
    adhaar_entries = []
    for i in range(number_of_people):
        adhaar_frame = ctk.CTkFrame(adhaar_container, fg_color="#383838")
        adhaar_frame.pack(fill='x', padx=5, pady=5)
        
        adhaar_label = ctk.CTkLabel(adhaar_frame, text=f"Adhaar Number {i+1}:", font=adhaar_font, anchor='w')
        adhaar_entry = ctk.CTkEntry(adhaar_frame)
        
        adhaar_label.pack(side='left', padx=5)
        adhaar_entry.pack(side='right', fill='x', padx=5, ipadx=30)
        
        labels.append(adhaar_label)
        entries.append(adhaar_entry)
        adhaar_entries.append(adhaar_entry)
    return adhaar_entries
def handle_adhaar_fields(entry):
    """Handle the event when 'Number of People' entry loses focus, and create Adhaar fields."""
    try:
        number_of_people = int(entry.get())
        return create_adhaar_fields(adhaar_container, number_of_people)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for 'Number of People'")
        return []
def show_room_assignment_form(room_name):
    """Function to show the room assignment input fields in the assignment frame."""
    global adhaar_container, current_room
    current_room = room_name
    
    for widget in vertical_frame.winfo_children():
        widget.destroy()

    # Title label for the assignment section with room name
    assignation_label = ctk.CTkLabel(vertical_frame, text=f"Room Assignment: {room_name}", font=custom_font, anchor='center')
    assignation_label.pack(pady=10)

    entry_font = ("Segoe UI", 18)  # Increased font size for credential fields
    current_date = datetime.now().strftime("%Y-%m-%d")
    fields = [
        "Name:", "Address:", "Date of Check-in:",
        "Number of People:", "Email:", "Phone No:",
        "Extra Exclusive Services:",'Accommodation Services:',
        "Wellness and leisure facilities:",'On-site Events:',
        'Pet-Centric Amenities:','Private Dining:',"Special Occasion Facilities:"
    ]
    data = {}
    adhaar_entries = []
    for field in fields:
        container = ctk.CTkFrame(vertical_frame, fg_color="#383838")
        container.pack(fill='x', padx=5, pady=5)
        
        label = ctk.CTkLabel(container, text=field, font=entry_font, anchor='w')
        
        if field == "Date of Check-in:":
            entry = ctk.CTkLabel(container, text=current_date, font=entry_font, anchor='w')
            data["date_of_checkin"] = current_date
        elif field == "Extra Exclusive Services:":
            entry = ctk.CTkCheckBox(container, text="")
            data["extra_services"] = entry
        elif field == "Number of People:":
            entry = ctk.CTkEntry(container)
            entry.bind("<FocusOut>", lambda e, entry=entry: adhaar_entries.extend(handle_adhaar_fields(entry)))
            data["number_of_people"] = entry
        elif field == 'Accommodation Services:':
            
            entry = ctk.CTkCheckBox(container, text='')
            data['accomodation_services'] = entry
        elif field == 'On-site Events:':
            
            entry = ctk.CTkCheckBox(container, text='')
            data['Events'] = entry

        elif field == 'Wellness and leisure facilities:':
            
            entry = ctk.CTkCheckBox(container, text='')
            data['wellness'] = entry
        elif field == 'Pet-Centric Amenities:':
            
            entry = ctk.CTkCheckBox(container, text='')
            data['pets'] = entry
        elif field == 'Private Dining:':
            
            entry = ctk.CTkCheckBox(container, text='')
            data['private_dining'] = entry  
        elif field == 'Special Occasion Facilities:':
            
            entry = ctk.CTkCheckBox(container, text='')
            data['occasion'] = entry                    
        else:
            entry = ctk.CTkEntry(container)
            data[field.lower().replace(" ", "_").replace(":", "")] = entry

        label.pack(side='left', padx=5)
        entry.pack(side='right', fill='x', padx=5, ipadx=50)
        
        labels.append(label)
        entries.append(entry)
    # Prepare the container for Adhaar fields
    adhaar_container = ctk.CTkFrame(vertical_frame, fg_color="#383838")
    adhaar_container.pack(fill='x', padx=5, pady=5)
    # Add an 'Assign' button to the vertical frame
    assign_button = ctk.CTkButton(
        master=vertical_frame,
        text="Assign",
        width=100,
        height=40,
        fg_color="#007ACC",
        text_color="white",
        hover_color='#005A9E',
        command=lambda: assign_room(room_name, data, adhaar_entries)
    )
    assign_button.pack(pady=1)
def assign_room(room_name, data, adhaar_entries):
    """Function to save room assignment details and update room status."""
    try:
        # Gather data from input fields
        
        guest_data = (
            room_name,
            data["name"].get(),
            data["address"].get(),
            data["date_of_checkin"],
            int(data["number_of_people"].get()),
            data["email"].get(),
            data["phone_no"].get(),
            data["extra_services"].get(),
            data['accomodation_services'].get(),
            data['Events'].get(),
            data['wellness'].get(),
            data['pets'].get(),
            data['private_dining'].get(),
            data['occasion'].get(),
            ','.join([entry.get() for entry in adhaar_entries])
        )
        # Insert data into the database
        backend.insert_assignment(guest_data)

        # Change room button color to red
        buttons[room_name].configure(fg_color="red",hover_color='#870303')
        
        # Display confirmation and show invoice page
        messagebox.showinfo("Assignment Complete", f"Room {room_name} assigned successfully!")
        show_invoice_page(room_name)
        room_status(room_name)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to assign room: {e}")

def show_invoice_page(room_name):
    dashboard_updater()
    """Function to display the invoice page with the latest data from the database."""
    xname =['extra_services','accomodation_services','events','wellness','pets','private_dining','occasion']
    latest_data = backend.get_latest_assignment(room_name)
 
    for i in xname:
        if latest_data[i] == 1:
            latest_data[i] = 'Yes'
        else:
            latest_data[i] = 'No'    
    if latest_data:
        for widget in vertical_frame.winfo_children():
            widget.destroy()

        invoice_label = ctk.CTkLabel(vertical_frame, text=f"Room Info - Room {room_name}", font=custom_font, anchor='center')
        invoice_label.pack(pady=10)

        entry_font = ("Segoe UI", 24)
        for key, value in latest_data.items():
            container = ctk.CTkFrame(vertical_frame, fg_color="#383838")
            container.pack(fill='x', padx=5, pady=5)
            
            label = ctk.CTkLabel(container, text=f"{key.replace('_', ' ').title()}: {value}", font=entry_font, anchor='w')
            label.pack(side='left', padx=5)
        
        global biling
        biling = ctk.CTkButton(vertical_frame,text ='Invoice',command=final_biling)
        biling.pack(anchor= 'center')

def final_biling():
    biling.pack_forget()
    latest_data = backend.get_latest_assignment(current_room)
    
    check_out_date = datetime.now().date()
    check_in_date = latest_data["date_of_checkin"]
    days_stayed = (check_out_date - check_in_date).days
    base_rate = room_details[current_room]["price"] * days_stayed
    select_sum = 0
    xname =['extra_services','accomodation_services','events','wellness','pets','private_dining','occasion']
    for i in xname:
        if latest_data[i] == 'Yes':
            select_sum += 500
        else:
            select_sum += 0
    try:
     food_sum = backend.get_fooddata( backend.get_latest_assignment(current_room)['id'])['Total_bill']
    except:
        food_sum = 0
    total = base_rate + select_sum + food_sum                  
    invoice_details = [f'days stayed: {days_stayed}' ,
                       f"Food Bill(included in Invoice): {food_sum}",
        f"Check-out Date: {check_out_date.strftime('%Y-%m-%d')}",
        f"Total Bill: ₹ {total} "
    ]
    for widget in vertical_frame.winfo_children():
        widget.destroy()
    invoice_label = ctk.CTkLabel(vertical_frame, text=f"Invoice - Room {current_room}", font=custom_font, anchor='center')
    invoice_label.pack(pady=10)
    entry_font = ("Segoe UI", 18)
    for key, value in latest_data.items():
            container = ctk.CTkFrame(vertical_frame, fg_color="#383838")
            container.pack(fill='x', padx=5, pady=5)
            
            label = ctk.CTkLabel(container, text=f"{key.replace('_', ' ').title()}: {value}", font=entry_font, anchor='w')
            label.pack(side='left', padx=5)
       
    invoice_frame = ctk.CTkFrame(vertical_frame, fg_color="#383838")
    invoice_frame.pack(fill='x', padx=5, pady=5)
    
    for detail in invoice_details:
        invoice_line = ctk.CTkLabel(invoice_frame, text=detail, font=("Segoe UI", 24, 'bold'), anchor='w')
        invoice_line.pack(fill='x', padx=5, pady=2)
    idata=(backend.get_latest_assignment(current_room)['id'],check_out_date.strftime('%Y-%m-%d'),days_stayed,total)    
    backend.insert_invoice(idata)
    final_data =(backend.get_latest_assignment(current_room)['id'],backend.get_latest_assignment(current_room)['room_name'],
                 backend.get_latest_assignment(current_room)['name'],backend.get_latest_assignment(current_room)['address'],
                 backend.get_latest_assignment(current_room)['date_of_checkin'],backend.get_latest_assignment(current_room)['number_of_people'],
                 backend.get_latest_assignment(current_room)['email'],backend.get_latest_assignment(current_room)['phone_no'],
                 backend.get_latest_assignment(current_room)['extra_services'],backend.get_latest_assignment(current_room)['accomodation_services'],
                 backend.get_latest_assignment(current_room)['events'],backend.get_latest_assignment(current_room)['wellness'],
                 backend.get_latest_assignment(current_room)['pets'],backend.get_latest_assignment(current_room)['private_dining'],
                 backend.get_latest_assignment(current_room)['occasion'],backend.get_latest_assignment(current_room)['adhaar_numbers'],
                 check_out_date.strftime('%Y-%m-%d'),days_stayed,total) 
    backend.insert_combined(final_data)                    
    # Change room button color to gray temporarily
    buttons[current_room].configure(fg_color="gray", hover_color="#696969")
    room_status(current_room)
    # Schedule a function to reset the color after 15 minutes (900000 milliseconds)
    window.after(5000, lambda: buttons[current_room].configure(fg_color="green", hover_color="#016e03"))
room_details = {
    "A1": {"price": 7000, "description": "Luxurious sea-facing room with a private balcony and modern decor. Enjoy a king-sized bed, plush linens, a spacious bathroom with a soaking tub, and complimentary Wi-Fi."},
    "A2": {"price": 7000, "description": "Spacious room with oceanfront views, premium furniture, and a cozy ambiance. Features include a queen-sized bed, a mini-bar, a seating area, and a state-of-the-art entertainment system."},
    "A3": {"price": 7000, "description": "Exquisite room with breathtaking sea views and a comfortable lounge area. Includes a king-sized bed, a work desk, floor-to-ceiling windows, and a luxurious bathroom with a rain shower."},
    "A4": {"price": 7000, "description": "Elegant suite offering serene ocean views and upscale amenities. Comes with a separate living area, a king-sized bed, a walk-in closet, and a private bathroom with a soaking tub."},
    "A5": {"price": 7000, "description": "Luxury room with direct sea view, ideal for relaxation and comfort. Features a king-sized bed, a private balcony, an espresso machine, and a bathroom with a jacuzzi."},
    
    "B1": {"price": 5000, "description": "Room with garden views, providing a calm and refreshing environment. Includes a queen-sized bed, a private patio, a writing desk, and modern bathroom amenities."},
    "B2": {"price": 5000, "description": "Spacious garden-view room, perfect for nature lovers. Features a king-sized bed, a seating area, large windows, and a bathroom with a rain shower."},
    "B3": {"price": 5000, "description": "Relaxing room with a lovely view of lush gardens and comfortable furnishings. Comes with a queen-sized bed, a private balcony, a mini-bar, and a modern bathroom."},
    "B4": {"price": 5000, "description": "Garden-facing room with modern amenities and a tranquil setting. Features a queen-sized bed, a workspace, a private patio, and a luxurious bathroom."},
    "B5": {"price": 5000, "description": "Charming room overlooking the gardens, with a cozy atmosphere. Includes a double bed, a seating area, complimentary Wi-Fi, and a bathroom with all essential amenities."},
    
    "C1": {"price": 4000, "description": "High-floor room with city views, ideal for business travelers. Features a king-sized bed, a spacious work desk, high-speed internet, and a modern bathroom."},
    "C2": {"price": 4000, "description": "Modern room offering panoramic views of the bustling cityscape. Comes with a queen-sized bed, a cozy seating area, a work desk, and a well-appointed bathroom."},
    "C3": {"price": 4000, "description": "Comfortable city-view room with a contemporary design and workspace. Includes a double bed, a work desk, complimentary Wi-Fi, and a bathroom with a shower."},
    "C4": {"price": 4000, "description": "Urban-inspired room with stunning city views and sleek decor. Features a king-sized bed, a lounge chair, high-speed internet, and a bathroom with modern fixtures."},
    "C5": {"price": 4000, "description": "Elegant room with a high-floor view of the city, perfect for relaxation. Includes a queen-sized bed, a seating area, a flat-screen TV, and a well-equipped bathroom."},
    
    "D1": {"price": 6000, "description": "Poolside room with easy access to the pool and resort-style amenities. Features a king-sized bed, a private patio with sun loungers, complimentary Wi-Fi, and a luxurious bathroom."},
    "D2": {"price": 6000, "description": "Room adjacent to the pool, ideal for a relaxing vacation experience. Comes with a queen-sized bed, a seating area, direct pool access, and a bathroom with modern amenities."},
    "D3": {"price": 6000, "description": "Comfortable poolside room with a patio and sun loungers. Includes a double bed, a private terrace, a mini-bar, and a well-appointed bathroom."},
    "D4": {"price": 6000, "description": "Poolside room with modern amenities and a refreshing atmosphere. Features a king-sized bed, a private patio, high-speed internet, and a bathroom with luxurious fixtures."},
    "D5": {"price": 6000, "description": "Elegant room with direct pool access, perfect for resort-style relaxation. Includes a queen-sized bed, a seating area, a private balcony, and a spacious bathroom."},
    
    "E1": {"price": 3000, "description": "Standard economy room with essential amenities for a comfortable stay. Features a double bed, a work desk, complimentary Wi-Fi, and a bathroom with all basic amenities."},
    "E2": {"price": 3000, "description": "Budget-friendly room with basic amenities and cozy interiors. Comes with a single bed, a small seating area, free Wi-Fi, and a well-equipped bathroom."},
    "E3": {"price": 3000, "description": "Economy room designed for practical comfort and affordability. Includes a twin bed, a work desk, complimentary internet, and a bathroom with necessary facilities."},
    "E4": {"price": 3000, "description": "Simple and comfortable room, perfect for short stays on a budget. Features a double bed, a small desk, free Wi-Fi, and a bathroom with essential amenities."},
    "E5": {"price": 3000, "description": "Affordable room with all the essentials for a convenient stay. Comes with a single bed, a seating area, complimentary Wi-Fi, and a basic but functional bathroom."}
}
def room_combobox_changed():
   
    room_name = room_combobox.get()
    if buttons[room_name].cget('fg_color') == 'green':
        cstat = 'Available'
    elif buttons[room_name].cget('fg_color') == 'red':
        cstat = 'Occupied'
    
    else:

        cstat = 'Under service'
    return cstat
def room_status(room_name):
    room_info = room_details.get(room_name, {})
    # Set the status based on room button color
    if buttons[room_name].cget('fg_color') == 'green':
        stat = 'Available'
    elif buttons[room_name].cget('fg_color') == 'red':
        stat = 'Occupied'
    else:
        stat = 'Under service'
    # Clear previous content in the status frame
    for widget in status_frame.winfo_children():
        widget.destroy()
    # Format content row by row, from left to right
    blank_label = ctk.CTkLabel(status_frame, text="                           ", font=('Segoe UI', 30), anchor='w')
    room_status_label = ctk.CTkLabel(status_frame, text=f"𝗦𝘁𝗮𝘁𝘂𝘀: {stat}", font=('Segoe UI', 25), anchor='w')
    blank_label = ctk.CTkLabel(status_frame, text="                           ", font=('Segoe UI', 30), anchor='w')
    room_price_label = ctk.CTkLabel(status_frame, text=f"𝗣𝗿𝗶𝗰𝗲 𝗽𝗲𝗿 𝗡𝗶𝗴𝗵𝘁: ₹{room_info.get('price')}", font=('Segoe UI', 25), anchor='w')
    blank_label = ctk.CTkLabel(status_frame, text="                           ", font=('Segoe UI', 30), anchor='w')
    room_description_label = ctk.CTkLabel(status_frame, text=f"𝗗𝗲𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻: {room_info.get('description')}", font=('Segoe UI', 25), anchor='w', wraplength=500)
    
    # Use grid to layout the labels in rows and columns
    room_status_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
    room_price_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
    room_description_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)
    blank_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
    # Set the frame to not allow its size to change dynamically based on content
    status_frame.grid_propagate(False)  # Prevent resizing based on content
left_frame = ctk.CTkScrollableFrame(tabview.tab("Food Menu"), width=(widthh // 2) - 50, height=heightt, fg_color="#383838", corner_radius=10)
left_frame.pack(padx=10, pady=10, side="left",fill='y')
right_container = ctk.CTkFrame(
    tabview.tab("Food Menu"),
    width=(widthh // 2) - 50,
    height=heightt,
    corner_radius=10,
    fg_color="#2b2b2b",
)
right_container.grid_rowconfigure(0, minsize=430)  # Fixed height for right_frame
right_container.grid_rowconfigure(1, weight=1)    # Remaining space for right_frame_2
right_container.grid_columnconfigure(0, weight=1)
right_frame = ctk.CTkFrame(
    right_container,
    width=(widthh // 2) - 50,
    height=680,
    fg_color="#383838",
    corner_radius=10
)
right_frame_2 = ctk.CTkFrame(
    right_container,
    width=(widthh // 2) - 50,
    
    fg_color="#383838",
    corner_radius=10
)
total = 0
right_container.pack(side="right", padx=10, pady=10, fill="y", anchor="n")
# Pack the frames vertically inside the parent container
right_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
right_frame_2.grid(row=1, column=0, sticky="nsew")
cart_frame = ctk.CTkScrollableFrame(right_frame, fg_color="#333333", corner_radius=0,height = 530)
cart_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(10,5)) 
cart_frame.grid_propagate()
right_frame_2.update_idletasks()
right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_columnconfigure(2, weight=1)
right_frame.grid_propagate(False)
  # Adjust padding and sticky
 #Configure `right_frame` grid to handle the layout more effectively
right_frame.grid_rowconfigure(1, weight=1)  # Allow `cart_frame` to expand vertically
right_frame.grid_columnconfigure(0, weight=0)
right_frame.grid_columnconfigure(1, weight=0)
right_frame.grid_rowconfigure(1, weight=1)
cart_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
right_frame.update_idletasks()
cart_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")
cart_frame.grid_propagate()
cart_frame.update_idletasks()
special_instructionLabel = ctk.CTkLabel(right_frame_2, text="Special Instructions:", font=("Segoe UI", 20, 'bold'), anchor='w')
special_instructionLabel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
special_instructionEntry = ctk.CTkEntry(right_frame_2, font=("Segoe UI", 20), fg_color="#404040",width=400)
special_instructionEntry.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")    
total_frame = ctk.CTkFrame(right_frame_2, fg_color="#404040", corner_radius=10)
total_frame.grid(  row =1, column=0, columnspan=2,padx=10, pady=10, sticky="e")
total_label = ctk.CTkLabel(total_frame, text=f"Total: ₹0.00", font=("Segoe UI", 20, 'bold'), anchor="w")
total_label.grid(row=1, column=0, padx=10, pady=10)

def order():
    current_room_combobox = room_combobox.get()
    buttonorder.configure(text='Proceed', command=proceed)
    # Calculate total price
    total = sum(entry['total_price'] for entry in cart_items)
    total_label.configure(text=f"Total: ₹{total:.2f}")
    # Disable remove button and configure
    for i in remove_buttons:
      if i.winfo_exists():
          i.destroy()
        # Disable "Add" buttons and quantity entries
    for button in add_buttons:
        button.configure(state="disabled", fg_color="#036903")
    for entry in quantity_entries:
        entry.configure(state="disabled")
    messagebox.showinfo("Thank You", "Order succesfully added to final Invoice")
     # Display total amount label in place of `buttonorder`
    # Adjust row and column configuration for resizing behavior
    right_frame.grid_rowconfigure(3, weight=1)
    # Save order data in backend
    latest_assignment = backend.get_latest_assignment(current_room_combobox)
    if latest_assignment:
        room_id = latest_assignment['id']
        backend.insert_fooddata(room_id, total)
    else:
        print("No assignment found for the selected room.")
def proceed():
    # Clear the cart items and destroy the cart item frame
    cart_items.clear()
    if len(cart_items) == 0:
        global buttonorder
        buttonorder.configure(state = 'disabled', fg_color="#758468")
    for i in item_frames:
        if i.winfo_exists():
            i.destroy()
    total_label.configure(text=f"Total: ₹0.00")    
    
    special_instructionEntry.delete(0,ctk.END)
    room_for_rest('c')
    buttonorder.configure(text='Order', command=order)
def create_menu_section(title, items):
    section_title = ctk.CTkLabel(left_frame, text=title, font=("Segoe UI", 22, 'bold'), anchor="center")
    section_title.pack(pady=(10, 5), padx=10)
    for idx, (item, price) in enumerate(items):
        # Create a frame for each row item
        item_frame = ctk.CTkFrame(left_frame, fg_color="#383838", corner_radius=10)
        item_frame.pack(fill="x", padx=10, pady=5)

        # Create label for the item name
        item_label = ctk.CTkLabel(
            item_frame, 
            text=item, 
            font=("Segoe UI", 18), 
            anchor="w"
        )
        item_label.grid(row=idx, column=0, padx=(10, 5), sticky="w")

        # Create label for the item price
        price_label = ctk.CTkLabel(
            item_frame, 
            text=f"₹{price:.2f}", 
            font=("Segoe UI", 18), 
            anchor="e"
        )
        price_label.grid(row=idx, column=1, padx=(5, 10), sticky="e")
        global add_button, quantity_entry
        # Create the quantity entry box
        quantity_entry = ctk.CTkEntry(
            item_frame,
            width=50,  # Width of the quantity entry box
            font=("Segoe UI", 16),
            state = 'disabled',
            justify="center"
        )
        quantity_entry.grid(row=idx, column=2, padx=(10, 5), pady=5, sticky="e")
        # Create the "Add" button
        add_button = ctk.CTkButton(
            item_frame, 
            text="Add", 
            font=("Segoe UI", 18), 
            width=60, 
            height=30, 
            fg_color="#4b5448", 
            hover_color="#45A049",
            state = 'disabled',
           
            command=lambda item=item, price=price,entry=quantity_entry: add_item_to_cart(item,price, entry)
        )
        add_button.grid(row=idx, column=3, padx=(5, 10), pady=5, sticky="e")
        # Configure grid columns for better alignment
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=0)
        item_frame.grid_columnconfigure(2, weight=0)
        item_frame.grid_columnconfigure(3, weight=0)
        add_buttons.append(add_button)
        quantity_entries.append(quantity_entry)

add_buttons =[]
quantity_entries=[]
remove_buttons =[]
item_frames =[]
# Place "Order" button directly below `cart_frame` in `right_frame`
buttonorder = ctk.CTkButton(
    right_frame_2,
    text="Order",
    fg_color="#758468",
    hover_color="#45A049",
    font=("Segoe UI", 16, "bold"),
    width=640,
    height=40,
    corner_radius=10,
    command=order  # Assuming you have an order function defined
)
buttonorder.grid(row=2, column=0, columnspan=3,padx=10, pady=(5, 10) ,sticky="s")  # Button spans width and is at the bottom
# Create cart label within the scrollable `cart_frame`
cart_label = ctk.CTkLabel(cart_frame, text="Cart", font=("Segoe UI", 22, 'bold'), anchor="center")
cart_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")
cart_frame.grid_columnconfigure(0, weight=1)
# Function for adding item to cart
def add_item_to_cart(item, price, quantity_entry):
    try:
        quantity = int(quantity_entry.get())
    except ValueError:
        quantity = 0
    if quantity > 0:
        total_price = price * quantity
        global cart_item_frame
        # Create frame for each cart item
        cart_item_frame = ctk.CTkFrame(cart_frame, fg_color="#404040", corner_radius=10)
        cart_item_frame.grid(  padx=10, pady=5,sticky ='nsew')
          
        # Configure columns within cart item frame
        cart_item_frame.grid_columnconfigure(0, weight=3)
        cart_item_frame.grid_columnconfigure(1, weight=1)
        cart_item_frame.grid_columnconfigure(2, weight=1)
        
        # Create item label
        item_label = ctk.CTkLabel(cart_item_frame, text=f"{item} (x{quantity})", font=("Segoe UI", 18), anchor="w")
        item_label.grid(row=0, column=0, padx=10, sticky="w")

        # Price label
        price_label = ctk.CTkLabel(cart_item_frame, text=f"₹{total_price:.2f}", font=("Segoe UI", 18), anchor="center")
        price_label.grid(row=0, column=1, padx=10, sticky="e")

        # Remove button for cart item
        global remove_button
        remove_button = ctk.CTkButton(cart_item_frame, text="❌", font=("Segoe UI", 18), width=30, height=30, fg_color="#FF4C4C", hover_color="#FF1F1F",command=lambda: remove_item_from_cart(cart_item_frame, item, total_price))
        remove_button.grid(row=0, column=2, padx=(5, 10), sticky="e")
        remove_buttons.append(remove_button)
        # Add item to cart_items list for tracking
        cart_items.append({"item": item, "quantity": quantity, "total_price": total_price})
        item_frames.append(cart_item_frame)
        # Clear quantity entry after adding to cart
        quantity_entry.delete(0, 'end')
        if len(cart_items) > 0:
            buttonorder.configure(state="normal", fg_color="#4CAF50")
         # Ensure button is visible if items are added
# Adjusted function to remove item and hide the button if cart is empty
def remove_item_from_cart(cart_item_frame, item, total_price):
    cart_item_frame.destroy()
    for cart_item in cart_items:
        if cart_item['item'] == item and cart_item['total_price'] == total_price:
            cart_items.remove(cart_item)
            break
    if len(cart_items) == 0:
        global buttonorder
        buttonorder.configure(state = 'disabled', fg_color="#758468")
# Menu sections with item names and prices
beverages = [
    ("Regular Tea", 20.00),
    ("Masala Tea", 25.00),
    ("Coffee", 25.00),
    ("Cold drink", 25.00),
    ("Bread Butter", 30.00),
    ("Bread Jam", 30.00),
    ("Veg. Sandwich", 50.00),
    ("Veg. Toast Sandwich", 50.00),
    ("Cheese Toast Sandwich", 70.00),
    ("Grilled Sandwich", 70.00),
]
soups = [
    ("Tomato Soup", 110.00),
    ("Hot And Sour", 110.00),
    ("Veg. Noodle Soup", 110.00),
    ("Sweet Corn", 110.00),
    ("Veg. Munchow", 110.00),
]
main_course = [
    ("Shahi Paneer", 110.00),
    ("Kadai Paneer", 110.00),
    ("Handi Paneer", 120.00),
    ("Palak Paneer", 120.00),
    ("Chilli Paneer", 140.00),
    ("Matar Paneer", 140.00),
    ("Mix Veg", 140.00),
    ("Jeera Aloo", 140.00),
    ("Malai Kofta", 140.00),
    ("Aloo Matar", 140.00),
    ("Dal Fry", 140.00),
    ("Dal Makhani", 150.00),
    ("Dal Tadka", 150.00),
]
roti = [
    ("Plain Roti", 15.00),
    ("Butter Roti", 15.00),
    ("Tandoori Roti", 20.00),
    ("Butter Naan", 20.00),
]
rice = [
    ("Plain Rice", 90.00),
    ("Jeera Rice", 90.00),
    ("Veg. Pulao", 110.00),
    ("Matar Pulao", 110.00),
]
south_indian = [
    ("Plain Dosa", 100.00),
    ("Onion Dosa", 110.00),
    ("Masala Dosa", 130.00),
    ("Paneer Dosa", 130.00),
    ("Idli", 130.00),
]
# Adding each category to the menu
create_menu_section("BEVERAGES", beverages)
create_menu_section("SOUPS", soups)
create_menu_section("MAIN COURSE", main_course)
create_menu_section("ROTI", roti)
create_menu_section("RICE", rice)
create_menu_section("SOUTH INDIAN", south_indian)
label3 = None
def room_for_rest(room):
    global label3
    if label3:
        label3.destroy()
    if room_combobox_changed() == 'Available':
        label3 = ctk.CTkLabel(right_frame, text="Not Occupied", font=("Segoe UI", 20, 'bold'), text_color="red")
        label3.grid(row=0, column=2,sticky = 'w',padx=10, pady=10)
        for button in add_buttons:
         button.configure(state="disabled", fg_color="#4b5448")
        for entry in quantity_entries: 
         entry.configure(state="disabled")
    elif room_combobox_changed() == 'Occupied':
        label3 = ctk.CTkLabel(right_frame, text="Occupied", font=("Segoe UI", 20, 'bold'), text_color="green")
        label3.grid(row=0, column=2, sticky = 'w',padx=10, pady=10)    
        for button in add_buttons:
         button.configure(state="normal",fg_color="#4CAF50")
        for entry in quantity_entries: 
         entry.configure(state="normal")
        window.after(5000, lambda: label3.destroy()) 
label2 = ctk.CTkLabel(right_frame, text="Order for:", font=("Segoe UI", 30, 'bold'))
room_combobox = ctk.CTkComboBox(right_frame, values=room_names, font=("Segoe UI", 20), width=200,command=room_for_rest, height=30)
room_combobox.set("Select Room")
label2.grid(row=0, column=0,padx=20, pady=10, sticky="w") 
room_combobox.grid(row=0, column=1, pady=10, sticky="w") 
tabview.tab("Dashboard").grid_columnconfigure(0, weight=0)
tabview.tab("Dashboard").grid_columnconfigure(1, weight=1)
tabview.tab("Dashboard").grid_columnconfigure(2, weight=1)
tabview.tab("Dashboard").grid_columnconfigure(3, weight=0)
tottalbooking_frame = ctk.CTkFrame(tabview.tab("Dashboard"), width=490, height=90, fg_color="#383838", corner_radius=10)
tottalbooking_frame.grid(row=0, column=1, padx=20, pady=20, sticky="e")
tottalbooking_frame.grid_propagate(False)
nopeople_frame = ctk.CTkFrame(tabview.tab("Dashboard"), width=490, height=90, fg_color="#383838", corner_radius=10)
nopeople_frame.grid(row=0, column=2, padx=20, pady=20, sticky="w")
nopeople_frame.grid_propagate(False)
total_bookings_label = ctk.CTkLabel(tottalbooking_frame, text=f"  Total Bookings:  {backend.total_bookings()['total_bookings']}", font=("Segoe UI", 40, 'bold'))
total_bookings_label.grid(row=0, column=0, padx=10, pady=10)
no_people_label = ctk.CTkLabel(nopeople_frame, text=f" Total People Served:  {backend.total_no_of_people()['tnop']}", font=("Segoe UI", 36, 'bold'))
no_people_label.grid(row=0, column=0, padx=10, pady=10)
def dashboard_updater():
   for i in tottalbooking_frame.winfo_children():
      i.destroy()
   for i in nopeople_frame.winfo_children():
      i.destroy()  
   total_bookings_label = ctk.CTkLabel(tottalbooking_frame, text=f"  Total Bookings:  {backend.total_bookings()['total_bookings']}", font=("Segoe UI", 40, 'bold'))
   total_bookings_label.grid(row=0, column=0, padx=10, pady=10)

   no_people_label = ctk.CTkLabel(nopeople_frame, text=f" Total People Served:  {backend.total_no_of_people()['tnop']}", font=("Segoe UI", 36, 'bold'))
   no_people_label.grid(row=0, column=0, padx=10, pady=10) 

graph_frame = ctk.CTkFrame(tabview.tab("Dashboard"),width=1400, height=570,  fg_color="#383838", corner_radius=10)
graph_frame.grid( row = 1 ,column=0, columnspan=4,padx=20, pady=20, sticky="n")
graph_frame.grid_propagate(False)

graph_frame.columnconfigure(0, weight=3)
graph_frame.columnconfigure(1, weight=1)
graph_frame.columnconfigure(2, weight=1)
graph_frame.columnconfigure(3, weight=1)

graph_frame.rowconfigure(0, weight=1)
graph_frame.rowconfigure(1, weight=1)
graph_frame.rowconfigure(2, weight=1)
graph_frame.rowconfigure(3, weight=1)
def update_graph():
    try: 
        
         values = ["Monthly Revenue", "Popularity of Amenities", "Room Assignment"]
         for ik in values:
             if ik == "Monthly Revenue":
                 for i in graph_frame.winfo_children():
                     i.destroy()
                 descn = "Monthly revenue graph illustrating the hotel's income trends over a year highlighting peak revenue periods and identifying potential low-performing months for strategic planning and performance analysis."
                 revenue_data = backend.get_monthly_revenue()
                 data = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                 label = ctk.CTkLabel(graph_frame, text="Monthly Revenue Analysis", font=("Segoe UI", 33, 'bold'))
                 label.grid(row=0, column=2, padx=10, pady=10, sticky="n")
                 desc1_label = ctk.CTkLabel(graph_frame, text=descn, font=("Segoe UI", 28), wraplength=500)
                 desc1_label.grid(row=0, column=2, padx=10, pady=10)
                 fig_l = Figure(figsize=(9, 7), facecolor="#383838")
                 ax_1 = fig_l.add_subplot()
                 ax_1.fill_between(data, revenue_data['revenue'], alpha=0.7)
                 ax_1.set_facecolor("#383838")
                 ax_1.tick_params(axis='x', labelsize=10, colors="gainsboro")
                 ax_1.tick_params(axis='y', labelsize=10, colors="gainsboro")
                 fig_l.autofmt_xdate()
                 ax_1.plot(data, revenue_data['revenue'], color="deepskyblue")
                 ax_1.grid(visible=True, color="black")
                 canvas = FigureCanvasTkAgg(figure=fig_l, master=graph_frame)
                 canvas.draw()
                 canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="s")
                 time.sleep(5)
                 
             elif ik == "Popularity of Amenities":
                 for i in graph_frame.winfo_children():
                     i.destroy()
                 sdata_values = [
                     backend.total_extra_services(),
                     backend.total_accomodation_services(),
                     backend.total_wellness(),
                     backend.total_events(),
                     backend.total_pets(),
                     backend.total_private_dining(),
                     backend.total_occasion()
                 ]
                 desc = "Hotel service usage bar graph detailing the popularity of extra services, accommodation options, wellness facilities, and more, highlighting guest preferences for effective service planning and improvement."
                 label = ctk.CTkLabel(graph_frame, text="Popularity of Amenities", font=("Segoe UI", 33, 'bold'))
                 label.grid(row=0, column=2, padx=10, pady=10, sticky="n")
                 desc2_label = ctk.CTkLabel(graph_frame, text=desc, font=("Segoe UI", 28), wraplength=500)
                 desc2_label.grid(row=0, column=2, padx=10, pady=10)
                 values = [item['tes'] for item in sdata_values]
                 sname = [
                     "Extra Exclusive Services", 'Accommodation Services',
                     "Wellness and Leisure Facilities", 'On-site Events',
                     'Pet-Centric Amenities', 'Private Dining', "Special Occasion Facilities"
                 ]
                 fig_2 = Figure(figsize=(9, 7), facecolor="#383838")
                 ax_2 = fig_2.add_subplot()
                 ax_2.barh(sname, values, color="deepskyblue", height=0.5, alpha=0.7)
                 ax_2.grid(visible=True, color="black")
                 ax_2.set_facecolor("#383838")
                 ax_2.tick_params(axis='x', labelsize=10, colors="gainsboro")
                 ax_2.tick_params(axis='y', colors="gainsboro", labelsize=12)
                 fig_2.subplots_adjust(left=0.35)
                 max_value = max(values)
                 ax_2.set_xlim(0, max_value * 1.2)
                 canvas1 = FigureCanvasTkAgg(figure=fig_2, master=graph_frame)
                 canvas1.draw()
                 canvas1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="s")
                 time.sleep(5)
                 
             elif ik == "Room Assignment":
                 for i in graph_frame.winfo_children():
                     i.destroy()
                 desco = "Pie chart illustrating the continuous booking rates for hotel rooms, highlighting the most frequently occupied rooms and providing insights into booking patterns to enhance room allocation strategies."
                 label = ctk.CTkLabel(graph_frame, text="Most Occupied Rooms", font=("Segoe UI", 33, 'bold'))
                 label.grid(row=0, column=2, padx=10, pady=10, sticky="n")
                 desc3_label = ctk.CTkLabel(graph_frame, text=desco, font=("Segoe UI", 28), wraplength=500)
                 desc3_label.grid(row=0, column=2, padx=10, pady=10)
                 fig = Figure(figsize=(9, 7), facecolor="#383838")
                 ax = fig.add_subplot()
                 roomn = [item['room_name'] for item in backend.total_each_room()]
                 exp = [0.1 if x == 'A1' else 0.05 for x in roomn]
                 valuess = [item['total_bookings'] for item in backend.total_each_room()]
                 ax.pie(valuess, radius=1.4, labels=roomn, shadow=True, textprops={'color': 'white'}, colors=sns.color_palette('dark'), labeldistance=0.7, explode=exp)
                 chart1 = FigureCanvasTkAgg(fig, graph_frame)
                 chart1.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky="s")
                 time.sleep(5)
        
    except Exception as e:
        print(e)
update_graph()
#x= threading.Thread(target=update_graph,daemon=True)
#x.start()               
# Create room buttons and display the initial layout
create_room_buttons()

window.mainloop()
