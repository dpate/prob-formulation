import networkx as nx
import matplotlib.pyplot as plt
import numpy
import pylab
import itertools
import random

random.seed(10)

def cab(DG,s,m,n,w,p,pos):
    # this function creates the nodes and edges associated with an analysis block
    # sample input: cab(DG,'A',1,1,5,(2,3),pos);
    # DG = given directed graph
    # s = name of analysis block
    # m = number of local inputs
    # n = number of local outputs
    # w = cost of analysis
    # p = position for plotting
    # pos = dictionary for plotting
    #DG.graph['analyses'].append(s)
    local_inputs = []
    local_outputs = []
    si=s+'i'
    so = s+'o'
    DG.add_node(si,type='analysis_start',analysis_block=s)
    DG.add_node(so,type='analysis_finish',analysis_block=s)
    pos.update({si:numpy.array([p[0]-0.1,p[1]]),
                so:numpy.array([p[0]+0.1,p[1]]),
                s:numpy.array([p[0],p[1]])})
    DG.add_weighted_edges_from([(si,so,w)],type='analysis')
    x = numpy.arange(1,m+1) # local inputs
    y = numpy.arange(1,n+1) # local outputs
    for j in x:
        DG.add_node(si+str(j),type='local_input',analysis_block=s);
        local_inputs.append(si+str(j))
        if m>1:
            pos.update({si+str(j):numpy.array([p[0]-0.27,p[1]+0.2-0.4/(m-1)*(j-1)])})
        else:
            pos.update({si+str(j):numpy.array([p[0]-0.27,p[1]])})
        DG.add_weighted_edges_from([(si+str(j),si,0)],type='in')
    for j in y:
        DG.add_node(so+str(j),type='local_output',analysis_block=s);
        local_outputs.append(so+str(j))
        if n>1:
            pos.update({so+str(j):numpy.array([p[0]+0.25,p[1]+0.2-0.4/(n-1)*(j-1)])})
        else:
            pos.update({so+str(j):numpy.array([p[0]+0.25,p[1]])})
        DG.add_weighted_edges_from([(so,so+str(j),0)],type='out')
    nodes = {'local_inputs':local_inputs,'analysis_start':[si],'analysis_finish':[so],'local_outputs':local_outputs}
    DG.graph['analyses'][s]=nodes
    return;

def create_sample_graph():
    # Build the sample graph. Treat x as the root of all inputs without loss of generality.
    pos=dict() # for plotting

    w=0;
    DG=nx.DiGraph(type='maximal_connectivity',analyses=dict())
    DG.add_nodes_from(['x'],type='global_input',analysis_block='')
    DG.add_nodes_from(['y1','y2','y3','y4'],type='global_output',analysis_block='')
    pos.update({'x':numpy.array([1,2.5]),
                'y1':numpy.array([5,4]),
                'y2':numpy.array([5,3]),
                'y3':numpy.array([5,2]),
                'y4':numpy.array([5,1]),
                'y':numpy.array([6,3])})

    a = [];
    b = [];
    cab(DG,'A',2,2,1,(2,4),pos);
    a.append('x');  b.append('Ai1');
    a.append('Ao1');b.append('Ei1');
    a.append('Ao1');b.append('Fi1');
    a.append('Ao2');b.append('Ei2');

    cab(DG,'B',1,2,1,(2,3),pos)
    a.append('x');  b.append('Bi1');
    a.append('Bo1');b.append('Fi2');
    a.append('Bo2');b.append('Gi1');

    cab(DG,'C',1,1,1,(2,2),pos)
    a.append('x');  b.append('Ci1');
    a.append('Co1');b.append('Gi1');
    a.append('Co1');b.append('Hi1');
    a.append('Co1');b.append('Ai2');

    cab(DG,'D',3,1,1,(2,1),pos)
    a.append('x');  b.append('Di1');
    a.append('Do1');b.append('Gi2');
    a.append('Do1');b.append('Hi2');

    cab(DG,'E',2,2,1,(3,4),pos)
    a.append('Eo1');b.append('Ii1');
    a.append('Eo2');b.append('Ji1');

    cab(DG,'F',2,3,1,(3,3),pos)
    a.append('Fo1');b.append('Ii2');
    a.append('Fo1');b.append('Ji1');
    a.append('Fo1');b.append('Ki1');

    cab(DG,'G',2,2,1,(3,2),pos)
    a.append('Go1');b.append('Ji1');
    a.append('Go1');b.append('Li1');

    cab(DG,'H',2,3,1,(3,1),pos)
    a.append('Ho1');b.append('Li2');
    a.append('Ho1');b.append('Ki1');

    cab(DG,'I',2,2,1,(4,4),pos)
    a.append('Io1');b.append('y1');

    cab(DG,'J',3,1,1,(4,3),pos)
    a.append('Jo1');b.append('y2');

    cab(DG,'K',3,2,1,(4,2),pos)
    a.append('Ko1');b.append('y3');

    cab(DG,'L',2,2,1,(4,1),pos)
    a.append('Lo1');b.append('y3');
    a.append('Lo2');b.append('y4');
    j=0;
    for i in a:
        DG.add_edge(i,b[j],weight=0,type='connection',fixed=False,rank=random.randint(1,10));
        j+=1;
    
    # add a few more connections
    DG.add_weighted_edges_from([('Io2','Ai2',w),
        ('Ao1','Hi1',w),
        ('Fo2','Gi2',w),
        ('Ko2','y1',w),
        ('Ho3','Di3',w),
        ('Fo3','Di2',w),
        ('Io2','Ki2',w),
        ('Ho2','y2',w),
        ('Do1','Ji2',w)],
        type='connection',fixed=True,rank=1)
    return[DG,pos];

def remove_node(DG,i):
    analysis = DG.node[i]['analysis_block']
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['local_inputs'])
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['local_outputs'])
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['analysis_start'])
    DG.remove_nodes_from(DG.graph['analyses'][analysis]['analysis_finish'])
    del DG.graph['analyses'][analysis]
    return DG;

def resolve_conflict(edgs,DG):
    #print len(edgs)
    print "Conflicted edges:",edgs
    # We must determine which of the edges to choose from are fixed
    fxd = [];
    nfxd = 0;
    for edg in edgs:
        check = DG.edge[edg[0]][edg[1]]['fixed']
        fxd.append(check);
        if check==True:
            nfxd=nfxd+1;
        #print 'nfxd',nfxd
    if nfxd>1:
        print '  More than one edge at node',edg[1],'is fixed'
        quit()
    elif nfxd==1:
        chosen_edge = edgs[fxd.index(True)] # choose the edge that is not fixed
        print '  Edge',edg,'is fixed'
    else:
        # ---- A decision only needs to be made when none of the edges are fixed ----
        choice = 'user';
        if choice=='rank':
            rnk = [];
            for edg in edgs:
                rnk.append(DG.edge[edg[0]][edg[1]]['rank'])
            hghst = max(rnk);
            chosen_edge = edgs[rnk.index(hghst)];
        elif choice=='random':
            chosen_edge = edgs[0]; # "randomly" choose the first element
        elif choice=='user':
            print "Please enter the index of the connection to resolve the conflict: "
            inp_int = int(raw_input())
            chosen_edge = edgs[inp_int];
        elif choice=='metric':
            print 'metric'
        else:
            print 'Invalid choice for conflict resolution'
            quit()
    print '  Edge',chosen_edge,'was chosen'
    edgs.remove(chosen_edge)
    DG.remove_edges_from(edgs) # Remove all the edges except for the one that was selected
    
def obtain_fpf(maxDG):
    DG = maxDG.copy()
    
    # -- find and remove any holes (must iterate)
    check = True
    while check:
        nodes = DG.nodes()
        holes = []
        for i in nodes:
            if DG.node[i]['type']=='local_input':
                ins = DG.in_edges(i)
                if len(ins)==0:
                    holes.append(i)
        if len(holes)==0:
            check = False
        for i in holes:
            print 'Removed node',i
            DG = remove_node(DG,i)
    
    # -- find and remove any conflicts
    nodes = DG.nodes()
    for i in nodes:
        if (DG.node[i]['type']=='local_input') | (DG.node[i]['type']=='global_output'):
            ins = DG.in_edges(i)
            if len(ins)>1:
                resolve_conflict(ins,DG)
    
    # -- delete any analyses with no used inputs (must iterate)
    check = True
    while check:
        extraneous = []
        analyses = DG.graph['analyses']
        for i in analyses:
            outs = analyses[i]['local_outputs']
            j = 0
            for k in outs:
                j = j+len(DG.successors(k))
            if j==0:
                extraneous.append(k)
        if len(extraneous)==0:
            check = False
        for k in extraneous:
            DG = remove_node(DG,k)
    return DG;

def extract_simple_graph(DG):
    SG = nx.DiGraph()

    # add nodes
    nodes = DG.nodes()
    for i in nodes:
        if DG.node[i]['type']=='global_input':
            SG.add_node(i,type='global_input')
        if DG.node[i]['type']=='global_output':
            SG.add_node(i,type='global_output')
        if DG.node[i]['type']=='analysis_start':
            node = DG.node[i]['analysis_block']
            SG.add_node(node,type='analysis_block')
    
    # add edges
    edges = DG.edges()
    for i in edges:
        if DG.edge[i[0]][i[1]]['type']=='connection':
            type1 = DG.node[i[0]]['type']
            type2 = DG.node[i[1]]['type']
            if type1=='local_output':
                node1 = DG.node[i[0]]['analysis_block']
            else:
                node1 = i[0]
            if type2=='local_input':
                node2 = DG.node[i[1]]['analysis_block']
            else:
                node2 = i[1]
            SG.add_edge(node1,node2)
    return SG;

def find_cycles(DG):
    CG = nx.DiGraph()
    CG.add_nodes_from(DG.nodes())
    cycles = nx.simple_cycles(DG)
    for i in cycles:
        L = range(0,len(i)-1)
        for j in L:
            CG.add_edge(i[j],i[j+1])
    return [CG,cycles];

out = create_sample_graph()
maxDG = out[0]
pos = out[1]

FPF = obtain_fpf(maxDG)

SG = extract_simple_graph(maxDG)

out = find_cycles(SG) 
CGSG = out[0]
cyclesSG = out[1]
print cyclesSG
print CGSG.edges()

out = find_cycles(FPF) 
CG = out[0]
cycles = out[1]
#print len(cycles)
#print cycles
#print FPF.edge['Co1']['Gi1']

pylab.figure(1)
#nx.draw(maxDG,pos,width=3)
#nx.draw(FPF,pos,width=1.5,edge_color='b')
#nx.draw_networkx_edges(CG,pos,width=0.75,edge_color='y')
nx.draw(SG,pos,width=2)
#nx.draw_networkx_edges(FPF,pos,width=1.25,edge_color='b')
nx.draw_networkx_edges(CGSG,pos,width=0.75,edge_color='y')

pylab.figure(2)
nx.draw(maxDG,pos,width = 0.5)

pylab.show()