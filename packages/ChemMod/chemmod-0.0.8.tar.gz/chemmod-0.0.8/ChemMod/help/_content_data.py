content_data = {
    "element_data": {
        "Info": str(f'''element_data is a library containing all the elements in the periodic system.
        \n It contains the following information about the elements:
        \n\t Atomic number
        \n\t Molar mass
        \n\t Valency
        \n\t Name
        \n\t Electronegativity
        \n\n The data is structured as follows:'''
        + '''\n\n     "H": {
        \n\t"AtomicNumber": 1,
        \n\t"MolarMass": 1.008,
        \n\t"Valency": 1,
        \n\t"Name": "Hydrogen",
        \n\t"Electronegativity": 2.20
        \n\t},
        \n\nTo extract the wanted information write the following (Works for all elements, we use Helium (He) in this example):
        \n\tAtomic Number:
        \n\telement_data['He']['AtomicNumber']
        \n\tMolar Mass:
        \n\telement_data['He']['MolarMass']
        \n\tValency:
        \n\telement_data['He']['Valency']
        \n\tName:
        \n\telement_data['He']['Name']
        \n\tElectronegativity:
        \n\telement_data['He']['Electronegativity']
    '''),
    },
    "M": {"Info": str(f'''M is a function that calculates the molarmass of a given atom or molecule.
        \n It contains the following information about the elements:
        \n\t Atomic number
        \n\t Molar mass
        \n\t Valency
        \n\t Name
        \n\t Electronegativity
        \n\n The data is structured as follows:'''
        + '''\n\n     "H": {
        \n\t"AtomicNumber": 1,
        \n\t"MolarMass": 1.008,
        \n\t"Valency": 1,
        \n\t"Name": "Hydrogen",
        \n\t"Electronegativity": 2.20
        \n\t},
        \n\nTo extract the wanted information write the following (Works for all elements, we use Helium (He) in this example):
        \n\tAtomic Number:
        \n\telement_data['He']['AtomicNumber']
        \n\tMolar Mass:
        \n\telement_data['He']['MolarMass']
        \n\tValency:
        \n\telement_data['He']['Valency']
        \n\tName:
        \n\telement_data['He']['Name']
        \n\tElectronegativity:
        \n\telement_data['He']['Electronegativity']
    '''),
    },
    "gibbs_plot": {"Info": str(f'''g
    '''),
    },
    "bjerrum_plot": {"Info": str(f'''b
    '''),
    },
    "order_plot": {"Info": str(f'''o
    '''),
    },
    "arrhenius_plot": {"Info": str(f'''a
    '''),
    },
    "equil": {"Info": str(f'''e
    '''),
    },
}
