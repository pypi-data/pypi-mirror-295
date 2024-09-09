import os
import re

import numpy as np
import pandas as pd
from pymatgen.core.structure import Structure
from pymatgen.io.cif import CifParser, CifWriter
from multiprocessing import Pool
import gemmi
from tqdm import tqdm


def WriteEcif(df, out, idName='ID', cifColName='CIF', properties=None):
    """
    Write a pandas dataframe to an ECIF file
    """
    
    if cifColName not in df.columns:
        raise ValueError("No column named %s in dataframe" % cifColName)
    
    cifblock = CifBlock()

    for cif in df[cifColName]:
        if isinstance(cif, gemmi.SmallStructure):
            processStructure = cifblock.SetCifFromGemmicif
            break
        elif isinstance(cif, Structure):
            processStructure = cifblock.SetCifFromPymatgen
            break
        else:
            raise ValueError("CIF column must contain either pymatgen or gemmi structures")
    
    if properties is None:
        properties = []
    else:
        properties = list(properties)

    if cifColName in properties:
        properties.remove(cifColName)
    if idName in properties:
        properties.remove(idName)

    if os.path.exists(out):
        print("Warning: %s already exists. Overwriting." % out)
    
    with open(out, 'w') as file:

        for num, row in enumerate(df.iterrows()):
            
            if idName is not None:
                if idName == 'ID':
                    cifblock.SetProp('_Name', str(row[0]))
                else:
                    cifblock.SetProp('_Name', str(row[1][idName]))

            structure = row[1][cifColName]
            processStructure(structure)

            for prop in properties:
                cell_value = row[1][prop]
                # Make sure float does not get formatted in E notation
                if np.issubdtype(type(cell_value), np.floating):
                    s = '{:f}'.format(cell_value).rstrip("0")  # "f" will show 7.0 as 7.00000
                    if s[-1] == ".":
                        s += "0"  # put the "0" back on if it's something like "7."
                    cifblock.SetProp(prop, s)
                else:
                    cifblock.SetProp(prop, str(cell_value))

            cif_block = cifblock.GetBlock(cifColName)
            num_cif_block = re.sub(r'(<.*?>)(.*?)(?=\s|$)', fr'\1 ({num})', cif_block)
            file.write(num_cif_block)
            file.write('\n\n$$$$\n\n')

def LoadEcif(ecif_file, idName='ID', cifColName='CIF', type='gemmi'):
    """
    Load ECIF file into a pandas dataframe
    """
        
    with open(ecif_file, 'r') as file:
        lines = file.readlines()
    
    df = pd.DataFrame()
    block = []
    rows = []
    cifblocks = []
    for line in lines:
        if line.strip() == '$$$$':   
            cifblock = CifBlock()   
            cifblock.SetBlock('\n'.join(block), cifColName=cifColName)
            block = []
            cifblocks.append(cifblock)
            row = _CifBlockToRow(cifblock, cifColName, type=type)
            rows.append(row)
        else:
            block.append(line)

    df = pd.DataFrame(rows)

    if idName in df.columns:
        df.set_index(idName, inplace=True)

    for col in df.columns:
        if col != cifColName:
            df[col] = pd.to_numeric(df[col], errors='ignore')

    return df

def _CifBlockToRow(cifblock, cifColName, type='gemmi'):
    row = {}
    for key, value in cifblock._props.items():
        row[key] = value
    if type == 'gemmi':
        row[cifColName] = cifblock.GetGemmicif()
    elif type == 'pymatgen':
        row[cifColName] = cifblock.GetPymatgenStructure()
    return row

class CifBlock:
    def __init__(self):
        self._props = {}
        self._cif = []
        self.pattern = re.compile(r'<(.*?)>\s\(\d+\)\n(.*?)(?=<|$)', re.DOTALL)
    
    def SetProp(self, key, value):
        self._props[key] = value
    
    def GetProp(self, key):
        return self._props[key]
    
    def SetCifFromString(self, string):
        self._cif = string.split('\n')

    def GetCif(self):
        return self._cif

    def SetBlock(self, block, cifColName='CIF'):
        
        matches = self.pattern.findall(block)

        block_dict = {key: value.strip() for key, value in matches}

        self._cif = block_dict[cifColName].split('\n')
        for key, value in block_dict.items():
            if key != cifColName:
                self._props[key] = value

    def GetBlock(self, cifColName='CIF'):
        block = []
        block.append('<ID>\n%s\n' % self._props['_Name'])
        block.append(f'<{cifColName}>')
        for line in self._cif:
            block.append(line)
        for key, value in self._props.items():
            if key != '_Name':
                block.append('<%s>\n%s' % (key, value))
        block_str = '\n'.join(block)
        return block_str

    def SetCifFromPymatgen(self, structure):
        cif_writer = CifWriter(structure)
        cif_string = cif_writer.__str__()
        cif_string = cif_string.split('\n')
        self._cif = []
        for line in cif_string:
            self._cif.append(line)   

    def SetCifFromGemmicif(self, structure):
        cif_string = structure.make_cif_block().as_string()
        cif_string = cif_string.split('\n')
        self._cif = []
        for line in cif_string:
            self._cif.append(line)

    def GetPymatgenStructure(self):
        cif_str = '\n'.join(self._cif)
        cif_parser = CifParser.from_str(cif_str)
        return cif_parser.get_structures(on_error='ignore')[0]
    
    def GetGemmicif(self):
        cif_str = '\n'.join(self._cif)
        cif_parser = gemmi.cif.read_string(cif_str)
        return gemmi.make_small_structure_from_block(cif_parser.sole_block())

    def WriteCif(self, filename):
        with open(filename, 'w') as f:
            for key, value in self._props.items():
                f.write('_%s\n%s\n' % (key, value))
            f.write('\n')
            for line in self._cif:
                f.write(line + '\n')

if __name__ == '__main__':
    #df = LoadEcif('example/mb-jdft2d.ecif')
    #WriteEcif(df, 'output.ecif', properties=df.columns)
    #from pymatgen.core import Lattice
    #df = pd.DataFrame({
    #    'ID': ['test1', 'test2'],
    #    'CIF': [Structure(Lattice.cubic(4.225), ["Na"], [[0, 0, 0]]),
    #            Structure(Lattice.cubic(3.61), ["Cu", "Cu", "Cu", "Cu"], [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, #0.5]])
    #            ],
    #    'prop1': [1, 2],
    #    'prop2': [3, 4]
    #})
    #WriteEcif(df, 'test.ecif', properties=['prop1', 'prop2'])
    #df = LoadEcif('test.ecif')
    #WriteEcif(df, 'test2.ecif', properties=df.columns)

    #import cProfile
    #cProfile.run('df = LoadEcif("matbench/matbench_jdft2d/test_fold_0.ecif", cifColName="structure")')
    df = LoadEcif("matbench/matbench_mp_e_form/test_fold_0.ecif", cifColName="structure", type='gemmi')
    #df = LoadEcif("matbench/matbench_jdft2d/train_fold_0.ecif", cifColName="structure", type='gemmi')
    print(df)
    #df