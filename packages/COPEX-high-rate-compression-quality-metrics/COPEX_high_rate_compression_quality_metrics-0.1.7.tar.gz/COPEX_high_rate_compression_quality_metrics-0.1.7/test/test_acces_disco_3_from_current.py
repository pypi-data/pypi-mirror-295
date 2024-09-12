#\\disco3\Users\COPEX_DCC\Benchmark\S2_L1C
import os
import COPEX_high_rate_compression_quality_metrics.json_builder as COPEX_json_builder

network_path = r"\\disco3\Users\COPEX_DCC\Benchmark" #os.path.join("\\disco3","Users","COPEX_DCC","Benchmark",)
working_dir_abspath = os.path.abspath(network_path)
print("dir abspath = ",working_dir_abspath)
dataset_name = "S2_L1C" # str
test_case_number = 1 #int qui sera remis sur 3 digit automatiquement, ou str sur 3 digit, définit le test case ou l'on souhaite faire le benshmark
nnvvppp_algoname = "01-01-001_JJ2000_x50"
COPEX_json_builder.make_generic(root_directory=working_dir_abspath, dataset_name=dataset_name,test_case_number=test_case_number,nnvvppp_algoname=nnvvppp_algoname)


