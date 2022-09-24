'''
2022-9-21
This code paint spinup data
var is global ts and global ps
'''
def paint_spinup():
    import numpy as np
    import matplotlib.pyplot as plt

    src_path  =  '/home/sun/data/model_data/spin-up/'
    fname1    =  'spinup_TS.npy'

    f0        =  np.load(src_path + fname1,allow_pickle=True)

    labels    =  ['control','indian','inch','global1m','maritime']

    fig    =  plt.figure()
    ax     =  fig.add_subplot(111)

    ax.plot(f0[0],color='k',label='B1850 CTRL')
    ax.plot(f0[1],color='c',label='INDIAN')
    ax.plot(f0[2],color='m',label='INCH')
    ax.plot(f0[3],color='y',label='GLOBAL 1m')
    ax.plot(f0[4],color='blue',label='MARITIME')

    ax.legend(loc='upper left')

    ax.set_ylabel("TS")
    ax.set_xlabel("year")

    plt.savefig('/home/sun/paint/b1850_exp/spinup/spin-TS.pdf', bbox_inches='tight',dpi=1200)

def main():
    paint_spinup()

if __name__ == '__main__':
    main()