import os
import sys

# Ajoute le dossier 'COPEX_high_rate_compression_quality_metrics' au chemin de recherche des modules, pour pouvoir acceder a tout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import COPEX_high_rate_compression_quality_metrics.utils as utls

dataset_name = os.path.join("data", "RANDOM")
test_case_number = 4
nnvvppp_algoname = "01-01-002_JPEG2000"
result_path = utls.get_algorithm_results_full_path(dataset_name=dataset_name, test_case_number=test_case_number,
                                                   nnvvppp_algoname=nnvvppp_algoname)
original_path = utls.get_original_full_path(dataset_name=dataset_name,test_case_number=test_case_number)
print("\nresult_path = [",result_path,"}")
print("original_path = [",original_path,"}")
result_products = utls.get_product_path_list_from_path(path=result_path)
original_products = utls.get_product_path_list_from_path(path=original_path)
print("\nresult products = [",result_products,"}")
print("original products = [",original_products,"}")