import math

n = 4
exp_n = 2**n

no_change_prob = 0.9

symbol_list = []

class Node:

  def __init__(self, tot_prob=0.0, parent=None, children=[]):
    self.parent = parent
    self.children = children
    self.tot_prob = tot_prob
  
  def get_parent(self):
    return self.parent
    
  def get_tot_prob(self):
    return self.tot_prob
    
  def set_parent(self, parent):
    self.parent = parent
    
  def add_child(self, child):
    # if(len(self.children)==0):
      # self.tot_prob = child.get_tot_prob()
    # else:
      # self.tot_prob = self.tot_prob + child.get_tot_prob()
    self.children.append(child)
      
    
class Leaf(Node):
  def __init__(self, sym):
    super().__init__(tot_prob=sym.get_prob(), children=None)
    self.sym = sym
    
  def get_symbol(self):
    return self.sym

class Symbol:
  def __init__(self, num_signals, int_val, sym="", prob=0.0):
    self.state_trans = Symbol._int_to_bin_string(num_signals, int_val)
    self.prob = prob
    self.sym = sym
    # else: self.prob = 2.0*(1.0-no_change_prob)*Symbol._sym_prob(num_signals, Symbol._ones_count(num_signals, int_val))
    
  def get_state_trans(self):
    return self.state_trans
    
  def get_prob(self):
    return self.prob
    
  def get_symbol(self):
    return self.sym
    
  def get_k(self):
    return self.state_trans.count('1')
  
  def set_prob(self, prob):
    self.prob = prob 
    
  def set_symbol(self, sym):
    self.sym = sym
    
  def add_symbol_prefix(self, prefix):
    self.sym = prefix + self.symbol
    
  def add_symbol_suffix(self, suffix):
    self.sym = self.sym + suffix
    
  def __str__(self):
    return  "State Transition: " + self.get_state_trans() +\
            "\tProbability: " + str(self.get_prob()) +\
            "\tSymbol: " + self.get_symbol()
    
  def _int_to_bin_string(n, i):
    return format(i, ('0'+str(n)+'b'))
    
  # def _num_eq_k_bits_set(n, k):  
    # return (math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
  
  # def _sym_prob(n, k, first=True):
    # factor = Symbol._num_eq_k_bits_set(n, k)+1
    # # there is only one no change state
    # if(k==0 and first): return 0.5
    # elif(k==0): return factor
    # elif(first): return 1/(factor*Symbol._sym_prob(n, k-1, first=False))
    # else: return factor*Symbol._sym_prob(n, k-1, first=False)
    
  # def _ones_count(n, i):
    # return Symbol._int_to_bin_string(n, i).count('1')
    
class SymbolLibrary:
  def __init__(self, num_signals, no_change_prob=0.5):
    self.n = num_signals
    self.symbols = [Symbol(self.n, i) for i in range(self.n**2)]
    
    prob_dict = {0 : no_change_prob}
    tot_prob = no_change_prob
    for i in range(1, self.n):
      k_freq = SymbolLibrary.get_k_freq(self.n, i)
      prob_dict[i] = SymbolLibrary.prob_nk_plus_one(k_freq, 1.0-tot_prob)
      tot_prob = tot_prob + (k_freq * prob_dict[i])
    prob_dict[self.n] = 1.0-tot_prob
    
    for i in range(len(self.symbols)):
      self.symbols[i].set_prob(prob_dict[self.symbols[i].get_k()])
  
  def get_sym_list(self):
    return self.symbols
    
  def get_n(self):
    return self.n
    
  def print_sym_list(self):
    for i in range(len(self.symbols)):
      print(self.symbols[i])
  
  def sort_sym_list(self, func=Symbol.get_prob):
    self.symbols.sort(key=func, reverse=True)
  
  def get_k_freq(n, k):
    return (math.factorial(n)/(math.factorial(k)*math.factorial(n-k)))
  
  def prob_nk_plus_one(qty_with_eq_k, remaining_prob):
    return remaining_prob/(qty_with_eq_k+1)

    

lib = SymbolLibrary(4, no_change_prob=0.9)
lib.sort_sym_list()
lib.print_sym_list()
    
# create state transition symbol library
# if(no_change_prob != None): 
  # symbol_list = [Symbol(n, 0, prob=no_change_prob)]
  # symbol_list.extend([Symbol(n, i, no_change_prob=no_change_prob) for i in range(1, exp_n)])
# else:
  # symbol_list = [Symbol(n, i) for i in range(exp_n)]

# sort symbol library in ascending probablistic order 
# symbol_list.sort(key=Symbol.get_prob, reverse=True)

# add all symbols to leaf list
leaf_list = [Leaf(lib.get_sym_list()[i]) for i in range(len(lib.get_sym_list()))]
# leaf_list = [Leaf(symbol_list[i]) for i in range(exp_n)]

# get sum of all probabilities (this should theoretically be 1)
total_prob = sum([lib.get_sym_list()[i].get_prob() for i in range(len(lib.get_sym_list()))])
# total_prob = sum([symbol_list[i].get_prob() for i in range(len(symbol_list))])

tree = [Node(tot_prob=total_prob)]

def add_to_tree(root, possible_leafs):
  print("Number of nodes: " + str(len(tree)) + " " + str(len(possible_leafs)) + " leaves remaining with root prob: " + str(root.get_tot_prob()))
  sum=0
  for i in range(len(possible_leafs)):
    sum = sum + possible_leafs[i].get_tot_prob()
    if(sum>=(0.5*root.get_tot_prob())):
      for j in range(i+1):
        possible_leafs[j].get_symbol().add_symbol_suffix('0')
      for j in range(i+1, len(possible_leafs)):
        possible_leafs[j].get_symbol().add_symbol_suffix('1')
      if(i==0): 
        tree.append(possible_leafs[0])
        possible_leafs[0].set_parent(root)
        root.add_child(possible_leafs[0])
      else: 
        tree.append(Node(tot_prob=sum, parent=root))
        root.add_child(tree[-1])
        add_to_tree(tree[-1], possible_leafs[:(i+1)])
      if(len(possible_leafs)==2):
        tree.append(possible_leafs[1])
        possible_leafs[1].set_parent(root)
        root.add_child(possible_leafs[1])
      else:
        tree.append(Node(tot_prob=(root.get_tot_prob()-sum), parent=root))
        add_to_tree(tree[-1], possible_leafs[(i+1):])
        root.add_child(tree[-1])
      break
        
print("Starting tree formation")
add_to_tree(tree[0], leaf_list)
print("Tree formation finished! There are " + str(len(tree)) + " nodes.")        
  
# print symbol library  
# for i in range(exp_n):
  # print(symbol_list[i])
lib.print_sym_list()
  
avg_sym_length = 0  
for i in range(len(lib.get_sym_list())):
  avg_sym_length = avg_sym_length + (len(lib.get_sym_list()[i].get_symbol())*lib.get_sym_list()[i].get_prob()) 
# for i in range(exp_n):
  # avg_sym_length = avg_sym_length + (len(symbol_list[i].get_symbol())*symbol_list[i].get_prob())  
  
print("Average symbol length: " + str(avg_sym_length))

exit()