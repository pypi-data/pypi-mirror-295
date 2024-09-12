import numpy as np
from skimage import io
import os
import sys
import time

# Ajoute le dossier 'COPEX_high_rate_compression_quality_metrics' au chemin de recherche des modules, pour pouvoir acceder a tout
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import COPEX_high_rate_compression_quality_metrics.utils as utils
import COPEX_high_rate_compression_quality_metrics.metrics as metrics

root_directory = "DATA"
dataset_name = "S2_L1C"
test_case_number = 1
nnvvppp_algoname = "01-01-005_JJ2000"

original_folder_path = utils.get_original_full_path(root_directory=root_directory, dataset_name=dataset_name,
                                                    test_case_number=test_case_number)

original_products = utils.get_product_path_list_from_path(path=original_folder_path)

print("original products = [", original_products, "}")

# print(image1, " [shape =", image1.shape, ", min =", np.min(image1), ", max =", np.max(image1), ", dtype = ",
# image1.dtype, "]")

print("\n resampling...")
for i in range(0, 1):
    image1_input_path = original_products[i]
    image1_output_folder_path = os.path.join(original_folder_path, "resampled")
    utils.create_folder_if_do_not_exist(image1_output_folder_path)
    image1_output_path = os.path.join(image1_output_folder_path, os.path.basename(image1_input_path))
    # print(image1)
    start_time = time.time()  # Enregistre le temps de début
    result = utils.resample_band(input_path=image1_input_path, output_path=image1_output_path)
    end_time = time.time()  # Enregistre le temps de fin
    execution_time = end_time - start_time  # Calcule le temps d'exécution
    print(f"Temps d'exécution pour le resampling ({i}) : {execution_time:.4f} secondes")

"""print("\n calculating LPIPS...")
for i in (0,4,1):
    lossfn = metrics.initialize_LPIPS()
    image1 = io.imread(original_products[i])
    image2 = io.imread(result_products[i])
    start_time = time.time()  # Enregistre le temps de début
    result = metrics.calculate_lpips_multiband_v3(image1, image2,loss_fn=lossfn)
    print("LPIPS = ", result)
    end_time = time.time()  # Enregistre le temps de fin
    execution_time = end_time - start_time  # Calcule le temps d'exécution
    print(f"Temps d'exécution pour le LPIPS ({i}) : {execution_time:.4f} secondes")

for i in (0,4,1):
    lossfn = metrics.initialize_LPIPS()
    image1 = io.imread(original_products[i])
    image2 = io.imread(result_products[i])
    start_time = time.time()  # Enregistre le temps de début
    result = metrics.calculate_lpips_multiband(image1, image2,loss_fn=lossfn)
    print("LPIPS = ", result)
    end_time = time.time()  # Enregistre le temps de fin
    execution_time = end_time - start_time  # Calcule le temps d'exécution
    print(f"Temps d'exécution pour le LPIPS ({i}) : {execution_time:.4f} secondes")"""
"""note de resultats :calculating LPIPS...
D:\VisioTerra\technique\P382_ESRIN_COPEX-DCC\engineering\COPEX_high_rate_compression_quality_metrics\python_interpreter_test\Lib\site-packages\torchvision\models\_utils.py:208: UserWarning: The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.
  warnings.warn(
D:\VisioTerra\technique\P382_ESRIN_COPEX-DCC\engineering\COPEX_high_rate_compression_quality_metrics\python_interpreter_test\Lib\site-packages\torchvision\models\_utils.py:223: UserWarning: Arguments other than a weight enum or `None` for 'weights' are deprecated since 0.13 and may be removed in the future. The current behavior is equivalent to passing `weights=AlexNet_Weights.IMAGENET1K_V1`. You can also use `weights=AlexNet_Weights.DEFAULT` to get the most up-to-date weights.
  warnings.warn(msg)
D:\VisioTerra\technique\P382_ESRIN_COPEX-DCC\engineering\COPEX_high_rate_compression_quality_metrics\python_interpreter_test\Lib\site-packages\lpips\lpips.py:107: FutureWarning: You are using `torch.load` with `weights_only=False` (the current default value), which uses the default pickle module implicitly. It is possible to construct malicious pickle data which will execute arbitrary code during unpickling (See https://github.com/pytorch/pytorch/blob/main/SECURITY.md#untrusted-models for more details). In a future release, the default value for `weights_only` will be flipped to `True`. This limits the functions that could be executed during unpickling. Arbitrary objects will no longer be allowed to be loaded via this mode unless they are explicitly allowlisted by the user via `torch.serialization.add_safe_globals`. We recommend you start setting `weights_only=True` for any use case where you don't have full control of the loaded file. Please open an issue on GitHub for any issues related to this experimental feature.
  self.load_state_dict(torch.load(model_path, map_location='cpu'), strict=False)
block 1 [0:5000,0:5000]
LPIPS =  ([0.014096043072640896], 0.014096043072640896)
Temps d'exécution pour le LPIPS (0) : 4.1786 secondes
block 1 [0:5000,0:5000]
block 1 [0:5000,5000:10000]
block 1 [5000:10000,0:5000]
block 1 [5000:10000,5000:10000]
LPIPS =  ([0.4079781174659729, 0.770745038986206, 0.28891780972480774, 0.38991692662239075], 0.46438947319984436)
Temps d'exécution pour le LPIPS (4) : 38.5093 secondes
block 1 [0:5000,0:5000]
block 1 [0:5000,5000:10000]
block 1 [0:5000,10000:15000]
block 1 [5000:10000,0:5000]
block 1 [5000:10000,5000:10000]
block 1 [5000:10000,10000:15000]
block 1 [10000:15000,0:5000]
block 1 [10000:15000,5000:10000]
block 1 [10000:15000,10000:15000]
LPIPS =  ([0.08026184886693954, 0.4868659973144531, 0.6086241602897644, 0.009814420714974403, 0.002406204352155328, 0.16692383587360382, 0.012381207197904587, 0.08829136192798615, 0.033400923013687134], 0.16544110661682984)
Temps d'exécution pour le LPIPS (1) : 160.8614 secondes
LPIPS =  ([0.014096043072640896], 0.014096043072640896)
Temps d'exécution pour le LPIPS (0) : 4.2076 secondes
LPIPS =  ([0.39704033732414246], 0.39704033732414246)
Temps d'exécution pour le LPIPS (4) : 40.4872 secondes """
