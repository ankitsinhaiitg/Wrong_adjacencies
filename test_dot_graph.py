from wrong_adjacencies_dot_graph import run_dot_graph
import os

'''
list1=["6","9","12","15"]
list2=["200","300","400"]
list3=["100","200"]
for v1 in list1:
    for v2 in list2:
        for v3 in list3:
            for i in range(1,11):
                text = v1 + "_" + v2 + "_" + v3 + "_0" + "/" + str(i)
                text4=v1 + "_" + v2 + "_" + v3 + "_0"
                if text4!="12_200_200_0" and text4!="15_200_200_0":
                    sim_dir = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text + "/simul" # Location of simulated ancestral genome files
                    mgra_result = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text + "/MGRA/genomes" # Location of constructed ancestral genome file
                    res = "/Users/crandalllab/Ankit/data_wrong_adjacencies/" + v1 + "_" + v2 + "_" + v3 + "_0/"# Output file location
                    block = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text + "/MGRA/blocks.txt"
                    new_res=res + str(i)
                    if not os.path.exists(res):
                        os.mkdir(res)
                    if not os.path.exists(new_res):
                        os.mkdir(new_res)
                    run_dot_graph(sim_dir, mgra_result, new_res,block)
'''
text="6_200_100_0/1"
sim_dir = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text + "/simul"          # Location of simulated ancestral genome files
mgra_result = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text + "/MGRA/genomes"       # Location of constructed ancestral genome file
res = "/Users/crandalllab/Ankit/data_wrong_adjacencies/" + text                                 # Output file location
block = "/Users/crandalllab/Ankit/mgra-gos-asm2copy/only_reareg_5chr/" + text + "/MGRA/blocks.txt"
run_dot_graph(sim_dir,mgra_result,res,block)

