import rasterio
import rasterio.mask
from rasterio.plot import show
import numpy as np
import fiona
from rasterio.enums import Resampling
from rasterio.plot import show
from datetime import date, timedelta, datetime
from matplotlib import pyplot as plt

from meteo_importation import all_info
from sentinel_importation import get_img

#---------------------------Liste des fonctions-------------------------------

def resize(string, A, B):
    #Changer la resolution d'un raster "string" et le découpe selon "shapes"
    with rasterio.open(string) as HR_:
        C, HR_transform = rasterio.mask.mask(HR_, shapes, crop=True)
        HR_meta = HR_.meta
        kwargs = HR_meta
        kwargs.update(
            dtype=rasterio.float32,
            count=1,
            compress='lzw')

        with rasterio.open('./output/other/resh_HR.tif', 'w', **kwargs) as dstC:
            dstC.write(C.astype(rasterio.float32))

    D = rasterio.open('./output/other/resh_HR.tif')
    D = D.read(
            out_shape=(
                HR_.count,
                int(A),
                int(B)
            ),
            resampling=Resampling.bilinear
        )
    return(D)

def blur(img, radius, number):
    for i in range(number):
        if(i == 0):
            a = img
        else:
            a = arraylist_sum
        
        kernel = np.ones((radius,radius))
        kernel = kernel / np.sum(kernel)
        arraylist = []
        for y in range(radius):
            temparray = np.copy(a)
            temparray = np.roll(temparray, y - 1, axis=0)
            for x in range(radius):
                temparray_X = np.copy(temparray)
                temparray_X = np.roll(temparray_X, x - 1, axis=1)*kernel[y,x]
                arraylist.append(temparray_X)

        arraylist = np.array(arraylist)
        arraylist_sum = np.sum(arraylist, axis=0)
    return arraylist_sum

def calculate_DHFI(red, nir, swir, HR, Tempera, mxd, min_ndvi, max_ndvi, Vent):
    #Verif si tous aux memes dimensions
    """if(max_ndvi.shape != red.shape or max_ndvi.shape != nir.shape or max_ndvi.shape != swir.shape or max_ndvi.shape != HR.shape or max_ndvi.shape != Tempera.shape or max_ndvi.shape != mxd.shape or max_ndvi.shape != min_ndvi.shape):
        print("error dans les dimensions données entrée")
    else:
        print("données bonnes : debut calcul")
    """
    
    ndvi = (nir - red)/(nir + red) #!! aux NaN et invalide
    ndvi[ndvi > 1] = 1
    ndvi[ndvi < -1] = -1

    #Division par 255 pour avoir données entre 0 et 1
    gvmi =((nir/255+0.1)-(swir/255+0.02))/((nir/255+0.1)+(swir/255+ 0.02)) 

    ewt = (-(0.4743 * 0.006577 + (5.853*2.718-5) - 0.006577 * gvmi) + np.sqrt( ((0.4743 * 0.006577 + (5.853*2.718-5) - 0.006577 * gvmi))**2 - 4 * (5.853*2.71 -5 ) * 0.006577 * (0.4743-0.3967 - gvmi)))/(2*0.006577 *(5.853*2.71-5))

    greeness = (ndvi  - min_ndvi/255) /  (max_ndvi/255 - min_ndvi/255) 
    greeness[greeness > 1] = 1
    greeness[greeness < 0] = 0

    ndvi_mx = max_ndvi * 100 /255 + 100
    LF_rem = (greeness * (35 + 0.5 * (ndvi_mx -100)))/100

    ewt_barre = ewt / (np.nanmean(ewt) + 2 * np.nanstd(ewt))
    ewt_barre[ewt_barre > 1] = 1
    ewt_barre[ewt_barre < 0] = 0

    LFc = LF_rem * (1 + 0.2 * (ewt_barre - 1))

    EMC_A = (HR/100< 0.1)*(0.03229 + 0.262573 *HR- 0.001 *HR * Tempera)
    EMC_B = (HR/100 > 0.1) * (HR/100< 0.5) *(1.7544 + 0.160107 * HR- 0.02661 * Tempera)
    EMC_C = (HR/100 > 0.5)*(21.0606 + 0.005565 *(HR)**2 - 0.00063 * HR*Tempera - 0.494399 * HR)
    EMC_tot = EMC_A + EMC_B + EMC_C

    FM_ten = EMC_tot * 1.28

    TNf = (FM_ten)/(mxd*100)

    DHFI = (1 -LFc)*(1 - TNf)
    
    return DHFI, TNf, LFc

if (__name__ == '__main__'):
    print("Start calcul DHFI")
    #-------------------Telechargement données---------------------------------

    today = datetime.now()
    if(int(today.strftime("%H")) < 18):
        date_in = (today - timedelta(days = 1)).strftime("%Y-%m-%d")
        date_DHFI = today.strftime("%Y-%m-%d")
        print(f"Le programme est lancé avant 18h (Paris) le calcul du DHFI sera réalisé pour la journée du " + today.strftime("%d/%m/%Y"))
    else:
        date_in = today.strftime("%Y-%m-%d")
        date_DHFI = (today + timedelta(days = 1)).strftime("%Y-%m-%d")
        print(f"Debut calcul DHFI du " + (today + timedelta(days = 1)).strftime("%d/%m/%Y"))

    all_info(date_in)
    date_before = (today - timedelta(days = 5)).strftime("%Y-%m-%d")
    try:
        get_img(date_before, date_in)
    except:
        print("Sentinel download")
    
    #-----------------------Importation données--------------------------------

    #Importation du contour du département
    with fiona.open('./Input/contour_herault/admin-departement.shp', "r") as shapefile:
        shapes = [feature["geometry"] for feature in shapefile]

    #image jour departement
    #Tiff avec 3 couches @1 red @2 nir @3 swir
    dataset_ = rasterio.open(f'./Input/sentinel2/{date_in}.tiff')
    dataset, dataset_transform = rasterio.mask.mask(dataset_, shapes, crop=True)
    dataset_meta = dataset_.meta

    red = dataset[0]
    nir = dataset[1]
    swir = dataset[2]

    #ndvi max min 5 ans departement
    max_ndvi_ = rasterio.open('./Input/vegetation/Max_NDVI_.tif')
    max_ndvi, max_ndvi_transform = rasterio.mask.mask(max_ndvi_, shapes, crop=True)
    max_ndvi_meta = max_ndvi_.meta

    min_ndvi_ = rasterio.open('./Input/vegetation/Min_NDVI.tif')
    min_ndvi, min_ndvi_transform = rasterio.mask.mask(min_ndvi_, shapes, crop=True)
    min_ndvi_meta = min_ndvi_.meta

    #Données végétation departement
    mxd = resize("./Input/vegetation/MXd_finale.tif", min_ndvi.shape[1], min_ndvi.shape[2])

    #Données météo departement
    HR = resize(f"./Input/weather/{date_DHFI}/humidite_relative_{date_DHFI}_AROME.grib2", min_ndvi.shape[1], min_ndvi.shape[2])
    Tempera = resize(f"./Input/weather/{date_DHFI}/temp_{date_DHFI}_AROME.grib2", min_ndvi.shape[1], min_ndvi.shape[2])
    Vent = resize(f"./Input/weather/{date_DHFI}/vent_{date_DHFI}_AROME.grib2", min_ndvi.shape[1], min_ndvi.shape[2])


    #-------------------------Calcul----------------------------------

    try:
        DHFI, TNf, LFc = calculate_DHFI(red, nir, swir, HR, Tempera, mxd, min_ndvi, max_ndvi, Vent)
        print("Fin du calcul")

    except:
        print("Error")


    #------------------Exportation de données-------------------------

    kwargs = dataset_meta
    kwargs.update(
        dtype=rasterio.float32,
        count=1,
        compress='lzw')

    with rasterio.open(f'./Output/GeoTiff/DHFI_{date_DHFI}.tif', 'w', **kwargs) as dst:
        dst.write(DHFI.astype(rasterio.float32))

    with rasterio.open(f'./Output/other/TNf_{date_DHFI}.tif', 'w', **kwargs) as dstB:
        dstB.write(TNf.astype(rasterio.float32))

    with rasterio.open(f'./Output/other/LFc_{date_DHFI}.tif', 'w', **kwargs) as dstC:
        dstC.write(LFc.astype(rasterio.float32))

    test = np.zeros([DHFI.shape[1], DHFI.shape[2], 3])

    for x in range(DHFI.shape[1]):
        for y in range(DHFI.shape[2]):
            if(DHFI[0,x,y] <= 0.1):
                test[x,y,:] = [23,0,128]
            if(DHFI[0,x,y] > 0.1 and DHFI[0,x,y] <= 0.2):
                test[x,y,:] = [22,0,229]
            if(DHFI[0,x,y] > 0.2 and DHFI[0,x,y] <= 0.3):
                test[x,y,:] = [61,240,16]
            if(DHFI[0,x,y] > 0.3 and DHFI[0,x,y] <= 0.4):
                test[x,y,:] = [106,175,45]
            if(DHFI[0,x,y] > 0.4 and DHFI[0,x,y] <= 0.5):
                test[x,y,:] = [254,254,1]
            if(DHFI[0,x,y] > 0.5 and DHFI[0,x,y] <= 0.6):
                test[x,y,:] = [248,218,66]
            if(DHFI[0,x,y] > 0.6 and DHFI[0,x,y] <= 0.7):
                test[x,y,:] = [255,166,1]
            if(DHFI[0,x,y] > 0.7 and DHFI[0,x,y] <= 0.8):
                test[x,y,:] = [255,1,9]
            if(DHFI[0,x,y] > 0.8 and DHFI[0,x,y] <= 0.9):
                test[x,y,:] = [169,16,22]
            if(DHFI[0,x,y] > 0.9):
                test[x,y,:] = [103,0,13]

    kwargs = dataset_meta
    kwargs.update(
        count = 3,
        dtype=rasterio.int8,
        compress='lzw')
    
    test = test.astype(int)
    test_b = test.transpose(2,0,1)

    with rasterio.open(f'./Output/PNG/DHFI_RGB_{date_DHFI}.png', 'w', **kwargs) as dstC:
        dstC.write(test_b)
    
    plt.imshow(test)
    plt.show()
            
            
                



