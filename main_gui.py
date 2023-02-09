import tkinter as tk
from tkinter import ttk
from DataStructure import DLinkedList
import macro_functions as macro
from pathlib import Path

root = macro.get_project_root()

mouse_dir = (root / 'Mouse Macros')
key_dir = (root/'Keyboard Macros')
combo_dir = (root/'Combo Macros')


class Windows(tk.Tk):
    active_frame = None
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.wm_title("Macro")

        container = tk.Frame(self, height=500, width=300)
        toolbar = Toolbar(container,self)
        toolbar.grid(row=0,column=0,sticky='n')
        container.pack(side="top", fill="both", expand=False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MousePage, KeyboardPage, ComboPage):
            frame = F(container, self)


            self.frames[F] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame(MousePage)
        Windows.active_frame = MousePage

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        Windows.active_frame = frame
        print(Windows.active_frame)


class Toolbar(tk.Frame):  # The toolbar holds all the buttons and their functions
    def __init__(self, parent,controller):
        tk.Frame.__init__(self, parent)

        # Button for saving the menu
        self.create_button("Mouse Macro", lambda:controller.show_frame(MousePage), 2, 20)

        self.create_button("Keyboard Macro", lambda :controller.show_frame(KeyboardPage), 2, 20)

        self.create_button("Combination Macro", lambda:controller.show_frame(ComboPage), 2, 20)


    def create_button(self, text, command, height, width):
        self.button = tk.Button(self,
                                text=text, height=height, width=width)
        self.button['command'] = command
        self.button.pack(side='left')


class OverviewFrame(ttk.Frame):
    data_list = []

    def __init__(self, container, controller, directory):

        ttk.Frame.__init__(self,container)
        self.directory = directory
        self.row = 1
        self.item_list = DLinkedList()
        self.data_list.append(self.item_list)

        canvas = tk.Canvas(self,bg="white",height=400, width=600)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.load_macros()

    def new_macro(self, name):
        macro_name = tk.Label(self.scrollable_frame, text=name, padx=10, pady=10)
        play_btn = tk.Button(self.scrollable_frame, text="Start",
                             command=lambda: macro.convert_macro_text(name, self.directory), padx=20)
        del_btn = tk.Button(self.scrollable_frame, text="Delete",
                            command=lambda: self.delete_widgets(macro_name),padx=20)

        macro_name.grid(row=self.row, column=1)
        play_btn.grid(row=self.row, column=2)
        del_btn.grid(row=self.row, column=3)

        self.item_list.push_item(macro_name)
        self.item_list.add_data(play_btn)
        self.item_list.add_data2(del_btn)

        self.row += 1

    def delete_widgets(self, item):
       self.delete_macro(item.cget('text'))
       print(item)
       items = self.item_list.find_item(item,1)
       print(items)
       for i in items:
            i.destroy()
       self.row -= 1
       return self.item_list.remove_item(item)

    def delete_macro(self, name):
        macro.delete_file(name, self.directory)

    def load_macros(self):
        files = [x for x in Path(self.directory).iterdir() if x.is_file()]
        for file in files:
            name = Path(file).stem
            self.new_macro(name)


class MousePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.var = tk.BooleanVar(self)
        self.directory = mouse_dir

        new_btn = tk.Button(self, text='New Macro',padx=5,pady=5, command=self.new_macro_press)
        self.name_box = tk.Entry(self)
        self.name_box.insert(0, "Macro name")
        time_chck = tk.Checkbutton(self, text="Time sensitive?", variable=self.var)
        self.record_btn = tk.Button(self, text="Record (F5)",padx=10,pady=10,
                                    command=self.record_button_press)
        self.save_btn = tk.Button(self, text="Save (F6)",padx=10,pady=10,
                                  command=lambda : self.save_macro(self.name_box.get()))
        overview_label = tk.Label(self, text='My Macros')

        self.save_btn.configure(state='disabled')

        new_btn.grid(row=0, column=1)
        self.name_box.grid(row=1, column=0)
        time_chck.grid(row=1, column=1)
        self.record_btn.grid(row=1, column=2)
        self.save_btn.grid(row=1,column=3)
        overview_label.grid(row=2,column=1)

        self.overview = OverviewFrame(self,controller, mouse_dir)
        self.overview.grid(row=3,column=0,columnspan=4)
        parent.bind('<F5>', self.record_button_press)
        parent.bind('<F6>', lambda x : self.save_macro(self.name_box.get()))

    def record_button_press(self, event=None):
            self.save_btn.config(state='normal')
            self.record_btn.config(state='disabled')
            macro.create_file(self.name_box.get(), mouse=True, timeing=self.var.get())
            self.name_box.config(state='disabled')

    def save_macro(self, name, event=None):
        macro.end_record()
        self.record_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.overview.new_macro(name)
        self.new_macro_press()

    def new_macro_press(self):
        self.name_box.config(state='normal')
        self.save_btn.config(state='disable')
        self.record_btn.config(state='normal')
        self.name_box.delete(0, tk.END)
        self.name_box.insert(0,'New Macro')






class KeyboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.directory = key_dir
        self.var = tk.BooleanVar(self)
        new_btn = tk.Button(self, text='New Macro', padx=5, pady=5, command= self.new_macro_press)
        self.name_box = tk.Entry(self)
        self.name_box.insert(0, "Macro name")
        time_chck = tk.Checkbutton(self, text="Time sensitive?", variable=self.var)
        self.record_btn = tk.Button(self, text="Record (F5)", padx=10, pady=10,
                                    command=self.record_button_press)

        self.save_btn = tk.Button(self, text="Save (F6)", padx=10, pady=10,
                                  command=lambda : self.save_macro(self.name_box.get()))
        overview_label = tk.Label(self, text='My Macros')

        self.save_btn.config(state='disabled')

        new_btn.grid(row=0, column=1)
        self.name_box.grid(row=1, column=0)
        time_chck.grid(row=1, column=1)
        self.record_btn.grid(row=1, column=2)
        self.save_btn.grid(row=1, column=3)
        overview_label.grid(row=2, column=1)

        self.overview = OverviewFrame(self, controller, key_dir)
        self.overview.grid(row=3, column=0, columnspan=4)
        #controller.bind('<F5>', self.record_button_press)
        #controller.bind('<F6>', lambda x: self.save_macro(self.name_box.get()))

    def record_button_press(self, event=None):
            self.save_btn.config(state='normal')
            self.record_btn.config(state='disabled')
            macro.create_file(self.name_box.get(), keyboard=True, timeing=self.var.get())
            self.name_box.config(state='disabled')

    def save_macro(self, name):
        macro.end_record()
        self.record_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.overview.new_macro(name)
        self.new_macro_press()

    def new_macro_press(self):
        self.name_box.config(state='normal')
        self.save_btn.config(state='normal')
        self.record_btn.config(state='normal')
        self.name_box.delete(0, tk.END)
        self.name_box.insert(0,'New Macro')

    def disable_frame(self):
        for child in self.winfo_children():
            print(child)



class ComboPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.var = tk.BooleanVar(self)

        new_btn = tk.Button(self, text='New Macro', padx=5, pady=5, command=self.new_macro_press)
        self.name_box = tk.Entry(self)
        self.name_box.insert(0, "Macro name")
        time_chck = tk.Checkbutton(self, text="Time sensitive?", variable=self.var)
        self.record_btn = tk.Button(self, text="Record (F5)", padx=10, pady=10,
                                    command=self.record_button_press)
        self.save_btn = tk.Button(self, text="Save (F6)", padx=10, pady=10,
                                  command=lambda: self.save_macro(self.name_box.get()))
        overview_label = tk.Label(self, text='My Macros')

        self.save_btn.configure(state='disabled')

        new_btn.grid(row=0, column=1)
        self.name_box.grid(row=1, column=0)
        time_chck.grid(row=1, column=1)
        self.record_btn.grid(row=1, column=2)
        self.save_btn.grid(row=1, column=3)
        overview_label.grid(row=2, column=1)

        self.overview = OverviewFrame(self, controller, combo_dir)
        self.overview.grid(row=3, column=0, columnspan=4)
        #controller.bind('<F5>', self.record_button_press)
        #controller.bind('<F6>', lambda x: self.save_macro(self.name_box.get()))

    def record_button_press(self, event=None):
        self.save_btn.config(state='normal')
        self.record_btn.config(state='disabled')
        macro.create_file(self.name_box.get(), mouse=True, keyboard=True, timeing=self.var.get())
        self.name_box.config(state='disabled')

    def save_macro(self, name, event=None):
        macro.end_record()
        self.record_btn.config(state='normal')
        self.save_btn.config(state='normal')
        self.overview.new_macro(name)
        self.new_macro_press()

    def new_macro_press(self):
        self.name_box.config(state='normal')
        self.save_btn.config(state='normal')
        self.record_btn.config(state='normal')
        self.name_box.delete(0, tk.END)
        self.name_box.insert(0, 'New Macro')

    def disable_frame(self):
        for child in self.winfo_children():
            print(child)





if __name__ == "__main__":
    macro.setup_listeners()
    mainframe = Windows()
    mainframe.mainloop()
