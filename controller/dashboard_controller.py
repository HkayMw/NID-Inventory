from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.garden.matplotlib import FigureCanvasKivyAgg
import kivy.garden.matplotlib
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt
import datetime

from model.model import Model
from controller.controller import Controller

class DashboardController(Controller):
    def __init__(self):
        super().__init__(Model)
    
    
    graph_layout = ObjectProperty(None)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.figure, self.ax = plt.subplots()
    #     self.canvas = FigureCanvasKivyAgg(self.figure)
    #     self.graph_layout.add_widget(self.canvas)  # Add graph to the layout

    def load_data(self, period):
        data, x_ticks = self.get_data_by_period(period)

        # Clear the current graph and plot new data
        self.ax.clear()
        self.ax.plot(x_ticks, data, label=f"Data for {period}")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Count")
        self.ax.legend()

        # Refresh the canvas without reloading the entire graph
        self.canvas.draw()

    def get_data_by_period(self, period):
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        if period == 'day':
            # Fetch data for the last 24 hours, changes each hour
            query = "SELECT hour, COUNT(id) FROM ids_added WHERE date = ? GROUP BY hour"
            date_today = datetime.date.today()
            cursor.execute(query, (date_today,))
        elif period == 'week':
            # Fetch data for the last 7 days, changes each day
            query = "SELECT day, COUNT(id) FROM ids_added WHERE week = ? GROUP BY day"
            current_week = datetime.date.today().isocalendar()[1]
            cursor.execute(query, (current_week,))
        elif period == 'month':
            # Fetch data for the last 4 weeks, changes each week
            query = "SELECT week, COUNT(id) FROM ids_added WHERE month = ? GROUP BY week"
            current_month = datetime.date.today().month
            cursor.execute(query, (current_month,))
        elif period == 'year':
            # Fetch data for the last 12 months, changes each month
            query = "SELECT month, COUNT(id) FROM ids_added WHERE year = ? GROUP BY month"
            current_year = datetime.date.today().year
            cursor.execute(query, (current_year,))
        
        data = cursor.fetchall()
        x_ticks, y_data = zip(*data) if data else ([], [])

        conn.close()

        return y_data, x_ticks

