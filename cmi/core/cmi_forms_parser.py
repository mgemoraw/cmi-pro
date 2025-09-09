"""
This module parses cmi data collection forms from xlsx file
"""
from openpyxl import Workbook, load_workbook
import os



class LaborFormParser:
    def __init__(self, file, format="xlsx"):
        self.wb = load_workbook(file)
        self.labor_ws = None

        try:
            self.labor_ws = self.wb['labor']
            self.ws_ws = self.wb['WorkSampling']
            self.dv_ws = self.wb['DailyVariables']

        except Exception as e:
            self.labor_ws = None
            self.ws_ws = None
            self.dv_ws = None
        
        self.format = format


    def parse(self):
        pass


        
