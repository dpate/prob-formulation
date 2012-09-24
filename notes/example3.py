import networkx as nx
import matplotlib.pyplot as plt
import set_ops as so
import numpy
import pylab

pos=dict()

def cab(DG,s,m,n,w,p,pos):
    #create an anlysis block
    si=s+'i'
    so = s+'o'
    DG.add_node(si)
    DG.add_node(so)
    pos.update({si:numpy.array([p[0]-0.1,p[1]]),
                so:numpy.array([p[0]+0.1,p[1]])})
    DG.add_weighted_edges_from([(si,so,w)])
    DG[si][so]['type'] = 'analysis'
    x = numpy.arange(1,m+1)
    y = numpy.arange(1,n+1)
    for j in x:
        DG.add_node(si+str(j));
        if m>1:
            pos.update({si+str(j):numpy.array([p[0]-0.27,p[1]+0.2-0.4/(m-1)*(j-1)])})
        else:
            pos.update({si+str(j):numpy.array([p[0]-0.27,p[1]])})
        DG.add_weighted_edges_from([(si+str(j),si,0)])
        DG[si+str(j)][si]['type'] = 'in2analysis'
    for j in y:
        DG.add_node(so+str(j));
        if n>1:
            pos.update({so+str(j):numpy.array([p[0]+0.25,p[1]+0.2-0.4/(n-1)*(j-1)])})
        else:
            pos.update({so+str(j):numpy.array([p[0]+0.25,p[1]])})
        DG.add_weighted_edges_from([(so,so+str(j),0)])
        DG[so][so+str(j)]['type'] = 'analysis2out'
    return;

def dict2tree(Gx,DG1,DG2):
    DG2.add_nodes_from(DG1.nodes())
    nds=Gx.keys()
    vls=Gx.values()
    j=0
    for i in nds:
        if len(vls[j])>1:
            nd=vls[j][-2]
            DG2.add_weighted_edges_from([(nd,i,DG1[nd][i]['weight'])])
        j+=1
    return DG2;

# Build the sample graph. Treat x as the root of all inputs without loss of generality.
DG=nx.DiGraph()
DG.add_nodes_from(['x','y1','y2'])
pos.update({'x':numpy.array([1,2]),
            'y1':numpy.array([3,2.5]),
            'y2':numpy.array([3,1.5])})

w=0;
cab(DG,'A',1,1,5,(2,3),pos);
a='x';
b='Ai1';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'
a='Ao1';
b='y1';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'

cab(DG,'B',1,1,6,(2,2),pos)
a='x';
b='Bi1';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'
a='Bo1';
b='y1';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'
a='Bo1';
b='y2';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'

cab(DG,'C',1,1,5,(2,1),pos)
a='x';
b='Ci1';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'
a='Co1';
b='y2';
DG.add_weighted_edges_from([(a,b,w)])
DG[a][b]['type']='out2in'

Gx=nx.single_source_dijkstra_path(DG,'x')


DGdijk=nx.DiGraph()
DGdijk=dict2tree(Gx,DG,DGdijk)

pylab.figure(1)
nx.draw(DG,pos,width=2)
nx.draw_networkx_edges(DGdijk,
                    pos,
                    width=0.5,
                    edge_color='g',
                    style='dotted')
# specifiy edge labels explicitly
edge_labels=dict([((u,v,),d['weight'])
             for u,v,d in DG.edges(data=True)])
nx.draw_networkx_edge_labels(DG,pos,edge_labels=edge_labels)

pylab.show()

##nx.draw_networkx(DG,
##                 pos,
##                 with_labels=True,
##                 width=2)
##
##nx.draw_networkx_edges(DGdijk,
##                    pos,
##                    width=0.5,
##                    edge_color='b')
##
##plt.show()
##    

### Create a graph with the edges reversed
##DGR = nx.DiGraph()
##DGR.add_nodes_from(DG.nodes())
##for i in DG.edges():
##    DGR.add_weighted_edges_from([(i[1],i[0],5)])
##
##nx.draw_networkx(DGR,
##                 pos,
##                 with_labels=True)

#Gx=[nx.single_source_dijkstra_path(DGR,'y1')]

#T = nx.DiGraph()
#T.add_nodes_from(DG.nodes())


#plt.show()

##
###nx.draw_networkx(DG,
###                 pos,
###                 with_labels=True)
###plt.show()
##
### Apply Dijkstra's algorithm starting from x, the input
##Gx=[nx.single_source_dijkstra_path(DG,'x1'),
##    nx.single_source_dijkstra_path(DG,'x2')]
##def make_tree(G,s,T,ii):
##    nds = G.keys()
##    #print 's',s
##    if not(s in nds):
##        return;
##    L = G[s] # L is the shortest path from the start to s
##    preds = []; # this will hold the *i nodes along path L
##    T[ii].add_nodes_from(L) # include the nodes from L
##    for i in L:
##        if len(i) == 2:
##            if i[1]=='i': # Find the nodes that are of the form *i, for example Ai
##                preds = so.union(preds,DG.predecessors(i)) # The predecessors to *i are the inputs that need to be provided
##    #print 'preds',preds
##    if len(preds) > 0:
##        for j in preds:
##            make_tree(G,j,T,ii) # For each input, recursively repeat the process of adding the paths to T
##    return;
##T = [nx.DiGraph(),nx.DiGraph()] # one for each of the x's
##clrs = ['b','g']
##lst = [[],[]]
##for jj in [0,1]:
##    make_tree(Gx[jj],'y1',T,jj) # this will fill T with the nodes from DG that are used in the data flow
##    lst[jj] = T[jj].nodes()
##    lst[jj].sort()
##    for n,nbrs in DG.adjacency_iter():
##        for nbr,eattr in nbrs.items():
##            if (n in lst[jj]) & (nbr in lst[jj]):
##                data=eattr['weight']
##                T[jj].add_weighted_edges_from([(n,nbr,data)])
##    nx.draw_networkx_edges(T[jj],
##                       pos,
##                       with_labels=False,
##                       edge_color=clrs[jj],
##                       width=3)
##    
####    lst = T[jj].nodes()
####    lst.sort()
####    print lst
####    
####
##### Include the edges that are used in the dataflow and total their weight
####t=0
####for n,nbrs in DG.adjacency_iter():
####    for nbr,eattr in nbrs.items():
####        if (n in lst) & (nbr in lst):
####            data=eattr['weight']
####            T[0].add_weighted_edges_from([(n,nbr,data)])
####            t=t+data
####
####print 'dataflow length',t
##
##
##
####nx.draw_networkx_edges(T[0],
####                       pos,
####                       with_labels=False,
####                       edge_color='b',
####                       width=3)
##plt.show()
