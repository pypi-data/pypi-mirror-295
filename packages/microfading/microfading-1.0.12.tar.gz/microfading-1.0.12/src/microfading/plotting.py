import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import colour
from typing import Optional, Union


def spectra(data, stds=[], labels=[], title='none', fontsize=24, fontsize_legend:Optional[int] = 22, x_range=(), colors:Union[str, list] = None, lw:Optional[int] = 2, ls:Union[str, list] = '-', text:Optional[str] = '', save=False, path_fig='cwd', derivation="none", *args, **kwargs):
    """
    Description: Plot the reflectance spectrum of one or several datasets.

    
    Args:
        _ data (list): A list of data elements, where each element corresponding to a reflectance spectrum is a numpy array. 

        _ std (list, optional): A list of standard variation values respective to each element given in the data parameter. Defaults to [].

        _ labels (list, optional): A list of labels respective to each element given in the data parameter that will be shown in the legend. When the list is empty there is no legend displayed. Defaults to [].
        
        _ title (str, optional): Suptitle of the figure. When 'none' is passed as an argument, there is no suptitle displayed. Defaults to 'none'.
        
        _ color_data (str or list, optional): Color of the data points. When 'sample' is passed as an argument, the color will correspond to the srgb values of the sample. A list of colors - respective to each element given in the data parameter - can be passed. Defaults to 'sample'.
        
        _ fs (int, optional): Fontsize of the plot (title, ticks, and labels). Defaults to 24.    

        _ x_range (tuple, optional): Lower and upper limits of the x-axis. Defaults to (). 

        

    
    Returns: A figure showing the reflectance spectra.
    """
    data = data
    
    # Set the observer and illuminant
    observer = colour.colorimetry.MSDS_CMFS_STANDARD_OBSERVER["CIE 1964 10 Degree Standard Observer"] 
    illuminant = colour.SDS_ILLUMINANTS['D65'] 
    d65 = colour.CCS_ILLUMINANTS["cie_10_1964"]["D65"]
    
    # Create the figure
    sns.set_theme(context='paper', font='serif', palette='colorblind')
    fig, ax = plt.subplots(1,1, figsize=(15, 9))
    
    # Set the list of labels
    if len(labels) == 0:
        labels = ['none'] * len(data)

    # Set the list of colors
    if colors == None:
        colors = [None] * len(data)
    
    elif colors == 'sample':
        colors = ['sample'] * len(data)

    # Set the linestyle
    if isinstance(ls, str):
        ls = [ls] * len(data)

    # Set the linewidth
    if isinstance(lw, int):
        lw = [lw] * len(data)
         
    # Initiate a for loop to plot the data
    
    for i, d in enumerate(data):

        df_sp = pd.DataFrame(data=d[1], index=d[0])

        # Index data according the x_range values
        if x_range not in [(), None]:            
            df_sp = df_sp.loc[x_range[0]:x_range[1]]

        # Get the wavelengths and spectral values
        wl = df_sp.index.values
        sp = df_sp.iloc[:,0].values

        
        if colors[i] == 'sample':                      
            sd = colour.SpectralDistribution(sp,wl)  
            XYZ = colour.sd_to_XYZ(sd,observer, illuminant=illuminant) 
            srgb = colour.XYZ_to_sRGB(XYZ / 100, illuminant=d65).clip(0, 1)
            color = np.array(srgb)           
        
        else:
            color = colors[i]
            

        
        ax.plot(wl,sp, color=color, lw=lw[i], ls=ls[i], label=labels[i])
        
            
    
    if x_range not in [(), None]:
        ax.set_xlim(x_range[0],x_range[1])
    
    ax.set_xlabel('Wavelength $\lambda$ (nm)', fontsize = fontsize)

    if derivation == "none":
        ax.set_ylabel('Reflectance factor', fontsize = fontsize)
    elif derivation == "first":
        ax.set_ylabel(r'$\frac{dR}{d\lambda}$', fontsize = fontsize+10)

    ax.xaxis.set_tick_params(labelsize = fontsize)
    ax.yaxis.set_tick_params(labelsize = fontsize)

    if title != 'none':
        ax.set_title(title, fontsize = fontsize+3)
    
    if len(labels) > 6:
        ncols = 2
    else:
        ncols = 1

    if labels[0] != 'none' and len(labels) < 19:
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))  
        #plt.legend(labels, fontsize=fontsize_legend, title='Measurement $n^o$', title_fontsize=fontsize_legend) 
        plt.legend(by_label.values(), by_label.keys(), ncol=ncols, fontsize=fontsize_legend, title='Measurement $n^o$', title_fontsize=fontsize_legend)

    
    if text != '':
        props = dict(boxstyle='round', facecolor='white', alpha=0.7)
        ax.text(0.01,0.05,text,transform=ax.transAxes,fontsize=fontsize-6,verticalalignment='top', bbox=props)
            

    plt.tight_layout()
    plt.show()