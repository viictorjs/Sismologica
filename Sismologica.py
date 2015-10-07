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
import numpy as np


class Sismologica(Tk):

    arquivos, fig, valorFigx, valorFigy, eixo = None, None, None, None, None
    plotExiste = False
    sts, tracos = [], []
    PpicksArts, PpicksValues = {}, {}

    def __init__(self):

        Tk.__init__(self)
        self.title('Sismologica')
        parent = Frame(self)
        parent.grid(row = 0, column = 0, sticky = 'we')
        
        if platform.system() == 'Windows':

            self.wm_state('zoomed')

            self.valorFigx = self.winfo_screenwidth()/80

            if self.winfo_screenheight() == 1080:
                
                self.valorFigy = self.winfo_screenheight()/93.1

            elif self.winfo_screenheight() == 768:

                self.valorFigy = self.winfo_screenheight()/100.5

            elif self.winfo_screenheight() == 1024:

                self.valorFigy = self.winfo_screenheight()/94.1

            elif self.winfo_screenheight() == 900:

                self.valorFigy = self.winfo_screenheight()/96.5

            elif self.winfo_screenheight() == 720:

                self.valorFigy = self.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = self.winfo_screenheight()/99

            try:

                self.iconbitmap("%s/imagens/terra1.ico"%os.getcwd())

            except:

                pass

        else:
            
            self.attributes('-zoomed',True)

            self.valorFigx = self.winfo_screenwidth()/83

            if self.winfo_screenheight() == 1080:
                
                self.valorFigy = self.winfo_screenheight()/93.1

            elif self.winfo_screenheight() == 768:

                self.valorFigy = self.winfo_screenheight()/96

            elif self.winfo_screenheight() == 1024:

                self.valorFigy = self.winfo_screenheight()/94.1

            elif self.winfo_screenheight() == 900:

                self.valorFigy = self.winfo_screenheight()/96.5

            elif self.winfo_screenheight() == 720:

                self.valorFigy = self.winfo_screenheight()/101.5

            else: # 800

                self.valorFigy = self.winfo_screenheight()/99
            
        BarraMenu = Menu(self)
        self.configure(menu=BarraMenu)
        menu_arquivo = Menu(BarraMenu)
        BarraMenu.add_cascade(label='Arquivo',menu=menu_arquivo)
        menu_arquivo.add_command(label='Abrir                    Ctrl+A',
                                      command=self.abrir_pt1)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label='Sair                         Alt+S',
                                      command=self.destroy)

        Abrir = Button(parent, command = self.abrir_pt1)
        img_abrir = PhotoImage(file="%s/imagens/abrir.gif"%os.getcwd())
        Abrir.config(image=img_abrir)
        Abrir.grid(row=0,column=0,sticky=W)
        Salvar = Button(parent, command = self.salvar)
        img_salvar = PhotoImage(file="%s/imagens/salvar.gif"%os.getcwd())
        Salvar.config(image=img_salvar)
        Salvar.grid(row=0,column=1,sticky=W)
        Lupa = Button(parent, command = self.zoom)
        img_lupa = PhotoImage(file="%s/imagens/lupa.gif"%os.getcwd())
        Lupa.config(image=img_lupa)
        Lupa.grid(row=0,column=2,sticky=W)
        Pick = Button(parent, command = self.pickP)
        img_pick = PhotoImage(file="%s/imagens/pick.gif"%os.getcwd())
        Pick.config(image=img_pick)
        Pick.grid(row=0,column=3,sticky=W)

        self.status = Label(parent, text = '', fg = 'red')
        self.status.grid(row = 0, column = 4)
        self.statusZoom = Label(parent, text = '', fg = 'blue')
        self.statusZoom.grid(row = 0, column = 5)
        self.mainloop()

    def abrir_pt1(self):

        self.status.configure(text = 'Abrindo arquivos...')
        self.arquivos = sorted(filedialog.askopenfilenames(title='Abrir',
                        filetypes=[('SAC','*.sac')]))

        if len(self.arquivos) > 0:

            try:

                for i in self.arquivos:

                    self.sts.append(read(i))

               # for i in self.sts:

                #    print(i[0].stats.station)'''

                self.abrir_pt2()

            except:

                messagebox.showerror("Sismologica","Erro na leitura do arquivo.")
                self.status.configure(text = '')
                del self.sts[:]
                self.arquivo = None

    def abrir_pt2(self):

        self.fig, axs = plt.subplots(len(self.arquivos), sharex = True, figsize = (self.valorFigx, self.valorFigy))
        self.fig.set_facecolor('#F0F0F0')

        for ax,i in zip(self.fig.axes, range(len(self.arquivos))):

            traco, = ax.plot([j*self.sts[i][0].stats.delta for j in range(self.sts[i][0].stats.npts)],self.sts[i][0], color='black', picker = 5)
            ax.tick_params(axis='y',which='both',left='off',right='off',labelleft='off')
            ax.set_ylabel('Station: %s'%self.sts[i][0].stats.station)
            ax.grid()
            self.tracos.append(traco)
            self.PpicksArts[ax] = None
            self.PpicksValues[ax] = None

        self.fig.axes[0].set_title('Network: %s'%self.sts[0][0].stats.network)
        self.fig.axes[-1].set_xlabel('Seconds passed since %s'%str(self.sts[0][0].stats.starttime))
        self.fig.subplots_adjust(hspace=.2)
        frame = Frame(self)
        frame.grid(row = 1, column = 0, sticky = 'nsew')
        canvas = FigureCanvasTkAgg(self.fig, frame)
        canvas.show()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack(fill='both', expand=True)
        self.status.configure(text = '')
        self.plotExiste = True
            
    def salvar(self):

        if self.plotExiste == True:

            print(self.PpicksValues.values())

    def zoom(self):

        if self.plotExiste == True:

            def onclick(event):

                root = Tk()
                new_frame = Frame(root)
                new_frame.grid(row = 0, column = 0, sticky = 'nsew')
                new_fig = plt.figure()
                new_ax = new_fig.add_subplot(111)
                new_ax.plot(event.artist.get_xdata(),event.artist.get_ydata(), color='black')
                new_ax.set_xlabel('Time since %s'%str(self.sts[0][0].stats.starttime))
                new_canvas = FigureCanvasTkAgg(new_fig, new_frame)
                new_canvas.show()
                new_canvas.get_tk_widget().pack(fill='both', expand=True)
                new_toolbar = NavigationToolbar2TkAgg(new_canvas, new_frame)
                new_toolbar.update()
                new_canvas._tkcanvas.pack(fill='both', expand=True)

            cid = self.fig.canvas.mpl_connect('pick_event', onclick)

    def pickP(self):

        if self.plotExiste == True:

            def pick(event):

                if self.PpicksArts[self.eixo] == None:

                    Ppick = self.eixo.axvline(event.xdata, -10000, 10000, color = 'red')
                    self.fig.canvas.draw()
                    self.PpicksArts[self.eixo] = Ppick
                    self.PpicksValues[self.eixo] = event.xdata

                else:
                    
                    self.PpicksArts[self.eixo].remove()
                    Ppick = self.eixo.axvline(event.xdata, -10000, 10000, color = 'red')
                    self.fig.canvas.draw()
                    self.PpicksArts[self.eixo] = Ppick
                    self.PpicksValues[self.eixo] = event.xdata

            def axis_id(event):

                if event.inaxes in self.fig.axes:

                    self.eixo = event.inaxes

            cid = self.fig.canvas.mpl_connect('button_press_event', pick)
            cid2 = self.fig.canvas.mpl_connect('axes_enter_event', axis_id)

run = Sismologica()




