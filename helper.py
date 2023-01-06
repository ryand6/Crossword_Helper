import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re


def main():
    # start of window object
    root = tk.Tk()
    root.title("Crossword Helper")

    # get user's screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # make window size to user's screen
    root.geometry(f"{screen_width}x{screen_height}")

    frame1 = tk.Frame(root, height=(screen_height//5)*2, width=screen_width)
    frame1.pack(side="top", fill="both", expand=True)

    frame2 = tk.Frame(root, relief="raised", bd=10, height=(screen_height//5)*3, width=screen_width)
    frame2.pack(side="bottom", fill="both", expand=True)

    instructions = tk.Label(frame1, 
        text="Find potential answers to your crossword puzzle clues by entering all known characters in the corresponding boxes. \
Select the length of the word using the drop down answer length boxes and click on 'Find Answers' to retrieve all potential \
words that match based on the characters found. Empty boxes that are within the answer length will match all letters.",
        font="Raleway",
        wraplength=screen_width - 10)
    instructions.pack(fill="x", padx=20, pady=0)
    
    entry_frame = tk.Frame(frame1, bd=0, height=((screen_height//5)*2)//2)
    entry_frame.pack(padx=20, pady=0, fill="x")
    
    numbers_frame = tk.Frame(frame1, bd=0, height=((screen_height//5)*2)//8)
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
        number_box = tk.Label(numbers_frame, text=i+1)
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

        pattern = "^" + pattern + "$"

        nonlocal matches
        matches = set()

        # walk through dictionary and store words that match the regex pattern
        open_fh = open("dictionary.txt", "r")
        for line in open_fh:
            if re.match(pattern, line.strip()):
                matches.add(line.strip())

        res_page = tk.Frame(frame2, relief="groove", bd=5, height=(screen_height//5)*3, width=screen_width)
        res_page.pack(fill="both", expand=True, padx=20, pady=20)
        result_pages.append(res_page)

        res_frame = tk.Frame(res_page, height=((screen_height//5)*3)//6)
        res_frame.pack(side="top", expand=True, fill="x")

        counter = 0

        for match in matches:
            if counter % 30 == 0 and counter:
                res_page = tk.Frame(frame2, height=(screen_height//5)*3, width=screen_width)
                result_pages.append(res_page)
                break

            if counter % 5 == 0 and counter:
                result_frames.append(res_frame)
                res_frame = tk.Frame(res_page, width=screen_width, height=((screen_height//5)*3)//6)
                res_frame.pack(side="top", fill="x", expand=True)

            res_label = tk.Label(res_frame, text="- " + match)
            res_label.pack(side="left", expand=True)
            result_labels.append(res_label)
            
            counter += 1
   

    def clear_button_click():
        for entry in entries:
            entry.delete(0, "end")

    options_frame = tk.Frame(frame1)
    options_frame.pack(fill="x")

    clear_answers = tk.Button(options_frame, text="Clear", command=clear_button_click)
    clear_answers.pack(side="right", pady=20, padx=20)

    generate_answers = tk.Button(options_frame, text="Find Answers", command=generate_button_click)
    generate_answers.pack(pady=20, padx=20, side="right")

    wordlength = ttk.Combobox(options_frame, textvariable=selected_option, values=wordlengths[2:])
    wordlength.set(4)
    wordlength.bind("<<ComboboxSelected>>", option_selected)
    wordlength.pack(pady=20, padx=20, side="right")

    wordlength_label = tk.Label(options_frame, text="Please specify length of answer: ")
    wordlength_label.pack(pady=20, side="right")

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