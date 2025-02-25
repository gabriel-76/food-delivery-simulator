from math import ceil
from typing import List

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

from src.main.statistic.board import Board
from src.main.statistic.metric import Metric


class SummarizedDataBoard(Board):
    image_counter = 0  # Variável estática para controlar o nome das imagens

    def __init__(self, metrics: List[Metric], num_drivers: int, num_establishments: int, use_tkinter: bool = False):
        super().__init__(metrics)
        self.num_drivers = num_drivers
        self.num_establishments = num_establishments
        self.use_tkinter = use_tkinter

    @classmethod
    def get_next_image_name(cls) -> str:
        """Gera um nome de arquivo único para evitar sobrescrições."""
        cls.image_counter += 1
        return f"run_{cls.image_counter}_results_fig.png"

    def view(self) -> None:
        if self.use_tkinter:
            self._view_with_tkinter()
        else:
            self._view_with_matplotlib()

    def _calculate_fig_height(self) -> float:
        """
        Calcula a altura do gráfico com base na quantidade de motoristas e restaurantes.
        """
        base_height = 3  # Altura base para cada linha
        additional_height = (max(self.num_drivers, self.num_establishments)) * 0.8  # Altura adicional por item
        num_rows = ceil((len(self.metrics) - 1) / 2) + 1  # Número de linhas baseado nas métricas
        return num_rows * base_height + additional_height

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
        fig_height = self._calculate_fig_height()
        fig = plt.figure(figsize=(12, fig_height))
        gs = fig.add_gridspec(ceil((len(self.metrics) - 1) / 2) + 1, 2, hspace=0.9)

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
        fig_height = self._calculate_fig_height()
        fig = plt.figure(figsize=(12, fig_height))
        gs = fig.add_gridspec(ceil((len(self.metrics) - 1) / 2) + 1, 2, hspace=0.9)

        # Primeiro gráfico destacado
        ax1 = fig.add_subplot(gs[0, :])
        self.metrics[0].view(ax1)

        # Gráficos restantes
        for i, metric in enumerate(self.metrics[1:], start=1):
            row = (i + 1) // 2
            col = (i - 1) % 2

            ax = fig.add_subplot(gs[row, col])
            metric.view(ax)

        # Gerar nome de arquivo único e salvar imagem
        image_name = self.get_next_image_name()
        fig.savefig("C:/Users/marco/OneDrive/Área de Trabalho/Modelo treinado 6000000 PPO/figs/" + image_name, dpi=300, bbox_inches='tight')

        # Mostrar gráficos
        # plt.show()
