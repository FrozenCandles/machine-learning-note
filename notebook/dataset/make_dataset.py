
"""
A simple point dataset maker
TODO: add function for point deletion
TODO: add scroolbar for listbox
"""

from typing import NamedTuple, Tuple, List
import os

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class Point(NamedTuple):
    x: float
    y: float
    label: int
    screen_x: int
    screen_y: int
    
    def __str__(self):
        return f'{self.x},{self.y} ({self.label})'
    
    def export_string(self):
        return f'{self.x},{self.y},{self.label}'



class UI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.title('Dataset Maker')
        self._f_left = ttk.LabelFrame(self, text='canvas')
        self._f_right = ttk.Frame(self)
        self._f_btns = ttk.LabelFrame(self._f_right, text='current label')
        self._f_listsbox = ttk.LabelFrame(self._f_right, text='current points')

        self.CANVAS_WIDTH = 960
        self.CANVAS_HEIGHT = 720
        self.canvas = tk.Canvas(self._f_left, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        self._w_canvas_status = ttk.Label(self._f_left, text='no action')
        
        self.canvas.bind('<Button-1>', self.__canvas_click_callback)
        
        self.points: List[Point] = []
        self.points_list_var = tk.StringVar()
        self.points_list = tk.Listbox(
            self._f_listsbox, 
            listvariable=self.points_list_var, 
            height=18)
        self._w_export = ttk.Button(
            self._f_listsbox,
            text='Export All data',
            command=self.export_all) 
        
        self.label_colors = {
            0: '#ffffff',
            1: '#ff0000',
            2: '#00ff00',
            3: '#0000ff',
            4: '#ffff00',
            5: '#ff00ff',
            6: '#00ffff'
        }
        
        self.w_label_chooser = [
            tk.Button(self._f_btns, text=str(i), width=12, relief=tk.GROOVE, bg='lightgrey',
                       command=(lambda i: (lambda: self.change_current_label(i)))(i))
            for i in self.label_colors.keys()
        ]
        self.current_label = next(iter(self.label_colors.keys()))
        self.change_current_label(self.current_label)
        
        self.prepare_options()
        self.create_window()

    
    def prepare_options(self):
        
        self.xlim = (0, 11)
        self.ylim = (-1, 8)
        self.actual_xlim = (self.xlim[0], self.xlim[1] + 1)
        self.actual_ylim = (self.ylim[0] - 1, self.ylim[1])
        self.xtick = self.xlim[1] - self.xlim[0] + 1
        self.ytick = self.ylim[1] - self.ylim[0] + 1
        
        self.CANVAS_TICK = 60
        self.CANVAS_X_START = 100
        self.CANVAS_X_STOP = self.CANVAS_X_START + self.xtick * self.CANVAS_TICK
        self.CANVAS_Y_START = 40
        self.CANVAS_Y_STOP = self.CANVAS_Y_START + self.ytick * self.CANVAS_TICK

        
    
    def create_window(self):
        
        self._f_left.pack(side=tk.LEFT, padx=20, pady=20, ipadx=15, ipady=15)
        self._f_right.pack(side=tk.RIGHT)
        self._f_btns.pack(fill=tk.BOTH, padx=20, pady=20, ipadx=20)
        self._f_listsbox.pack(fill=tk.BOTH, padx=20, pady=20, ipadx=20)
        
        self.points_list.pack()
        self._w_export.pack(pady=15)
        for w in self.w_label_chooser:
            w.pack()
        self.canvas.pack()
        self._w_canvas_status.pack()
        
        self.__canvas_draw_grid()
        
    
    def change_current_label(self, new_label):

        self.w_label_chooser[self.current_label].config(bg='lightgrey')
        self.current_label = new_label
        self.w_label_chooser[self.current_label].config(bg=self.label_colors.get(new_label))
    
    
    def __canvas_draw_grid(self):
        """May not be accurate"""
        for x in range(self.xtick + 1):
            self.canvas.create_line(
                self.CANVAS_X_START + x * self.CANVAS_TICK, self.CANVAS_Y_START, 
                self.CANVAS_X_START + x * self.CANVAS_TICK, self.CANVAS_Y_STOP)
            self.canvas.create_text(
                self.CANVAS_X_START + x * self.CANVAS_TICK - 2,
                self.CANVAS_Y_STOP + 20,
                font=('', 16),
                text=str(self.xlim[0] + x))
            
        for y in range(self.ytick + 1):
            self.canvas.create_line(
                self.CANVAS_X_START, self.CANVAS_Y_START + y * self.CANVAS_TICK, 
                self.CANVAS_X_STOP, self.CANVAS_Y_START + y * self.CANVAS_TICK)
            self.canvas.create_text(
                self.CANVAS_X_START - 20,
                self.CANVAS_Y_START + y * self.CANVAS_TICK - 10,
                font=('', 16),
                text=str(self.ylim[1] - y))
        
        
    def __canvas_click_callback(self, event):
        coords = self.screencoord_to_abscoord(event.x, event.y)
        self._w_canvas_status.config(text=f'add point: ({coords[0]:.4f}, {coords[1]:.4f})')
        self.canvas.create_oval(
            event.x - 3, event.y - 3, 
            event.x + 3, event.y + 3,
            fill=self.label_colors.get(self.current_label))
        self.points_list.insert(tk.END, 
            f'({coords[0]:.4f}, {coords[1]:.4f}) {self.current_label}')
        self.points.append(
            Point(
                x=coords[0], 
                y=coords[1], 
                label=self.current_label,
                screen_x=event.x,
                screen_y=event.y
            )
        )
        
        
    def screencoord_to_abscoord(self, screencoord_x: int, 
                                screencoord_y: int) -> Tuple[float, float]:
        return (
            self.xlim[0] + (screencoord_x - self.CANVAS_X_START) / self.CANVAS_TICK,
            self.ylim[1] - (screencoord_y - self.CANVAS_Y_START) / self.CANVAS_TICK
        )
        # return screencoord_x, screencoord_y
        
    def export_all(self):
        n = 1
        filename = f'point dataset ({n}).csv'
        while os.path.exists(filename):
            n += 1
            filename = f'point dataset ({n}).csv'
            
        with open(filename, 'w') as file:
            file.write('x,y,label\n')
            for p in self.points:
                file.write(Point.export_string(p))
                file.write('\n')

        showinfo('Export', f'Successfully exported data to file "{filename}"')
        
        
if __name__ == '__main__':
    UI().mainloop()