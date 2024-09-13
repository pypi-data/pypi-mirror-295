import matplotlib.pyplot as plt
import numpy as np
from math import pi,sqrt,gcd
from matplotlib.patches import Rectangle
from crystals import Crystal
from utils.glob_colors import*
import utils.displayStandards as dsp
import utils.handler3D as h3d

cs = {1:unicolor(0.75),3:(1,0,0),6:unicolor(0.25),7:(0,0,1),8:(1,0,0),16:(1,1,0)}

wbs = np.array([1,3,6,7,8,10])*0.01
wobbles = dict(zip([1,3,6,7,8,16],wbs))
Rot = lambda a:np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])

##########################################################################
# orient crystal along n_u
def orient_crystal(coords,ez=[0,0,1],n_u=[0,0,1],T=True,theta=0):
    ''' Rotate the object so that n_u becomes e_z [1] :\n
    - coords : 3xN (or Nx3 array if T=True)
    - n : axis to align e_z against
    - T : transpose if True (input is Nx3)
    [1] [rotation matrix from axis and angle](https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle)
    '''
    e_z,n = np.array(ez)/np.linalg.norm(ez),np.array(n_u)/np.linalg.norm(n_u)
    n_not_ez = np.linalg.norm(n-e_z)
    if n_not_ez:
        u,ct = np.cross(n,e_z), np.dot(e_z,n)
        u /= np.linalg.norm(u)
        st = np.sqrt(1-ct**2)
        ux,uy,uz = u
        ux2,uy2,uz2 = u**2
        R = np.array([
            [ct+ux2*(1-ct), ux*uy*(1-ct)-uz*st, ux*uz*(1-ct)+uy*st ],
            [uy*ux*(1-ct)+uz*st, ct+uy2*(1-ct), uy*uz*(1-ct)-ux*st ],
            [uz*ux*(1-ct)-uy*st, uz*uy*(1-ct)+ux*st, ct+uz2*(1-ct) ],
            ])
        if T :
            coords = R.dot(coords.T).T
        else:
            coords = R.dot(coords)
    if theta :
        t = np.deg2rad(theta)
        st,ct = np.sin(t),np.cos(t)
        if T :
            coords = np.array([[ct,st,0],[-st,ct,0],[0,0,1]]).dot(coords.T).T
        else:
            coords = np.array([[ct,st,0],[-st,ct,0],[0,0,1]]).dot(coords)
    return coords


def get_crystal_rotation(u=None,omega=0,eo='z',alpha=0):
    '''Return the rotation matrix of alpha about u
    - alpha : float - rotation angle
    - u     : [ux,uy,uz] - rotation axis
    - omega : float - angle of rotation of the rotation axis
    - eo    : 'x','y','z' - normal plane to the rotation for computing u from omega
    '''
    omega,alpha = np.deg2rad(omega),np.deg2rad(alpha)
    if not u:
        if   eo=='x':u = [0,np.cos(omega),np.sin(omega)]
        elif eo=='y':u = [np.cos(omega),0,np.sin(omega)]
        elif eo=='z':u = [np.cos(omega),np.sin(omega),0]
    u = np.array(u)
    ux,uy,uz = u
    ux2,uy2,uz2 = u**2
    ct,st = np.cos(alpha),np.sin(alpha)
    R = np.array([
            [ct+ux2*(1-ct), ux*uy*(1-ct)-uz*st, ux*uz*(1-ct)+uy*st ],
            [uy*ux*(1-ct)+uz*st, ct+uy2*(1-ct), uy*uz*(1-ct)-ux*st ],
            [uz*ux*(1-ct)-uy*st, uz*uy*(1-ct)+ux*st, ct+uz2*(1-ct) ],
            ])
    return R

# rotate crysral for periodic run
def rotate_xyz(file,nx,nz,Nx=40,Nz=5,name='',opt='',**kwargs):
    '''Generates .xyz files corresponding to individual rotation
    - file : path to cif file (.xyz files will be put in the same folder )
    - Nrot : number of rotation to perform within 0,pi/2
    '''
    crys = file
    if isinstance(file,str):
        crys = Crystal.from_cif(file)
        if not name : name = file.replace('.cif','')

    a1,a2,a3    = np.array(crys.lattice_vectors)
    ax1,by2,cz3 = np.array(crys.lattice_parameters[:3])
    nxz   = int(cz3/ax1)
    #int(nx.max()+nxz*nz.max()), int(nx.max()/nxz+nz.max())
    xy0   = (0,(Nz-nz.max())*cz3)
    print('super cell calculation ...')
    crys0   = crys.supercell(Nx,1,Nz)
    pattern = np.array([
        [a.atomic_number]+list(a.coords_cartesian)+[a.occupancy,wobbles[a.atomic_number]] for a in crys0.atoms])
    coords0 = np.array([a.coords_cartesian for a in crys0.atoms])

    files = []
    Cs = [cs[E] for E in pattern[:,0]]
    for i1,i2 in zip(nx,nz):
        # i1,i2 = i,Nrot-i; n0 = gcd(i1,i2)
        # i1,i2 = i1/n0,i2/n0;#print(i1,i2)
        cz = i1*a1+i2*a3; #print(cz)
        ax = np.array([cz[1],-cz[0]]); #print(cz)
        c,angle = np.linalg.norm(cz),np.arctan(cz[0]/cz[2])
        if not i1%i2*nxz:
            n0 = i1/gcd(i1,i2*nxz)
            if not n0%2 : n0/=2
            a = np.linalg.norm([i2*nxz/i1,1])*cz3*n0
        else:
            a = np.linalg.norm([i2*nxz,i1])*cz3
        # a = np.linalg.norm([i2*nxz,i1])*cz3

        print(green+'i1=%d,i2=%d,angle=%.2f' %(i1,i2,angle*180/np.pi)+black)
        rect=Rectangle(xy0,1.0*a,1.0*c,angle=-angle*180/np.pi,edgecolor='k',linewidth=2,alpha=0.1)
        print('finding points ...')
        idc = rect.contains_points(coords0[:,[0,2]],radius=0.001)
        print('done')
        n   = (i1,0,i2)
        xyz = name+'%d%d%d.xyz' %n
        if opt:
            path = dsp.dirname(name)

            x,z = coords0[:,[0,2]].T;
            x0,z0 = (coords0[idc,:])[:,[0,2]].T
            X,Z = np.hstack([x,x0]),np.hstack([z,z0])
            S = np.array([10]*x.size+[30]*x0.size)
            C = Cs+list(np.array(Cs)[idc,:])
            dsp.stddisp(scat=[X,Z,S,C],patches=[rect],equal=1,figsize='12',
                xyTicks=[ax1,cz3],pOpt='tGeX',xylims=[0,40*ax1,-10*cz3,10*cz3],
                opt=opt,name=path+'figures/'+dsp.basename(xyz).replace('xyz','png'))
            plt.show()

        lat_vec = [a,a2[1],c]#np.array([Nrot*(a3+a1),a2,Nrot*(a3-a1)])#
        cc = coords0[idc,:]
        cc[:,2]-=xy0[1]
        coords  = Rot(-angle).dot(cc.T).T
        pattern[idc,1:4] = coords
        # make_xyz(xyz,pattern[idc,:],np.diag(lat_vec),n,fmt='%.4f',dopt='s')
        files+=[xyz] #dsp.basename(xyz)]
    return files


##########################################################################
#unit cell display
##########################################################################
def show_grid(file,opt='',**kwargs):
    with open(file,'r') as f:l=list(map(lambda s:s.strip().split(' '),f.readlines()))
    pattern = np.array(l[2:-1],dtype=float)
    a1,a2,a3 = np.array(l[1],dtype=float)
    #a1,a2,a3,alpha,beta,gamma=crys.lattice_parameters
    if opt:
        Z,x,y,z = pattern[:,:4].T
        Z = np.array(Z,dtype=int)
        C = [cs[E] for E in Z]
        pps = [Rectangle((0,0),a1,a3,linewidth=2,edgecolor='b',alpha=0.1)]

        fig,ax = dsp.stddisp(labs=['$x$','$z$'],patches=pps,scat=[x,z,C],ms=50,
            opt=opt,**kwargs)
    return [a1,a2,a3],pattern
    # a,b,angle=a3,a1,beta
    # lat_vec = lattice.get_lattice_vec('oblique',a=a,b=b,alpha=angle,v=0)
    # lattice.plot_lattice(lat_vec,opts='',nh=3,nk=3,
    #     ax=ax,labs=['$z$','$x$'],lw=2,
    #     pOpt='tG',pad=1,xyTicks=[1.5,5.0],xylims=[-6,15,0,21])#,xyTicksm=1.0,xylims=[0,100,0,100])

def show_unit_cell(ax,n=[0,0,1],ez=[0,0,1],a=0.2,c='b',lw=2,ls='-',lat_params=[1,1,1]):
    '''Orthorombic unit cell from lattice parameters  '''
    Xfaces = get_cubic_cell_mesh(lat_params)
    #change cube orientation and plot
    for X,i in zip(Xfaces,range(len(Xfaces))) :
        x,y,z = X
        coords = np.array([x,y,z]).reshape(3,4).T
        coords = orient_crystal(coords,n_u=n,ez=ez)
        x,y,z  = coords.T.reshape(3,2,2)
        Xfaces[i] = [x,y,z]
        ax.plot_surface(x,y,z,color=c,alpha=a+(i==0)*0.2,linestyle=ls,linewidth=lw,edgecolor=c)
    #cube diagonals
    # (x0,x1),(y0,y1),(z0,z1) = np.array(Xfaces[0])[:,:,0]
    # (x2,x3),(y2,y3),(z2,z3) = np.array(Xfaces[3])[:,:,1]
    # ax.plot([x0,x3],[y0,y3],[z0,z3],'--',color=dsp.unicolor(0.5))
    # ax.plot([x1,x2],[y1,y2],[z1,z2],'--',color=dsp.unicolor(0.5))

def get_cubic_cell_mesh(lat_params,opt=0):
    a1,a2,a3 = lat_params
    #Cube faces
    (x00,y00),z00 = np.meshgrid([0,a1],[0,a2]), np.zeros((2,2))
    (x10,z10),y10 = np.meshgrid([0,a1],[0,a3]), np.zeros((2,2))
    (y20,z20),x20 = np.meshgrid([0,a2],[0,a3]), np.zeros((2,2))
    (x01,y01),z01 = np.meshgrid([0,a1],[0,a2]), np.ones((2,2))*a3
    (x11,z11),y11 = np.meshgrid([0,a1],[0,a3]), np.ones((2,2))*a2
    (y21,z21),x21 = np.meshgrid([0,a2],[0,a3]), np.ones((2,2))*a1
    if opt:
        Xfaces = [  np.array([x00,x10,x20,x01,x11,x21]),
                    np.array([y00,y10,y20,y01,y11,y21]),
                    np.array([z00,z10,z20,z01,z11,z21]),]
    else:
        Xfaces = [[x00,y00,z00],[x10,y10,z10],[x20,y20,z20],
                  [x01,y01,z01],[x11,y11,z11],[x21,y21,z21]]

    return Xfaces



##########################################################################
# misc
##########################################################################
def show_diffraction_planes(r0=1,h=2,npts=10,**kwargs):
    '''Generates the rotation figure'''
    n10,n01,n11,u = [1,0],[0,1],np.array([1,-1])/sqrt(2),[0,0,1]
    Xc0,Yc0,Zc0=get_cylinder(0,pi/2 ,r0,h,npts)
    Xc1,Yc1,Zc1=get_cylinder(pi,3*pi/2,r0,h,npts)
    Xp10,Yp10,Zp10=get_plane(n10,u,w=2*r0,h=h)
    Xp01,Yp01,Zp01=get_plane(n01,u,w=2*r0,h=h)
    Xp11,Yp11,Zp11=get_plane(n11,u,w=2*r0,h=h)
    fig,ax=dsp.stddisp(rc='3d',legOpt=0)
    ax.plot_surface(Xc0, Yc0, Zc0, color='b', alpha=0.2)#,edgecolor='b',linewidth=2)#
    ax.plot_surface(Xc1, Yc1, Zc1, color='b', alpha=0.2 )#,edgecolor='b',linewidth=2)#
    ax.plot_surface(Xp10, Yp10, Zp10, color='b', alpha=0.2,linewidth=2,edgecolor='b'   )#
    ax.plot_surface(Xp01, Yp01, Zp01, color='b', alpha=0.2,linewidth=2,edgecolor='b'   )#
    ax.plot_surface(Xp11, Yp11, Zp11, color='r', alpha=0.4,linewidth=2,edgecolor='r'   )#
    ax.plot([0,0],[0,0],[-h/2,h/2],color ='k',linewidth=2)

    W = 0.75*max(2*r0,h)
    xylims = [-W/2,W/2,-W/2,W/2,-W/2,W/2]
    dsp.standardDisplay(ax,xylims=xylims,axPos=[0,0,1,1],setPos=1,is_3d=1,gridOn=0,ticksOn=0,legOpt=0,**kwargs)

def get_plane(n=[1,0,0],u=[0,1,0],w=1,h=1,x0=[0,0,0]):
    x,y = np.meshgrid([-w/2,w/2],[-h/2,h/2])
    u1,u2 = u,np.cross(n,u)
    Xp = x*u1[0] + y*u2[0] + x0[0]
    Yp = x*u1[1] + y*u2[1] + x0[1]
    Zp = x*u1[2] + y*u2[2] + x0[2]
    return Xp,Yp,Zp

def get_cylinder(ti,tf,r0=1,h=1,npts=10,x0=[0,0,0]):
    t,z,h2 = np.linspace(ti,tf,npts),np.array([-1,1])[:,None],h/2
    Xc = r0*np.tile(np.cos(t),[2,1])  + x0[0]
    Yc = r0*np.tile(np.sin(t),[2,1])  + x0[1]
    Zc = h2*np.tile(z,[1,npts]) + x0[2]
    return Xc,Yc,Zc



########################################################################
# def : tests
########################################################################
def bcc_coords():
    (x,y,z),xc  = np.meshgrid([0,1],[0,1],[0,1]), [0.5,0.5,0.5] #bcc
    coords = np.array([x.flatten(),y.flatten(),z.flatten()]).T
    coords = np.concatenate((coords,[xc]),axis=0)
    return coords

def _test_orient(n=[1,1,1],**kwargs):
    coords = bcc_coords()
    coords = orient_crystal(coords,n)
    scat    = coords.T.tolist()
    fig,ax  = dsp.stddisp(scat=scat,ms=100,rc='3d',opt='',legOpt=0)
    show_unit_cell(ax,n,a=0.1,c='b',lw=2)
    W = np.sqrt(3);xylims = [-W/2,W/2,-W/2,W/2,0,W]
    dsp.standardDisplay(ax,xylims=xylims,gridOn=0,ticksOn=0,legOpt=0,**kwargs)

def _test_trihedron():
    fig,ax = dsp.stddisp(rc='3d',std=0)
    show_trihedron(ax,x0=[0,0,0],cs=None,labs=None,
        lw=1,rc=0.1,h=0.2)
    uvw = np.array([[1,0,0],[0,2,2],[1,1,1]])
    show_trihedron(ax,uvw,x0=[-2,-2,-2],cs=['r','g','b'],labs=['$x$','$y$','$z$'],
        lw=2,rc=0.1,h=0.2)
    dsp.stddisp(ax=ax,pOpt='e',opt='p')

def _test_get_arrow():
    #N = 1
    U = np.array([[0,1,1],[1,1,1],[1,0,1]])
    x0 = [0,0,1]
    cs,lw = dsp.getCs('viridis',U.shape[0]),2
    plots,surfs = [],[]
    for u,cu in zip(U,cs) :
        (x,y,z),(xl,yl,zl) = get_arrow_3d(u,x0,rc=0.1,h=0.2)
        plots += [[xl,yl,zl,cu]]
        surfs += [[x,y,z,cu,None,lw,cu]]

    dsp.stddisp(rc='3d',plots=plots,surfs=surfs,lw=lw,pOpt='e')#,texts=txts)

if __name__ == "__main__":
    plt.close('all')
    #show_diffraction_planes(name='figures/cylinder.png',figopt='t2', opt='p')
    #_test_get_arrow()
    #_test_orient(n=[0,0,1],name='docs_fig/orient_crystal001.png',figopt='2',view=[10,-30],opt='p')#;dsp.crop_fig('docs_fig/orient_crystal001.png',[800,800,600,500])
    #_test_orient(n=[1,1,0],name='docs_fig/orient_crystal110.png',figopt='2',view=[10,-30],opt='p')#;dsp.crop_fig('docs_fig/orient_crystal110.png',[800,800,300,400])
    #_test_orient(n=[1,1,1],name='docs_fig/orient_crystal111.png',figopt='2',view=[10,-30],opt='p')#;dsp.crop_fig('docs_fig/orient_crystal111.png',[800,800,450,350])
    _test_trihedron()
