import tkinter as tk
import webbrowser
import requests
from bs4 import BeautifulSoup

def make_api_request(username, page):
    base_url = f"https://usersearch.org/results_advanced{page}.php?URL_username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"  # Brave user agent example
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def parse_results(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    profile_links = []
    for link in soup.find_all('a', class_='pretty-button results-button'):
        if link['href'] != "https://www.usersearch.ai":  # Check for unwanted URL
            profile_links.append({
                'link': link['href'],
            })
    return profile_links

def open_selected_link():
    selected_index = link_listbox.curselection()
    if selected_index:
        selected_link = link_listbox.get(selected_index)
        webbrowser.open(selected_link)

def generate_table_output(profile_links):
    link_listbox.delete(0, tk.END)  # Clear previous links
    for link in profile_links:
        if link['link'] != "https://www.usersearch.ai":  # Check for unwanted URL
            link_listbox.insert(tk.END, link['link'])

def search_button_clicked():
    username = username_entry.get()
    
    all_profile_links = []
    
    # Loop through pages 1 to 10
    for page in range(1, 11):  # Pages 1 to 10
        html_content = make_api_request(username, str(page))
        if html_content:
            profile_links = parse_results(html_content)
            all_profile_links.extend(profile_links)  # Add links from this page to the list
    
    if all_profile_links:
        generate_table_output(all_profile_links)  # Display all links at once
    else:
        output_label.config(text="No results found.")
        
# Create the main window
window = tk.Tk()
window.title("User Search Tool")

# Create UI elements
username_label = tk.Label(window, text="Username:")
username_entry = tk.Entry(window)
page_label = tk.Label(window, text="Page Number (optional):")
page_entry = tk.Entry(window)
page_entry.insert(0, "1")
search_button = tk.Button(window, text="Search", command=search_button_clicked)
output_label = tk.Label(window)

# Create a frame for the Listbox and Scrollbar to manage the layout
listbox_frame = tk.Frame(window)

# Create a Listbox with a larger width for better visibility of the links
link_listbox = tk.Listbox(listbox_frame, width=100, height=10)  # Set a larger width for the listbox
link_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a horizontal scrollbar to the Listbox
scrollbar = tk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL, command=link_listbox.xview)
link_listbox.config(xscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Pack the Listbox frame
listbox_frame.pack()

# Open button to open the selected link
open_button = tk.Button(window, text="Open Link", command=open_selected_link)

# Pack the UI elements
username_label.pack()
username_entry.pack()
search_button.pack()
output_label.pack()
open_button.pack()

window.mainloop()

