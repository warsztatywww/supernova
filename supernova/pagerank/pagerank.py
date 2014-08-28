from websites import models
import subprocess
from supernova.settings import BASE_DIR

def perform_pagerank_update ():
  domain_pk_dict={} #debug
  domain_links={}
  domain_pageranks={}

  c=0
  l=0

  for domain in models.Domain.objects.all():
    domain_pk_dict[domain.pk]=domain.name
    domain_links[domain.pk]=[]
    domain_pageranks[domain.pk]=domain.pagerank
    c+=1

  for link in models.Link.objects.all():
    domain_links[link.start.domain.pk].append(link.end.domain.pk)
    l+=1

  s=str(c)+" "+str(l)+"\n"+\
  "\n".join(
            str(domainpk)+" "+\
            str(domain_pageranks[domainpk])+" "+\
            str(len(domain_links[domainpk]))+" "+\
            " ".join(str(link) for link in domain_links[domainpk])
            for domainpk in domain_pk_dict)

  print(s)              #debug
  print(domain_pk_dict) #debug

  task=subprocess.Popen([BASE_DIR+"/pagerank/iterate_pagerank"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = task.communicate(input=bytes(s, "utf-8"))

  l=list(map(lambda x: (int(x[0]), float(x[1])), (e.split(" ") for e in out.decode("utf-8").split("\n") if e)))

  def commit_pageranks (ranks):
    for pk, pagerank in ranks:
      print(pk, pagerank)
      domain=models.Domain.objects.get(pk=pk)
      domain.pagerank=pagerank
      domain.save()

  commit_pageranks(l)
