import glob
import os
import re
from typing import List, Optional, Dict, Any

import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.enums import Resampling

compressed_folder_name = "compressed"
decompressed_folder_name = "decompressed"
original_folder_name = "original"

def get_product_name_from_final_folder_path(original_folder_path,num_de_dossier_en_partant_de_la_fin=-2):
    """
        Extrait l'avant-dernier dossier dans un chemin donné et isole la partie spécifique du nom de dossier.

        Args:
            path (str): Le chemin de fichier complet.
            num_de_dossier_en_partant_de_la_fin(int) : de combien on recule pour prendre le  nom de dossier, -2 = on regule de 1

        Returns:
            tuple: (avant_dernier_dossier, partie_extraite)
        """
    # Récupérer l'avant-dernier dossier du chemin
    #print("getting product name from ",original_folder_path)
    path_parts = original_folder_path.split(os.sep)  # Divise le chemin en parties
    if len(path_parts) < 2:
        raise ValueError("Le chemin n'a pas suffisamment de dossiers.")

    avant_dernier_dossier = path_parts[num_de_dossier_en_partant_de_la_fin]  # Avant-dernier dossier
    #print("avant_dernier_dossier = ",avant_dernier_dossier)
    # Isoler la partie avant ']_' du dossier
    #match = re.search(r'^(\[.*?\])', avant_dernier_dossier)
    if avant_dernier_dossier:
        product_name = avant_dernier_dossier.split(']_')[1][1:]  # Enlever les crochets []
    else:
        product_name = None  # Aucun match trouvé

    return avant_dernier_dossier, product_name
def create_folder_if_do_not_exist(folder_path):
    """
    Crée un dossier s'il n'existe pas déjà.

    :param folder_path: Chemin du dossier à créer.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Dossier créé : {folder_path}")
    else:
        return
        #print(f"Le dossier existe déjà : {folder_path}")

# Exemple d'utilisation
create_folder_if_do_not_exist('/chemin/vers/le/dossier')


def resample_band(input_path, output_path, scale_factor=2, resampling_method=Resampling.nearest):
    """
    Fonction pour rééchantillonner une bande d'image raster en utilisant le
    facteur d'échelle spécifié (2 = on multiplie par 2 le nombre de pixels de l'image en x et y).
     Le rééchantillonnage est, par défaut, fait en
    utilisant la méthode du plus proche voisin, mais peut être modifié via le paramètre.

    Args:
        input_path (str): Chemin du fichier raster d'entrée.
        output_path (str): Chemin du fichier raster de sortie.
        scale_factor (float, optional): Facteur par lequel redimensionner l'image.
                                        Par défaut, le facteur est 2.
        resampling_method (rasterio.enums.Resampling, optional): Méthode de rééchantillonnage.
                                        Par défaut, la méthode du plus proche voisin (nearest).

    Returns:
        None. Le fichier rééchantillonné est écrit dans output_path.

    Exemple:
        resample_band("input.tif", "output.tif", scale_factor=3, resampling_method=Resampling.bilinear)
    """
    with rasterio.open(input_path) as src:
        # Récupérer les métadonnées
        profile = src.profile

        # Calculer les nouvelles dimensions
        new_width = int(src.width * scale_factor)
        new_height = int(src.height * scale_factor)

        # Mettre à jour le profil pour le fichier de sortie
        profile.update(
            width=new_width,
            height=new_height,
            transform=src.transform * src.transform.scale(
                (src.width / new_width),
                (src.height / new_height)
            )
        )

        # Rééchantillonner l'image
        data = src.read(
            out_shape=(src.count, new_height, new_width),
            resampling=resampling_method
        )

        # Écrire les données rééchantillonnées
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data)

    print(f"{input_path} rééchantillonné et sauvegardé sous {output_path}")


def get_nn_vv_ppp_from_full_nnvvppp_algo_name(nnvvppp_algo_name: str) -> str:
    """
    Extrait la partie NN-VV-PPP du nom complet de l'algorithme.

    Args:
        nnvvppp_algo_name (str): Le nom complet de l'algorithme au format 'NN-VV-PPP_suffixedetails'.

    Returns:
        str: La partie NN-VV-PPP extraite du nom complet de l'algorithme.

    Raises:
        ValueError: Si le nom de l'algorithme ne contient pas de séparateur '_' ou si la partie avant le premier '_'
                    est trop courte pour être valide.
    """
    split_list = nnvvppp_algo_name.split("_")[0]
    if len(split_list) < 2:
        raise ValueError(
            f"Le chemin spécifié '{nnvvppp_algo_name}' n'est pas un nom valide, avoir un format nnvvppp_algoname.")
    return nnvvppp_algo_name.split("_")[0]


def get_product_path_list_from_path(path: str) -> List[str]:
    """
    Récupère tous les fichiers TIFF (.tif et .tiff) présents dans le dossier spécifié.

    Args:
        path (str): Le chemin du dossier à explorer.

    Returns:
        List[str]: Une liste des chemins complets des fichiers TIFF trouvés dans le dossier.
    """
    # Liste pour stocker les chemins des fichiers TIFF
    tiff_files = []

    # Vérifier si le chemin spécifié est un dossier
    if not os.path.isdir(path):
        raise ValueError(f"Le chemin spécifié '{path}' n'est pas un dossier valide.")

    # Lister tous les fichiers dans le dossier
    for file_name in os.listdir(path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(path, file_name)

        # Vérifier si c'est un fichier
        if os.path.isfile(file_path):
            # Extraire l'extension du fichier
            _, ext = os.path.splitext(file_name)

            # Vérifier si l'extension est .tif ou .tiff
            if ext.lower() in {'.tif', '.tiff'}:
                tiff_files.append(file_path)

    return tiff_files


def add_data_to_dict(base_dict: Dict[str, Any], data_to_add: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ajoute des données au dictionnaire de base de manière modulaire.

    Args:
        base_dict (Dict[str, Any]): Le dictionnaire de base auquel les données seront ajoutées.
        data_to_add (Dict[str, Any]): Les données à ajouter au dictionnaire de base.

    Returns:
        Dict[str, Any]: Le dictionnaire mis à jour avec les nouvelles données.
    """
    for key, value in data_to_add.items():
        if isinstance(value, dict):
            # Si la valeur est un dictionnaire, on fusionne les dictionnaires récursivement
            base_dict[key] = add_data_to_dict(base_dict.get(key, {}), value)
        else:
            # Sinon, on ajoute ou remplace la valeur dans le dictionnaire de base
            base_dict[key] = value

    return base_dict


def get_product_name_list_from_path(path: str) -> List[str]:
    """
    Récupère tous les fichiers TIFF (.tif et .tiff) présents dans le dossier spécifié.

    Args:
        path (str): Le chemin du dossier à explorer.

    Returns:
        List[str]: Une liste des chemins complets des fichiers TIFF trouvés dans le dossier.
    """
    # Liste pour stocker les chemins des fichiers TIFF
    tiff_files = []

    # Vérifier si le chemin spécifié est un dossier
    if not os.path.isdir(path):
        raise ValueError(f"Le chemin spécifié '{path}' n'est pas un dossier valide.")

    # Lister tous les fichiers dans le dossier
    for file_name in os.listdir(path):
        # Construire le chemin complet du fichier
        file_path = os.path.join(path, file_name)

        # Vérifier si c'est un fichier
        if os.path.isfile(file_path):
            # Extraire l'extension du fichier
            _, ext = os.path.splitext(file_name)

            # Vérifier si l'extension est .tif ou .tiff
            if ext.lower() in {'.tif', '.tiff'}:
                tiff_files.append(os.path.basename(file_path))

    return tiff_files


def get_test_case_number_str(number) -> str:
    """
        Convertit un nombre entier en une chaîne de caractères sur 3 digits.

        Args:
            number: Le nombre à convertir.

        Returns:
            str: Le nombre formaté en chaîne de caractères sur 3 digits (par exemple, 1 -> '001').
        """
    if type(number) == int:
        return f"{number:03d}"
    else:
        return number


def get_compression_factor_from_compressed_folder_name(folder_name):
    bracket_content = get_bracket_content(folder_name, 2)
    return bracket_content.split("x")[-1]


def get_compressed_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers compressés.

    Returns:
        str: Le nom du dossier compressé.
    """
    return compressed_folder_name


def get_decompressed_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers décompressés.

    Returns:
        str: Le nom du dossier décompressé.
    """
    return decompressed_folder_name


def get_original_folder_name() -> str:
    """
    Retourne le nom du dossier contenant les fichiers originaux.

    Returns:
        str: Le nom du dossier original.
    """
    return original_folder_name


def find_matching_file(image_full_name, folder_path):
    """
    Trouve le fichier correspondant dans le répertoire donné qui commence par le nom de base spécifié.

    Args:
        image_full_name (str): Nom de base du fichier (sans extension).
        folder_path (str): Le chemin vers le répertoire où chercher les fichiers.

    Returns:
        str: Le chemin complet du fichier trouvé ou None si aucun fichier correspondant n'est trouvé.
    """
    # Construire le motif de recherche pour les fichiers qui commencent par image_full_name

    base_name = os.path.splitext(image_full_name)[0]
    # Lister tous les fichiers dans le dossier
    all_files = os.listdir(folder_path)

    # Chercher un fichier qui contient le base_name dans son nom
    for file_name in all_files:
        if base_name in file_name and file_name.endswith(('.tif', '.tiff')):
            return os.path.join(folder_path, file_name)
    return None


def get_algorithm_results_full_path(root_directory: str, dataset_name: str, test_case_number: int,
                                    nnvvppp_algoname: str) -> str:
    """
    Construit le chemin complet vers les résultats d'un algorithme spécifique pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.
        nnvvppp_algoname (str): Le nom de l'algorithme dans le format NN VV PPP_algo.

    Returns:
        str: Le chemin complet vers les résultats de l'algorithme.
    """
    # print("getting algo result folder full path...")
    return os.path.join(root_directory,
                        dataset_name,
                        get_test_case_folder(root_directory, dataset_name, get_test_case_number_str(test_case_number)),
                        get_decompressed_folder_name(),
                        get_algorithm_results_folder(root_directory, dataset_name,
                                                     get_test_case_number_str(test_case_number), nnvvppp_algoname)
                        )


def get_original_full_path(root_directory: str, dataset_name: str, test_case_number: int) -> str:
    """
    Construit le chemin complet vers les fichiers originaux pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        str: Le chemin complet vers les fichiers originaux.
    """
    return os.path.join(
        root_directory,
        dataset_name,
        get_test_case_folder(root_directory, dataset_name, get_test_case_number_str(test_case_number)),
        get_original_folder_name()
    )


def get_algorithm_results_folder(root_directory: str, dataset_name: str, test_case_number: int, nnvvpp_algoname: str) -> \
        Optional[str]:
    """
    Retourne le nom du dossier contenant les résultats d'un algorithme spécifique.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.
        nnvvpp_algoname (str): Le nom de l'algorithme dans le format NN VV PPP_algo.

    Returns:
        Optional[str]: Le nom du dossier contenant les résultats de l'algorithme,
        ou None si aucun dossier ne correspond.
    """
    test_case_folder_name = get_test_case_folder(root_directory, dataset_name,
                                                 get_test_case_number_str(test_case_number))
    # print("test_case_folder_name = ",test_case_folder_name)
    root_dir = os.path.join(root_directory, dataset_name, test_case_folder_name, decompressed_folder_name)
    try :
        result = list_matching_folders(root_dir=root_dir, search_str=nnvvpp_algoname, bracket_num=0).pop(0)
        return result
    except :
        ValueError("no result found from root dir ",root_dir," with nnvvpp = ",nnvvpp_algoname," in bracket number 0")


def get_test_case_folder(root_directory: str, dataset_name: str, test_case_number: int) -> Optional[str]:
    """
    Retourne le nom du dossier contenant les données pour un test donné.

    Args:
        dataset_name (str): Le nom du dataset.
        test_case_number (str): Le numéro du test case.

    Returns:
        Optional[str]: Le nom du dossier de test case, ou None si aucun dossier ne correspond.
    """
    test_case_root_folder = os.path.join(root_directory, dataset_name)
    result = list_matching_folders(test_case_root_folder, get_test_case_number_str(test_case_number), 0).pop(0)
    return result


def get_bracket_content(folder_name: str, bracket_num: int) -> str:
    """
    Extrait le Nième champ entre crochets dans une chaîne de caractères et vérifie s'il contient une sous-chaîne spécifique.

    Args:
        folder_name (str): Le nom du dossier au format [001]_[1c_256_256]_[1]..[] ou chempin du dossier
        (si c est un chemin de dossier, alors on le découpera et regardera uniquement le dernier dossier.
        search_str (str): La sous-chaîne à rechercher dans le champ extrait.
        bracket_num (int): Le numéro du champ entre crochets à extraire (commençant à 0).

    Returns:
        bool: True si le Nième champ contient la sous-chaîne, False sinon.
    """
    # Extraire tous les champs entre crochets
    # print("checking bracket contents for ",search_str,"...")
    # Vérifier si folder_name est un chemin complet et extraire le nom du dernier dossier
    if os.path.sep in folder_name:
        folder_name = os.path.basename(folder_name)

    fields = folder_name.split('[')[1:]  # Diviser la chaîne et ignorer tout avant le premier crochet ouvrant
    # print("fields = ",fields)
    fields = [field.split(']')[0] for field in fields]  # Extraire les contenus des crochets
    # print("fields = ",fields)

    # Vérifier que le numéro de champ demandé est valide
    if 0 <= bracket_num <= len(fields):
        # Extraire le Nième champ
        selected_field = fields[bracket_num]

        return selected_field
    else:
        # Si le numéro de champ est invalide, retourner False
        raise ValueError("Si le numéro de champ est invalide ou le champs n'existe pas")


def check_bracket_content(folder_name: str, search_str: str, bracket_num: int) -> bool:
    """
    Extrait le Nième champ entre crochets dans une chaîne de caractères et vérifie s'il contient une sous-chaîne spécifique.

    Args:
        folder_name (str): Le nom du dossier au format [001]_[1c_256_256]_[1]..[].
        search_str (str): La sous-chaîne à rechercher dans le champ extrait.
        bracket_num (int): Le numéro du champ entre crochets à extraire (commençant à 0).

    Returns:
        bool: True si le Nième champ contient la sous-chaîne, False sinon.
    """
    # Extraire tous les champs entre crochets
    # print("checking bracket contents for ",search_str,"...")
    # Vérifier si folder_name est un chemin complet et extraire le nom du dernier dossier
    if os.path.sep in folder_name:
        folder_name = os.path.basename(folder_name)

    fields = folder_name.split('[')[1:]  # Diviser la chaîne et ignorer tout avant le premier crochet ouvrant
    fields = [field.split(']')[0] for field in fields]  # Extraire les contenus des crochets
    # print("fields = ",fields)

    # Vérifier que le numéro de champ demandé est valide
    if 0 <= bracket_num <= len(fields):
        # Extraire le Nième champ
        selected_field = fields[bracket_num]
        # Vérifier si la sous-chaîne est présente
        # print(search_str in selected_field)
        return search_str in selected_field
    else:
        # Si le numéro de champ est invalide, retourner False
        return False


def list_matching_folders(root_dir: str, search_str: str, bracket_num: int) -> List[str]:
    """
    Liste les sous-dossiers d'un répertoire racine et vérifie si le Nième champ
    entre crochets dans leur nom contient une sous-chaîne spécifique.

    Args:
        root_dir (str): Le chemin du répertoire racine.
        search_str (str): La sous-chaîne à rechercher dans le Nième champ.
        bracket_num (int): Le numéro du champ entre crochets à vérifier (commençant à 1).

    Returns:
        List[str]: Une liste de chemins complets des sous-dossiers correspondants.
    """
    # print("matching folders from ",root_dir,"...")
    matching_folders = []

    # Lister tous les sous-dossiers dans le répertoire racine
    for folder_name in os.listdir(root_dir):
        # print("folder names [",folder_name,"]...")
        folder_path = os.path.join(root_dir, folder_name)

        # Vérifier si l'élément est bien un dossier
        if os.path.isdir(folder_path):
            # Utiliser check_bracket_content pour vérifier le contenu du Nième champ
            if check_bracket_content(folder_name, search_str, bracket_num):
                # Si trouvé, ajouter le chemin complet du dossier à la liste
                matching_folders.append(folder_name)

    return matching_folders


def normalize_image(image: np.ndarray) -> np.ndarray:
    """
    Normalize the image for display, regardless of the value range.

    This function adjusts the image data to a standard range for display purposes.
    It handles different data types and scales the image values accordingly.

    Args:
        image (np.ndarray): The input image as a NumPy array.

    Returns:
        np.ndarray: The normalized image.
    """
    # Check the data type and normalize accordingly
    if image.dtype == np.uint16:
        # For 16-bit unsigned integer images, scale to the range [0, 1]
        image = image.astype(np.float32) / 65535.0
    elif image.dtype == np.float32:
        # For floating-point images, clip values to the range [0, 1]
        image = np.clip(image, 0, 1)
    else:
        # For other data types, normalize to the range [0, 1]
        image = image.astype(np.float32)
        image_min = np.min(image)
        image_max = np.max(image)
        # Avoid division by zero if the image has a uniform value
        if image_max > image_min:
            image = (image - image_min) / (image_max - image_min)
        else:
            image = np.zeros_like(image)

    return image


def display_multiband_tiffs(image1: np.ndarray, image2: np.ndarray) -> None:
    """
    Display two TIFF images with appropriate normalization and visualization.

    This function displays two images side by side. It handles different numbers of channels and normalizes
    the images for better visualization. It supports single-channel, multi-channel (e.g., RGB), and images
    with more than three channels.

    Args:
        image1 (np.ndarray): The first image as a NumPy array (HxWxC or HxW).
        image2 (np.ndarray): The second image as a NumPy array (HxWxC or HxW).

    Returns:
        None
    """
    plt.figure(figsize=(10, 5))

    # Normalize images for display
    image1 = normalize_image(image1)
    image2 = normalize_image(image2)

    plt.subplot(1, 2, 1)
    plt.title('Image 1')
    if image1.ndim == 3:
        if image1.shape[2] == 1:
            # Display single-channel image as grayscale
            plt.imshow(image1[:, :, 0], cmap='gray')
        if image1.shape[2] == 2:
            # Display  a two-channel image
            plt.imshow(image1[:, :, :1])
        elif image1.shape[2] == 3:
            # Display RGB image
            plt.imshow(image1)
        else:
            # Display the first three channels of an image with more than 3 channels
            img_to_show = image1[:, :, :3]
            # Normalize data for better visualization
            img_to_show = (img_to_show - np.min(img_to_show)) / (np.max(img_to_show) - np.min(img_to_show))
            plt.imshow(img_to_show)
    elif image1.ndim == 2:
        # Display grayscale image
        plt.imshow(image1, cmap='gray')
    plt.axis('off')

    # Display Image 2
    plt.subplot(1, 2, 2)
    plt.title('Image 2')
    if image2.ndim == 3:
        if image2.shape[2] == 1:
            # Display single-channel image as grayscale
            plt.imshow(image2[:, :, 0], cmap='gray')
        if image2.shape[2] == 2:
            # Display a two-channel image
            plt.imshow(image2[:, :, :1])
        elif image2.shape[2] == 3:
            # Display RGB image
            plt.imshow(image2)
        else:
            # Display the first three channels of an image with more than 3 channels
            img_to_show = image2[:, :, :3]
            # Normalize data for better visualization
            img_to_show = (img_to_show - np.min(img_to_show)) / (np.max(img_to_show) - np.min(img_to_show))
            plt.imshow(img_to_show)
    elif image2.ndim == 2:
        # Display grayscale image
        plt.imshow(image2, cmap='gray')
    plt.axis('off')

    plt.show()
