from bg import graphviz  # bg --> https://github.com/aganezov/bg/tree/development/bg
from bg import grimm
from os.path import isfile, join
from os import listdir
import os
import get_wrong_adjacencies
import logging


def run_dot_graph(simulated, result, result_dir, block):
    # Opens the pair of ancestral files and gets wrong adjacencies and then runs wrong_adjacencies_dot_graph.
    res11 = result_dir + "/wrong_adjacencies.txt"
    onlyfiles = [f for f in listdir(result) if isfile(join(result, f))]
    resultfile = []
    for file in onlyfiles:
        if file[len(file) - 4:] == "gen":
            resultfile.append(file)
    simfile = [f for f in listdir(simulated) if isfile(join(simulated, f))]
    if not simfile:
        logging.warning("NO SIMULATED FILES FOUND")
        return
    if not resultfile:
        logging.warning("NO RESULT FILES FOUND")
        return
    wrongedgefile = open(res11, "w")
    flag = 0
    for f in resultfile:
        for j in simfile:
            if f.split(".")[0] == j.split(".")[0]:
                flag = 1
                x = get_wrong_adjacencies.get_wrong_adjacencies(simulated + "/" + j, result + "/" + f)
                if x:
                    wrongedgefile.write("\n".join(x) + "\n")
    wrongedgefile.close()
    if not flag:
        logging.warning("NO MATCHING PAIR OF ANCESTRAL AND SIMULATED GENOMES FOUND")
        return 
    wrong_adjacencies_dot_graph(block, result_dir)


def get_edge(edges):
    # Returns the edges list.
    edge_list = []
    for ed in edges:
        edge_dict = ed.split(" ")
        edge_list.append([edge_dict[0].split("\"")[1], edge_dict[2].split("\"")[1]])
    return edge_list


def get_vertices(vertices_dict):
    # Returns dictionary of vertices.
    vertices_dict1 = {}
    for i in range(len(vertices_dict)):
        vertices_dict1[vertices_dict[i].split()[0].split("\"")[1]] = vertices_dict[i].split()[1].split("\"")[1]
    return vertices_dict1


def get_wrong_edges(res11):
    # Returns the wrong adjacencies.
    wrong = []
    with open(res11, "r") as wrong_file:
        for i in wrong_file:
            i = i.strip("\n").split("\t")
            wrong.append(i)
    return wrong


def is_accurate_result(wrong, res11):
    # Checks if there is 100% accuracy between the ancestral and constructed genomes.
    if not wrong:
        print("Result has 100% accuracy.")
        os.remove(res11)
        return 0


def genome_edge_processor(wrong, bettergraph, vertex, p):
    # Finds the edges of genome in depth 1 of the wrong edges.
    finalgraph, newpoint = [], []
    for w in wrong:
        for b in bettergraph:
            if b.split(" ")[0].split("\"")[1] in w[0:2]:
                finalgraph.append(b)
                if b.split(" ")[2].split("\"")[1] in p:
                    k = b.split(" ")[2].split("\"")[1]
                    newpoint.append(vertex[int(k) - 1])
            if b.split(" ")[2].split("\"")[1] in w[0:2]:
                finalgraph.append(b)
                if b.split(" ")[0].split("\"")[1] in p:
                    k = b.split(" ")[0].split("\"")[1]
                    newpoint.append(vertex[int(k) - 1])
    return [finalgraph, newpoint]


def wrong_edge_processor(wrong):
    # Processes the wrong edges and return.
    num = 0
    wrongedge, wrongpoint = [], []
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
    return [wrongedge, wrongpoint]


def wrong_adjacencies_dot_graph(block, result_dir):
    # Outputs dot graph file and also in png format of wrong adjacencies.
    res11 = result_dir + "/wrong_adjacencies.txt"
    res121 = result_dir + "/wrong_adjacencies.dot"
    blocks = open(block, "r")
    graph = grimm.GRIMMReader.get_breakpoint_graph(blocks)
    one = graphviz.BreakpointGraphProcessor()
    bp_genome = one.export_graph_as_dot(graph)
    bp_genome = get_wrong_adjacencies.modified_dot_file(bp_genome)
    edges = bp_genome[1].split("\n")
    vertex = bp_genome[2].split("\n")
    edge_list = get_edge(edges)
    vertex_dict = get_vertices(vertex)
    bettergraph, point, p = [], [], []
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
    wrong = get_wrong_edges(res11)
    is_accurate_result(wrong, res11)
    r1 = genome_edge_processor(wrong, bettergraph, vertex, p)
    finalgraph, newpoint = r1[0], r1[1]
    finalgraph = list(set(finalgraph))
    r2 = wrong_edge_processor(wrong)
    wrongedge, wrongpoint = r2[0], r2[1]
    finaldotgraph = "graph{\nrankdir=LR;\n" + "\n".join(finalgraph) + "\n" + "\n".join(wrongedge) + "\n" + "\n".join(
        wrongpoint) + "\n" + "\n".join(newpoint) + "\n}"
    with open(res121, "w") as gen:
        gen.write(finaldotgraph)
    os.system("dot -Tpng:quartz:quartz -O " + res121)
