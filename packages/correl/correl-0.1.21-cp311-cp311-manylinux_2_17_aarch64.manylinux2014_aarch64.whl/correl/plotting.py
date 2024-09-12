#!/usr/bin/python
"""
Python module for various plotting helpers to display
generalized susceptibility matrices.
"""
import numpy as np
import scipy as sp
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def cdict_cw(points = 1_001):
    """
    returns:
        colormap dictionary inspired by Patrick Chalupa: the colormap
        is a sequential blue-white-red map and enhances the visibility
        of small deviations from the central value
    """
    half = points//2
    cp = np.linspace(0,1,points,endpoint=True)
    cf = np.linspace(0,1,points//2,endpoint=True)
    cf_inv = (1-(1-cf)**2)/2

    gr_p = np.zeros(points)
    gr_p [:half]=cf_inv
    gr_p [half]=0.5
    gr_p [half+1:]=1-cf_inv[::-1]

    green = np.zeros(points)
    blue = np.zeros(points)
    red = np.zeros(points)

    green[:half]= cf
    green[half]= 1
    green[half+1:]= cf[::-1]
    red[half]= 1
    red[half+1:]= 1-cp[1:half+1]/2
    blue[half]= 1
    blue[:half]= 1-cp[1:half+1][::-1]/2


    Gn = np.column_stack((gr_p[:],green[:],green[:]))
    Rd = np.column_stack((cp[:],red[:],red[:]))
    Bu = np.column_stack((cp[:],blue[:],blue[:]))

    return  {'green':  Gn,
             'blue':  Bu,
             'red':  Rd}


def cdict_gr(points = 1_001):
    """
    returns:
        colormap dictionary: the colormap is a sequential 
        green-brown-red map and enhances the visibility
        of small deviations from the central value
    """
    half = points//2
    cp = np.linspace(0,1,points,endpoint=True)

    green = np.zeros(points)
    blue = np.zeros(points)
    red = np.zeros(points)

    #green[:half]= (1-2.*cp[:half])**(1/2)
    #green[half]=green[half-1]/2
    #red[half+1:]= 0.25+(np.array(1.-2*cp[:half])[::-1])**(1/2)
    #red[half]= red[half+1]/2
    #blue[np.where(red>1)]= red[np.where(red>1)]-1.
    #red[np.where(red>1)] = 1.
    green[:]= (1.105+(1-2.*cp[:]))/2.105
    green[np.where(green<0)]=0
    red[:]= (4+(np.array(1-2*cp[:])[::-1]))/5
    red[np.where(red>1)] = 1.
    red[np.where(red<0)]= 0
    blue[:half+1] = 2*cp[:half+1]*0.247
    blue[half:] = 2*cp[half::-1]*0.247

    Gn = np.column_stack((cp[:],green[:],green[:]))
    Rd = np.column_stack((cp[:],red[:],red[:]))
    Bu = np.column_stack((cp[:],blue[:],blue[:]))

    return  {'green':  Gn,
             'blue':  Bu,
             'red':  Rd}

def cdict_gy(points = 1_001):
    """
    returns:
        colormap dictionary: the colormap is a sequential 
        green-black-yellow map and enhances the visibility
        of small deviations from the central value
    """
    half = points//2
    cp = np.linspace(0,1,points)

    green = np.zeros(points)
    blue = np.zeros(points)
    red = np.zeros(points)

    green[:half]= (1-2.*cp[:half])**(1/7)
    green[half+1:]= 0.8*(1-2.*cp[:half][::-1])**(1/7)
    green[half] = 0.
    red[half]= 0.
    red[half+1:]= 0.25+(np.array(1.-2*cp[:half])[::-1])**(1/7)
    blue[np.where(red>1)]= red[np.where(red>1)]-1.
    red[np.where(red>1)] = 1.


    Gn = np.column_stack((cp[:],green[:],green[:]))
    Rd = np.column_stack((cp[:],red[:],red[:]))
    Bu = np.column_stack((cp[:],blue[:],blue[:]))


    return  {'green':  Gn,
             'blue':  Bu,
             'red':  Rd}

def cmap_gy(points = 10_001):
    """
    returns:
        sequential green-black-yellow colormap with enhanced visibility
        of small deviations from the central value
    """
    return mpl.colors.LinearSegmentedColormap('reitner_gy',
                                              segmentdata = cdict_gy()
                                              ,N=points).reversed()

def cmap_gr(points = 10_001):
    """
    returns:
        sequential green-brown-red colormap with enhanced visibility
        of small deviations from the central value
    """
    return mpl.colors.LinearSegmentedColormap('reitner_gr',
                                              segmentdata = cdict_gr()
                                              ,N=points).reversed()
def cmap_w(points = 10_001):
    """
    returns:
        sequential blue-white-red colormap with enhanced visibility
        of small deviations from the central value
        Inspired by Patrick Chalupa
    """
    return mpl.colors.LinearSegmentedColormap('chalupa_white',
                                              segmentdata = cdict_cw()
                                              ,N=points)
def cmap_w_old(points = 10_000):
    # -------------------------------------
    # colormap inspired by Patrick Chalupa
    # -------------------------------------
    cdict_white = {'blue':  [[0.0, 0.6, 0.6],
                       [0.499, 1.0, 1.0],
                       #[0.5, 0.0, 0.0],
                       [0.5, 1.0, 1.0],
                       [0.501, 0.0, 0.0],
                       [1.0, 0., 0.]],
             'green': [[0.0, 0.0, 0.0],
                       [0.02631578947368421, 7.673360394717657e-06, 7.673360394717657e-06],
                       [0.05263157894736842, 0.00012277376631548252, 0.00012277376631548252],
                       [0.07894736842105263, 0.0006215421919721302, 0.0006215421919721302],
                       [0.10526315789473684, 0.0019643802610477203, 0.0019643802610477203],
                       [0.13157894736842105, 0.004795850246698536, 0.004795850246698536],
                       [0.15789473684210525, 0.009944675071554084, 0.009944675071554084],
                       [0.18421052631578946, 0.018423738307717093, 0.018423738307717093],
                       [0.21052631578947367, 0.031430084176763524, 0.031430084176763524],
                       [0.23684210526315788, 0.050344917549742546, 0.050344917549742546],
                       [0.2631578947368421, 0.07673360394717657, 0.07673360394717657],
                       [0.2894736842105263, 0.11234566953906126, 0.11234566953906126],
                       [0.3157894736842105, 0.15911480114486534, 0.15911480114486534],
                       [0.3421052631578947, 0.21915884623353094, 0.21915884623353094],
                       [0.3684210526315789, 0.2947798129234735, 0.2947798129234735],
                       [0.39473684210526316, 0.3884638699825815, 0.3884638699825815],
                       [0.42105263157894735, 0.5028813468282164, 0.5028813468282164],
                       [0.4473684210526315, 0.6408867335272133, 0.6408867335272133],
                       [0.47368421052631576, 0.8055186807958807, 0.8055186807958807],
                       [0.499, 1.0, 1.0],
                       #[0.5, 0.0, 0.0],
                       [0.5, 1.0, 1.0],
                       [0.501, 1.0, 1.0],
                       [0.5263157894736843, 0.8055186807958807, 0.8055186807958807],
                       [0.5526315789473685, 0.6408867335272133, 0.6408867335272133],
                       [0.5789473684210527, 0.5028813468282164, 0.5028813468282164],
                       [0.6052631578947368, 0.3884638699825815, 0.3884638699825815],
                       [0.631578947368421, 0.2947798129234735, 0.2947798129234735],
                       [0.6578947368421053, 0.21915884623353094, 0.21915884623353094],
                       [0.6842105263157895, 0.15911480114486534, 0.15911480114486534],
                       [0.7105263157894737, 0.11234566953906126, 0.11234566953906126],
                       [0.736842105263158, 0.07673360394717657, 0.07673360394717657],
                       [0.7631578947368421, 0.050344917549742546, 0.050344917549742546],
                       [0.7894736842105263, 0.031430084176763524, 0.031430084176763524],
                       [0.8157894736842105, 0.018423738307717093, 0.018423738307717093],
                       [0.8421052631578947, 0.009944675071554084, 0.009944675071554084],
                       [0.868421052631579, 0.004795850246698536, 0.004795850246698536],
                       [0.8947368421052632, 0.0019643802610477203, 0.0019643802610477203],
                       [0.9210526315789473, 0.0006215421919721302, 0.0006215421919721302],
                       [0.9473684210526316, 0.00012277376631548252, 0.00012277376631548252],
                       [0.9736842105263158, 7.673360394717657e-06, 7.673360394717657e-06],
                       [1.0, 0.0, 0.0]],
             'red':   [[0.0, 0., 0.],
                       [0.499, 0.0, 0.0],
                       [0.5, 1.0, 1.0],
                       #[0.5, 0.0, 0.0],
                       [0.501, 1.0, 1.0],
                       [1.0, 0.6, 0.6]]}

    return mpl.colors.LinearSegmentedColormap('chalupa_white',segmentdata = cdict_white,N=points)

# ---------------------------------------
# normalize colormap around zero value
# ---------------------------------------
class norm(mpl.colors.Normalize):
    """
    class to normalize matplotlib colorbar around midpoint from stackoverflow

    attributes:
        matrix (float, array) array to calculate colormap norm
        midpoint (float, optional) midpoint
        clip (bool, optional)

    """
    def __init__(self, matrix, midpoint=0, clip=False):
        # normalize only real part
        M= np.real(matrix)
        vmin = np.amin(M)
        vmax = np.amax(M)
        self.midpoint = midpoint
        mpl.colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        """
        args:
            value (float)
            clip (optional)
        
        returns:
            masked array for colorbar normalization
        """
        if self.vmax == 0:
            normalized_min = 0
        else:
            normalized_min = max(0, 1 / 2 * (1 - abs((self.midpoint - self.vmin) \
                                                     / (self.midpoint - self.vmax))))
        if self.vmin == 0:
            normalized_max = 1
        else:
            normalized_max = min(1, 1 / 2 * (1 + abs((self.vmax - self.midpoint) \
                                                     / (self.midpoint - self.vmin))))
        normalized_mid = 0.5
        x = [self.vmin, self.midpoint, self.vmax] 
        y = [normalized_min, normalized_mid, normalized_max]
        return np.ma.masked_array(np.interp(value, x, y))

#--------------------
# matplotlib plotting
#--------------------
def plot_X(chi,beta=None,cmap='cmap_w',figsize=(8,3.5)):
    fig, axs = plt.subplots(1,2,figsize=figsize)

    Niwf = chi.shape[0]//4
    ticks =  np.linspace(-2*Niwf,2*Niwf,9)
    labelsf = np.concatenate((np.linspace(-Niwf,Niwf,5)[:-1],
                              np.linspace(-Niwf,Niwf,5)))
    labels = ["{:g}".format(a) for a in labelsf]

    plt.setp(axs, xticks=ticks, xticklabels=labels,
        yticks=ticks,yticklabels=labels)
    
    extent=[-2*Niwf,2*Niwf,2*Niwf,-2*Niwf]
    ns = np.linspace(-Niwf,Niwf,Niwf)

    axs[0].set_ylabel(r"$\nu_n$")
    axs[0].set_xlabel(r"$\nu'_n$")
    axs[0].set_title('Re')
    c0 = axs[0].imshow(chi.real,
                    cmap=globals()[cmap](),
                    vmin=-np.amax(chi.real), 
                    vmax=np.amax(chi.real),
                    interpolation='nearest',
                    aspect='equal',
                    extent=extent
                    )

    axs[0].axvline(color='black',lw=0.5)
    axs[0].axhline(color='black',lw=0.5)
    div0 = make_axes_locatable(axs[0])
    cax0 = div0.append_axes('right', size='5%', pad=0.05)
    fig.colorbar(c0,cax=cax0)
    

    axs[1].set_title('Im')
    axs[1].set_xlabel(r"$\nu'_n$")
    c1 = axs[1].imshow(chi.imag,
                    cmap=globals()[cmap](),
                    interpolation='nearest',
                    vmin=-np.amax(chi.imag), 
                    vmax=np.amax(chi.imag),
                    aspect='equal',
                    extent=extent
                    )
    axs[1].axvline(color='black',lw=0.5)
    axs[1].axhline(color='black',lw=0.5)
    div1 = make_axes_locatable(axs[1])
    cax1 = div1.append_axes('right', size='5%', pad=0.05)
    axs[1].axes.yaxis.set_ticklabels([]) # ausblenden der y labels
    fig.colorbar(c1,cax=cax1)
    fig.subplots_adjust(bottom=0.2)
    #plt.show()
    return fig, axs

def eig_analysis(matrix,indx,option=None,cmplx_offset=1e-4):
    ee,ev = np.linalg.eig(matrix)
    index = np.argsort(ee)
    where_real = np.where(abs(ee.imag)<cmplx_offset)
    where_cmplx = np.where(abs(ee.imag)>=cmplx_offset)
    if option is None:
        ii = index[indx]
    elif option == 'real':
        real_index = index[np.where(np.isin(index,where_real))]
        ii = real_index[indx]
    elif option == 'cmplx':
        cmplx_index = index[np.where(np.isin(index,where_cmplx))]
        ii = cmplx_index[indx]
    else: 
        ii = 0
    ov = ev/np.sqrt(np.diag(ev.T@ev))
    box = matrix.shape[0]//2
    ws_sort = np.sum(ov[:box,ii]*ov[:box,ii])
    weigth_s = np.sum(ov[:box,ii])*np.sum(ov[:box,ii])
    wc_sort = np.sum(ov[box:,ii]*ov[box:,ii])
    weigth_c = np.sum(ov[box:,ii])*np.sum(ov[box:,ii])
    pc_sort = abs(wc_sort)/(abs(ws_sort) + abs(wc_sort))
    ps_sort = abs(ws_sort)/(abs(ws_sort) + abs(wc_sort))
    spincharge = ps_sort-pc_sort
    ticks =  np.linspace(0,2*box,9)
    Niwf= box//2
    labelsf = np.concatenate((np.linspace(-Niwf,Niwf,5)[:-1],
                                np.linspace(-Niwf,Niwf,5)))
    labels = ["{:g}".format(a) for a in labelsf]

    ff, ax = plt.subplots(1,2)
    ff.suptitle(f'$\\alpha = {indx}$')
    ax[0].plot(ov[:,ii].real,'-',label='Re$V_\\alpha(\\nu)$')
    ax[0].plot(ov[:,ii].imag,'--',label='Im$V_\\alpha(\\nu)$')
    ax[0].axvline(box,color='black',lw=1)
    ax[0].set_xticks(ticks)
    ax[0].set_xticklabels(labels)
    ax[0].set_xlabel('spin $\\nu$ charge')
    ax[0].legend()

    ax[1].scatter(ee.real,ee.imag,marker='.',color='0.7')
    s = ax[1].scatter(ee[ii].real,ee[ii].imag, c = spincharge, 
                        cmap=cmap_gr(),vmin=-1, vmax=1)
    cbar = plt.colorbar(s)
    cbar.set_label("charge - spin")
    ax[1].axhline(color='black',lw=1)
    ax[1].axvline(color='black',lw=1)
    ax[1].set_xlabel('Re$\\lambda_\\alpha$')
    ax[1].set_ylabel('Im$\\lambda_\\alpha$')
    plt.tight_layout()

    Nee = np.sum(np.where(ee<0))
    real = ee[where_real]
    cmplx = ee[where_cmplx]
    try:
        max_imag = np.amax(cmplx.imag)
    except ValueError:
        max_imag = 1

    cmplx_interset = cmplx[np.where(cmplx.imag>=max_imag/2)]


    print('eig[indx]:',ee[ii], 'spincharge:',spincharge,
          'spin_w:',ws_sort, 'charge_w:',wc_sort)
    print('real eig:') 
    print(np.sort(np.real(real)))
    print('interesting cmplx eig:')
    print(np.sort(cmplx_interset))
    print('#Re(lamda)<0:', np.sum(np.where(ee.real<0)))
    print('#Re(lamda)<0 and Im<10E-5:',
           np.sum(np.logical_and(ee.real<0, abs(ee.imag)<1e-5)))
    print('weight spin:', weigth_s)
    print('weight charge:', weigth_c)
    return ff