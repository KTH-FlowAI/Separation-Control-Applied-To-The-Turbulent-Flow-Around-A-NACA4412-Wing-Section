import numpy as np
from PIL import Image
import os,sys


def CorpImage(image_name,org_path,save_path):

  image_format = image_name[image_name.find('.'):]
  new_format=".pdf"

  image_path  = os.path.join(org_path,image_name)
  image_name = image_name[:image_name.find('.')] + new_format

  manual_cropped_image_path = os.path.join(save_path,
                                          'CROP_'+image_name,
                                          )
  image = Image.open(image_path)
  # Convert the image to a NumPy array for manual cropping
  image_array = np.array(image)
  # Identify the non-white (content) regions
  non_white_pixels = np.where(np.all(image_array != [255, 255, 255], axis=-1))
  min_row, max_row = np.min(non_white_pixels[0]), np.max(non_white_pixels[0])
  min_col, max_col = np.min(non_white_pixels[1]), np.max(non_white_pixels[1])
  # Crop the image based on the detected content area
  manual_cropped_image = image.crop((min_col, min_row, max_col, max_row))
  manual_cropped_image.save(manual_cropped_image_path)
  print(f'[IO] CROPPED IMAGE SAVED: {manual_cropped_image_path}')

  return



Image_List = [
              # '2D-CTRL.png', 
              # '2D-NOCTRL.png',
              # 'MESH.png',
              # 'MESH-CLOSE.png',
              # 'MESH-CLOSER-2.png',
              'Rebuttal_R1_REF_TE.jpeg',
              'Rebuttal_R1_CASEA_TE.jpeg',
              'Rebuttal_R1_CASEB_TE.jpeg',
              'Rebuttal_R1_CASEC_TE.jpeg',
              'Rebuttal_R1_CASED_TE.jpeg',
              'Rebuttal_R1_CASEE_TE.jpeg',

              ]

org_path ='Figs/99-SNAPSHOTS/'
save_path = 'Figs/99-SNAPSHOTS/'

for image_name in Image_List:
  CorpImage(image_name,org_path,save_path)
