import prefix_code_gen as prefix

def ascii_to_int(char):
  return int.from_bytes(char.encode(), 'big')
  
def int_to_bin_str(integer):
  return format(integer, '08b')

def ascii_to_bin_str(char):
  return format(ascii_to_int(char),'08b')

def compress_file(prefix_dict, readfile, compfile):
  with open(readfile, mode='r') as file, open(compfile, mode='w') as compress:
    x = file.read(1)
    x_bin = ascii_to_bin_str(x)
    x_int = ascii_to_int(x)
    char_cnt = 8
    string = prefix_dict["state"] + x_bin[0:6]
    sym_cnt = len(string)
    compress.write(string)
    prev_x_int = x_int
    while(True):
      x = file.read(1)
      if(x == ''): break
      x_bin = ascii_to_bin_str(x)
      x_int = ascii_to_int(x)
      # print(x + ' : ' + x_bin)
      diff = int_to_bin_str(x_int ^ prev_x_int)
      print(int_to_bin_str(x_int) + ' ' + int_to_bin_str(prev_x_int) + ' ' + diff)
      symbol = prefix_dict[diff[0:6]]
      compress.write(' '+symbol)
      prev_x_int = x_int
      char_cnt += 8
      sym_cnt += len(symbol)
  print("Character count: " + str(char_cnt))
  print("Symbol count: " + str(sym_cnt))

def main():
  lib = prefix.SymbolLibrary(6, no_change_prob=0.01,\
    additional_symbols=[prefix.Symbol("state", prob=0.01)])
  print(lib)
  prefix_dict = lib.get_sym_dict()
  compress_file(prefix_dict,\
    "C:/Users/jeswi/Documents/Logic Analyzer/logic_analyzer/test.txt",\
    "C:/Users/jeswi/Documents/Logic Analyzer/logic_analyzer/comp.txt")
  
if(__name__ =='__main__'):
  main()