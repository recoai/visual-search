# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.5.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import sys
sys.path.append("../python/recoai_visual_search/")
from visual_search import RecoAIVisualSearch
from models import *
import json
from glob import glob
import ipyplot
from matplotlib import pyplot as plt
from tqdm import tqdm

# Creating a collection to keep the images 
# -------------
# In this case we are using MOBILE_NET_V2 as the feature extractor

api = RecoAIVisualSearch(bearer_token="secrettoken", address="http://localhost:8890")
upsert_collection = UpsertCollection(
    config=GenericModelConfig(
        model_architecture=ModelArchitecture.MOBILE_NET_V2
    ), 
    name="images"
)
response = api.upsert_collection(upsert_collection)

# Indexing images
# -----------

for img_path in tqdm(sorted(glob("../../images/imagenet-sample-images/*.JPEG"))):
    image_id = img_path.split("/")[-1].split(".")[0]
    with open(img_path, "rb") as inp:
        image_bytes = list(inp.read())
    image_source = ImageSource(image_bytes=ImageBytes(image_bytes))
    add_image = AddImage(collection_name="images", id=image_id, source=image_source)
    resp = api.add_image(add_image)

# Searching for a cat 
# -----------

with open("../../images/cat.jpeg", "rb") as inp:
    image_bytes = list(inp.read())
image_source = ImageSource(image_bytes=ImageBytes(image_bytes))
search_image = SearchImage(collection_name="images", n_results=8, source=image_source)
search_results = json.loads(api.search_image(search_image).content)
search_results

images_paths = []
for result in search_results["results"]:
    fn = "/home/pawel/logicai/visual-search/images/imagenet-sample-images/{}.JPEG".format(result["id"])
    img = plt.imread(fn)
    images_paths.append(img)    
ipyplot.plot_images(images_paths)


