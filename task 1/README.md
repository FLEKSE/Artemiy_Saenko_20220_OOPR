# Artemiy_Saenko_20220_OOPR

Task_1: Создание программы "Учет расходов" на базе Tkinter
1) Программа должна быть в ООП стиле.
2) Проверка вводимых значений в поля.
3) Всплывающие подсказки группы товара.
4) Сортировка по цене max min. 
5) Сортировка по группам товара.


Программа позволяет создавать, сохранять, открывать и редактировать таблицы расширения .csv. Если пользователь ввёл корректные данные, то они будут добавлены в таблицу.

```python
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv
import time


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Учёт расходов")
        weight = 660
        height = 460
        self.geometry(f"{weight}x{height}")
        self.resizable(False, False)

        self.category_list = []

        self.open_button = ttk.Button(text="Открыть файл", command=self.open_file)
        self.open_button.grid(column=1, row=6, sticky='NSEW', padx=10)   

        self.save_button = ttk.Button(text="Сохранить файл", command=self.save_file) 
        self.save_button.grid(column=2, row=6, sticky='NSEW', padx=10) 

        self.labelData = tk.Label(self, text="Дата (ДД.ММ.ГГГГ)") 
        self.labelData.grid(row=1, column=0, sticky="ew")        

        self.entryData = tk.Entry(self, width=22)
        self.entryData.grid(row=1, column=1)    

        self.labelCategory = tk.Label(self, text="Категория")
        self.labelCategory.grid(row=2, column=0, sticky="ew")  

        self.entryCategory = ttk.Combobox(self, values=self.category_list)  
        self.entryCategory.grid(row=2, column=1) 

        self.labelAmount = tk.Label(self, text="Цена")     
        self.labelAmount.grid(row=3, column=0, sticky="ew") 

        self.entryAmount = tk.Entry(self, width=22)                         
        self.entryAmount.grid(row=3, column=1, sticky="ew")  

        self.addButton = ttk.Button(self, text="Добавить", command=self.write)  
        self.addButton.grid(row=4, column=0, columnspan=2, pady=20)   
        
        self.delete_button = ttk.Button(self, text="Удалить выбранное", command=self.delete_selected)  
        self.delete_button.grid(row=6, column=0, sticky='NSEW', padx=10)
        
        self.scrollbar = ttk.Scrollbar(self, orient="vertical")  
        self.scrollbar.grid(row=5, column=4, sticky="ns")      

        self.tree = ttk.Treeview(self, columns=("Дата", "Категория", "Цена"), yscrollcommand=self.scrollbar.set, show="headings") 
        self.tree.heading("Дата", text="Дата")                                                                                     
        self.tree.heading("Категория", text="Категория", command=lambda: self.treeview_sort_column(self.tree, "Категория", True))     
        self.tree.heading("Цена", text="Цена", command=lambda: self.treeview_sort_column(self.tree, "Цена", True))  

        self.tree.column("Дата", width=weight // 3)
        self.tree.column("Категория", width=weight // 3)
        self.tree.column("Цена", width=weight // 3)                         
        self.tree.grid(row=5, columnspan=3, sticky="nsew")  

        self.scrollbar.config(command=self.tree.yview)    
        self.grid_rowconfigure(5, weight=1)     
        self.grid_columnconfigure(0, weight=1)  
        
        self.get_categories()
        self.sum() 

    def delete_selected(self):
        selected_items = self.tree.selection()
        for item in selected_items:
            self.tree.delete(item)
        self.sum() 
        self.get_categories()
    
   
    def write(self):
        self.date = self.entryData.get()
       
        self.category = self.entryCategory.get()
        
        self.amount = self.entryAmount.get()
       
        if (self.check(self.date, 0) and self.check(self.amount, 1)):
            self.tree.insert("", tk.END, values=(self.date, self.category, self.amount))
            self.entryData.delete(0, tk.END)
            self.entryCategory.delete(0, tk.END)
            self.entryAmount.delete(0, tk.END)
            self.get_categories()
            self.sum()  
        else:
            self.open_window()
        print(self.category_list)
    
    def get_categories(self) -> None:
        for item in self.tree.get_children(""):
            for i in [self.tree.item(item, option='values')]:
                if not(i[1] in self.category_list): self.category_list.append(i[1])
        try: self.delete(self.entryCategory)  
        except: pass                   
        self.entryCategory = ttk.Combobox(self, values=self.category_list)
        self.entryCategory.grid(row=2, column=1)

   
    def sum(self):
        self.s = 0
        for item in self.tree.get_children(""):
            for i in [self.tree.item(item, option='values')]: 
                self.s += int(i[2])
        try: self.delete(self.labelB)  
        except: pass                   
        self.labelB = tk.Label(self, text="Сумма: "+str(self.s))  
        self.labelB.grid(row=7,  columnspan=2)  
    
 
    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])  
        if filepath != "": 
            with open(filepath, mode='w', encoding='utf-8', newline='') as output:
                w = csv.writer(output, quoting=csv.QUOTE_ALL)   
                for item in self.tree.get_children(""):                
                    w.writerow(self.tree.item(item, option='values'))  


    def open_file(self):
        filepath = filedialog.askopenfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])  
        if filepath != "":  
            with open(filepath) as file:
                self.tree.delete(*self.tree.get_children())  
                r = csv.reader(file) 
                for el in r:                                 
                    self.tree.insert("", tk.END, values=el)  


    def check(self, ver: str, mode: int):
        if mode == 0:                                        
            ver = ver.replace('.', '/')                      
            try:                                             
                time.strptime(ver, '%m/%d/%Y')               
                return True                                  
            except ValueError:                               
                return False                                 

        elif mode == 1:                                      
            try:                                             
                int(ver)                                   
                return True                                  
            except TypeError:                                
                pass                                         
        return False                                         
    
    
    def treeview_sort_column(self, tv, col, reverse, key=str):
            l = [(tv.set(k, col), k) for k in tv.get_children()]
            l.sort(reverse=reverse, key=lambda t: key(t[0]))

            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse, key=key))

if __name__ == "__main__":
    app = App()
    app.mainloop()
```

Результатом работы программы является файл с разрешением .csv в котором храниться талица с категориями, датами и ценами

![Main interface](https://github.com/KingMem/Victor_Masis_20220_OOPR/blob/main/Task_1/img/main_interface.png)
![Amount sorting](https://github.com/KingMem/Victor_Masis_20220_OOPR/blob/main/Task_1/img/amount_sort.png)
![Category sorting](https://github.com/KingMem/Victor_Masis_20220_OOPR/blob/main/Task_1/img/category_sort.png)
![Tip for category](https://github.com/KingMem/Victor_Masis_20220_OOPR/blob/main/Task_1/img/list.png)