# Gerekli kütüphaneleri import edin
from sentinelhub import SentinelHubRequest, DataCollection, MimeType, CRS, BBox, SHConfig, Geometry
from PIL import Image
import numpy as np
import os
from datetime import datetime, timedelta

# Kimlik bilgileri
config = SHConfig()
config.sh_client_id = '7d3e8b9c-0c04-495d-bf78-4360832f1e4e'
config.sh_client_secret = 'Y4IoArDDiTk2oE9IErmu8h74chabJ1VC'

# Evalscript tanımı
evalscript = """
//VERSION 3
function setup() {
  return {
    input: ["B03", "B08", "dataMask"],
    output: { bands: 3 }
  }
}

const ramp = [
  [-0.8, 0x008000],
  [0, 0xFFFFFF],
  [0.8, 0x0000CC]
];

let viz = new ColorRampVisualizer(ramp);

function evaluatePixel(samples) {
  const val = index(samples.B03, samples.B08);
  let imgVals = viz.process(val);
  return imgVals.concat(samples.dataMask);
}
"""

# Bölge tanımı
bbox = BBox(bbox=[42.22985639137869, 38.265091672395926, 43.71413491289499, 39.0263509496782], crs=CRS.WGS84)
geometry = Geometry(geometry={"coordinates":[[[43.38841330803652,39.0217025445518],[43.000306101879005,38.961543286984835],[42.92615779468585,38.839802107766474],[42.74413979458299,38.84580573676271],[42.36115884325298,38.76368458929801],[42.24998276461844,38.572319754135975],[42.22985639137869,38.443760203964814],[42.821470542872135,38.40307558985978],[42.86739128405853,38.265091672395926],[43.15524163345694,38.27303471242237],[43.388125737972274,38.4200814371319],[43.38950673498229,38.556924016237105],[43.230935168313636,38.66150952601399],[43.36656879212549,38.768988069350655],[43.65015955580523,38.880905059407496],[43.71413491289499,38.964679501241704],[43.5002944852844,39.0263509496782],[43.38841330803652,39.0217025445518]]],"type":"Polygon"}, crs=CRS.WGS84)

# 'images' klasörünü oluşturun
if not os.path.exists('images'):
    os.makedirs('images')

# Başlangıç ve bitiş tarihleri
start_date = datetime(2016, 1, 1)
end_date = datetime(2024, 11, 1)

# Tarih aralığında haftalık döngü
current_date = start_date
while current_date < end_date:
    week_start = current_date
    week_end = current_date + timedelta(days=6)
    current_date = week_end + timedelta(days=1)

    # Tarih formatlarını belirleyin
    start_date_str = week_start.strftime('%Y-%m-%d')
    end_date_str = week_end.strftime('%Y-%m-%d')

    print(f"{start_date_str} - {end_date_str} dönemi işleniyor...")

    # İstek oluşturma
    request = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=(start_date_str, end_date_str),
                other_args={"dataFilter": {"maxCloudCoverage": 5}}
            ),
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.JPG),
        ],
        bbox=bbox,
        geometry=geometry,
        size=[2000, 1306.463],
        config=config
    )

    # Veri alma ve kaydetme
    try:
        response = request.get_data()
        if response:
            image = response[0]
            image2 = Image.fromarray(image)
            filename = os.path.join('images', f'{week_start.strftime("%Y-%m-%d")}_to_{week_end.strftime("%Y-%m-%d")}.jpg')
            image2.save(filename)
            print(f"{filename} kaydedildi.")
        else:
            print(f"{start_date_str} - {end_date_str} için veri bulunamadı.")
    except Exception as e:
        print(f"{start_date_str} - {end_date_str} için hata oluştu: {e}")
