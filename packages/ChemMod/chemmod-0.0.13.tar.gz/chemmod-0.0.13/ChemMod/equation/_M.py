#M - Find molar masses of different atoms and molecules by inputting a string

def M(molecule):
  if type(molecule)!=str:
    raise TypeError(type(molecule),molecule,"STOP wtf I want a f*cking string dumb ass")
  else:
    molarmass=0
    molecule1=molecule.split()
    molecule_atoms=[]
    molecule_n_atoms=[]
    for i in range(len(molecule1)):
      try:
        molecule_n_atoms.append(int(molecule1[i]))
      except ValueError:
        molecule_atoms.append(molecule1[i])
        try:
          a=int(molecule1[i+1])
        except ValueError:
          molecule_n_atoms.append(int(1))
        except IndexError:
          molecule_n_atoms.append(int(1))
    for i in range(len(molecule_atoms)):
      molarmass+=molecule_n_atoms[i]*element_data[molecule_atoms[i]]['MolarMass']
  return molarmass



