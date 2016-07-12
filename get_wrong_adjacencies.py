from bg import graphviz       # bg --> https://github.com/aganezov/bg/tree/development/bg
from bg import grimm

## Calculates the wrong adjacencies between simulated ancestral genomes and MGRA constructed ancestral genome.
def modified_dot_file(bp_genome):
    genome=bp_genome[0].split("\n")
    one, two = [], []
    for gen in genome:
        if "--" in gen.split(" "):
            one.append(gen)
        elif "graph" not in gen.split(" ") and "}" not in gen.split(" "):
            two.append(gen)
    res_gen=[]
    res_gen.append(bp_genome[0])
    res_gen.append("\n".join(one))
    res_gen.append("\n".join(two))
    return res_gen
def get_wrong_adjacencies(dir_path,r):              #dir_part -> path of simulated ancestor ,, r -> path of constructed ancestor.
    file = open(dir_path, "r")
    file_res = open(r, "r")
    graph = grimm.GRIMMReader.get_breakpoint_graph(file)
    graph_res = grimm.GRIMMReader.get_breakpoint_graph(file_res)
    one = graphviz.BreakpointGraphProcessor()
    one_res = graphviz.BreakpointGraphProcessor()
    now = one.export_graph_as_dot(graph)
    now_res = one_res.export_graph_as_dot(graph_res)
    now=modified_dot_file(now)
    now_res=modified_dot_file(now_res)
    file_res.close()
    file.close()
    edges = now[1].split("\n")
    edges_res = now_res[1].split("\n")

    def get_edge(edges):
        edge_list = []
        for ed in edges:
            edge_dict = ed.split(" ")
            edge_list.append([edge_dict[0].split("\"")[1], edge_dict[2].split("\"")[1]])
        return edge_list

    edge_list = get_edge(edges)
    edge_list_res = get_edge(edges_res)
    vertices_dict = now[2].split("\n")
    vertices_dict_res = now_res[2].split("\n")

    def get_vertices(vertices_dict):
        vertices_dict1 = {}
        for i in range(len(vertices_dict)):
            vertices_dict1[vertices_dict[i].split()[0].split("\"")[1]] = vertices_dict[i].split()[1].split("\"")[1]
        return vertices_dict1

    ver_dict = get_vertices(vertices_dict)
    ver_dict_res = get_vertices(vertices_dict_res)

    def edge_vert(edge_list, ver_dict):
        edge_list_up = []
        for edge in range(len(edge_list)):
            temp = [ver_dict[edge_list[edge][0]], ver_dict[edge_list[edge][1]]]
            edge_list_up.append(set(temp))
        return edge_list_up

    edge_list_up = edge_vert(edge_list, ver_dict)
    edge_list_up_res = edge_vert(edge_list_res, ver_dict_res)
    wrongedge=[]
    for edge in edge_list_up_res:
            if edge in edge_list_up:
                edge=list(edge)
            else:
                edge=list(edge)
                wrongedge.append("\t".join(edge))
    return wrongedge
