import os
import cv2
import numpy as np

# İşlem yapılacak klasör
image_folder = "images"  # 'images' klasörü mevcut dizinde olmalı

# Klasördeki tüm dosyaları tarar
for filename in os.listdir(image_folder):
    filepath = os.path.join(image_folder, filename)
    
    # Görüntü dosyası olup olmadığını kontrol et
    if not filename.lower().endswith(('.png', '.jpg')):
        continue

    # Görüntüyü yükle
    image = cv2.imread(filepath)

    # Görüntünün tam beyaz piksel sayısını kontrol et
    if image is not None:
        total_pixels = image.shape[0] * image.shape[1]
        white_pixels = np.sum(np.all(image == [255, 255, 255], axis=-1))
        
        # Tam beyaz piksel oranı %50'den fazlaysa dosyayı yazdır ve sil
        if white_pixels / total_pixels > 0.5:
            print(f"Siliniyor: {filename}")
            os.remove(filepath)
