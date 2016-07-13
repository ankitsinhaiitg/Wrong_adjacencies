from bg import graphviz  # bg --> https://github.com/aganezov/bg/tree/development/bg
from bg import grimm
from os.path import isfile, join
from os import listdir
import  os
import get_wrong_adjacencies

def test_dot_graph(simulated_dir,MGRA_result_dir,result_dir):

    simulated = simulated_dir + "/simul"
    result = MGRA_result_dir + "/MGRA/genomes"
    res11 = result_dir + "/wrong_adjacencies.txt"
    onlyfiles = [f for f in listdir(result) if isfile(join(result, f))]
    resultfile = []
    for file in onlyfiles:
        if file[len(file) - 3:] == "gen":
            resultfile.append(file)
    simfile = [f for f in listdir(simulated) if isfile(join(simulated, f))]
    wrongedgefile = open(res11, "w")
    for f in resultfile:
        for j in simfile:
            if f.split(".")[0] == j.split(".")[0] :
                x = get_wrong_adjacencies.get_wrong_adjacencies(simulated + "/" + j, result + "/" + f)#, dic[f.split(".")[0]])
                if x:
                    wrongedgefile.write("\n".join(x) + "\n")
    wrongedgefile.close()
    wrong_adjacencies_dot_graph(MGRA_result_dir,result_dir)

####################################################################################################################
def wrong_adjacencies_dot_graph(MGRA_result_dir,result_dir):
    res11 = result_dir+"/wrong_adjacencies.txt"
    res121 = result_dir+"/wrong_adjacencies.dot"
    blocks = open(MGRA_result_dir + "/MGRA/blocks.txt", "r")

    graph = grimm.GRIMMReader.get_breakpoint_graph(blocks)
    one = graphviz.BreakpointGraphProcessor()
    bp_genome = one.export_graph_as_dot(graph)

    bp_genome=get_wrong_adjacencies.modified_dot_file(bp_genome)


    edges = bp_genome[1].split("\n")
    vertex = bp_genome[2].split("\n")

    def get_edge(edges):
        edge_list = []
        for ed in edges:
            edge_dict = ed.split(" ")
            edge_list.append([edge_dict[0].split("\"")[1], edge_dict[2].split("\"")[1]])
        return edge_list
    edge_list = get_edge(edges)
    def get_vertices(vertices_dict):
        vertices_dict1 = {}
        for i in range(len(vertices_dict)):
            vertices_dict1[vertices_dict[i].split()[0].split("\"")[1]] = vertices_dict[i].split()[1].split("\"")[1]
        return vertices_dict1
    vertex_dict = get_vertices(vertex)
    bettergraph = []
    point,p = [],[]
    for ed in edges:
        if vertex_dict[ed.split(" ")[0].strip("\"")] != 'point':
            first = vertex_dict[ed.split(" ")[0].strip("\"")]
        else:
            first = ed.split(" ")[0].strip("\"")
        if vertex_dict[ed.split(" ")[2].strip("\"")] != "point":
            second = vertex_dict[ed.split(" ")[2].strip("\"")]
        else:
            second = ed.split(" ")[2].strip("\"")
        bettergraph.append(
            "\"" + first + "\" " + ed.split(" ")[1] + " \"" + second + "\" " + " ".join(ed.split(" ")[3:]))
    for key in vertex_dict:
        if vertex_dict[key] == "point":
            point.append(vertex[int(key) - 1])
            p.append(key)

    wrong = []
    with open(res11, "r") as wrong_file:
        for i in wrong_file:
            i = i.strip("\n").split("\t")
            wrong.append(i)
    if not wrong:
        print(" 100% accuracy")
        os.remove(res11)
        return 0
    finalgraph = []
    newpoint=[]
    for w in wrong:
        for b in bettergraph:
            if b.split(" ")[0].split("\"")[1] in w[0:2]:
                finalgraph.append(b)
                if b.split(" ")[2].split("\"")[1] in p:
                    k=b.split(" ")[2].split("\"")[1]
                    newpoint.append(vertex[int(k) - 1])
            if b.split(" ")[2].split("\"")[1] in w[0:2]:
                finalgraph.append(b)
                if b.split(" ")[0].split("\"")[1] in p:
                    k=b.split(" ")[0].split("\"")[1]
                    newpoint.append(vertex[int(k) - 1])
    finalgraph = list(set(finalgraph))
    wrongedge,wrongpoint = [],[]
    num = 0;
    for w in wrong:
        if "point" not in w:
            wrongedge.append(
                "\"" + w[0] + "\" -- \"" + w[1] + "\" [color=\"black\", style=\"dotted\", penwidth=\"2\"];")
        else:
            if w[0] == "point":
                w[0] = str(num) + "_"
                wrongedge.append(
                    "\"" + w[0] + "\" -- \"" + w[1] + "\" [color=\"black\", style=\"dotted\", penwidth=\"2\"];")
                wrongpoint.append(" \"" + w[0] + "\" [shape=\"point\", penwidth=\"1\"];")
                num += 1
            elif w[1] == "point":
                w[1] = str(num) + "_"
                wrongedge.append(
                    "\"" + w[0] + "\" -- \"" + w[1] + "\" [color=\"black\", style=\"dotted\", penwidth=\"2\"];")
                wrongpoint.append(" \"" + w[1] + "\" [shape=\"point\", penwidth=\"1\"];")
                num += 1
    finaldotgraph = "graph{\nrankdir=LR;\n" + "\n".join(finalgraph) + "\n" + "\n".join(wrongedge) + "\n" +"\n".join(wrongpoint)+"\n"+ "\n".join(newpoint) + "\n}"
    with open(res121, "w") as gen:
        gen.write(finaldotgraph)
    os.system("dot -Tpng:quartz:quartz -O " + res121)

