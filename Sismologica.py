from obspy import read
import matplotlib
matplotlib.use('TkAgg')                                                                  
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from tkinter import *
from tkinter import filedialog, messagebox
from matplotlib.widgets import Slider
import platform
import os


class Sismologica(Tk):

    arquivos, fig, axs = None, None, None
    sts, tracos = [], []

    def __init__(self):

        Tk.__init__(self)
        self.title('Geosis - Sispick')
        
        if platform.system() == 'Windows':

            self.wm_state('zoomed')

            try:

                self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

            except:

                pass

        else:
            
            self.attributes('-zoomed',True)
            
        BarraMenu = Menu(self)
        self.configure(menu=BarraMenu)
        menu_arquivo = Menu(BarraMenu)
        BarraMenu.add_cascade(label='Arquivo',menu=menu_arquivo)
        menu_arquivo.add_command(label='Abrir                    Ctrl+A',
                                      command=self.abrir)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Sair                         Alt+S',
                                      command=self.destroy)

        Abrir = Button(self, command = self.abrir)
        img_abrir = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        Abrir.config(image=img_abrir)
        Abrir.grid(row=0,column=0,sticky=W)

    def abrir(self):

        self.arquivos = sorted(filedialog.askopenfilenames(title='Abrir',
                        filetypes=[('SAC','*.sac')]))

        if len(self.arquivos) > 0:

            frame = Frame(self)
            frame.grid(row = 0, column = 0, sticky = 'nsew')

            for i in self.arquivos:

                self.sts.append(read(i))

            self.fig, self.axs = plt.subplots(len(self.arquivos), sharex = True)

            for ax,i in zip(self.axs.flat, range(len(self.arquivos))):

                traco, = ax.plot([j*self.sts[i][0].stats.delta for j in range(self.sts[i][0].stats.npts)],self.sts[i][0], color='black', picker = 5)
                self.tracos.append(traco)

            self.axs.flat[0].set_title(str(self.sts[0][0].stats.starttime))

            canvas = FigureCanvasTkAgg(self.fig, frame)
            canvas.show()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            toolbar = NavigationToolbar2TkAgg(canvas, frame)
            toolbar.update()
            canvas._tkcanvas.pack(fill='both', expand=True)

            def onclick(event):

                root = Tk()
                new_fig = plt.figure()
                new_ax = new_fig.add_subplot(111)
                new_ax.plot(event.artist.get_xdata(),event.artist.get_ydata(), color='black')
                new_canvas = FigureCanvasTkAgg(new_fig, root)
                new_canvas.show()
                new_canvas.get_tk_widget().pack(fill='both', expand=True)
                toolbar = NavigationToolbar2TkAgg(canvas, root)
                toolbar.update()
                new_canvas._tkcanvas.pack(fill='both', expand=True)

            cid = self.fig.canvas.mpl_connect('pick_event', onclick)

run = Sismologica()






