import crepe
import sys
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import tkinter as tk
from scipy.io import wavfile
from time import sleep
import threading


class Plotter:
    def plot_data(self, first_set, second_set):
        self.close_figure()
        dataset = {'x': first_set[0], 'y1': first_set[1], 'y2': second_set[1]}
        plt.plot( 'x', 'y1', data=dataset, marker='', color='red', linewidth=2, label="Melody")
        plt.plot( 'x', 'y2', data=dataset, marker='', color='blue', linewidth=2, label="Singing")
        plt.ylabel("Frequency [Hz]")
        plt.xlabel("Time [Sec]")
        plt.legend()
        plt.show()


    def close_figure(self):
        plt.close('all')

    


class Analyzer:
    def __init__(self, file1, file2):
        super().__init__()
        self.sr, self.file1 = wavfile.read(file1)
        self.sr2, self.file2 = wavfile.read(file2)
        self.first_set, self.second_set = [], []
        self.cut_clips_to_min_size()
        self.processed = 0


    def calculate_min_file_size(self):
        return min(len(self.file1), len(self.file2))

    def cut_clips_to_min_size(self):
        min_size = self.calculate_min_file_size()
        self.file1 = self.file1[:min_size]
        self.file2 = self.file2[:min_size]

    def analyze_chunk(self, chunk_size=1000000):
        """if (self.processed + chunk_size > len(self.file1)):
            chunk_size = len(self.file1) - self.processed"""
        chunk_size = len(self.file1)
        self.first_set += crepe.predict(self.file1[self.processed:self.processed+chunk_size], self.sr, viterbi=True)
        self.second_set += crepe.predict(self.file2[self.processed:self.processed+chunk_size], self.sr, viterbi=True)
        self.processed += chunk_size
        

def ask_for_file():
    root = tk.Tk()
    root.withdraw()
    
    root.filename = askopenfilename()
    return root.filename

def main():
    while True:
        try:
            melody_path = ask_for_file()
            singing_path = ask_for_file()
            print(melody_path, singing_path)
            analyzer = Analyzer(melody_path, singing_path)
            break
        except:
            print("Wrong file format, you need a 16-bit WAV file")
    plotter = Plotter()
    #update_thread = threading.Thread(target=lambda: plotter.plot_data(analyzer.first_set, analyzer.second_set), daemon=True)
    while analyzer.processed < len(analyzer.file1):
        analyzer.analyze_chunk()
    plotter.plot_data(analyzer.first_set, analyzer.second_set)

main()