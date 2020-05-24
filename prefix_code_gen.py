import math

class Node:
  def __init__(self, tot_prob=0.0, parent=None, children=[]):
    self.parent = parent
    self.children = children
    self.prob = tot_prob
  
  def get_parent(self):
    return self.parent
    
  def get_prob(self):
    return self.prob
    
  def set_prob(self, prob):
    self.prob = prob
    
  def set_parent(self, parent):
    self.parent = parent
    
  def add_child(self, child):
    self.children.append(child)

class Symbol(Node):
  def __init__(self, definition, state_trans=False, sym="", prob=0.0):
    super().__init__(tot_prob=prob, children=None)
    self.definition = definition
    self.state_trans = state_trans
    self.sym = sym
    
  def get_definition(self):
    return self.definition
    
  def get_symbol(self):
    return self.sym
    
  def get_k(self):
    return self.definition.count('1')
    
  def set_symbol(self, sym):
    self.sym = sym
    
  def add_symbol_prefix(self, prefix):
    self.sym = prefix + self.symbol
    
  def add_symbol_suffix(self, suffix):
    self.sym = self.sym + suffix
    
  def __str__(self):
    if(self.state_trans):
      string = "State Transition:\t"
    else:
      string = "Symbol Definition:\t"
    string +=  self.definition +\
            "\tProbability: " + str(format(self.prob, "05f")) +\
            "\tSymbol: " + self.sym
    return string
            
  def __len__(self):
    return len(self.sym)
    
    
class SymbolLibrary:
  def __init__(self, num_signals, no_change_prob=0.5, additional_symbols=[]):
    self.n = num_signals
    self.symbols = [Symbol(SymbolLibrary._int_to_bin_string(self.n, i), state_trans=True)\
      for i in range(2**self.n)]
    
    prob_dict = {0 : no_change_prob}
    tot_prob = no_change_prob + sum([sym.get_prob() for sym in additional_symbols])
    for i in range(1, self.n):
      k_freq = SymbolLibrary.get_k_freq(self.n, i)
      prob_dict[i] = SymbolLibrary.prob_nk_plus_one(k_freq, 1.0-tot_prob)
      tot_prob = tot_prob + (k_freq * prob_dict[i])
    prob_dict[self.n] = 1.0-tot_prob
    
    for sym in self.symbols:
      sym.set_prob(prob_dict[sym.get_k()])
    
    self.symbols.extend(additional_symbols)
      
    self.populate_syms()
      
  def __len__(self):
    return len(self.symbols)
    
  def __str__(self):
    string = ""
    for sym in self.symbols:
      string += '\n' + str(sym)
    string += "\nAverage symbol length: " + str(self.get_avg_sym_len())
    return string
  
  def get_sym_list(self):
    return self.symbols
    
  def get_sym_dict(self):
    return {sym.get_definition() : sym.get_symbol()\
      for sym in self.symbols}
    
  def get_n(self):
    return self.n
  
  def sort_sym_list(self, func=Symbol.get_prob):
    self.symbols.sort(key=func, reverse=True)
    
  def get_avg_sym_len(self):  
    return sum([len(sym)*sym.get_prob() for sym in self.symbols])
    
  def populate_syms(self):
    
    def add_to_tree(root, possible_leafs):
      # print("Number of nodes: " + str(len(tree)) + " " + str(len(possible_leafs)) +\
      #   " leaves remaining with root prob: " + str(root.get_prob()))
      # a leaf has been reached, no further work to do
      if(len(possible_leafs)==1):
        return
      sum=0
      for i, leaf in enumerate(possible_leafs):
        sum = sum + leaf.get_prob()
        if(sum>=(0.5*root.get_prob())):
          for j, leaf in enumerate(possible_leafs):
            if(j>i): leaf.add_symbol_suffix('1')
            else: leaf.add_symbol_suffix('0')
          if(len(possible_leafs[:(i+1)])==1): 
            tree.append(possible_leafs[0])
            possible_leafs[0].set_parent(root)
          else: 
            tree.append(Node(tot_prob=sum, parent=root))
          root.add_child(tree[-1])
          add_to_tree(tree[-1], possible_leafs[:(i+1)])
          if(len(possible_leafs[(i+1):])==1):
            tree.append(possible_leafs[1])
            possible_leafs[1].set_parent(root)
          else:
            tree.append(Node(tot_prob=(root.get_prob()-sum), parent=root))
          root.add_child(tree[-1])
          add_to_tree(tree[-1], possible_leafs[(i+1):])
          break
    
    self.sort_sym_list(func=Symbol.get_prob)
    total_prob = sum([sym.get_prob() for sym in self.symbols])
    tree = [Node(tot_prob=total_prob)]
    # print("Starting tree formation")
    add_to_tree(tree[0], self.symbols)
    # print("Tree formation finished! There are " + str(len(tree)) + " nodes.")  
  
  def _int_to_bin_string(n, i):
    return format(i, ('0'+str(n)+'b'))
    
  def get_k_freq(n, k):
    return (math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
  
  def prob_nk_plus_one(qty_with_eq_k, remaining_prob):
    return remaining_prob/(qty_with_eq_k+1)

def main():
  lib = SymbolLibrary(8, no_change_prob=0.5)
  print(lib)
  
if(__name__ =='__main__'):
  main()