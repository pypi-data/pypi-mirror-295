# %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from experimentalTreatingIsiPol.machines._68FM100 import _68FM100,_tracao_tipo_5_ave
from experimentalTreatingIsiPol.machines._68FM100_biaxial import _68FM100_biaxial
from experimentalTreatingIsiPol.machines._older_machine import _Older_Machine, _MarcoPvMachine
from experimentalTreatingIsiPol.machines._generalMachine import GeneralMachine
import os
import re
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io  # For working with in-memory files
from matplotlib.backends.backend_pdf import PdfPages
import warnings


blue_tonalities_options = [
    '#1f0794', 
    '#000080', 
    '#6476d1', 
    '#00008B', 
    '#003366', 
    '#191970', 
    '#0000CD', 
    '#27414a', 
    '#4B0082', 
    '#2f6b6b', 
    '#00688B', 
    '#483D8B', 
    '#4682B4', 
    '#708090', 
    '#4169E1', 
    '#778899', 
    '#7B68EE', 
    '#6495ED'
]


linestyles_options = [
    "-",    # solid
    "--",   # dashed
    "-.",   # dashdot
    ":",    # dotted
    " ",    # no line (blank space)
    "-",    # solid (thicker)
    (0, (1, 10)), # loosely dotted
    (0, (5, 10)), # loosely dashed
    (0, (3, 5, 1, 5)), # dashdotted
    (0, (3, 1, 1, 1)), # densely dashdotted
    (0, (5, 5)),  # dashed with same dash and space lengths
    (5, (10, 3)), # long dashes with offset
    (0, (3, 10, 1, 15)), # complex custom dash pattern
    (0, (1, 1)), # densely dotted
    (0, (1, 5)), # moderately dotted
    (0, (3, 1)), # densely dashed
    (0, (3, 5, 1, 5, 1, 5)), # dashdotdot
    (0, (3, 10, 1, 10, 1, 10)), # dashdashdash
]

marker_options = [
    ".",      # point
    ",",      # pixel
    "o",      # circle
    "v",      # triangle down
    "^",      # triangle up
    "<",      # triangle left
    ">",      # triangle right
    "1",      # tripod down
    "2",      # tripod up
    "3",      # tripod left
    "4",      # tripod right
    "s",      # square
    "p",      # pentagon
    "*",      # star
    "h",      # hexagon1
    "H",      # hexagon2
    "+",      # plus
    "x",      # x
    "D",      # diamond
    "d",      # thin diamond
]

def plot_helper(ax,x,y,label,xlabel,ylabel,color='blue', linestyle='-.', marker='<', markersize=1, linewidth=1,**kwargs):

    ax.plot(x,y, label = label, color = color, marker = marker, 
            markersize = markersize, 
            linestyle = linestyle,
            linewidth = linewidth,**kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def scatter_helper(ax,x,y,label, xlabel, ylabel,color='blue', marker='+', markersize=10, **kwargs):

    ax.scatter(x,y, label = label, color = color, marker = marker,
             s = markersize,
             **kwargs)
    ax.grid()
    ax.legend()
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def several_plots_helper(ax,xs,ys,labels,xlabel,ylabel,colors: list | None = None, 
                         linestyles: list | None =None, markers : list | None = None, 
                         markersize=1, linewidth=1.5, 
                         color_scheme = 'blue_tonalities_options',
                         filter_data = False,
                         **kwargs
                         ):
    '''
    Função para plotar diversos gráficos.
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de pares.')
    

    if not (colors and markers and linestyles): 

        for each_x, each_y, each_label in zip(xs,ys,labels):
 
            if len(each_x)>100 and filter_data:
                slice = int(len(each_x)/100)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            if color_scheme ==  'blue_tonalities_options': # adicionando opcao para tonalidade de azul
                color = blue_tonalities_options[np.random.random_integers(0,17)]
            if color_scheme ==  'matplotlib_default':
                color = None
            marker = marker_options[np.random.random_integers(0,17)]
            linestyle = linestyles_options[np.random.random_integers(0,17)]

            ax.plot(each_x,each_y, label = each_label, color = color, marker = None, 
                    markersize = markersize, 
                    linestyle = None,
                    linewidth = linewidth,**kwargs)

    else:
        for each_x, each_y, each_label,each_color, each_marker, each_linestyle in zip(xs,ys,labels,colors,markers,linestyles): 
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            ax.plot(each_x,each_y, label = each_label, color = each_color, marker = each_marker, 
                    markersize = markersize, 
                    linestyle = each_linestyle,
                    linewidth = linewidth,**kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid()
    fig_obj = ax.get_figure()
    fig_height = fig_obj.get_figheight()
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -fig_height/20),
        ncol=3,
        framealpha=1,
        )
    
    return ax

def several_scatter_helper(ax,xs,ys,labels,xlabel,ylabel,colors: list | None = None, linestyles: list | None =None, markers : list | None = None, markersize=1, linewidth=1, **kwargs):
    '''
    Função para plotar diversos gráficos.

    PAREI AQUI
    '''
    if len(xs)!=len(ys):
        raise Exception('As dimensões das variáveis xs e ys devem ser iguais.')
    
    if len(labels)!=len(ys):
        raise Exception('A quantidade de labels deve ser igual à quantidade de pares.')
    
    ax.grid()

    if not (colors and markers and linestyles): 

        for each_x, each_y, each_label in zip(xs,ys,labels): 

            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            color = blue_tonalities_options[np.random.random_integers(0,17)]
            marker = marker_options[np.random.random_integers(0,17)]

            ax.scatter(each_x,each_y, label = each_label, color = color, marker = marker, 
                    s = markersize, 
                    **kwargs)

    else:
        for each_x, each_y, each_label,each_color, each_marker in zip(xs,ys,labels,colors,markers): 
           
            if len(each_x)>100:
                slice = int(len(each_x)/20)
                each_x=each_x[::slice]
                each_y=each_y[::slice]

            ax.scatter(each_x,each_y, label = each_label, color = each_color, marker = each_marker, 
                    s = markersize, 
                    **kwargs)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig_obj = ax.get_figure()
    fig_height = fig_obj.get_figheight()
    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -fig_height/15),
        ncol=3,
        framealpha=1,
        )
    
    return ax

class ReadExperimentalData():
    
    def __init__(self, archive_name,
                 column_delimitador = ';',
                 skiprows = 10,
                 decimal = ','):
        
        self.raw_data = pd.read_csv(archive_name, sep=column_delimitador,
                                                encoding_errors='backslashreplace', 
                                                on_bad_lines='skip', 
                                                skiprows=skiprows, 
                                                decimal=decimal)

class MechanicalTestFittingLinear():
    '''
    Classe para determinar propriedades mecânicas em regimes lineares. Ela servirão para Moduli de Young e Cisalhamento. 
    '''
    def __init__(self, machineName: str, archive_name : str, linearRegionSearchMethod='Deterministic', verbose : bool = True, 
                 materialType : str = 'composite',
                 direction : str = 'parallel',
                 generalMachineData : GeneralMachine = None,
                 x_min = None,
                 x_max = None 
                 ) -> None:
        
        self.verbose = verbose
        self.machineName = machineName

        self.direction = direction

        # if self.__checkMaterialType(materialType): # TODO :  CHECAR A DIREÇÃO DO MATERIAL
            # self.direction = materialType

        self.materialType = materialType


        
        self.rawdata, self.cleaned_raw_data, deformation_range_x, force = self.dataExtract(machineName=machineName, 
                                                                archive_name= archive_name,
                                                                linearRegionSearchMethod=linearRegionSearchMethod,
                                                                generalMachineData  = generalMachineData,
                                                                x_min = x_min,
                                                                x_max = x_max  
                                                                )
        self.deformationRange = None
        self.__selectStandardRange(materialType, deformation_range_x,force)
        pass

    def _68FM100_Data_Aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Método para a leitura e aquisição de dados de ensaio efetuados na 68FM100
        '''
        machine  = _68FM100() # Instanciando um novo objeto do tipo Instron 
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=10, decimal=machine.decimal)
        raw_data.columns = machine.colunas

        raw_data[machine.colunas[4]] = raw_data[machine.colunas[4]]/100 # porque está em % (axial)
        raw_data[machine.colunas[5]] = raw_data[machine.colunas[5]]/100 # porque está em % (axial)
        raw_data[machine.colunas[6]] = raw_data[machine.colunas[6]]/100 # porque está em % (transversal)

        x = raw_data[machine.colunas[4]]
        y = raw_data[machine.colunas[3]]
        
        new_x, new_y = self.__generalDataAquisition(x=x,y=y, x_label=machine.colunas[4], y_label=machine.colunas[3], linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[machine.colunas[3]]>new_y[0]]

        return raw_data,cleaned_raw_data,new_x,new_y
    
    def _68FM100_biaxial_Data_Aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Método para a aquisição de dados dos testes biaxiais
        '''
        machine =  _68FM100_biaxial()
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=3, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
        
        raw_data[machine.colunas[4]] = raw_data[machine.colunas[4]]/100 # porque está em % (axial)
        raw_data[machine.colunas[5]] = raw_data[machine.colunas[5]]/100 # porque está em % (axial)
        raw_data[machine.colunas[6]] = raw_data[machine.colunas[6]]/100 # porque está em % (transversal)
        raw_data[machine.colunas[3]] = raw_data[machine.colunas[3]]

        x = raw_data[machine.colunas[4]]
        y = raw_data[machine.colunas[3]]

        new_x, new_y  = self.__generalDataAquisition(x=x,
                                      y=y,
                                      x_label=machine.colunas[4], 
                                      y_label=machine.colunas[3], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[machine.colunas[3]]>new_y[0]]

        return raw_data, cleaned_raw_data, new_x, new_y
    
    def _tracao_tipo_5_ave_Data_Aquisition(self, archive_name : str, linearRegionSearchMethod):
        '''
        Método para aquisição de dados do tipo tração tipo 5 AVE
        '''

        machine =  _tracao_tipo_5_ave()
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=3, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        raw_data = raw_data.dropna(axis=0) # remove linhas com na
        
        x = raw_data[machine.colunas[5]]/100 # porque é %
        y = raw_data[machine.colunas[3]]

        new_x, new_y  = self.__generalDataAquisition(x=x,y=y,
                                      x_label=machine.colunas[5], 
                                      y_label=machine.colunas[3], 
                                      linearRegionSearchMethod=linearRegionSearchMethod)
        
        cleaned_raw_data = raw_data[raw_data[machine.colunas[3]]>new_y[0]]

        return raw_data, cleaned_raw_data, new_x,new_y
    

    def __filterDataOnlyBelowMaxForce(self, deformation_range_x, force):
        '''
        Method to only consider the strain data below de max force point
        '''
        #  Selecionando porção dos dados na região menor do que a máxima força
        deformation_range_x = pd.Series(deformation_range_x)
        force = pd.Series(force)
        forceMaxIndex = force[force==max(force)].index[0] # Pegando o índice
        force = force[0:forceMaxIndex]
        deformation_range_x = deformation_range_x[0:forceMaxIndex]

        return deformation_range_x, force


    def __selectStandardRange(self,materialType, deformation_range_x, force):
        '''
        Method to select the range of deformation, based on the standard
        '''

        deformation_range_x, force = self.__filterDataOnlyBelowMaxForce(deformation_range_x=deformation_range_x, 
                                                                        force=force)

        if materialType == 'polymer':
            inf_limit = 0.002
            sup_limit = 0.003

        else:

            if max(deformation_range_x) > 0.006:
                inf_limit = 0.001
                sup_limit = 0.003
            else:
                inf_limit = 0.25
                sup_limit = 0.5

        self.deformationRange = inf_limit,sup_limit

    def __checkMaterialType(self, materialType)->bool:
        '''
        Method to check material type param
        '''
        if materialType not in('composite','metal', 'polymer'):
            raise Exception('Unknown material type. Must be either composite, metal or polymer')
        
        else:
            return True
    
    def __onlyReadData(self, archive_name, archive_data):
        '''
        Método apenas para ler os dados
        '''

        self.raw_data = pd.read_csv(archive_name, sep=archive_data.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=archive_data.skiprows, decimal=archive_data.decimal)


    def _olderMachine_Data_Aquisition(self, archive_name :  str, linearRegionSearchMethod,
                                      x_min = None,
                                      x_max = None
                                      ):
        '''
        Method to analyse data of the older machine (the one used before instron arrived)
        '''

        machine  = _Older_Machine() # Instanciando um novo objeto do tipo _Older_Machine 
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=10, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        offset_num = self.__filterInitGraph(y=raw_data[machine.colunas[2]],linearRegionSearchMethod=linearRegionSearchMethod)
        x = raw_data[machine.colunas[3]]
        y = raw_data[machine.colunas[2]]
        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)
    
        if linearRegionSearchMethod == 'custom':
            x_linear, y_linear = self.__chooseRegionLinear(x,y,x_min=x_min, x_max=x_max)

        a,b,root = self.__equationFit(x_linear, y_linear)
        self.plotDataFinalComparison(x,y,x_linear,y_linear,machine.colunas[3],machine.colunas[2])
        self.plotComparisonExcludedData(x,y,x_linear,y_linear,machine.colunas[3],machine.colunas[2])

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        self.plotCleanedData(new_x, new_y, machine.colunas[3],machine.colunas[2])

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        cleaned_raw_data = raw_data[raw_data[machine.colunas[2]]>new_y[0]]

        return raw_data,cleaned_raw_data, new_x, new_y
    
    def __general_machine_Data_aquisition(self,  archive_name :  str, linearRegionSearchMethod, 
                                          generalMachineData : GeneralMachine,
                                          x_min = None,
                                          x_max = None):
        '''
        Trata dos dados de forma customizada
        '''
    
        machine  = generalMachineData # Instanciando um novo objeto do tipo _Older_Machine 
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, 
                               encoding_errors='backslashreplace', 
                               on_bad_lines='skip', skiprows=machine.skip_rows, 
                               decimal=machine.decimal)
        raw_data.columns = machine.colunas
        offset_num = self.__filterInitGraph(y=raw_data[machine.y_column],linearRegionSearchMethod=linearRegionSearchMethod)
        x = raw_data[machine.x_column]
        y = raw_data[machine.y_column]
        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        if linearRegionSearchMethod == 'custom':
            x_linear, y_linear = self.__chooseRegionLinear(x,y,x_min=x_min, x_max=x_max)

        a,b,root = self.__equationFit(x_linear, y_linear)
        self.plotDataFinalComparison(x,y,x_linear,y_linear,machine.x_column,machine.y_column)
        self.plotComparisonExcludedData(x,y,x_linear,y_linear,machine.x_column,machine.y_column)

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        self.plotCleanedData(new_x, new_y, machine.x_column,machine.y_column)

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        cleaned_raw_data = raw_data[raw_data[machine.y_column]>new_y[0]]

        return raw_data,cleaned_raw_data, new_x, new_y
    
    def __chooseRegionLinear(self, x : pd.Series, y: pd.Series, x_min, x_max):
        '''
        Method to uniquely choose the linear region
        '''
        x_index_min = x[x>x_min].index[0]
        x_index_max = x[x>x_max].index[0]

        return x[x_index_min:x_index_max], y[x_index_min:x_index_max]    
    
    def __MarcoPvMachine_Data_Aquisition(self, archive_name :  str, linearRegionSearchMethod, x_min = None, x_max = None):
        '''
        Method to analyse data of the older machine (the one used before instron arrived)
        '''

        machine  = _MarcoPvMachine() # Instanciando um novo objeto do tipo _Older_Machine 
        raw_data = pd.read_csv(archive_name, sep=machine.column_delimitador, encoding_errors='backslashreplace', on_bad_lines='skip', skiprows=12, decimal=machine.decimal)
        raw_data.columns = machine.colunas
        offset_num = self.__filterInitGraph(y=raw_data[machine.colunas[2]],linearRegionSearchMethod=linearRegionSearchMethod)
        x = raw_data[machine.colunas[3]]
        y = raw_data[machine.colunas[2]]
        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        if linearRegionSearchMethod == 'custom':
            x_linear, y_linear = self.__chooseRegionLinear(x,y,x_min=x_min, x_max=x_max)

        a,b,root = self.__equationFit(x_linear, y_linear)
        self.plotDataFinalComparison(x,y,x_linear,y_linear,machine.colunas[3],machine.colunas[2])
        self.plotComparisonExcludedData(x,y,x_linear,y_linear,machine.colunas[3],machine.colunas[2])

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        self.plotCleanedData(new_x, new_y, machine.colunas[3],machine.colunas[2])

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        cleaned_raw_data = raw_data[raw_data[machine.colunas[2]]>new_y[0]]

        return raw_data,cleaned_raw_data, new_x, new_y
    
    def __equationFit(self, x_linear, y_linear):
        '''
        Retorna os coeficientes a, b, e a raiz (-b/a) de uma equaçãoo linear f(x)=ax+b
        '''
        def linear(x,a,b):
            return a*x+b

        popt,_ = curve_fit(linear, x_linear, y_linear)
        return tuple([popt[0],popt[1],-popt[1]/popt[0]])
    
    def __compositeUltimateStress(self,stress_info):
        '''
        Método para cálcular o stress último, baseado na norma 
        '''
        return 1,1,max(stress_info)
    
    def __cut_garbage_data(self,x,y,x_linear,a,b,root):
        '''
        Método para cortar os dados iniciais do ensaio
        x -> Dados Originais (x)
        y -> Dados Originais (y)
        x_linear -> Conjunto do eixo x, dos dados originais, em que a informação é válida
        a,b -> Coef. das retas ajustadas na região linear
        root -> Raiz da eq. ajustada na parte linear
        '''

        x_cleaned = x[x_linear.index[-1]:x.index[-1]] # Exclui os primeiros dados
        y_cleaned = y[x_linear.index[-1]:x.index[-1]] # Exclui os primeiros dados
        x_init = np.linspace(root,x[x_linear.index[-1]],20) # Array da raiz do gráfico até o início dos dados originais
        y_init = [a*x+b for x in x_init] # Y ajustado na parte linear
        
        new_x = list(x_init) + list(x_cleaned) 
        new_x = np.subtract(new_x,root) # descontando a raiz
        new_y = list(y_init) + list(y_cleaned)
        return new_x, new_y
    
    def __selectGraphRange(self, var, i, scale=1):
        '''
        Método para retornar um range de dados, dado seu tamanho, e posição. 
        '''
        offset = int(len(var)/50)*scale
        return var[offset*(i-1):offset+offset*(i-1)]

    def __findConvergencePoisson(self, x_strain_linear, y_strain_linear, x_load_linear):
        '''
        Método para encontrar a convergênci da razão de Poisson
        '''
        # Corta os dados no mesmo tamanho
        if len(x_strain_linear)>len(y_strain_linear):
            x_strain_linear = x_strain_linear[0:len(y_strain_linear)]
        else:
            y_strain_linear = y_strain_linear[0:len(x_strain_linear)]

        ratio = np.divide(y_strain_linear,x_strain_linear)
        ratio_inverted = ratio[::-1]

        convergedRatio = self.__selectGraphRange(ratio_inverted,1)

        if len(convergedRatio)>0:
            return np.mean(convergedRatio)

        else:
            last_50_p = int(len(ratio)/2)
            return np.mean(ratio[:-last_50_p])
    
    def __filterInitGraph(self, y : pd.Series, linearRegionSearchMethod: str = 'Deterministic', scale=1)->int:
        '''
        Recebe os dados de ensaios experimentais, e encontra a primeira região linear pela diminuição do desvio padrão da segunda derivada
        '''
        if linearRegionSearchMethod == 'Deterministic':
            i=1
            y_current = self.__selectGraphRange(y,i,scale=scale)
            derivative = np.gradient(y_current)
            # second_order_derivative = np.gradient(derivative)
            std_derivative = np.std(derivative)
            mean_derivative = np.mean(derivative)
            init_caos = std_derivative/mean_derivative
            cov = init_caos
            convergence_criteria = init_caos/2

            # Se os dados já estão lineares, não há porque filtrar
            if init_caos<0.1:
                return i #

            while(cov > convergence_criteria):
                i+=1
                y_current = self.__selectGraphRange(y,i)
                derivative = np.gradient(y_current)
                second_order_derivative = np.gradient(derivative)
                cov = np.std(second_order_derivative)
                if i>100:
                    raise Exception('loop inf')

            return i    
        
        if linearRegionSearchMethod =='custom':
            return 1
        raise Exception('Método de determinação da região Linear Inválido')

    def __findEndLinearRegion(self, y : pd.Series):
        '''
        TODO -> Progrmar uma forma de se obter a região linear, ou seja, até onde realizar o fitting para o módulo
        '''
        pass     

    def __selectYoungModulusRange(self, strain : np.array, stress: np.array, init : float, end :float):
        '''
        Método para selecionar a faixa, baseada na % inicial e final de deformação
        '''

        strain = pd.Series(strain)
        stress = pd.Series(stress)

        init_index = strain[strain>init].index[0]
        end_index = strain[strain<end].index[-1]

        return strain[init_index:end_index], stress[init_index:end_index]
    
    def __selectStrainRange(self, strain_axial : np.array, strain_tranversal: np.array, init : float, end :float):
        '''
        Method to selecet the range of parallel and tranverse strain
        '''    
        strain_axial = pd.Series(strain_axial)
        strain_tranversal = pd.Series(strain_tranversal)

        init_index = strain_axial[strain_axial>init].index[0]
        end_index = strain_axial[strain_axial>end].index[0]

        return strain_axial[init_index:end_index], strain_tranversal[init_index:end_index]


    def __findYeldStress(self, x: pd.Series, y: pd.Series, E, method = 'percent', max_percentil : float = 0.25,
                         offset_yield : float = 0.002
                         ):
        '''
        Metodo para determinar a tensao de escoamento basead em medo
        '''
        if self.materialType == 'composite':
            x_offset, y_offset, yieldStress = self.__compositeUltimateStress(y)
            return x_offset, y_offset,yieldStress
        if method == 'percent':
            x_offset, y_offset, yieldStress = self.__percentYeldStressMethod(x, y, E, max_percentil,offset_yield)
            return x_offset, y_offset,yieldStress
    
    def __findMaxPolymerStress(self,x, y):
        '''
        Encontra o máximo do polímero, e retorna o x max
        '''
        y = pd.Series(y)
        x = pd.Series(x)
        y_derivative = np.gradient(y)
        y_derivative = pd.Series(y_derivative)

        # Divide o gráfico em 50 partes iguais:
        y_derivative_divided = []
        for i in range(50):
            y_derivative_divided.append(self.__selectGraphRange(y_derivative,i))

        for i in range(50):
            grad_mean = np.mean(y_derivative_divided[i])

            if grad_mean<0.04:
                max_y_region = i
                break

    
        index_y_max = y_derivative_divided[max_y_region].index[0]

        return x[int(index_y_max)]


    def __percentYeldStressMethod(self, x: pd.Series, y: pd.Series, E : float, max_percentil : float = 0.25, offset_yield = 0.002):
        '''
        Metodo para encontrar a tensao de escoamento baseado em um offset de 0.2%
        '''
        y = pd.Series(y)
        x = pd.Series(x)
        if self.materialType=='polymer':
            x_max = self.__findMaxPolymerStress(x,y)
        else:
            index_y_max = y[y==max(y)].index[0]
            x_max = x[index_y_max]
        x_linear = np.linspace(0,x_max,100)
        y_linear = [E*x for x in x_linear]
        x_offset = x_linear + offset_yield
        y_offset = [E*x for x in x_offset]
        y_interpolated = np.interp(x_offset, x,y)

        def FindYield():
            minGlobal = min(abs(y_interpolated- y_linear))
            for each_i in range(len(y_interpolated)):
                if abs(y_interpolated[each_i]-y_linear[each_i])==minGlobal:
                    return y_interpolated[each_i]
                
        yieldPoint = FindYield()
        
        return x_offset, y_linear, yieldPoint
    def __generalDataAquisition(self, x : pd.Series, y : pd.Series, x_label : str, y_label : str, linearRegionSearchMethod : str):
        '''
        Metodo DRY para executar os comandos referentes a aquisicao de dados
        '''
        offset_num = self.__filterInitGraph(y=y,linearRegionSearchMethod=linearRegionSearchMethod)

        x_linear = self.__selectGraphRange(x,offset_num)
        y_linear = self.__selectGraphRange(y,offset_num)

        a,b,root = self.__equationFit(x_linear, y_linear)
        if self.verbose:
            self.plotDataFinalComparison(x,y,x_linear,y_linear,x_label,y_label)
        if offset_num>1 and self.verbose and self.materialType != 'composite':
            self.plotComparisonExcludedData(x,y,x_linear,y_linear,x_label,y_label)

        new_x, new_y = self.__cut_garbage_data(x,y,x_linear,a,b,root)
        if self.verbose:
            self.plotCleanedData(new_x, new_y, x_label, y_label)

        self.new_x = new_x # Salvando internamente os dados limpos (x)
        self.new_y = new_y # Salvando internamente os dados limpos (y)

        return new_x, new_y

    def __typeCheck(self, var, type_correct):
        '''
        Função de apoio para checar se o tipo passo estão correto
        '''
        if type(var) != type_correct:
            raise Exception(f'O argumento machineName deve ser uma {type_correct}. Recebeu um {type(var)}')
        
    def __standard_ASTM_D638(self, axial_strain_linear,transverse_strain_linear,load_linear_axial):
        '''
        Method to compute the poisson ratio following D638
        '''

        coef_axial, _, _ = self.__equationFit(load_linear_axial,axial_strain_linear)
        coef_transversal, _, _ = self.__equationFit(load_linear_axial,transverse_strain_linear)

        ratio = abs(coef_transversal/coef_axial)
        return ratio
    
    def __standard_ASTM_D3039(self, axial_strain, transverse_strain)->float:
        '''
        Method to compute the poisson ration following the chord method by ASTM D3039
        '''
        inf_quantile, upper_quantile = self.deformationRange

        if inf_quantile == 0.001: # hard coded value defined by the standard
            axial_strain_computation, transversal_strain_computation = self.__selectStrainRange(axial_strain, transverse_strain, inf_quantile, upper_quantile)
        else:
            a = np.quantile(axial_strain,inf_quantile)
            b = np.quantile(axial_strain,upper_quantile)
            axial_strain_computation, transversal_strain_computation = self.__selectStrainRange(axial_strain, transverse_strain, a, b)


        deltaAxial = max(axial_strain_computation) - min(axial_strain_computation)

        index_max = axial_strain_computation[axial_strain_computation==max(axial_strain_computation)].index[0]
        index_min = axial_strain_computation[axial_strain_computation==min(axial_strain_computation)].index[0]

        deltaTransversal = transversal_strain_computation[index_max] - transversal_strain_computation[index_min]

        new_axial_strain_data  = [min(axial_strain_computation),max(axial_strain_computation)]
        new_transversa_strain_data  = [transversal_strain_computation[index_min], transversal_strain_computation[index_max]]

        poissonRatio = abs(deltaTransversal/deltaAxial)
        # Plotando o gráfico para comparação

        if self.verbose:
            fig, ax = plt.subplots(figsize=(8,4))

            if self.direction == 'paralell':
                label =  r'$\nu_{12}$='+f'{poissonRatio:.4f}'
            else:
                label =  r'$\nu_{21}$='+f'{poissonRatio:.4f}'

            ax = scatter_helper(ax=ax, x = axial_strain_computation, y=transversal_strain_computation, 
                            label=label, 
                            ylabel=r'$\varepsilon_{t}$', 
                            xlabel=r'$\varepsilon_{l}$', 
                            color=blue_tonalities_options[10], linestyle=linestyles_options[10])
            
            ax.plot(new_axial_strain_data, new_transversa_strain_data)
            
            axial_strain_as_list = list(axial_strain_computation)

            lim_sup_x = axial_strain_as_list[-1]
            lim_inf_x = axial_strain_as_list[0]

            limit_y = max(transversal_strain_computation)
            text_x_position = (lim_inf_x+lim_sup_x)/2.5
            text_y_position =limit_y
            ax.text(text_x_position, text_y_position, r'$\frac{\Delta \varepsilon_t}{\Delta \varepsilon_l}=$'+fr'{deltaTransversal:.2e}/{deltaAxial:.2e}', fontsize=15, bbox={'facecolor': 'orange', 'alpha': 0.8, 'pad': 2})

        return poissonRatio

    def dataExtract(self, machineName : str, archive_name : str, linearRegionSearchMethod : str,
                     generalMachineData : GeneralMachine = None,
                     x_min = None,
                     x_max = None
                     )->pd.DataFrame:
        '''
        Funçãoo para obter, a parte de um tipo de máquina, identificado pelo nome, os dados brutos do ensaio.
        '''
        # Verificação dos argumentos
        self.__typeCheck(machineName, str)
        self.__typeCheck(archive_name, str)

        if machineName == '68FM100':
            return self._68FM100_Data_Aquisition(archive_name, linearRegionSearchMethod)
        
        if machineName == '_older_machine': # Nome temporário, até conseguir o nome correto da máquina
            return self._olderMachine_Data_Aquisition(archive_name, linearRegionSearchMethod, x_min, x_max)
        
        if machineName == '68FM100_biaxial':
            return self._68FM100_biaxial_Data_Aquisition(archive_name, linearRegionSearchMethod)
        
        if machineName == 'tracao_tipo_5_ave':
            return self._tracao_tipo_5_ave_Data_Aquisition(archive_name, linearRegionSearchMethod)

        if machineName == 'MarcoPvMachine':
            return self.__MarcoPvMachine_Data_Aquisition(archive_name, linearRegionSearchMethod, x_min, x_max)
        
        if machineName == 'generalMachine':
            return self.__general_machine_Data_aquisition(archive_name, linearRegionSearchMethod, generalMachineData, x_min, x_max)
        
        raise Exception('Tipo de Máquina não encontrado')
    
    def MeasureYoungModulus(self,length : float = None,
                            thickess : float = None,
                            width : float = None, 
                            max_percentil : float = 0.25,
                            calculus_method : str = 'linearSearch',
                            offset = 0.002
                            ):
        '''
        Método para medir o módulo de Young
        '''
        axial_strain, force_data = self.__filterDataOnlyBelowMaxForce(self.new_x, self.new_y)


        quantile_map = {
            'standard-ASTM-D3039': self.deformationRange, # porção sugerida pela norma
            'linearSearch': (0, 0.01), # porção utilizada pela experiência,
            'standard-ASTM-D638': (0, 0.01) # porção utilizada pela experiência,
        }

        lower_quantile, upper_quantile = quantile_map[calculus_method] # selecionando o quartil, pelo método passado
        # Filtrando dadas para o cálculo do Módulo de Young
        if self.materialType == 'composite' and lower_quantile == 0.001: # valor especial, fixo, adotado pela ASTM-D3039
            a = lower_quantile
            b = upper_quantile
        elif self.materialType == 'polymer' and calculus_method=='standard-ASTM-D3039':
            a = lower_quantile
            b = upper_quantile
        else:
            a = np.quantile(axial_strain, lower_quantile)
            b = np.quantile(axial_strain, upper_quantile)

        

            
        linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(axial_strain, force_data, a,b)

        E,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
        self.E = E
        
        # # plotando os dados em 5 em 5
        # slice = int(len(self.new_x)/100)
        # x=self.new_x[::slice]
        # y=self.new_y[::slice]
        # self.plotStressStrain(x,y,E, max_percentil)

        if self.machineName == '_older_machine':

            strain = np.divide(self.new_x, length)
            area = thickess*width
            stress =  np.divide(self.new_y, area)
            a = np.quantile(strain, lower_quantile)
            b = np.quantile(strain, upper_quantile)

            linear_region_strain, linear_region_stress = self.__selectYoungModulusRange(strain, stress, a,b)
            E,b,root=self.__equationFit(x_linear=linear_region_strain, y_linear=linear_region_stress)
            self.plotStressStrain(strain,stress,E,offset)
        else:
            self.plotStressStrain(self.new_x,self.new_y,E, max_percentil,offset)

    def MeasurePoissonRatio(self, calculus_method = 'linearSearch'):
        '''
        Método para medir a razão de poisson
        '''

        quantile_map = {
            'standard-ASTM-D3039': self.deformationRange, # porção sugerida pela norma
            'linearSearch': (0, 0.1), # porção utilizada pela experiência
            'standard-ASTM-D638' : (0, 0.1)
        }

        lower_quantile, upper_quantile = quantile_map[calculus_method] # selecionando o quartil, pelo método passado


        if self.machineName == '68FM100_biaxial':
            machineConfig = _68FM100_biaxial()

            scale_find_linear = 4
            scale_calculus = 10
            self.poisson_computation_procedure(scale_calculus=scale_calculus 
                                            ,scale_find_linear=scale_find_linear
                                            ,strain_parallel_column=5
                                            ,strain_transverse_column=6
                                            ,load_column=2
                                            ,machineConfig=machineConfig
                                            ,calculus_method=calculus_method
                                            )

        if self.machineName == '68FM100':
            machineConfig = _68FM100()

            scale_find_linear = 4
            scale_calculus = 10
            self.poisson_computation_procedure(scale_calculus=scale_calculus 
                                               ,scale_find_linear=scale_find_linear
                                               ,strain_parallel_column=5
                                               ,strain_transverse_column=6
                                               ,load_column=2
                                               ,machineConfig=machineConfig
                                               ,calculus_method=calculus_method
                                               )
           
        if self.machineName == 'tracao_tipo_5_ave':

            warnings.warn(f"A máquina {self.machineName} não possui dados de deformação transversa")

            return


    def poisson_computation_procedure(self, scale_find_linear:int , scale_calculus : int,strain_parallel_column : int, strain_transverse_column :int, load_column : int, machineConfig,calculus_method : str):
        '''
        Medida do poisson generalziada para cada método
        '''
        # Encontrar a região linear da deformação axial pela carga
        axial_strain =  np.abs(self.cleaned_raw_data[machineConfig.colunas[strain_parallel_column]])

        get_axial_range_scale = {
            'standard-ASTM-D3039': (1,1), # range_axial and scale for ASTM-D3039
            # 'standard-ASTM-D638' : (self.__filterInitGraph(axial_strain, scale=scale_find_linear), scale_calculus),
            'standard-ASTM-D638' : (1,2),
            'linearSearch': (1,scale_calculus), # porção utilizada pela experiência
        }

        # if calculus_method=='standard-ASTM-D638':
        #     range_axial  = self.__filterInitGraph(axial_strain, scale=scale_find_linear)

        # if self.materialType == 'composite' and calculus_method == 'linearSearch':
        #     range_axial  = self.__filterInitGraph(axial_strain, scale=scale_find_linear)
        # else:
        #     range_axial = 1
        #     scale_calculus = 1

        range_axial, scale_calculus = get_axial_range_scale[calculus_method]
        axial_strain_linear = self.__selectGraphRange(axial_strain, range_axial,scale_calculus)

        # Encontrar a região linear da deformação transversal pela carga (assumida a ser a mesma da axial)
        transverse_strain =  np.abs(self.cleaned_raw_data[machineConfig.colunas[strain_transverse_column]])
        # range_transverse  = self.__filterInitGraph(transverse_strain, scale=scale)
        range_transverse = range_axial # pegando o mesmo range de dados
        transverse_strain_linear = self.__selectGraphRange(transverse_strain, range_transverse,scale_calculus)

        load = self.cleaned_raw_data[machineConfig.colunas[load_column]]

        load_linear_axial = self.__selectGraphRange(load, range_axial,scale_calculus)
        load_linear_tranversal = self.__selectGraphRange(load, range_transverse,scale_calculus)

        if calculus_method == 'standard-ASTM-D3039':
            self.poisson_ratio = self.__standard_ASTM_D3039(axial_strain, transverse_strain)
        if calculus_method == 'standard-ASTM-D638':
            self.poisson_ratio = self.__standard_ASTM_D638(axial_strain_linear,transverse_strain_linear,load_linear_axial)
        else:
            self.poisson_ratio = self.__findConvergencePoisson(axial_strain_linear,transverse_strain_linear,load_linear_axial)

        def selectData(data):

            slice = int(len(data)/80)
            return data[::1]
        
        axial_strain = selectData(axial_strain)
        transverse_strain = selectData(transverse_strain)
        axial_strain_linear = selectData(axial_strain_linear)
        load = selectData(load)
        load_linear_axial = selectData(load_linear_axial)
        transverse_strain_linear = selectData(transverse_strain_linear)
        load_linear_tranversal = selectData(load_linear_tranversal)
        
        if calculus_method == 'linearSearch' and self.verbose:
            ax_total, ax_linear = self.plotComparisonPoissonRatioLinear(axial_strain_total=axial_strain,
                                                transversal_strain_total=transverse_strain
                                                ,axial_train_linear=axial_strain_linear
                                                ,load_total=load
                                                ,load_axial_linear = load_linear_axial
                                                ,transversal_strain_linear=transverse_strain_linear
                                                ,load_transversal_linear=load_linear_tranversal
                                                )
            
        
            plt.show()

        if calculus_method == 'standard-ASTM-D638' and self.verbose:

            self.plotASTMD638_poission(axial_strain_total=axial_strain,
                                                transversal_strain_total=transverse_strain
                                                ,axial_train_linear=axial_strain_linear
                                                ,load_total=load
                                                ,load_axial_linear = load_linear_axial
                                                ,transversal_strain_linear=transverse_strain_linear
                                                ,load_transversal_linear=load_linear_tranversal
                                                )
            
        
            plt.show()

    def plotComparisonExcludedData(self, x,y, x_linear,y_linear, x_label, y_label):
        '''
        Método comparar dados excluídos da análise
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x[0:len(x_linear)], y=y[0:len(y_linear)], label='Dados Originais', ylabel=y_label, xlabel=x_label)
        ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Curva linear', ylabel=y_label, xlabel=x_label, color='red')
        lim_sup_x = x[len(x_linear)] 
        lim_inf_x = x[0] 
        y_max= y[len(y_linear)]
        y_min= y[0]
        
        ax.arrow(x=lim_sup_x,y=y_min,dx=0,dy=(y_max-y_min)*1.2, color='orange')
        ax.arrow(x=lim_inf_x,y=y_min,dx=0,dy=(y_max-y_min)*1.2, color='orange')
        text_x_position = (lim_inf_x)*1.01
        text_y_position = y_max*1.3
        ax.text(text_x_position, text_y_position, r'Região excluída', fontsize=7, bbox={'facecolor': 'orange', 'alpha': 0.1, 'pad': 2})
        ax.legend(loc ='lower right')
        plt.show()

    def plotCleanedData(self, x,y, x_label, y_label):
        '''
        Método para plotar os dados limpos
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x, y=y, label='Dados Ajustados', ylabel=y_label, xlabel=x_label)    
        plt.show()

    def plotComparisonPoissonRatioLinear(self,axial_strain_total
                                             ,transversal_strain_total
                                             ,load_total
                                             ,axial_train_linear, load_axial_linear
                                             ,transversal_strain_linear, load_transversal_linear
                                         ):
        '''
        Método para plotar a comparação entre as regiões lineares na parte das deformações axial (para gerar um gráfico parecido com a norma)
        '''
        fig_total, ax = plt.subplots(figsize=(8,4), constrained_layout=True)
        # partes totais

        y_label =  r"Deformação absoluta $||\varepsilon||$"
        ax = plot_helper(ax=ax, x = load_total, y=axial_strain_total, label='Dados da deformação axial totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[0], linestyle=linestyles_options[0])
        ax = plot_helper(ax=ax, x = load_total, y=transversal_strain_total, label='Dados da deformação transversal totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[5], linestyle=linestyles_options[5])
        ax = plot_helper(ax=ax, x = load_axial_linear, y=axial_train_linear, label='Parte linear da deformação axial', ylabel=y_label, xlabel='Carregamento [kN]', color='orange', linestyle=linestyles_options[10])
        ax = plot_helper(ax=ax, x = load_transversal_linear, y=transversal_strain_linear, label='Parte linear da deformação transversal', ylabel=y_label, xlabel='Carregamento [kN]', color='red', linestyle=linestyles_options[12])
        
        fig_total.savefig('total_poisson.pdf')
        fig_total.savefig('total_poisson.svg')
        fig_total.savefig('total_poisson.png')

        fig, ax3 = plt.subplots(figsize=(8,4), constrained_layout=True)
        ratio = np.divide(transversal_strain_total, axial_strain_total)

        if self.direction == 'parallel':
            label = r'Convergência do razão de Poisson, $\nu_{12}$'+f'={self.poisson_ratio:.3f}'
        else:
            label = r'Convergência do razão de Poisson, $\nu_{21}$'+f'={self.poisson_ratio:.3f}'

        ax3 = plot_helper(ax=ax3, x = load_total, y=ratio, 
                          label=label, 
                          ylabel=r'$||\frac{\varepsilon_{y}}{\varepsilon_{x}}||$', 
                          xlabel='Carregamento [kN]', 
                          color=blue_tonalities_options[10], linestyle=linestyles_options[10])
        
        load_linear_as_list = list(load_axial_linear)

        lim_sup_x = load_linear_as_list[-1]
        lim_inf_x = load_linear_as_list[0]

        ax3.arrow(x=lim_sup_x,y=0,dx=0,dy=max(ratio)/2, color='orange', head_width=0.05)
        ax3.arrow(x=lim_inf_x,y=0,dx=0,dy=max(ratio)/2, color='orange', head_width=0.05)
        text_x_position = (lim_inf_x)*1.2
        text_y_position = max(ratio)/2
        ax3.text(text_x_position, text_y_position, r'Região de Cálculo', fontsize=7, bbox={'facecolor': 'orange', 'alpha': 0.1, 'pad': 2})
        

        plt.show()
    

        return ax, ax3


    def plotASTMD638_poission(self,axial_strain_total
                                             ,transversal_strain_total
                                             ,load_total
                                             ,axial_train_linear, load_axial_linear
                                             ,transversal_strain_linear, load_transversal_linear
                                ):
        
        fig_total, ax = plt.subplots(figsize=(8,4), constrained_layout=True)
        # partes totais

        y_label =  r"Deformação absoluta $||\varepsilon||$"
        ax = plot_helper(ax=ax, x = load_total, y=axial_strain_total, label='Dados da deformação axial totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[0], linestyle=linestyles_options[0])
        ax = plot_helper(ax=ax, x = load_total, y=transversal_strain_total, label='Dados da deformação transversal totais', ylabel=y_label, xlabel='Carregamento [kN]', color=blue_tonalities_options[5], linestyle=linestyles_options[5])
        ax = plot_helper(ax=ax, x = load_axial_linear, y=axial_train_linear, label='Parte linear da deformação axial', ylabel=y_label, xlabel='Carregamento [kN]', color='orange', linestyle=linestyles_options[10])
        ax = plot_helper(ax=ax, x = load_transversal_linear, y=transversal_strain_linear, label='Parte linear da deformação transversal', ylabel=y_label, xlabel='Carregamento [kN]', color='red', linestyle=linestyles_options[12])
        text_x_position = max(load_total)/10

        if max(axial_strain_total)>max(transversal_strain_total):
            y = max(axial_strain_total)
        else:
            y = max(transversal_strain_total)

        text_y_position = y*0.1
        ax.text(text_x_position, text_y_position,r"$\nu_{12}$"+f" = {self.poisson_ratio:.4f}", bbox={'facecolor': 'orange', 'alpha': 0.8, 'pad': 2})

        fig_total.savefig('total_poisson.pdf')
        fig_total.savefig('total_poisson.svg')
        fig_total.savefig('total_poisson.png')

        plt.show()
    

        return 
    
    def plotDataFinalComparison(self,x,y, x_linear,y_linear, x_label,y_label):
        '''
        Método para graficar os dados originais e a parte linear
        '''
        fig, ax = plt.subplots(figsize=(6,3))
        ax = plot_helper(ax=ax, x = x, y=y, label='Dados Originais', ylabel=y_label, xlabel=x_label)
        ax = plot_helper(ax=ax, x = x_linear, y=y_linear, label='Curva linear', ylabel=y_label, xlabel=x_label, color='red')
        plt.show()

    def plotStressStrain(self,x,y,E, max_percentil : float = 0.25,
                         offset = 0.002
                         ):
        '''
        Método para graficar a curva de tensão e deformação

        TODO - generalizar para a função receber um eixo, assim ela pode receber diversos corpos de prova
        '''
        y = pd.Series(y)
        x = pd.Series(x)
        if self.materialType == 'polymer':
            x_max = self.__findMaxPolymerStress(x,y)
        else:
            index_y_max = y[y==max(y)].index[0]
            x_max = x[index_y_max]


        
        x_linear = np.linspace(0,x_max)
        y_linear = [E*x for x in x_linear]

        if self.direction == 'parallel':
            modulus_text = r"$E_1$"
            ylabel = r'$\sigma_{1} \ [MPa]$'
        else:
            modulus_text = r"$E_2$"
            ylabel = r'$\sigma_{2} \ [MPa]$'
        if self.verbose:
            fig, ax = plt.subplots(figsize=(6,3), constrained_layout=True)
            ax = plot_helper(ax=ax, x = x, y=y, 
                             label='Curva de tensão', 
                             ylabel=ylabel, 
                             xlabel=r'$\varepsilon \ \frac{mm}{mm}$',
                             linestyle='-.',
                             )
            ax = plot_helper(ax=ax, x = x_linear.astype(float),
                              y=y_linear, 
                             label='Módulo ajustado', 
                             ylabel=ylabel,
                              xlabel=r'$\varepsilon \ \frac{mm}{mm}$', 
                              color='orange',
                              linestyle='-',
                              marker=None,
                              )
            ax.text(x_linear[-1]*0.8,y_linear[-1]*0.3,modulus_text+fr'={E:.2f} [MPa]',bbox={'facecolor': 'white', 'alpha': 1, 'pad': 3})
        x_offset, y_offset , yieldStress= self.__findYeldStress(x,y,E,max_percentil=max_percentil, offset_yield=offset)
        if self.verbose and (self.materialType=='metal' or self.materialType == 'polymer'):
            ax = plot_helper(ax=ax, x = x_offset, y=y_offset, label=fr'Offset ($\sigma_y={yieldStress:.2f} [MPa]$)', ylabel=r'$\sigma_{x} \ [MPa]$', xlabel=r'$\varepsilon \ \frac{mm}{mm}$', color=blue_tonalities_options[8], linewidth=0.1, linestyle='-.')
            pass
        self.YeldStress = yieldStress
        self.strain = x
        self.stress = y

class SeveralMechanicalTestingFittingLinear():

    def __init__(self, machineName: str, archive_name: str, archivePattern = 'numeric', 
                 linearRegionSearchMethod='Deterministic',
                 materialType : str = 'composite',
                 direction : str = 'parallel',
                 calculus_method : str = 'linearSearch',
                 verbose : bool = False,
                 offset :float = 0.002,
                 generalMachineData : GeneralMachine = None
                 ) -> None:
        
        self.__findOtherArchives(machineName, archive_name, 
                                 archivePattern, 
                                 linearRegionSearchMethod, 
                                 materialType,
                                 direction,
                                 calculus_method,
                                 verbose=verbose,
                                 offset = offset,
                                 generalMachineData = generalMachineData
                                 )

    
    def __findOtherArchives(self, machineName: str, archive_name :  str, 
                            archivePattern : str, 
                            linearRegionSearchMethod='Deterministic', 
                            materialType : str = 'composite',
                            direction :  str = 'parallel',
                            calculus_method : str = 'linearSearch',
                            verbose : bool = False,
                            offset : bool  = 0.002,
                            generalMachineData : GeneralMachine = None
                            ):
        '''
        Method to find others files based on the archive name
        '''
        # get parent dir
        parent_dir = os.path.dirname(archive_name)
        # get all files
        files = os.listdir(parent_dir)
        youngModulusArray = []
        YieldStressArray = []
        PoissonArray = []
        cpName = []
        stress_array = []
        strain_array = []

        for each_file in os.listdir(parent_dir):
            if re.search(pattern=r"\d*.csv", string=each_file):
                full_path_name = os.path.join(parent_dir, each_file)
                c = MechanicalTestFittingLinear(machineName=machineName, archive_name=full_path_name, 
                                                linearRegionSearchMethod=linearRegionSearchMethod, verbose=verbose,
                                                materialType = materialType,
                                                direction=direction,
                                                generalMachineData=generalMachineData
                                                )
                c.MeasureYoungModulus(max_percentil=0.75, calculus_method=calculus_method, offset=offset)
                c.MeasurePoissonRatio(calculus_method=calculus_method)
                youngModulusArray.append(c.E)
                YieldStressArray.append(c.YeldStress)
                if machineName == '68FM100_biaxial':
                    PoissonArray.append(c.poisson_ratio)
                if machineName == '68FM100':
                    PoissonArray.append(c.poisson_ratio)
                if machineName == 'tracao_tipo_5_ave':
                    PoissonArray.append(0)
                cpName.append(each_file.split(sep='.csv')[0])
                stress_array.append(c.stress)
                strain_array.append(c.strain)

        
        # Dicionario com os dados para o boxPlot
        dictMechanical = {'Corpo de Prova': cpName
                          ,'Módulo de Young': youngModulusArray
                          ,'Tensão de Escoamento': YieldStressArray
                          ,'Poisson': PoissonArray
                          ,'strain': strain_array
                          ,'stress': stress_array
                          }
        # Figuras para colocar os boxplots
        fig_YoungModuls,ax_youngModulus = plt.subplots(figsize=(4,3))
        fig_YieldStress,ax_YieldStress = plt.subplots(figsize=(4,3))
        sns.boxplot(data=dictMechanical, x="Módulo de Young", ax=ax_youngModulus)
        sns.boxplot(data=dictMechanical, x="Tensão de Escoamento", ax=ax_YieldStress)

        if machineName == '68FM100_biaxial':
            fig_PoissonRatio,ax_PoissonRatio = plt.subplots(figsize=(4,3))
            sns.boxplot(data=dictMechanical, x="Poisson", ax=ax_PoissonRatio)
            if direction == 'parallel':
                ax_PoissonRatio.set_xlabel(r'$\nu_{12}$')
            else:
                ax_PoissonRatio.set_xlabel(r'$\nu_{21}$')

            fig_PoissonRatio.savefig('poissonRatio.png',  bbox_inches='tight')
            fig_PoissonRatio.savefig('poissonRatio.pdf',  bbox_inches='tight')

        if machineName == '68FM100':
            fig_PoissonRatio,ax_PoissonRatio = plt.subplots(figsize=(4,3))
            sns.boxplot(data=dictMechanical, x="Poisson", ax=ax_PoissonRatio)
            if direction == 'parallel':
                ax_PoissonRatio.set_xlabel(r'$\nu_{12}$')
            else:
                ax_PoissonRatio.set_xlabel(r'$\nu_{21}$')

            fig_PoissonRatio.savefig('poissonRatio.png',  bbox_inches='tight')
            fig_PoissonRatio.savefig('poissonRatio.pdf',  bbox_inches='tight')
            
        if materialType =='polymer' or materialType=='metal':
            ax_youngModulus.set_xlabel("Módulo de Young [MPa]")
            ax_YieldStress.set_xlabel("Tensão de Escoamento [MPa]")
        if materialType =='composite':
            ax_youngModulus.set_xlabel("Módulo de Young [MPa]")
            ax_YieldStress.set_xlabel("Tensão de Ruptura [MPa]")
            
            
        fig_YieldStress.show()
        fig_YoungModuls.show()
        fig_YieldStress.savefig('tensao_limite.png',  bbox_inches='tight')
        fig_YieldStress.savefig('tensao_limite.pdf',  bbox_inches='tight')
        fig_YoungModuls.savefig('modulo_elastico.png',  bbox_inches='tight')
        fig_YoungModuls.savefig('modulo_elastico.pdf',  bbox_inches='tight')

        self.dictMechanical =  dictMechanical
        fig_stress_mat, _ = self.__plotStressStrain(direction)

        self.__createExcelReport()
        # array_figures = [fig_YoungModuls, fig_YieldStress, fig_stress_mat]

        # self.__createrPDFReport(array_figures)

    def __createExcelReport(self):
        '''
        Método para salvar os resultados em um Excel
        '''

        df = pd.DataFrame(self.dictMechanical)
        dfList = []
        for each_cpName in df['Corpo de Prova']:
            data = {
                    'strain': list(df[df['Corpo de Prova']==each_cpName]['strain'].values)[0],
                    'stress': list(df[df['Corpo de Prova']==each_cpName]['stress'].values)[0]
                    }
            dfList.append(pd.DataFrame(data=data))

        df1 = df.drop(columns=['strain', 'stress'])
        try:
            with pd.ExcelWriter('resultados.xlsx', mode='w') as writer:  
                df1.to_excel(writer, sheet_name='Resultados Mecânicos')
                df1.describe().to_excel(writer, sheet_name='Estatística Básica')
                for each_cpName, df_stress_strain in zip(df['Corpo de Prova'], dfList):
                    df_stress_strain.to_excel(writer, sheet_name=f'{each_cpName} | Tensão | Deformação')
        except Exception as e:
            print(e)

    def __plotStressStrain(self, direction : str):
        '''
        Metodo para plotar as curvas de tensao/deformacao, para comparacao posterior
        '''
        fig,ax = plt.subplots(figsize=(10,4))
        
        xs = self.dictMechanical['strain']
        ys = self.dictMechanical['stress']

        x_E_s =[]
        y_E_s =[]
        for each_E in self.dictMechanical['Módulo de Young']:
            x_linear = np.linspace(0,0.008)
            x_E_s.append(x_linear)   
            y_E_s.append([x*each_E for x in x_linear])   
        labels = self.dictMechanical['Corpo de Prova']
        if direction == 'parallel':
            several_plots_helper(ax=ax, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _1 $ [MPa]', color_scheme= 'matplotlib_default')
        if direction == 'transversal':
            several_plots_helper(ax=ax, xs=xs, ys=ys,labels=labels,xlabel=r'Deformação $[mm/mm]$', ylabel=r'$\sigma _2 $ [MPa]', color_scheme= 'matplotlib_default')

        fig.show()

        fig_plotly = go.Figure()
        for each_cp,x,y,x_E,y_E in zip(labels,xs,ys, x_E_s, y_E_s):
                    fig_plotly.add_trace(
            go.Scatter(
                x=x,  # X-axis (assuming 10 time points or measurements)
                y=y,
                mode="lines",
                name=f"{each_cp}",  # Legend entry
            )
        )
                    fig_plotly.add_trace(
                     
                                 go.Scatter(
                x=x_E,  # X-axis (assuming 10 time points or measurements)
                y=y_E,
                mode="lines",
                name=f"{each_cp} - Módulo",  # Legend entry
            )
                 )
        fig_plotly.update_layout(title='Ensaio de Tração Realizado',
        xaxis_title='Deformação [mm/mm]',
        yaxis_title='Tensão [MPa]')
        fig_plotly.show()
        fig_plotly.write_html('exp_data.html')

        return fig,fig_plotly

    def __createrPDFReport(self, figs_array : list):
        '''
        Save info into a pdf (PENSAR EM UM FORMA DE COMO CRIAR UM REPORT COM AS INFORMACOES, ASSIM COM E FEITO NA INSTRON)
        '''
        # with PdfPages("output_plots.pdf") as pdf:
        #     for fig in figs_array:
        #         fig.show()
        #         pdf.savefig()  # Save each plot to the PDF file
        #         plt.close()

class MonteCarloErrorPropagation():
    '''
    Classe para calcular a propagação de erros mediante uma simulação de Monte Carlo

    Ex.:

    def density(m,r,t):
        return m/(np.pi*r**2*t)

    measured_r = [10.01,10.02,10.00,10.05]
    measured_t = [1.01,1.02,1.00,1.05]
    measured_m = [10.50,10.35,10.44,10.42]

    MonteCarloErrorPropagation(density, measured_r,measured_t,measured_m)

    '''

    def __init__(self, f : any, *measured_vars):
        self.__computeError(f, *measured_vars)
        self.__plotDistribution()

        pass

    def __computeError(self,f, *params):
        '''
        
        '''
        array_distributions = []

        for each_param in params:
            var = np.array(each_param)
            var_MC = var.mean()+var.std()*np.random.normal(size=10000)
            array_distributions.append(var_MC)

        self.f_MC : np.array = f(*array_distributions)
        self.f_mean = self.f_MC.mean()
        self.f_max = self.f_MC.mean() + 2*self.f_MC.std()
        self.f_min = self.f_MC.mean() - 2*self.f_MC.std()

    def __plotDistribution(self):
        
        graph_limit_min = min(self.f_MC)
        graph_limit_max = max(self.f_MC)
        confidence_inf = self.f_MC.mean()-2*self.f_MC.std()
        confidence_sup = self.f_MC.mean()+2*self.f_MC.std()

        y_confidence_lenght = len(self.f_MC[self.f_MC>confidence_sup])
        fig,ax = plt.subplots(figsize=(4,3))
        ax.hist(self.f_MC, bins=np.linspace(graph_limit_min,graph_limit_max))
        ax.plot([confidence_inf,confidence_inf],[0, y_confidence_lenght], color='orange')
        ax.plot([confidence_sup,confidence_sup],[0,y_confidence_lenght],color='orange')

        self.ax = ax

class SimpleStatistics():
    '''
    Classe para avaliação simples de estatíticas, dado um conjunto de dados
    '''
    def __init__(self, samples : np.array):

        self.samples : np.array = samples
        self.__computeStatistics()
        pass
    
    def __computeStatistics(self):
        '''
        Calcula estatísticas simples
        '''
        self.std = self.samples.std()
        self.mean = self.samples.mean()
        self.median = np.median(self.samples)
        self.first_quartil = np.quantile(self.samples,0.25)
        self.third_quartil = np.quantile(self.samples,3/4)

    def plot_results(self):
        
        self.fig, self.ax = plt.subplots(figsize=(4,3))
        height_bar =  len(self.samples[self.samples>np.quantile(self.samples,0.9)])
        self.ax.hist(self.samples, bins=20)
        self.ax.plot([self.first_quartil, self.first_quartil],[0,height_bar], color='orange')
        self.ax.plot([self.third_quartil, self.third_quartil],[0,height_bar], color='orange')
        self.ax.plot([self.mean, self.mean],[0,height_bar], color='green', label='Média')
        self.ax.plot([self.median, self.median],[0,height_bar], color='red', label='Mediana')
        self.ax.arrow(x=self.first_quartil,y=height_bar,dx=(self.third_quartil-self.first_quartil),dy=0, color='orange', label='Interquartil')
        self.ax.legend()

if __name__ == '__main__':
    # classInitOne =  MechanicalTestFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv')

    # classInitOne.MeasureYoungModulus()  
    # classInit = SeveralMechanicalTestingFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv')  
    classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\FlexCop\Experimental data\Tensile 90_SENAI_2.csv')
    classInit.MeasureYoungModulus(max_percentil=0.5, calculus_method='standard-ASTM-D3039')
    # classInit.MeasurePoissonRatio(calculus_method='linearSearch')
    # classInit.MeasurePoissonRatio(calculus_method='standard-ASTM-D3039')

# %%
# %%
# %%
