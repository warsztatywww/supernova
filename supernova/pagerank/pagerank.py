from websites import models
import subprocess
from django.db import transaction

domain_name_dict={}
domain_links={}
domain_pageranks={}

c=0
l=0

for domain in models.Domain.objects.all():
  domain_name_dict[domain.name]=domain.pk
  domain_links[domain.name]=[]
  domain_pageranks[domain.name]=domain.pagerank
  c+=1

for link in models.Link.objects.all():
  domain_links[link.start.domain.name].append(link.end.domain.name)
  l+=1

s=str(c)+" "+str(l)+"\n"+\
"\n".join(
          str(domain_name_dict[domain])+" "+\
          str(domain_pageranks[domain])+" "+\
          str(len(domain_links[domain]))+" "+\
          " ".join(str(domain_name_dict[link]) for link in domain_links[domain])
          for domain in domain_name_dict)

task=subprocess.Popen(["./iterate_pagerank"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = task.communicate(input=bytes(s, "utf-8"))

l=list(map(lambda x: (int(x[0]), float(x[1])), (e.split(" ") for e in out.split("\n") if e)))

@transaction.commit_manually
def commit_pageranks (ranks):
  for id, pagerank in ranks:
    with models.Domain.objects.get(pk=id) as domain:
      domain.pagerank=pagerank
      domain.save()
  transaction.commit()

commit_pageranks(l)
