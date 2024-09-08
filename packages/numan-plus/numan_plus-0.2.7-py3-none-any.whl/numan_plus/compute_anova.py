import numpy as np
from statistics import mean, stdev, sqrt
import scipy.stats as stats
from tqdm.notebook import tqdm

# Vectorized implementation of two-way ANOVA
def anova_two_way(A, B, Y):
    num_cells = Y.shape[1]
    
    A_levels = np.unique(A); a = len(A_levels)
    B_levels = np.unique(B); b = len(B_levels)
    Y4D = np.array([[Y[(A==i)&(B==j)] for j in B_levels] for i in A_levels])
    
    r = Y4D.shape[2]

    Y = Y4D.reshape((-1, Y.shape[1]))
    
    # only test cells (units) that are active (gave a nonzero response to at least one stimulus) to avoid division by zero errors
    active_cells = np.where(np.abs(Y).max(axis=0)>0)[0]
    Y4D = Y4D[:,:,:,active_cells]
    Y = Y[:, active_cells]
    
    N = Y.shape[0]
    
    Y_mean = Y.mean(axis=0)
    Y_mean_A = Y4D.mean(axis=1).mean(axis=1)
    Y_mean_B = Y4D.mean(axis=0).mean(axis=1)
    Y_mean_AB = Y4D.mean(axis=2)

    
    SSA = r*b*np.sum((Y_mean_A - Y_mean)**2, axis=0)
    SSB = r*a*np.sum((Y_mean_B - Y_mean)**2, axis=0)
    SSAB = r*((Y_mean_AB - Y_mean_A[:,None] - Y_mean_B[None,:] + Y_mean)**2).sum(axis=0).sum(axis=0)
    SSE = ((Y4D-Y_mean_AB[:,:,None])**2).sum(axis=0).sum(axis=0).sum(axis=0)
    SST = ((Y-Y_mean)**2).sum(axis=0)

    DFA = a - 1; DFB = b - 1; DFAB = DFA*DFB
    DFE = (N-a*b); DFT = N-1
    
    MSA = SSA / DFA
    MSB = SSB / DFB
    MSAB = SSAB / DFAB
    MSE = SSE / DFE
    
    FA = MSA / MSE
    FB = MSB / MSE
    FAB = MSAB / MSE
    
    pA = np.nan*np.zeros(num_cells)
    pB = np.nan*np.zeros(num_cells)
    pAB = np.nan*np.zeros(num_cells)
    
    pA[active_cells] = stats.f.sf(FA, DFA, DFE)
    pB[active_cells] = stats.f.sf(FB, DFB, DFE)
    pAB[active_cells] = stats.f.sf(FAB, DFAB, DFE)
    
    return pA, pB, pAB, FA, FB, FAB


def anova_two_way_permutations(A, B, Y, num_perm):
    a,b,c, FA0, FB0, FAB0 = anova_two_way(A,B,Y) # p is dimention of cells, F only of active cells
    num_cells = Y.shape[1]

    A_levels = np.unique(A); a = len(A_levels)
    B_levels = np.unique(B); b = len(B_levels)
    Y4D = np.array([[Y[(A==i)&(B==j)] for j in B_levels] for i in A_levels])
    
    r = Y4D.shape[2]

    Y = Y4D.reshape((-1, Y.shape[1]))
    
    # only test cells (units) that are active (gave a nonzero response to at least one stimulus) to avoid division by zero errors
    active_cells = np.where(np.abs(Y).max(axis=0)>0)[0]
    Y4D = Y4D[:,:,:,active_cells]
    Y = Y[:, active_cells]

    FA0 = np.expand_dims(FA0, axis=1)
    FB0 = np.expand_dims(FB0, axis=1)
    FAB0 = np.expand_dims(FAB0, axis=1)
    nperm = num_perm
    FA = np.nan*np.zeros((active_cells.shape[0], nperm)) #### check if is ok to take activecells along 0!!!!!!
    FB = np.nan*np.zeros((active_cells.shape[0], nperm))
    FAB = np.nan*np.zeros((active_cells.shape[0], nperm))

    for i in tqdm(range(nperm), desc='Permutations'):
        np.random.shuffle(Y)
        a,b,c, FA[:,i], FB[:,i], FAB[:,i] = anova_two_way(A,B,Y)

    pA = np.nan*np.zeros(num_cells)
    pB = np.nan*np.zeros(num_cells)
    pAB = np.nan*np.zeros(num_cells)

    pA[active_cells] = np.sum(np.greater_equal(FA,FA0), axis=1)/nperm
    pB[active_cells] = np.sum(np.greater_equal(FB,FB0), axis=1)/nperm
    pAB[active_cells] = np.sum(np.greater_equal(FAB,FAB0), axis=1)/nperm

    return pA, pB, pAB
