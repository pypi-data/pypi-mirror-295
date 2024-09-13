from experimentalTreatingIsiPol.machines._68FM100 import _68FM100,_tracao_tipo_5_ave
from experimentalTreatingIsiPol.machines._68FM100_biaxial import _68FM100_biaxial
from experimentalTreatingIsiPol.machines._older_machine import _MarcoPvMachine, _Older_Machine
from tabulate import tabulate
def print_machines():
    '''
    Função para mostrar cada uma das pré-formatações configuradas para as máquinas.
    '''
    machines = [
        _68FM100,
        _68FM100_biaxial,
        _Older_Machine,
        _MarcoPvMachine,
        _tracao_tipo_5_ave
    ]

    nomesMaquinas = [
                '68FM100'
                ,'68FM100_biaxial'
                ,'_older_machine'
                ,'MarcoPvMachine'
                ,'tracao_tipo_5_ave'
    ]
    for each_machine, each_machineName in zip(machines, nomesMaquinas):
        ClassInit = each_machine()

        string_coluns = ""
        for each_colum in ClassInit.colunas:
            string_coluns+=f'''
    - {each_colum}
'''
        print(F'''
==========================================================================================
machineName {each_machineName}
==========================================================================================
COLUNAS:
{string_coluns}
''')    
            


