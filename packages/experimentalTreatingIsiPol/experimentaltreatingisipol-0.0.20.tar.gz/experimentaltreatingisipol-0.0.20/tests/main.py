# %%
'''
Teste para gerar um gráfico de linha simples
'''
import os
import sys
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
from experimentalTreatingIsiPol.main import plot_helper
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = plot_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")

# %%
'''
Teste para o gráfico de linha simples sem GRID
'''
import os
import sys
import numpy as np
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))

fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = plot_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")

ax.grid()

# %%
'''
Teste de geração de um gráfico de dispersão
'''
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))

from experimentalTreatingIsiPol.main import scatter_helper
import numpy as np
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 5))
n_samples = 100
ax = scatter_helper(ax, x=np.linspace(1,n_samples, n_samples), 
            y=np.random.normal(5,0.01, n_samples), 
            xlabel='Amostra', ylabel='Espessura [mm]', 
            label=r"Espessuras dos CP's, $\mu=5 [mm]$ e $\sigma=0.01 [mm]$")
# %%
'''
Vários gráficos no mesmo meixo eixo (Método 1, sem utilizar o método automático)
'''
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))

from experimentalTreatingIsiPol.main import plot_helper, blue_tonalities_options
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 5))
x = np.linspace(-10,10)
y1 = np.multiply(x,2)
y2 = np.power(x,1/2)
ax = scatter_helper(ax, x=x,
            y=y1, 
            xlabel='x', ylabel='y', 
            label=r"$2x$", color=blue_tonalities_options[0])

ax = scatter_helper(ax, x=x,
            y=y2, 
            xlabel='x', ylabel='y', 
            label=r"$x^{\frac{1}{2}}$", color = blue_tonalities_options[5], )

# %%
'''
Utilização Simples para Retirada do módulo de elasticidade, da máquina antiga
'''
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))

from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear
import os
archive = os.path.join(os.getcwd(),r'..\DataArquives\Specimen_RawData_1.csv')
classInit =  MechanicalTestFittingLinear(machineName='_older_machine', archive_name=archive, direction = 'parallel', materialType='polymer')
classInit.MeasureYoungModulus(length = 50,thickess = 1,width = 12, max_percentil=0.01)   
# %%
'''
Teste para o cálculo da propagação de erros por simulação de Monte Carlo
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))

from experimentalTreatingIsiPol.main import MonteCarloErrorPropagation
import numpy as np


def density(m,r,t):
    return m/(np.pi*r**2*t)

measured_r = [10.01,10.02,10.00,10.00]
measured_t = [1.01,1.02,1.00,1.05]
measured_m = [15.50,5.35,1.44,15.42,1.44]

ClassInit = MonteCarloErrorPropagation(density, measured_m, measured_r, measured_t)
ClassInit.ax.set_title('Densidade calculada: ' + f'{ClassInit.f_mean:.2f}+/- {2*ClassInit.f_MC.std():.2f}')
# %%
'''
Testes para a plotagem de múltiplos gráficos padronizados, no mesmo eixo, (Método 2)
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import several_plots_helper,several_scatter_helper
import matplotlib.pyplot as plt

def createFakeExperimentalData(y_data, n):
    new_y = []
    for i in range(n):
        r = np.random.rand()
        mean = 0.01*(r-1)+0.01*(r)

        Y_with_noise = y_data -y_data*(np.random.normal(mean,0.1,1))

        new_y.append(Y_with_noise)

    return new_y

number_of_especimes = 18
number_of_points = 1000
several_x = [np.linspace(0,number_of_points,number_of_points) for _ in range(number_of_especimes)] # criando 10 amostras para o eixo x

data_y = np.sqrt(np.linspace(0,number_of_points,number_of_points))
several_y = createFakeExperimentalData(data_y,number_of_especimes) # criando 10 amostras para o eixo y
several_labels = [f'data {i}' for i in range(number_of_especimes)]

fig, ax = plt.subplots(figsize=(8,3))

fig.get_figwidth()
ax = several_scatter_helper(ax,xs=several_x,ys=several_y,labels=several_labels,
                          xlabel=f'X data',ylabel='Y data',markersize=5)
# %%
'''
Teste para análise de resultados de vários CPs, em materiais isotrópicos
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100', archive_name=r'D:\Jonas\ExperimentalData\OS894_22_PP40RE3AM.is_tens_Exports\YBYRÁ_Tensile_PP40RE3AM_SP-01.csv',
                                                  materialType = 'polymer'
                                                  ) 
# %%
'''
Teste da utilização da Instron, para ensaios biaxiais (para obter o Poisson) de materiais isotrópicos (metal),
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear
import matplotlib.pyplot as plt

classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'..\DataArquives\Specimen_biaxial.csv', 
                                        materialType='metal',
                                        direction = 'parallel')
classInit.MeasureYoungModulus(max_percentil=0.1)
classInit.MeasurePoissonRatio()

# %%
'''
Teste para a obtenção de Poisson e Young em materiais compósitos. Usando a norma standard-ASTM-D3039
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear

classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\FlexCop\Experimental data\Tensile 90_SENAI_2.csv', materialType ='composite', 
                                        direction = 'tranversal'
                                        )
classInit.MeasureYoungModulus(max_percentil=0.75, calculus_method = 'standard-ASTM-D3039')
classInit.MeasurePoissonRatio(calculus_method = 'standard-ASTM-D3039')
# %%
'''
Teste para a obtenção de Poisson e Young em materiais compósitos, sem usar a norma para nenhum dos dois
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear

classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\FlexCop\Experimental data\Tensile 90_SENAI_2.csv', materialType ='composite', 
                                        direction = 'tranversal'
                                        )
classInit.MeasureYoungModulus(max_percentil=0.75, calculus_method = 'linearSearch')
classInit.MeasurePoissonRatio(calculus_method = 'linearSearch')

# %%
'''
Teste para a obtenção de Poisson e Young em materiais compósitos, usando a norma apenas para o módulo
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear

classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\FlexCop\Experimental data\Tensile 90_SENAI_2.csv', materialType ='composite', 
                                        direction = 'tranversal'
                                        )
classInit.MeasureYoungModulus(max_percentil=0.75, calculus_method = 'standard-ASTM-D3039')
classInit.MeasurePoissonRatio(calculus_method = 'linearSearch')

# %%
'''
Teste para a obtenção de Poisson e Young em materiais compósitos, usando a norma apenas para o poisson
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear

classInit = MechanicalTestFittingLinear('68FM100_biaxial', archive_name=r'D:\Jonas\FlexCop\Experimental data\Tensile 90_SENAI_2.csv', materialType ='composite', 
                                        direction = 'tranversal'
                                        )
classInit.MeasureYoungModulus(max_percentil=0.75, calculus_method = 'linearSearch')
classInit.MeasurePoissonRatio(calculus_method = 'standard-ASTM-D3039')
# %%
'''
Teste para análise de resultados de vários CPs, em materiais ortotrópicos
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\IPF\Tração 90\Specimen 1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='standard-ASTM-D3039'
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df
# %%
'''
Teste para análise de resultados de vários CPs, em materiais ortotrópicos
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Madeira Plastica\OS894_22_PP20RE3AM.is_tens_Exports\Test-04\YBYRÁ_Tensile_PP20RE3AM_SP-01.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                #   calculus_method='standard-ASTM-D3039',
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])
# %%
'''
Teste para análise de resultados de vários CPs, em materiais ortotrópicos, metodo 2
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Perfil preto comercial da Falcon\Ybyrá_PerfilPreto_L.is_tens_Exports\Ybyrá_PerfilPreto_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('tracao_tipo_5_ave', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                #   calculus_method='standard-ASTM-D3039',
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])
# %%
'''
Teste para análise de resultados de vários CPs, PERFIL INJETADO
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Perfil preto comercial da Falcon\Injetado\Ybyrá_PerfilPreto_Inj.is_tens_Exports\Ybyrá_PerfilPreto_Inj_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('tracao_tipo_5_ave', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                  calculus_method='standard-ASTM-D3039',
                                                # verbose=True
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])
# %%
'''
Teste para análise de resultados de vários CPs, PERFIL PRETO L1
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Perfil preto comercial da Falcon\Ybyrá_PerfilPreto_L_tipo_1\Ybyrá_PerfilPreto_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('tracao_tipo_5_ave', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                  calculus_method='standard-ASTM-D3039',
                                                # verbose=True
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])

# %%
'''
Teste para análise de resultados de vários CPs, PERFIL PRETO L2
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Perfil preto comercial da Falcon\Ybyrá_PerfilPreto_L_tipo_2\Ybyrá_PerfilPreto_L_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('tracao_tipo_5_ave', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                  calculus_method='standard-ASTM-D3039',
                                                # verbose=True
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])
# %%
'''
Teste para análise de resultados de vários CPs, PERFIL PRETO T
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Perfil preto comercial da Falcon\Ybyrá_PerfilPreto_T.is_tens_Exports\Ybyrá_PerfilPreto_T_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('tracao_tipo_5_ave', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                  calculus_method='standard-ASTM-D3039',
                                                # verbose=True
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])
# %%
'''
Teste para análise de resultados de vários CPs, PERFIL PRETO T2
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Perfil preto comercial da Falcon\Ybyrá_PerfilPreto_T2.is_tens_Exports\Ybyrá_PerfilPreto_T2_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('tracao_tipo_5_ave', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                #   calculus_method='standard-ASTM-D3039',
                                                # verbose=True
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])

# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 90°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 1\Tração 90\Specimen1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='standard-ASTM-D3039',
                                                  ) 

# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 90°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 1\Tração 90\Specimen1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='linearSearch',
                                                  ) 
# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 90°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 2\Tração 90\Strain 1_SP1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='standard-ASTM-D3039',
                                                  ) 
# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 90°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 5\Tração 90\Specimen 2.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='standard-ASTM-D3039',
                                                  ) 
# %%
# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 90°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 3\Tração 90\Specimen 1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='standard-ASTM-D3039',
                                                  ) 
# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 90°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 00\Tração 0\Specimen 1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'parallel',
                                                  calculus_method='standard-ASTM-D3039',
                                                  ) 
# %%
'''
Teste para análise de resultados de vários CPs, Compósitos, tração a 0°
'''
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
import numpy as np
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto SIQ4TFP - General\07_DOCUMENTOS_TECNICOS\DADOS_ENSAIOS\Senai\Placa 00\tração_90\Tensile 90_SENAI_2.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100_biaxial', archive_name=arq_path,
                                                  materialType = 'composite',
                                                  direction = 'transversal',
                                                  calculus_method='standard-ASTM-D3039',
                                                  verbose=True
                                                  ) 

# %%
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Madeira Multilaminado\Ybyra_Multilaminado_L.is_tens_Exports\Ybyra_Multilaminado_L_1.csv"
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear
classInit = SeveralMechanicalTestingFittingLinear('68FM100', archive_name=arq_path,
                                                  materialType = 'polymer',
                                                  direction = 'parallel',
                                                  calculus_method='standard-ASTM-D3039',
                                                  ) 


import pandas as pd
df = pd.DataFrame(classInit.dictMechanical)
df = df.drop(columns=['strain', 'stress'])

# %%
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear, MechanicalTestFittingLinear
arq_path = r"C:\Users\user\Sistema Fiergs\DTI-Projeto Ybyra - General\07_DOCUMENTOS_TECNICOS\ME03\Ensaios\Tração\Instron 68FM100\Madeira Multilaminado\Ybyra_Multilaminado_L.is_tens_Exports\Ybyra_Multilaminado_L_8.csv"
c = MechanicalTestFittingLinear(
                            '68FM100', archive_name=arq_path,
                            materialType = 'polymer',
                            direction = 'parallel',
)

c.MeasureYoungModulus(calculus_method='linearSearch')
c.MeasurePoissonRatio(calculus_method='linearSearch')

# %%
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
arq_path = r"D:\Jonas\Mini Curso Python\experimental_data\exemplo_projeto\PEAD_Test6_Tensile_SP-01.csv"
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear

c = MechanicalTestFittingLinear(
                            'MarcoPvMachine', archive_name=arq_path,
                            materialType = 'polymer',
                            direction = 'parallel',
)

c.MeasureYoungModulus(length=10, thickess=0.3, width=2, offset=0.5)
# %%
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
arq_path = r"D:\Jonas\Mini Curso Python\experimental_data\exemplo_projeto\PEAD_Test6_Tensile_SP-01.csv"
from experimentalTreatingIsiPol.main import MechanicalTestFittingLinear
from experimentalTreatingIsiPol.machines._generalMachine import GeneralMachine
c = MechanicalTestFittingLinear(
                            'generalMachine', archive_name=arq_path,
                            materialType = 'polymer',
                            direction = 'parallel',
                            linearRegionSearchMethod='custom',
                            generalMachineData=GeneralMachine(colunas=['Tempo','Deslocamento','Força','Extensometro'],
                                                              decimal=',',
                                                              column_delimitador=';',
                                                              skip_rows=12,
                                                              x_column='Deslocamento',
                                                              y_column='Força'
                                                              ),
                            x_min=1,

                            x_max=2
)
c.MeasureYoungModulus(length=10, thickess=0.3, width=2, offset=1)
# %%
# %%
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
from experimentalTreatingIsiPol.main import SeveralMechanicalTestingFittingLinear

ClassInit = SeveralMechanicalTestingFittingLinear(
    archive_name=r'D:\Jonas\Mini Curso Python\experimental_data\exemplo_projeto\PEAD_Test6_Tensile_SP-02.csv',
    machineName='MarcoPvMachine', 
    materialType='polymer',
    calculus_method='linearSearch',
    verbose=False
)
# %%
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(),r'..\src'))
from experimentalTreatingIsiPol.machines import print_machines

print_machines()

# %%
