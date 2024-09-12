
import matplotlib.pyplot as plt
import datetime
from hjnwtx.colormap import cmp_hjnwtx
import os
import numpy as np
 


def drawimg(array_dt,temp = "temp"):
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    if len(array_dt.shape)==3:
        for i , img_ch_nel in enumerate(array_dt): 
            plt.imshow(img_ch_nel,vmin=0,vmax=100,cmap=cmp_hjnwtx["radar_nmc"])
            plt.colorbar()
            outpath = f"./radar_nmc/{temp}_{now_str}.png"
            mkDir(outpath)
            plt.savefig(outpath)
            plt.close()
    if len(array_dt.shape)==2:
            plt.imshow(array_dt,vmin=0,vmax=100,cmap=cmp_hjnwtx["radar_nmc"])
            plt.colorbar()
            outpath = f"./radar_nmc/{temp}_{now_str}.png"
            os.makedirs(outpath, exist_ok=True)
            mkDir(outpath)
            plt.savefig(outpath)
            plt.close()  

def mkDir(path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)

def drawimg_coor(array_dt, temp="temp"):
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    y_coords2, x_coords2 = np.where(array_dt > 0)
    
    def plot_and_save(image, path):
        plt.imshow(image, vmin=0, vmax=10, cmap=cmp_hjnwtx["radar_nmc"])
        for (x, y) in zip(x_coords2, y_coords2):
            plt.plot(x, y, 'ro', markersize=25)  # Increase point size
            plt.text(x, y, f'{(image[y, x] * 6):.1f}', color='white', fontsize=12, ha='center', va='center')  # Label the corresponding value
        plt.colorbar()
        os.makedirs(path, exist_ok=True)
        plt.savefig(path)
        plt.close()    
    if len(array_dt.shape) == 3:
        for i, img_ch_nel in enumerate(array_dt): 
            plot_and_save(img_ch_nel, f"./radar_nmc/{temp}_{now_str}.png")
    elif len(array_dt.shape) == 2:
        plt.imshow(array_dt, vmin=0, vmax=100, cmap=cmp_hjnwtx["radar_nmc"])
        plot_and_save(array_dt, f"./radar_nmc/{temp}_{now_str}.png")
