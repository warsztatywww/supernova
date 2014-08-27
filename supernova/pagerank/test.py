#!/usr/bin/env python3

from testgraph_generator import Generator
import subprocess

g1=Generator(1000,10)
g2=Generator(1000,100)

def run_pagerank (data):
  task=subprocess.Popen(["./iterate_pagerank"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = task.communicate(input=bytes(data, "utf-8"))
  return sum(float(e.split()[1]) for e in out.decode().split("\n") if e)

print(run_pagerank(g1.generate_text()))
print(run_pagerank(g2.generate_text()))
