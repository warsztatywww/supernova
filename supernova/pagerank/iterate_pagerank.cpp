#include <cstdio>
#include <vector>
#include <algorithm>

using namespace std;

const int N=1000*1000;  //max node number, be careful with more than 1e7
const int IT=100;        //iteration count
const float D=0.85;     //pagerank supression factor

vector<int>gr[N];
int node_nums[N];
float old_rank[N];
float tmp_rank[N];

int main ()
{
  int n, m;
  scanf("%d%d", &n, &m);
  for (int i=0; i<n; i++)
  {
    int w, k, a;
    float f;
    scanf("%d%f%d", &w, &f, &k);
    old_rank[w]=f;
    node_nums[i]=w;
    gr[w].reserve(k);
    for (int j=0; j<k; j++)
    {
      scanf("%d", &a);
      gr[w].push_back(a);
    }
  }
  
  for (int i=0; i<IT; i++)
  {
    for (int j=0; j<n; j++)
    {
      int w=node_nums[j];
      tmp_rank[w]=(1-D)/float(n);
    }
    for (int j=0; j<n; j++)
    {
      int w=node_nums[j];
      for (int e : gr[w])
        tmp_rank[e]+=(D*old_rank[w])/float(gr[w].size());
    }
    swap(old_rank, tmp_rank);
  }
  
  for (int i=0; i<n; i++)
    printf("%d %f\n", node_nums[i], old_rank[node_nums[i]]);
}
