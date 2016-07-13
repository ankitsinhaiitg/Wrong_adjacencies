from wrong_adjacencies_dot_graph import test_dot_graph
'''
list1=["12","15"]
list2=["200","300","400"]
list3=["100","200"]
for v1 in list1:
    for v2 in list2:
        for v3 in list3:
            for i in range(1,11):
                text = v1 + "_" + v2 + "_" + v3 + "_0" + "/" + str(i)
                text4=v1 + "_" + v2 + "_" + v3 + "_0"
                text11= v1 + "_" + v2 + "_" + v3 + "_0" + "_" + str(i)
                if text4!="12_200_200_0" and text4!="15_200_200_0":
                    test_dot_graph(text, text11)

'''
text="6_200_100_0/1"
sim_dir = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text           # Location of simulated ancestral genome files
mgra_result = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text       # Location of constructed ancestral genome file
res = "/Users/crandalllab/Ankit/wrongadjacencies"                                        # Output file location

test_dot_graph(sim_dir,mgra_result,res)

