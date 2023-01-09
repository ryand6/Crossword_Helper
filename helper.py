import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re


def main():
    # start of window object
    root = tk.Tk()
    root.title("Crossword Helper")

    # get user's screen width and height
    screen_width = int(root.winfo_screenwidth() // 2)
    screen_height = int(root.winfo_screenheight() // 2)

    # make window size to user's screen
    root.geometry(f"{screen_width}x{screen_height}")

    frame1 = tk.Frame(root, height=(screen_height//5)*1.5, width=screen_width, background="#D9D9F3")
    frame1.pack(side="top", fill="both")

    frame2 = tk.Frame(root, relief="raised", bd=10, height=(screen_height//5)*3.5, width=screen_width, background="#DDEDEA")
    frame2.pack(fill="both", expand=True)

    res_page = tk.Frame(frame2, relief="groove", bd=5, height=(screen_height//5)*3.5, width=screen_width, background="#DAEAF6")
    res_page.pack(fill="both", padx=40, pady=40, expand=True)

    instructions = tk.Label(frame1, 
        text="Find potential answers to your crossword puzzle clues by entering all known characters in the corresponding boxes. \
Select the length of the word using the drop down answer length boxes and click on 'Find Answers' to retrieve all potential \
words that match based on the characters found. Empty boxes that are within the answer length will match all letters.",
        font=("Arial", 12, "bold"),
        wraplength=screen_width - 20,
        background="#D9D9F3")
    instructions.pack(fill="x", padx=20, pady=20, expand=True)
    
    entry_frame = tk.Frame(frame1, bd=0, height=((screen_height//5)*2)//2, background="#D9D9F3")
    entry_frame.pack(padx=20, pady=0, fill="x")
    
    numbers_frame = tk.Frame(frame1, bd=0, height=((screen_height//5)*2)//8, background="#D9D9F3")
    numbers_frame.pack(padx=20, pady=0, fill="x")

    entries = []


    def on_release(event):
        entry_content = event.widget.get()
        entry_content = entry_content.upper()
        event.widget.delete(0, "end")
        event.widget.insert(0, entry_content)


    wordlengths = []

    for i in range(25):
        textbox = tk.Entry(entry_frame, width=1, justify="center", font=("Helvetica", ((screen_height//5)*2)//8), validate="key", validatecommand=(root.register(validate), "%P"))
        textbox.pack(side="left", fill="both", expand=True)
        textbox.bind("<KeyRelease>", on_release)
        entries.append(textbox)
        number_box = tk.Label(numbers_frame, text=i+1, background="#D9D9F3")
        number_box.pack(side="left", expand=True)
        wordlengths.append(i+1)

    selected_option = tk.StringVar()


    def option_selected(*args):
        nonlocal selected_option
        if isinstance(selected_option, str):
            return
        else:
            selected_option = selected_option.get()

    matches = set()
    result_pages = []
    result_frames = []
    result_labels = []


    def generate_button_click():
        nonlocal result_labels
        nonlocal result_frames
        nonlocal result_pages
        nonlocal selected_option
        nonlocal res_page

        res_page.forget()
        res_page.destroy()

        if result_pages:
            for page in result_pages:
                page.pack_forget()
                page.destroy()

        result_pages = []

        # get regex pattern by reading user input in text entry boxes
        pattern = ""
        for entry in entries:
            input = entry.get()
            if not input:
                input = "."
            pattern += input
        if isinstance(selected_option, str):
            pattern = pattern[:int(selected_option)]
        else:
            pattern = pattern[:int(selected_option.get())]
        if pattern.count(".") == len(pattern):
            messagebox.showerror("Error", "Pattern must contain atleast one letter!")
            return

        known_chars = []

        # used later as indices to change known chars to red
        for i in range(len(pattern)):
            if pattern[i].isalpha():
                known_chars.append(i)

        pattern = "^" + pattern + "$"

        nonlocal matches
        matches = set()

        # walk through dictionary and store words that match the regex pattern
        open_fh = open("dictionary.txt", "r")
        for line in open_fh:
            if re.match(pattern, line.strip()):
                matches.add(line.strip())

        res_page = tk.Frame(frame2, relief="groove", bd=5, height=(screen_height//5)*3.5, width=screen_width, background="#DAEAF6")
        res_page.pack(fill="both", padx=40, pady=40, expand=True)
        result_pages.append(res_page)

        res_frame = tk.Frame(res_page, height=((screen_height//5)*3.5)//6, background="#DAEAF6")
        res_frame.pack(side="top", fill="x")
        result_frames.append(res_frame)

        counter = 0

        for match in matches:
            if counter % 30 == 0 and counter:
                res_page = tk.Frame(frame2, relief="groove", bd=5, height=(screen_height//5)*3.5, width=screen_width, background="#DAEAF6")
                result_pages.append(res_page)

            if counter % 5 == 0 and counter:
                res_frame = tk.Frame(res_page, width=screen_width, height=((screen_height//5)*3.5)//6, background="#DAEAF6")
                res_frame.pack(side="top", fill="x", expand=True)
                result_frames.append(res_frame)

            res_label = tk.Text(res_frame, font=("Helvetica", ((screen_height//5)*2)//17, "bold"), height=1, width=20, background="#DAEAF6")
            res_label.pack(side="left", fill="x", expand=True)

            res_label.insert("1.0", "• " + match)

            # use to highlight the known characters in red
            res_label.tag_config("red", foreground="red")
            for char in known_chars:
                start = "1." + str(char + 2)
                end = "1." + str(char + 3) 
                res_label.tag_add("red", start, end)

            res_label.configure(state="disabled", background="#DAEAF6", relief="flat")

            result_labels.append(res_label)
            
            counter += 1
   

    def clear_button_click():
        nonlocal result_pages
        nonlocal result_frames
        nonlocal result_labels

        for entry in entries:
            entry.delete(0, "end")

        for p in result_pages:
            p.pack_forget()
            p.destroy()

        for f in result_frames:
            f.pack_forget()
            f.destroy()

        for l in result_labels:
            l.pack_forget()
            l.destroy()

        page_no.configure(text="1")


    options_frame = tk.Frame(frame1, height=((screen_height//5)*2)//8, background="#D9D9F3")
    options_frame.pack(fill="x")

    clear_answers = tk.Button(options_frame, text="Clear", command=clear_button_click)
    clear_answers.pack(side="right", pady=20, padx=20)

    generate_answers = tk.Button(options_frame, text="Find Answers", command=generate_button_click)
    generate_answers.pack(pady=20, padx=20, side="right")

    wordlength = ttk.Combobox(options_frame, textvariable=selected_option, values=wordlengths[2:])
    wordlength.set(4)
    wordlength.bind("<<ComboboxSelected>>", option_selected)
    wordlength.pack(pady=20, padx=20, side="right")

    wordlength_label = tk.Label(options_frame, text="Please specify length of answer: ", background="#D9D9F3")
    wordlength_label.pack(pady=20, side="right")

    change_page = tk.Frame(frame1, height=((screen_height//5)*2)//8, background="#D9D9F3")
    change_page.pack(fill="x", padx=20)


    def next_page():
        nonlocal result_pages
        if len(result_pages) <= 1:
            return
        page = int(page_no.cget("text"))
        if page == len(result_pages):
            return
        result_pages[page-1].pack_forget()
        result_pages[page].pack(fill="both", padx=40, pady=40, expand=True)
        page_no.configure(text=str(page + 1))


    def previous_page():
        nonlocal result_pages
        if len(result_pages) <= 1:
            return
        page = int(page_no.cget("text"))
        if page == 1:
            return
        result_pages[page-1].pack_forget()
        result_pages[page-2].pack(fill="both", padx=40, pady=40, expand=True)
        page_no.configure(text=str(page - 1))


    page_right = tk.Button(change_page, text=">", command=next_page)
    page_right.pack(side="right")

    page_no = tk.Label(change_page, text="1", background="#D9D9F3")
    page_no.pack(side="right")

    page_left = tk.Button(change_page, text="<", command=previous_page)
    page_left.pack(side="right")

    page_text = tk.Label(change_page, text="Answer Results", background="#D9D9F3")
    page_text.pack(side="right")

    root.mainloop()


def validate(S):
    if len(S) == 0:
        return True
    elif S.isalpha() and len(S) == 1:
        return True
    else:
        return False


if __name__ == "__main__":
    main()