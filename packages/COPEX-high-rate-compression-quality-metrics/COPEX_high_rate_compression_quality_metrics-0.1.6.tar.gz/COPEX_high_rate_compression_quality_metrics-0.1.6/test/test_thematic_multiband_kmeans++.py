import numpy as np
from skimage import io
import os
import sys
import time

# Ajoute le dossier 'COPEX_high_rate_compression_quality_metrics' au chemin de recherche des modules, pour pouvoir acceder a tout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import COPEX_high_rate_compression_quality_metrics.utils as utils
import COPEX_high_rate_compression_quality_metrics.metrics as metrics
import COPEX_high_rate_compression_quality_metrics.thematic as thematics


root_directory = "DATA"
dataset_name = "S2_L1C"
test_case_number = 1
nnvvppp_algoname = "01-01-005_JJ2000"

original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                    test_case_number=test_case_number)
print("original folder path = ",original_folder_path)
decompressed_folder_path = utils.get_algorithm_results_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                    test_case_number=test_case_number,nnvvppp_algoname=nnvvppp_algoname)
original_products = utils.get_product_path_list_from_path(path=original_folder_path)

print("original products = [", original_products, "}")

# print(image1, " [shape =", image1.shape, ", min =", np.min(image1), ", max =", np.max(image1), ", dtype = ",
# image1.dtype, "]")



results = thematics.compute_kmeans_score_for_multiband(original_folder_path=original_folder_path, decompressed_folder_path=decompressed_folder_path,
                                             satellite_type="S2")


print("results = ", results)
