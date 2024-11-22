from math import ceil
from typing import List

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

from src.main.statistic.board import Board
from src.main.statistic.metric import Metric


class SummarizedDataBoard(Board):

    def __init__(self, metrics: List[Metric], use_tkinter: bool = False):
        super().__init__(metrics)
        self.use_tkinter = use_tkinter

    def view(self) -> None:
        if self.use_tkinter:
            self._view_with_tkinter()
        else:
            self._view_with_matplotlib()

    def _view_with_tkinter(self) -> None:
        # Configuração inicial do Tkinter
        root = tk.Tk()
        root.title("Summarized Data Board")

        # Frame principal com barra de rolagem
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(frame)
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configurar barra de rolagem no canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Criar a figura Matplotlib
        num_metrics = len(self.metrics)
        num_rows = ceil((num_metrics - 1) / 2) + 1
        fig_height = num_rows * 3 + (num_rows - 1) * 0.5

        fig = plt.figure(figsize=(12, fig_height))
        gs = fig.add_gridspec(num_rows, 2, hspace=0.8)

        # Primeiro gráfico destacado
        ax1 = fig.add_subplot(gs[0, :])
        self.metrics[0].view(ax1)

        # Gráficos restantes
        for i, metric in enumerate(self.metrics[1:], start=1):
            row = (i + 1) // 2
            col = (i - 1) % 2

            ax = fig.add_subplot(gs[row, col])
            metric.view(ax)

        # Integrar figura ao Tkinter
        canvas_figure = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas_figure.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Mostrar janela
        root.mainloop()

    def _view_with_matplotlib(self) -> None:
        # Criar a figura Matplotlib
        num_metrics = len(self.metrics)
        num_rows = ceil((num_metrics - 1) / 2) + 1
        fig_height = num_rows * 3 + (num_rows - 1) * 0.5

        fig = plt.figure(figsize=(12, fig_height))
        gs = fig.add_gridspec(num_rows, 2, hspace=0.8)

        # Primeiro gráfico destacado
        ax1 = fig.add_subplot(gs[0, :])
        self.metrics[0].view(ax1)

        # Gráficos restantes
        for i, metric in enumerate(self.metrics[1:], start=1):
            row = (i + 1) // 2
            col = (i - 1) % 2

            ax = fig.add_subplot(gs[row, col])
            metric.view(ax)

        # Mostrar gráficos
        plt.show()
