import tkinter as tk
import webbrowser
import requests
from bs4 import BeautifulSoup

def make_api_request(username, page):
    base_url = f"https://usersearch.org/results_advanced{page}.php?URL_username={username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None

def parse_results(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    profile_links = []
    for link in soup.find_all('a', class_='pretty-button results-button'):
        if link['href'] != "https://www.usersearch.ai":  
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
    link_listbox.delete(0, tk.END)  
    for link in profile_links:
        if link['link'] != "https://www.usersearch.ai":  
            link_listbox.insert(tk.END, link['link'])

def search_button_clicked():
    username = username_entry.get()
    
    all_profile_links = []
    
    
    for page in range(1, 11):  
        html_content = make_api_request(username, str(page))
        if html_content:
            profile_links = parse_results(html_content)
            all_profile_links.extend(profile_links)  
    
    if all_profile_links:
        generate_table_output(all_profile_links)  
    else:
        output_label.config(text="No results found.")
        

window = tk.Tk()
window.title("User Search Tool")


username_label = tk.Label(window, text="Username:")
username_entry = tk.Entry(window)
page_label = tk.Label(window, text="Page Number (optional):")
page_entry = tk.Entry(window)
page_entry.insert(0, "1")
search_button = tk.Button(window, text="Search", command=search_button_clicked)
output_label = tk.Label(window)


listbox_frame = tk.Frame(window)


link_listbox = tk.Listbox(listbox_frame, width=100, height=10)  
link_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


scrollbar = tk.Scrollbar(listbox_frame, orient=tk.HORIZONTAL, command=link_listbox.xview)
link_listbox.config(xscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)


listbox_frame.pack()


open_button = tk.Button(window, text="Open Link", command=open_selected_link)


username_label.pack()
username_entry.pack()
search_button.pack()
output_label.pack()
open_button.pack()

window.mainloop()

