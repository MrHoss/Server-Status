from multiprocessing import Process
from functools import partial
from tkinter import *
import socket
import tkinter as tk
import sqlite3
import time

print("Software made by MrHoss")
print("GitHub: https://github.com/MrHoss")
print("Please dont f@ck with everything!!")


conn = sqlite3.connect("serverList.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    CREATE TABLE servers (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            url VARCHAR NOT NULL,
            port INTEGER
    );
    """)
    print("Tabela criada com sucesso!")
except:
    print("Conectado à tabela!")

class ScrollableFrame(tk.Frame):
        
    def __init__(self, master=None, scroll_speed:int=2, hscroll:bool=False,
                vscroll:bool=True, bd:int=0, scrollbar_kwargs={},
                bg="#f0f0ed", **kwargs):
        assert isinstance(scroll_speed, int), "`scroll_speed` must be an int"
        self.scroll_speed = scroll_speed
        self.master_frame = tk.Frame(master, bd=bd, bg=bg)
        self.master_frame.grid_rowconfigure(0, weight=1)
        self.master_frame.grid_columnconfigure(0, weight=1)
        self.dummy_canvas = tk.Canvas(self.master_frame, highlightthickness=0,
                                    bd=0, bg=bg, **kwargs)
        super().__init__(self.dummy_canvas, bg=bg)

            
        if vscroll:
            self.v_scrollbar = tk.Scrollbar(self.master_frame,
                                            orient="vertical",
                                            command=self.dummy_canvas.yview,
                                            **scrollbar_kwargs)
            self.v_scrollbar.grid(row=0, column=1, sticky="news")
            self.dummy_canvas.configure(yscrollcommand=self.v_scrollbar.set)
        if hscroll:
            self.h_scrollbar = tk.Scrollbar(self.master_frame,
                                            orient="horizontal",
                                            command=self.dummy_canvas.xview,
                                            **scrollbar_kwargs)
            self.h_scrollbar.grid(row=1, column=0, sticky="news")
            self.dummy_canvas.configure(xscrollcommand=self.h_scrollbar.set)

            
        self.dummy_canvas.bind_all("<MouseWheel>", self.scrolling_windows,
                                    add=True)
        self.dummy_canvas.bind_all("<Button-4>", self.scrolling_linux, add=True)
        self.dummy_canvas.bind_all("<Button-5>", self.scrolling_linux, add=True)
        self.bind("<Configure>", self.scrollbar_scrolling, add=True)

            
        self.dummy_canvas.create_window((0, 0), window=self, anchor="nw")
            
        self.dummy_canvas.grid(row=0, column=0, sticky="news")

        self.pack = self.master_frame.pack
        self.grid = self.master_frame.grid
        self.place = self.master_frame.place
        self.pack_forget = self.master_frame.pack_forget
        self.grid_forget = self.master_frame.grid_forget
        self.place_forget = self.master_frame.place_forget

    def scrolling_windows(self, event:tk.Event) -> None:
        assert event.delta != 0, "On Windows, `event.delta` should never be 0"
        y_steps = int(-event.delta/abs(event.delta)*self.scroll_speed)
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrolling_linux(self, event:tk.Event) -> None:
        y_steps = self.scroll_speed
        if event.num == 4:
            y_steps *= -1
        self.dummy_canvas.yview_scroll(y_steps, "units")

    def scrollbar_scrolling(self, event:tk.Event) -> None:
        region = list(self.dummy_canvas.bbox("all"))
        region[2] = max(self.dummy_canvas.winfo_width(), region[2])
        region[3] = max(self.dummy_canvas.winfo_height(), region[3])
        self.dummy_canvas.configure(scrollregion=region)

    def resize(self, fit:str=None, height:int=None, width:int=None) -> None:
           
        if height is not None:
                self.dummy_canvas.config(height=height)
        if width is not None:
                self.dummy_canvas.config(width=width)
        if fit == FIT_WIDTH:
            super().update()
            self.dummy_canvas.config(width=super().winfo_width())
        elif fit == FIT_HEIGHT:
            super().update()
            self.dummy_canvas.config(height=super().winfo_height())
        else:
            raise ValueError("Unknow value for the `fit` parameter.")
    fit = resize

class Application(tk.Frame):
    def __init__(self, parent):
        super(Application, self).__init__(parent)
        root.geometry("600x600")
        root.title("ServerStatus")
        
        def update1():
            print("updating")
            cursor.execute("""
            SELECT * FROM servers;
            """)
            for widget in ServerAdd.winfo_children():
                if widget.winfo_class() == 'Entry': # get Label widgets
                    widget.delete(0,END)
            for widget in frame.winfo_children():
                if widget.winfo_class() == 'Label': # get Label widgets
                    widget.destroy()
                    
                        
                    
            for _item in cursor.fetchall():
                        
                try:
                    print("______",_item,"______")
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((_item[2], _item[3]))
                    if result == 0:
                        status= "Online"
                        color1 = '#11bd3f'
                    else:
                        status= "Offline"
                        color1 = '#bd111a'
                    _serverAl=("({})-{}: {} : {}  STATUS= {} ".format(_item[0],_item[1], _item[2],_item[3],status))
                    tk.Label(frame,text=_serverAl,bg="#171717", fg=color1).pack(side="top")
                except:
                    tk.Label(frame,text="Servidor inválido! ID:({})\n".format(_item[0]), bg="#171717", fg='#bd111a').pack(side="left")
            print("updated")        
        ServerAdd = Canvas(self, bd=0, highlightthickness=0)
        ServerAdd.pack(side=BOTTOM, fill=BOTH, expand=TRUE)       
        frame = ScrollableFrame(root,bg="#171717", height=200, hscroll=False, vscroll=True)
        frame.pack(side="left", fill="both", expand=True)
            

            
        def addToList(name,server,port):
            try:    
                if (name.get() == []) or (server.get() == []) or (port.get() == []) or  (port.get() == 0) :
                    tk.Label(frame,text="Nenhum valor inserido",bg="#171717", fg='#ebd834').pack(side=TOP)
                else:
                    tk.Label(frame,text="Atualizando Lista do servidor",bg="#171717", fg='#ffffff').pack(side=TOP)
                    _serveraddList=[]
                    _item=[]
                    _item.append(name.get())
                    _item.append(server.get())
                    _item.append(port.get())
                    _serveraddList.append(_item[:])
                    _item.clear()
                    cursor.executemany("""
                    INSERT INTO servers (nome,url,port)
                    VALUES (?,?,?)
                    """,_serveraddList)

                    conn.commit()
                    update1()
            except:
                tk.Label(frame,text="Nenhum valor válido inserido!",bg="#171717", fg='#ebd834').pack(side=TOP)     
                
                    
                        
        def removeFromList(id):
            try:
                if id.get() == 0:
                    tk.Label(frame,text="Nenhum valor inserido!",bg="#171717", fg='#ebd834').pack(side=TOP) 
                else:
                    cursor.execute("""
                    DELETE FROM servers
                    WHERE id = ?
                    """, (id.get(),))

                    conn.commit()
                    update1()
            except:
                tk.Label(frame,text="Nenhum valor válido inserido!",bg="#171717", fg='#ebd834').pack(side=TOP) 
        id=tk.IntVar()
        nome=tk.StringVar()
        url=tk.StringVar()
        port=tk.IntVar()
        tk.Label(ServerAdd,text="Informe o nome do servidor:").pack()
        tk.Entry(ServerAdd, textvariable=nome).pack()
        tk.Label(ServerAdd,text="Informe a URL do servidor:").pack()
        tk.Entry(ServerAdd, textvariable=url).pack()
        tk.Label(ServerAdd,text="Informe a porta do servidor:").pack()
        tk.Entry(ServerAdd, textvariable=port).pack()
        addToList=partial(addToList,nome,url,port)
        tk.Button(ServerAdd,text="Adicionar Servidor", command=addToList).pack()
        tk.Label(ServerAdd,text="Remover servidor").pack()
        removeFromList=partial(removeFromList,id)
        tk.Entry(ServerAdd, textvariable=id).pack()
        tk.Button(ServerAdd, text="Remover", command=removeFromList).pack()
        tk.Button(ServerAdd, text="Atualizar", command=update1).pack()
        
    
    

        
            
if __name__ == "__main__":
    root = tk.Tk()
    main = Application(root)
    main.pack(fill="both", expand=True)
    root.protocol("WM_DELETE_WINDOW", exit)
    root.mainloop()
    
    
    
    
    
    

        