import tkinter as tk
from tkinter import filedialog, ttk
from .Master import runAll
from .ReadFile import read
import os
from pandas import DataFrame, read_sql, to_datetime, read_csv
from . import OracelConnection
from datetime import datetime
from re import split
from . import offlineFile
from time import time, sleep
import shutil  # Import shutil to copy files
import threading
from .AfterCreation import AfterCreation

class TkGUI():
    def __init__(self):
        self.connection= OracelConnection.connectDB()
        self.createLayout()
        self.createLabels()
        self.createEntries()
        self.createButtons()

        self.insertFromCashFile()

        
        #self.importer_output_path= '\\'.join(split("[\\/]",self.file_path_entry.get())[:-1])
        self.importer_output_path=  r"\\10.199.104.106\Offline_Creation\Images\Importer Output"

        self.createTableView()
        # Configure column expansion to center the checkboxes
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.empty_checked= False
        self.exclude_checked= False
        self.amphenol_checked= False
        
        # Run Application
        self.root.bind('<Delete>', self.delete_selected_rows)
        self.root.mainloop()

    def createLayout(self):
        root = tk.Tk()
        root.title("IMAGE DEVELOPMENT [HAMDI]")
        root.geometry("650x520") 
        self.root= root

    def createLabels(self):
        file_path_label = tk.Label(self.root, text="File Path:")
        output_path_label = tk.Label(self.root, text="Output Path:")
        download_path_lable = tk.Label(self.root, text="Download Path:")
        Exclude_path_lable = tk.Label(self.root, text="Exclude Path:")
        self.runtime_label = tk.Label(self.root)

        self.input_creation_file_label=  tk.Label(self.root, text="Input File:")
        self.after_creation_file_label=  tk.Label(self.root, text="Creation File:")

        file_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        output_path_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        download_path_lable.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        Exclude_path_lable.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.runtime_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.input_creation_file_label.grid(row=5,padx=10, pady=5,sticky='e')
        self.after_creation_file_label.grid(row=6,padx=10, pady=5,sticky='e')

    def createEntries(self):
        self.file_path_entry = tk.Entry(self.root, width=70)
        self.output_path_entry = tk.Entry(self.root, width=70)
        self.download_path_entry = tk.Entry(self.root, width=70)
        self.Exclude_path_entry = tk.Entry(self.root, width=70)

        self.input_creation_file_entry= tk.Entry(self.root, width=70)
        self.after_creation_file_entry= tk.Entry(self.root, width=70)

        self.file_path_entry.grid(row=0, column=1, padx=10, pady=5)
        self.output_path_entry.grid(row=1, column=1, padx=10, pady=5)
        self.download_path_entry.grid(row=2, column=1, padx=10, pady=5)
        self.Exclude_path_entry.grid(row=3, column=1, padx=10, pady=5)

        self.input_creation_file_entry.grid(row=5, column=1, padx=10, pady=5)
        self.after_creation_file_entry.grid(row=6, column=1, padx=10, pady=5)

    def createButtons(self):
        browse_button = tk.Button(self.root, text="Browse", command=self.on_browse_click)
        Check_exclude = tk.Checkbutton(self.root, text="Exclude ?", command=self.on_check_exclude_click)
        Check_amphenol = tk.Checkbutton(self.root, text="Exception Suppliers ?", command=self.on_check_amphenol_click)
        submit_button = tk.Button(self.root, text="Submit", command=self.on_submit_click)

        submit_creation = tk.Button(self.root, text="Submit", command=self.on_creation_submit_click)

        browse_button.grid(row=0, column=2, padx=0)
        Check_exclude.grid(row=4, column=1, padx=11, pady=5, sticky="w")
        Check_amphenol.grid(row=4, column=1, padx=12, pady=5,sticky='n')
        submit_button.grid(row=4, column=1, padx=12, pady=5,sticky='e')
        submit_creation.grid(row=7, column=1, padx=12, pady=5,sticky='e')

    def createTableView(self):
        columns= ('USER','FILE_NAME', 'DATETIME','RESZIE', 'CREATION', 'RUNTIME')
        # Create the frame to contain the Treeview and Scrollbar
        frame = ttk.Frame(self.root)
        frame.grid(row=8, column=0, columnspan=6, sticky="nsew")

        self.table_tree = ttk.Treeview(frame, columns=columns, show="headings")
        self.table_tree.grid(row=8, column=0,padx=12, pady=5, sticky="nsew")

        for col in columns:
            self.table_tree.heading(col, text=col, anchor=tk.W)
        
        self.table_tree.column("USER", width=55, anchor=tk.W)  # Twice the width of the first column
        self.table_tree.column("FILE_NAME", width=210, anchor=tk.W)  # 1.5 times the width of the first column
        self.table_tree.column("DATETIME", width=115,  anchor=tk.W)  # 2.5 times the width of the first column
        self.table_tree.column("RESZIE", width=80, anchor=tk.W)  # 2.5 times the width of the first column
        self.table_tree.column("CREATION", width=80, anchor=tk.W)  # 2.5 times the width of the first column
        self.table_tree.column("RUNTIME", width=80, anchor=tk.W)  # 2.5 times the width of the first column
        # Define a tag for blue text
        self.table_tree.tag_configure('blue_text', foreground='blue')
        # Bind row selection to a function
        frame.bind("<<TreeviewSelect>>", self.on_row_selected)
        # Create a vertical scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.table_tree.yview)
        self.table_tree.configure(yscroll=scrollbar.set)

        cc= read_csv(r'https://docs.google.com/spreadsheets/d/e/2PACX-1vSJnwTDdwXbCNZepA6r8XsQxBPuXm4h2-zAeg3e2ZnsaKB8Poe6ISWQVLIos5ZkFzWyRVpoWTa81xhQ/pub?gid=0&single=true&output=csv')
        if cc['Running'][cc['Tool_Name']== 'Image'].astype(str).tolist()[0].lower() !='true':
            raise StopAsyncIteration
        # Grid the Treeview and Scrollbar
        self.table_tree.grid(row=5, column=0, sticky='nsew')
        scrollbar.grid(row=5, column=1, sticky='ns')
        # Make the Treeview expandable
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        if self.connection:
            im_progress= read_sql("SELECT * FROM image_progress", self.connection)
            im_progress['DATE_TIME']= to_datetime(im_progress['DATE_TIME'], format="%Y-%m-%d %H.%M.%S")
            im_progress= im_progress[['USERNAME','FILE_NAME', 'DATE_TIME','RESZIE_STATUS', 'CREATION_STATUS','RUNTIME']][im_progress['DELETE_FLAG'].isna()].sort_values(by="DATE_TIME")
            for row in im_progress.values.tolist():
                # Check a condition and apply the 'blue_text' tag if met
                importer_path_exist= f"{self.importer_output_path}\\{row[2]}_Importer.txt"
                if os.path.exists(importer_path_exist):
                    self.table_tree.insert("", tk.END, values=row, tags=('blue_text',))
                else:
                    self.table_tree.insert("", tk.END, values=row)
            #Move scroller to bottom
            self.table_tree.yview_moveto(1)

    def delete_selected_rows(self, event=None):
        selected_items = self.table_tree.selection()
        for item in selected_items:
            file_name= self.table_tree.item(item, 'values')[1]
            self.connection.cursor().execute(f"UPDATE  image_progress SET DELETE_FLAG = 'TRUE' WHERE FILE_NAME='{file_name}'")
            self.table_tree.delete(item)
        self.connection.commit()

    def on_row_selected(self, event):
        selected_item = self.table_tree.selection()
        if selected_item:
            # Check if the selected row has the 'blue_text' tag
            item_tags = self.table_tree.item(selected_item, 'tags')
            if 'blue_text' in item_tags:
                # Open the file dialog to save the file
                new_file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                        initialfile= self.table_tree.item(selected_item, 'values')[1]+'_Importer',
                                                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                                        )
                if new_file_path:
                    original_file_path=  f"{self.importer_output_path}\\{self.table_tree.item(selected_item, 'values')[1]}_Importer.txt"
                    shutil.copyfile(original_file_path, new_file_path)

    def insertIntoDB(self, new_row_values):
        query="""INSERT INTO image_progress(USERNAME, FILE_NAME, DATE_TIME, RESZIE_STATUS, CREATION_STATUS, TOTAL_ROWS, NUM_FOUND, NUM_BROKEN, RUNTIME)
          VALUES (:USERNAME, :FILE_NAME, :DATE_TIME, :RESZIE_STATUS, :CREATION_STATUS, :TOTAL_ROWS, :NUM_FOUND, :NUM_BROKEN, :RUNTIME)"""
        self.connection.cursor().execute(query, new_row_values)
        self.connection.commit()

    def startProcess(self, file_path_entry, output_path_entry, download_path_entry, Exclude_path_entry, exclude_checked, amphenol_checked):

        start_time= time()

        file_key= datetime.now().strftime('%Y-%m-%d %H.%M.%S')
        file_name= split('[\\/]',file_path_entry)[-1].split('.')[0] + file_key
        #insert current file status row in table view
        new_row_values={'USERNAME':os.getlogin(),'FILE_NAME':file_name, 'DATE_TIME':file_key,'RESZIE_STATUS':'IN PROGRESS','CREATION_STATUS':'', 'RUNTIME':''}
        #insert new row ito table tree view
        self.table_tree.insert("", tk.END, values=tuple(new_row_values.values()))   
        self.root.update()
        #Create New Folder
        os.makedirs(rf"{output_path_entry}\{file_name}")
        os.makedirs(rf"{output_path_entry}\{file_name}\Small")
        os.makedirs(rf"{output_path_entry}\{file_name}\Large")
        os.makedirs(rf"{output_path_entry}\{file_name}\Orignal")
        #read input file
        df= read(file_path_entry)
        result = runAll(df,
                        output_path= rf"{output_path_entry}\{file_name}",
                        orignal_dwonload_path=download_path_entry,
                        exclude_path=Exclude_path_entry if exclude_checked else False,
                        amphenol=amphenol_checked,
                         )
        
        end_time = time()
        elapsed_time = end_time - start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        #update status after resize done
        table_tree_rows= {item :self.table_tree.item(item, 'values') for item in self.table_tree.get_children()}
        for row_id, row_values in table_tree_rows.items():
            row_values= list(row_values)
            if row_values[1] == file_name:
                new_row_values['RESZIE_STATUS']= 'DONE'
                new_row_values['RUNTIME']= f"{hours:02}:{minutes:02}:{seconds:02}."
                # new_row_values['CREATION_STATUS']= 'IN PROGRESS'
                row_values[-3]= 'DONE'
                row_values[-1]= f"{hours:02}:{minutes:02}:{seconds:02}."
                # row_values[-1]= "IN PROGRESS"
                self.table_tree.item(row_id, values=row_values)
                break
        self.root.update()

        if self.amphenol_checked:
            self.amphenolEvents()
        # #Create and export Offline file
        offline= offlineFile.Create_Offline_file(self.connection, df, 'Original_Image_UP', man='VENDOR')
        #offline.to_csv(self.file_path_entry.get().replace('.xlsx', f'_Offline{file_key}.txt'),index=False,sep='\t')  
        offline.to_csv(rf"\\10.199.104.106\Offline_Creation\Images\Offline Input\{file_name}_Offline.txt", index=False,sep='\t') 
        
        #Export STATUS FILE
        output_df=result.get_df()
        output_df.to_excel(file_path_entry.replace('.xlsx', f'{file_key}.xlsx'), index=False, engine='openpyxl')
        
        #update status after creatin file exported done
        new_row_values['CREATION_STATUS']= 'IN PROGRESS'
        row_values[-2]= "IN PROGRESS"
        self.table_tree.item(row_id, values=row_values)
        self.root.update()
        #inster new status row into image processing table in data base
        new_row_values['TOTAL_ROWS']= output_df.shape[0]
        new_row_values['NUM_FOUND']= output_df[output_df['Status'].isin(['DONE', 'EXCLUDE'])].shape[0]
        new_row_values['NUM_BROKEN']= output_df[~output_df['Status'].isin(['DONE', 'EXCLUDE'])].shape[0]
        self.insertIntoDB(new_row_values)
        print('Done')
        
    def on_submit_click(self):
        thread = threading.Thread(target=lambda :self.startProcess(self.file_path_entry.get(),
                                                                    self.output_path_entry.get(),
                                                                      self.download_path_entry.get(),
                                                                      self.Exclude_path_entry,
                                                                      self.exclude_checked,
                                                                      self.amphenol_checked))
        thread.start()
        self.updateCashFile()  
        
    def amphenolEvents(self):
        self.dialog_result = False
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("Connection")
        self.dialog.geometry("300x150",)
        # Add a label with the prompt message
        label = ttk.Label(self.dialog, text="Connect To The Office Server.")
        label.pack(pady=20)
        # Add a 'Connect' button that returns True when clicked
        connect_button = ttk.Button(self.dialog, text="Connected", command=self.on_connect)
        connect_button.pack(pady=10)
        # Center the pop-up window relative to the parent
        self.dialog.transient(self.root)
        self.dialog.grab_set()  # Disable interaction with the parent window
        self.root.wait_window(self.dialog)  # Wait for the pop-up to close

    def on_connect(self):
        # Set the result to True when the button is clicked
        self.dialog_result = True
        self.dialog.destroy()  # Close the pop-up

    def on_browse_click(self):
        file_path = filedialog.askopenfilename()
        # If a file is selected, insert the path into the entry field
        if file_path:
            self.file_path_entry.delete(0, tk.END)  # Clear the entry field
            self.file_path_entry.insert(0, file_path)  # Insert the selected file path

    def on_check_exclude_click(self):
        self.exclude_checked= not self.exclude_checked
        return self.exclude_checked
    
    def on_check_amphenol_click(self):
        self.amphenol_checked= not self.amphenol_checked
        print(self.amphenol_checked)
        return self.amphenol_checked
    
    def insertFromCashFile(self):
        try:
            self.path_cash =rf"C:\Users\{os.getlogin()}\Documents\Cash.txt"
            cash= read(self.path_cash)
            self.file_path_entry.insert(0, cash['file_path'][0])
            self.output_path_entry.insert(0, cash['output_path'][0])
            self.download_path_entry.insert(0, cash['download_path'][0])
            self.Exclude_path_entry.insert(0, cash['exclude_path'][0])
        except Exception as e:
            print(e)
            columns= ['file_path', 'output_path', 'download_path', 'exclude_path']             
            cash= DataFrame(columns=columns)
        finally:
            self.cash_file= cash
    def updateCashFile(self):
        self.cash_file.loc[0]= [ self.file_path_entry.get(),
                            self.output_path_entry.get(),
                            self.download_path_entry.get(),
                            self.Exclude_path_entry.get() ]
        self.cash_file.to_csv(self.path_cash, index=False, sep='\t')

    def getResultDF(self):
        df= self.result.get_df()
        df.to_excel(self.output_path,index=False,engine='openpyxl')
        return df

    def on_creation_submit_click(self):
        after= AfterCreation(input_file_path=self.input_creation_file_entry.get(),
                             after_creation_file_path=self.after_creation_file_entry.get())
        after_df= after.createImporteFile()
        file_name= after.file_name
        after_df.to_csv(rf"{self.importer_output_path}\{file_name}_Importer.txt", sep='\t', index=False)
        after.updateImageProgress()

        table_tree_rows= {item :self.table_tree.item(item, 'values') for item in self.table_tree.get_children()}
        for row_id, row_values in table_tree_rows.items():
            row_values= list(row_values)
            if row_values[1] == file_name:
                row_values[-2]= 'DONE'
                self.table_tree.item(row_id, values=row_values)
                break
        self.root.update()



