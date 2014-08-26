import random
import math

class Generator:
  def __init__ (self, nodes):
    self.__node_num=random.randint(1,nodes)
    self.__max_links=min(10,5*int(math.log2(self.__node_num)))
  def generate (self):
    node_dict={}
    for i in range(1,self.__node_num+1):
      node_dict[i]=[1, [random.randint(1,self.__node_num) for j in range(random.randint(0,self.__max_links))]]
    return node_dict
  def generate_text (self):
    d=self.generate()
    t=str(self.__node_num)+"\n"+\
    "\n".join(
              str(e)+" "+\
              str(d[e][0])+" "+\
              str(len(d[e][1]))+" "+\
              " ".join(str(x) for x in d[e][1])
              for e in d)
    return t
