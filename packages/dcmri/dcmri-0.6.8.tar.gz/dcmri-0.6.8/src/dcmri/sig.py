from scipy.linalg import expm

import numpy as np


def signal_dsc(R1, R2, S0:float, TR, TE)->np.ndarray:
    """Signal model for a DSC scan with T2 and T2-weighting.

    Args:
        R1 (array-like): Longitudinal relaxation rate in 1/sec. Must have the same size as R2.
        R2 (array-like): Transverse relaxation rate in 1/sec. Must have the same size as R1.
        S0 (float): Signal scaling factor (arbitrary units).
        TR (array-like): Repetition time, or time between successive selective excitations, in sec. If TR is an array, it must have the same size as R1 and R2.
        TE (array-like): Echo time, in sec. If TE is an array, it must have the same size as R1 and R2.

    Returns:
        np.ndarray: Signal in arbitrary units, same length as R1 and R2.
    """
    return S0*np.exp(-np.multiply(TE,R2))*(1-np.exp(-np.multiply(TR,R1)))


def signal_t2w(R2, S0:float, TE)->np.ndarray:
    """Signal model for a DSC scan with T2-weighting.

    Args:
        R2 (array-like): Transverse relaxation rate in 1/sec. Must have the same size as R1.
        S0 (float): Signal scaling factor (arbitrary units).
        TE (array-like): Echo time, in sec. If TE is an array, it must have the same size as R1 and R2.

    Returns:
        np.ndarray: Signal in arbitrary units, same length as R1 and R2.
    """
    return S0*np.exp(-np.multiply(TE,R2))

def conc_t2w(S, TE:float, r2=0.5, n0=1)->np.ndarray:
    """Concentration for a DSC scan with T2-weighting.

    Args:
        S (array-like): Signal in arbitrary units.
        TE (float): Echo time in sec.
        r2 (float, optional): Transverse relaxivity in Hz/M. Defaults to 0.5.
        n0 (int, optional): Baseline length. Defaults to 1.

    Returns:
        np.ndarray: Concentration in M, same length as S.
    """
    # S/Sb = exp(-TE(R2-R2b))
    #   ln(S/Sb) = -TE(R2-R2b)
    #   R2-R2b = -ln(S/Sb)/TE
    # R2 = R2b + r2C
    #   C = (R2-R2b)/r2
    #   C = -ln(S/Sb)/TE/r2
    Sb = np.mean(S[:n0])
    C = -np.log(S/Sb)/TE/r2
    return C



def _signal_ss(R1, Sinf, TR, FA)->np.ndarray:
    FA = FA*np.pi/180
    E = np.exp(-np.multiply(TR,R1))
    cFA = np.cos(FA)
    S = Sinf * (1-E) / (1-cFA*E)
    return np.sin(FA)*S

def _signal_ss_fex(v, R1, S0, TR:float, FA:float):
    if np.size(R1) == np.size(v):
        R1 = np.sum(np.multiply(v,R1))
        return _signal_ss(R1, S0, TR, FA)
    nc = R1.shape[0]
    R1fex = np.zeros(R1.shape[1:])
    for c in range(nc):
        R1fex += v[c]*R1[c,...]
    return _signal_ss(R1fex, S0, TR, FA)

def _signal_ss_nex(v, R1:np.ndarray, S0, TR:float, FA:float):
    if np.size(R1) == np.size(v):
        S = _signal_ss(R1, S0, TR, FA)
        return np.sum(np.multiply(v,S)) 
    nc, nt = R1.shape
    S = np.zeros(nt)
    for c in range(nc):
        S += v[c]*_signal_ss(R1[c,:], S0, TR, FA)
    return S

def _signal_ss_aex(PS, v, R1, S0, TR, FA):

    # Mathematical notes on water exchange modelling
    # ---------------------------------------------
    # Longitudinal magnetization in a 2-compartment system
    # with kinetic transport and free relaxation

    # v1*dm1/dt = fi1*mi1 - fo1*m1 + f12*m2 - f21*m1 + R1_1*v1*(m01-m1) 
    # v2*dm2/dt = fi2*mi2 - fo2*m2 + f21*m1 - f12*m2 + R1_2*v2*(m02-m2) 

    # v1*dm1/dt = fi1*mi1 - (fo1+f21+R1_1*v1)*m1 + f12*m2 + R1_1*v1*m01
    # v2*dm2/dt = fi2*mi2 - (fo2+f12+R1_2*v2)*m2 + f21*m1 + R1_2*v2*m02

    # f1 = fo1 + f21 + R1_1*v1 > 0
    # f2 = fo2 + f12 + R1_2*v2 > 0

    # J1(t) = fi1*mi1(t) + R1_1*v1*m01 > 0
    # J2(t) = fi2*mi2(t) + R1_2*v2*m02 > 0

    # v1*dm1/dt = J1 - f1*m1 + f12*m2 
    # v2*dm2/dt = J2 - f2*m2 + f21*m1 

    # K1 = (fo1 + f21)/v1 + R1_1
    # K2 = (fo2 + f12)/v2 + R1_2
    # K12 = f12/v2
    # K21 = f21/v1

    # dM1/dt = J1 - K1*M1 + K12*M2 
    # dM2/dt = J2 - K2*M2 + K21*M1 

    # K = [[K1, -K12],[-K21, K2]
    # dM/dt = J - KM

    # Use generic solution for n-comp system to solve for M(t)
    # Note with R1(t) this is not a stationary system

    # Solution with K and J constant in time:

    # M(t) = exp(-tK)M(0) + exp(-tK)*J
    # M(t) = exp(-tK)M(0) + (1-exp(-tK)) K^-1 J

    # Check

    # dM/dt 
    # = - K exp(-tK)M(0) + exp(-tK) J
    # J - KM 
    # = J - Kexp(-tK)M(0) - (1-exp(-tK))J 
    # = - K exp(-tK)M(0) + exp(-tK) J

    # Spoiled gradient echo steady state:
    # M = exp(-TR*K) cosFA M + (1-exp(-TR*K)) K^-1 J
    # (1 - cosFA exp(-TR*K)) M = (1-exp(-TR*K)) K^-1 J
    # M = (1 - cosFA exp(-TR*K))^-1 (1-exp(-TR*K)) K^-1 J
    # M = (1 - cosFA exp(-TR*K))^-1 K^-1 (1-exp(-TR*K))  J
    # M = [K(1 - cosFA exp(-TR*K))]^-1 (1-exp(-TR*K)) J

    # Inputs to the function:

    # f1 = fo1 + f21 + R1_1(t)*v1
    # f2 = fo2 + f12 + R1_2(t)*v2
    
    # J1 = fi1*S0*mi1(t) + R1_1(t)*v1*S0*m01
    # J2 = fi2*S0*mi2(t) + R1_2(t)*v2*S0*m02

    # K = [[f1/v1, -f21/v1], [-f12/v2, f2/v2]]
    # J = [J1, J2]

    # K dimensions = (ncomp, ncomp, nt)
    # J dimensions = (ncomp, nt)

    # Returns:

    # M = (1 - cosFA exp(-TR*K))^-1 (1-exp(-TR*K)) K^-1 J
    # M = [(1 - cosFA exp(-TR*K))K]^-1 (1-exp(-TR*K)) J

    # reshape for convenience
    n = np.shape(R1)
    R1 = np.reshape(R1, (n[0],-1))
    PS = np.array(PS)

    nc, nt = R1.shape
    J = np.empty((nc,nt))
    K = np.empty((nc,nc,nt))
    for c in range(nc):
        J[c,:] = S0*v[c]*R1[c,:]
        K[c,c,:] = R1[c,:] + np.sum(PS[:,c])/v[c]
        for d in range(nc):
            if d!=c:
                K[c,d,:] = -PS[c,d]/v[d]

    FA = FA*np.pi/180
    cFA = np.cos(FA)
    Mag = np.empty(nt)
    Id = np.eye(nc)
    for t in range(nt):
        Et = expm(-TR*K[:,:,t])
        Mt = np.dot(K[:,:,t], Id-cFA*Et)
        Mt = np.linalg.inv(Mt)
        Vt = np.dot(Id-Et, J[:,t])
        Vt = np.dot(Mt, Vt)
        Mag[t] = np.sum(Vt)

    # Return in original shape
    R1 = R1.reshape(n)
    return np.sin(FA)*Mag.reshape(n[1:])


def signal_ss(R1, S0, TR, FA, v=None, PSw=np.inf, R10=None)->np.ndarray:
    """Signal of a spoiled gradient echo sequence applied in steady state.

    Args:
        R1 (array-like): Longitudinal relaxation rates in 1/sec. For a tissue with n compartments, the first dimension of R1 must be n. For a tissue with a single compartment, R1 can have any shape.
        S0 (float): Signal scaling factor (arbitrary units).
        TR (float): Repetition time, or time between successive selective excitations, in sec. 
        FA (float): Flip angle in degrees.
        v (array-like, optional): volume fractions of each compartment. If v is not provided, the tissue will be treated as one-compartmental. If v is provided, the length must be same as the first dimension of R1 and values must add up to 1. Defaults to None.
        PSw (array-like, optional): Water permeability-surface area products through the interfaces between the compartments, in units of mL/sec/mL. With PSw=np.inf (default), water exchange is in the fast-exchange limit. With PSw=0, there is no water exchange between the compartments. For any intermediate level of water exchange, PSw must be a nxn array, where n is the number of compartments, and PSw[j,i] is the permeability for water moving from compartment i into j. The diagonal elements PSw[i,i] quantify the flow of water from compartment i to outside. Defaults to np.inf.
        R10 (float, optional): R1-value where S0 is defined. If not provided, S0 is the scaling factor corresponding to infinite R10. Defaults to None.

    Returns:
        np.ndarray: Signal in the same units as S0.
    """
    if R10 is None:
        Sinf = S0
    else:
        if v is not None:
            R10 = np.full(len(v), R10)
        Sinf = S0/signal_ss(R10, 1, TR, FA, v=v, PSw=PSw)
    if v is None:
        return _signal_ss(R1, Sinf, TR, FA)
    if np.isscalar(R1):
        raise ValueError('In a multi-compartment system, R1 must be an array with at least 1 dimension..')
    if np.ndim(R1)==1:
        if np.size(v) != np.size(R1):
            raise ValueError('v must have the same length as R1.')
    elif np.size(v) != np.shape(R1)[0]:
        raise ValueError('v must have the same length as the first dimension of R1.')
    if np.isscalar(PSw):
        if PSw==np.inf:
            return _signal_ss_fex(v, R1, Sinf, TR, FA)
        elif PSw==0:
            return _signal_ss_nex(v, R1, Sinf, TR, FA)
    else:
        if np.ndim(PSw) != 2:
            raise ValueError("For intermediate water exchange, PSw must be a square array")
        if np.shape(PSw)[0] != np.size(v):
            raise ValueError("Dimensions of PSw and v do not match up.")
        return _signal_ss_aex(PSw, v, R1, Sinf, TR, FA)


def conc_ss(S, TR:float, FA:float, T10:float, r1=0.005, n0=1)->np.ndarray:
    """Concentration of a spoiled gradient echo sequence applied in steady state.

    Args:
        S (array-like): Signal in arbitrary units.
        TR (float): Repetition time, or time between successive selective excitations, in sec.
        FA (float): Flip angle in degrees.
        T10 (float): baseline T1 value in sec.
        r1 (float, optional): Longitudinal relaxivity in Hz/M. Defaults to 0.005.
        n0 (int, optional): Baseline length. Defaults to 1.

    Returns:
        np.ndarray: Concentration in M, same length as S.
    """
    # S = Sinf * (1-exp(-TR*R1)) / (1-cFA*exp(-TR*R1))
    # Sb = Sinf * (1-exp(-TR*R10)) / (1-cFA*exp(-TR*R10))
    # Sn = (1-exp(-TR*R1)) / (1-cFA*exp(-TR*R1))
    # Sn * (1-cFA*exp(-TR*R1)) = 1-exp(-TR*R1)
    # exp(-TR*R1) - Sn *cFA*exp(-TR*R1) = 1-Sn
    # (1-Sn*cFA) * exp(-TR*R1) = 1-Sn
    Sb = np.mean(S[:n0])
    E0 = np.exp(-TR/T10)
    c = np.cos(FA*np.pi/180)
    Sn = (S/Sb)*(1-E0)/(1-c*E0)	        # normalized signal
    # Replace any Nan values by interpolating between nearest neighbours
    outrange = Sn >= 1
    if np.sum(outrange) > 0:
        inrange = Sn < 1
        x = np.arange(Sn.size)
        Sn[outrange] = np.interp(x[outrange], x[inrange], Sn[inrange])
    R1 = -np.log((1-Sn)/(1-c*Sn))/TR	# relaxation rate in 1/msec
    return (R1 - 1/T10)/r1 



def _signal_sr(R1, Sinf:float, TR:float, FA:float, TC:float, TP=0.0)->np.ndarray:

    if TP > TC:
        msg = 'Incorrect sequence parameters.'
        msg += 'Tsat must be smaller than TC.'
        raise ValueError(msg)
    
    FA = np.pi*FA/180
    cFA = np.cos(FA)
    T1_app = TR/(np.multiply(TR,R1)-np.log(cFA))

    ER = np.exp(-np.multiply(TR,R1))
    E_sat = np.exp(-np.multiply(TP,R1))
    E_center = np.exp(-(TC-TP)/T1_app)

    S_sat = Sinf * (1-E_sat)
    S_ss = Sinf * (1-ER)/(1-cFA*ER)

    S_ss = S_ss*(1-E_center) + S_sat*E_center

    return np.sin(FA)*S_ss


def _signal_sr_fex(v, R1, S0:float, TR:float, FA:float, TC:float, TP=0.0):
    if np.size(R1) == np.size(v):
        R1 = np.sum(np.multiply(v,R1))
        return _signal_sr(R1, S0, TR, FA, TC, TP)
    nc, nt = R1.shape
    R1fex = np.zeros(nt)
    for c in range(nc):
        R1fex += v[c]*R1[c,:]
    return _signal_sr(R1fex, S0, TR, FA, TC, TP)


def _signal_sr_nex(v, R1, S0:float, TR:float, FA:float, TC:float, TP=0.0):
    if np.size(R1) == np.size(v):
        S = _signal_sr(R1, S0, TR, FA, TC, TP)
        return np.sum(np.multiply(v,S)) 
    nc, nt = R1.shape
    S = np.zeros(nt)
    for c in range(nc):
        S += v[c]*_signal_sr(R1[c,:], S0, TR, FA, TC, TP)
    return S


def signal_sr(R1, S0:float, TR:float, FA:float, TC:float, TP=0.0, v=None, PSw=np.inf, R10=None)->np.ndarray:
    """Signal model for a saturation-recovery sequence with a FLASH readout.

    Args:
        R1 (array-like): Longitudinal relaxation rate in 1/sec.
        S0 (float): Signal scaling factor (arbitrary units).
        TR (float): Repetition time, or time between successive selective excitations, in sec. 
        FA (array-like): Flip angle in degrees.
        TC (float): Time (sec) between the saturation pulse and the acquisition of the k-space center.
        TP (float, optional): Time (sec) between the saturation pre-pulse and the first readout pulse. Defaults to 0.
        v (array-like, optional): volume fractions of each compartment. If v is not provided, the tissue will be treated as one-compartmental. If v is provided, the length must be same as the first dimension of R1 and values must add up to 1. Defaults to None.
        PSw (array-like, optional): Water permeability-surface area products through the interfaces between the compartments, in units of mL/sec/mL. With PSw=np.inf (default), water exchange is in the fast-exchange limit. With PSw=0, there is no water exchange between the compartments. For any intermediate level of water exchange, PSw must be a nxn array, where n is the number of compartments, and PSw[j,i] is the permeability for water moving from compartment i into j. The diagonal elements PSw[i,i] quantify the flow of water from compartment i to outside. Defaults to np.inf.

        R10 (float, optional): R1-value where S0 is defined. If not provided, S0 is the scaling factor corresponding to infinite R10. Defaults to None.

    Raises:
        ValueError: If TP is larger than TC.

    Returns:
        np.ndarray: Signal in arbitrary units, of the same length as R1.
    """
    if R10 is None:
        Sinf = S0
    else:
        if v is not None:
            R10 = np.full(len(v), R10)
        Sinf = S0/signal_sr(R10, 1, TR, FA, TC, TP, v=v)
    if v is None:
        return _signal_sr(R1, Sinf, TR, FA, TC, TP)
    if np.isscalar(R1):
        raise ValueError('In a multi-compartment system, R1 must be an array with at least 1 dimension..')
    if np.ndim(R1)==1:
        if np.size(v) != np.size(R1):
            raise ValueError('v must have the same length as R1.')
    if np.size(v) != np.shape(R1)[0]:
        raise ValueError('v must have the same length as the first dimension of R1.')
    if np.isscalar(PSw):
        if PSw==np.inf:
            return _signal_sr_fex(v, R1, Sinf, TR, FA, TC, TP)
        elif PSw==0:
            return _signal_sr_nex(v, R1, Sinf, TR, FA, TC, TP)
    else:
        if np.ndim(PSw) != 2:
            raise ValueError("For intermediate water exchange, PSw must be a square array")
        if np.shape(PSw)[0] != np.size(v):
            raise ValueError("Dimensions of PSw and v do not match up.")
        raise NotImplementedError('Internediate water exchange modelling is not yet available for SR sequences')
        #return _signal_sr_aex(PSw, v, R1, Sinf, TR, FA, TC, TP)


def signal_er(R1, S0:float, TR:float, FA:float, TC:float)->np.ndarray:
    """Signal model for a FLASH readout, starting from equilibrium (i.e. no preparation pulse).

    Args:
        R1 (array-like): Longitudinal relaxation rate in 1/sec.
        S0 (float): Signal scaling factor (arbitrary units).
        TR (float): Repetition time, or time between successive selective excitations, in sec. 
        FA (array-like): Flip angle in degrees.
        TC (float): Time (sec) between the saturation pulse and the acquisition of the k-space center.

    Returns:
        np.ndarray: Signal in arbitrary units, of the same length as R1.
    """
    #TI is the residence time in the slab
    FA = np.pi*FA/180
    cFA = np.cos(FA)
    R1_app = R1 - np.log(cFA)/TR

    ER = np.exp(-TR*R1)
    EI = np.exp(-TC*R1_app)

    Sss = S0 * (1-ER)/(1-cFA*ER)
    Sss = Sss*(1-EI) + S0*EI

    return np.sin(FA)*Sss


def signal_src(R1, S0, TC, R10=None):
    """Signal model for a saturation-recovery with a center-encoded readout.

    This can also be used with other encoding schemens whenever the effect of the readout pulses can be ignored, such as for fast flowing magnetization in arterial blood.

    Args:
        R1 (array-like): Longitudinal relaxation rate in 1/sec.
        S0 (float): Signal scaling factor (arbitrary units).
        TC (float): Time (sec) between the saturation pulse and the acquisition of the k-space center.

    Returns:
        np.ndarray: Signal in arbitrary units, of the same length as R1.
    """
    if R10 is None:
        Sinf = S0
    else:
        Sinf = S0/signal_src(R10, 1, TC)
    E = np.exp(-TC*R1)
    return Sinf * (1-E)


def conc_src(S, TC:float, T10:float, r1=0.005, n0=1)->np.ndarray:
    """Concentration of a saturation-recovery sequence with a center-encoded readout.

    Args:
        S (array-like): Signal in arbitrary units.
        TC (float): Time (sec) between the saturation pulse and the acquisition of the k-space center.
        T10 (float): baseline T1 value in sec.
        r1 (float, optional): Longitudinal relaxivity in Hz/M. Defaults to 0.005.
        n0 (int, optional): Baseline length. Defaults to 1.

    Returns:
        np.ndarray: Concentration in M, same length as S.

    Example:

        We generate some signals from ground-truth concentrations, then reconstruct the concentrations and check against the ground truth:

    .. plot::
        :include-source:

        >>> import matplotlib.pyplot as plt
        >>> import numpy as np
        >>> import dcmri as dc

        First define some constants:

        >>> T10 = 1         # sec
        >>> TC = 0.2        # sec
        >>> r1 = 0.005      # Hz/M

        Generate ground truth concentrations and signal data:

        >>> t = np.arange(0, 5*60, 0.1)     # sec
        >>> C = 0.003*(1-np.exp(-t/60))     # M
        >>> R1 = 1/T10 + r1*C               # Hz
        >>> S = dc.signal_src(R1, 100, TC)  # au

        Reconstruct the concentrations from the signal data:

        >>> Crec = dc.conc_src(S, TC, T10, r1)

        Check results by plotting ground truth against reconstruction:

        >>> plt.plot(t/60, 1000*C, 'ro', label='Ground truth')
        >>> plt.plot(t/60, 1000*Crec, 'b-', label='Reconstructed')
        >>> plt.title('SRC signal inverse')
        >>> plt.xlabel('Time (min)')
        >>> plt.ylabel('Concentration (mM)')
        >>> plt.legend()
        >>> plt.show()

    """
    # S = S0*(1-exp(-TC*R1))
    # S/Sb = (1-exp(-TC*R1))/(1-exp(-TC*R10))
    # (1-exp(-TC*R10))*S/Sb = 1-exp(-TC*R1)
    # 1-(1-exp(-TC*R10))*S/Sb = exp(-TC*R1)
    # ln(1-(1-exp(-TC*R10))*S/Sb) = -TC*R1
    # -ln(1-(1-exp(-TC*R10))*S/Sb)/TC = R1
    Sb = np.mean(S[:n0])
    E = np.exp(-TC/T10)
    R1 = -np.log(1-(1-E)*S/Sb)/TC	
    return (R1 - 1/T10)/r1 


def signal_lin(R1, S0:float)->np.ndarray:
    """Signal for any sequence operating in the linear regime.

    Args:
        R1 (array-like): Longitudinal relaxation rate in 1/sec.
        S0 (float): Signal scaling factor (arbitrary units).

    Returns:
        np.ndarray: Signal in arbitrary units, of the same length as R1.
    """
    return S0 * R1


def conc_lin(S, T10, r1=0.005, n0=1):
    """Concentration for any sequence operating in the linear regime.

    Args:
        S (array-like): Signal in arbitrary units.
        T10 (float): baseline T1 value in sec.
        r1 (float, optional): Longitudinal relaxivity in Hz/M. Defaults to 0.005.
        n0 (int, optional): Baseline length. Defaults to 1.

    Returns:
        np.ndarray: Concentration in M, same length as S.
    """
    Sb = np.mean(S[:n0])
    R10 = 1/T10
    R1 = R10*S/Sb	#relaxation rate in 1/msec
    return (R1 - R10)/r1 
