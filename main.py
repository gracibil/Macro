import tkinter as tk
from tkinter import ttk
from DataStructure import DLinkedList
import macro_functions as macro


class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Macro")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=500, width=300)
        toolbar = Toolbar(container,self)
        # specifying the region where the frame is packed in root
        toolbar.grid(row=0,column=0,sticky='n')

        container.pack(side="top", fill="both", expand=False)


        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MousePage, KeyboardPage, ComboPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=1, column=0, sticky="nsew")

        self.show_frame(MousePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class Toolbar(tk.Frame):  # The toolbar holds all the buttons and their functions
    def __init__(self, container,controller):
        tk.Frame.__init__(self, container)

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
    def __init__(self, container, controller):
        ttk.Frame.__init__(self,container)
        self.row = 1
        self.item_list = DLinkedList()
        self.data_list.append(self.item_list)
        canvas = tk.Canvas(self,bg="blue",height=400, width=600)
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



    def new_macro(self, name):
        macro_name = tk.Label(self.scrollable_frame, text=name, padx=10, pady=10)
        play_btn = tk.Button(self.scrollable_frame, text="Start", command=lambda: macro.convert_macro_text(name), padx=20)
        del_btn = tk.Button(self.scrollable_frame, text="Delete", command=lambda: self.delete_widgets(macro_name),padx=20)

        macro_name.grid(row=self.row, column=1)
        play_btn.grid(row=self.row, column=2)
        del_btn.grid(row=self.row, column=3)

        self.item_list.push_item(macro_name)
        self.item_list.add_data(play_btn)
        self.item_list.add_data2(del_btn)

        self.row += 1

    def delete_widgets(self, item):
       print(item)
       items = self.item_list.find_item(item,1)
       print(items)
       for i in items:
            i.destroy()
       self.row -= 1
       return self.item_list.remove_item(item)

       pass

    def record_macro(self):

        pass


class MousePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.var = tk.BooleanVar(self)

        new_btn = tk.Button(self, text='New Macro',padx=5,pady=5, command=self.save_macro)
        name_box = tk.Entry(self)
        name_box.insert(0, "Macro name")
        time_chck = tk.Checkbutton(self, text="Time sensitive?", variable=self.var)
        record_btn = tk.Button(self, text="Record (F5)",padx=10,pady=10, command=lambda : macro.create_file(name_box.get()))
        save_btn = tk.Button(self, text="Save (F6)",padx=10,pady=10, command=lambda : self.save_macro(name_box.get()))
        overview_label = tk.Label(self, text='My Macros')



        new_btn.grid(row=0, column=1)
        name_box.grid(row=1, column=0)
        time_chck.grid(row=1, column=1)
        record_btn.grid(row=1, column=2)
        save_btn.grid(row=1,column=3)
        overview_label.grid(row=2,column=1)


        self.overview = OverviewFrame(self,controller)
        self.overview.grid(row=3,column=0,columnspan=4)

    def get_bool(self):
        if self.var.get() == False:
            print('off')
        if self.var.get() == True:
            print('on')

    def record_macro(self):
        if self.var.get() == False:
            pass
        else:
            pass

    def save_macro(self, name):
        macro.end_record()
        self.overview.new_macro(name)



class KeyboardPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the Side Page")
        label.pack(padx=10, pady=10)

        overview = OverviewFrame(self, controller)
        overview.pack()


class ComboPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)

        overview = OverviewFrame(self, controller)
        overview.pack()


if __name__ == "__main__":
    macro.setup_listeners()
    testObj = windows()
    testObj.mainloop()