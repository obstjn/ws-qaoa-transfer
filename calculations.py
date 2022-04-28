import networkx as nx
import numpy as np
from networkx import Graph
from qiskit import Aer, execute, BasicAer

# Value of a given cut
cutValueDict = {}
def cut_value(G: Graph, x: str) -> int:
  #val = cutValueDict.get(x)
  #if val is not None:
  #  return val
  #else:
    result = 0
    x = x[::-1]  # reverse the string since qbit 0 is LSB
    for edge in G.edges():
      u, v = edge
      #weight = G.get_edge_data(u,v, 'weight')['weight']
      if x[u] != x[v]: 
        result += 1 #weight
    #result= -(len(G.edges())/2- result)
    cutValueDict[x] = result
    return result

def value_of_edge(G: Graph, x: str, edge) -> int:
    """
    Return 1 if the edge is cut given the cut x, 0 otherwise
    """
    u, v = edge
    if x[u] != x[v] and edge in G.edges() :
      return 1
    else:
      return 0


def get_energy(G, qaoa_qc, gamma, beta, edge, sim=Aer.get_backend('statevector_simulator'), shots=1024):
  """
  Calculates the energy for a qaoa instance with the given parameters.
  This corresponds to the expected MaxCut value.
  qaoa_qc has generic Parameter() that needs to be assigned.
  """
  # prepare circuit
  qaoa_instance = qaoa_qc.assign_parameters([beta, gamma])
  if str(sim) != 'statevector_simulator':
    qaoa_instance.measure_all()

  #execute circuit
  result = execute(qaoa_instance, sim, shots=shots).result()

  #calculate energy
  energy = 0
  for cut, prob in result.get_counts().items():
    #energy += cut_value(G, cut) * prob  #energy of whole graph
    energy += value_of_edge(G, cut, edge) * prob  #energy of single edge
    # normalize
  if str(sim) != 'statevector_simulator':
    energy = energy / shots

  return energy


def get_energy_grid(G, qaoa_qc, edge, gammaMax=2*np.pi, betaMax=np.pi, samples=100):
  """  Calculate the energies for a 2D parameter space.  """
  gammas, betas = np.mgrid[0:gammaMax:gammaMax/samples, 0:betaMax:betaMax/samples]
  result = np.empty((samples,samples))

  print('Calculating energy:')
  for i in range(samples):
    for j in range(samples):
      result[i,j] = get_energy(G, qaoa_qc, gammas[i,j], betas[i,j], edge)

      # progress bar
      bar_len = 60
      progress = int(bar_len*(i*samples + j)/(samples**2)) + 1
      print('\r{0}{1}'.format('\u2588' * progress, '\u2591' * (bar_len-progress)), end='')
      print('\t' + f'{(i*samples + j + 1)}/{samples**2} samples', end='')
  print()
  return result
