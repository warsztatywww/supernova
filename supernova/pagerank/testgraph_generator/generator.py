import random
import math

class Generator:
  def __init__ (self, nodes, edges):
    self.__node_num=nodes
    self.__max_links=edges
  def generate (self):
    node_dict={}
    for i in range(1,self.__node_num+1):
      node_dict[i]=[1, [random.randint(1,self.__node_num) for j in range(random.randint(0,self.__max_links))]]
    return node_dict
  def generate_text (self):
    d=self.generate()
    l=sum(len(d[e][1]) for e in d)
    t=str(self.__node_num)+" "+str(l)+"\n"+\
    "\n".join(
              str(e)+" "+\
              str(d[e][0])+" "+\
              str(len(d[e][1]))+" "+\
              " ".join(str(x) for x in d[e][1])
              for e in d)
    return t

"""
nodes_num
for each node:
  node_id, pagerank, links_num, {link for link in links}

{node:[pagerank, [link for link in links]]}
"""
