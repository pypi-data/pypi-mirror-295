from collections import deque
import numpy as np
from collections import defaultdict


def cycle(G, i, j):
    """
    Check whether a DAG G remains acyclic if an edge i->j is added.
    Return True if it is no longer a DAG.

    Examples
    --------
    Consider a DAG defined as:
    dag = np.array([[0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 0]])
    print(cycle(dag, 3, 2))
    """
    P = len(G)
    C = [0] * P
    C[i] = 1
    Q = deque([i])
    while Q:
        u = Q.popleft()
        parent_u = [ii for ii in range(P) if G[ii, u] != 0]
        for v in parent_u:
            if v == j:
                return True
            else:
                if C[v] == 0:
                    C[v] = 1
                    Q.append(v)
    return False


def objective(Gamma, sigma_hat, lam):
    P = len(Gamma)
    obj = sum([-2*np.log(Gamma[i, i]) for i in range(P)])
    obj += np.trace(Gamma@Gamma.T@sigma_hat)
    obj += lam*lam*(np.count_nonzero(Gamma)-P)
    return obj


def gamma_hat(Gamma, sigma_hat, u, v, lam):
    numerator = sum([2 * Gamma[i, v] * sigma_hat[i, u] for i in range(len(Gamma)) if i != u])
    return -numerator/sigma_hat[u, u]/2 if lam*lam <= numerator*numerator/(4*sigma_hat[u,u]) else 0


def gamma_hat_diag(Gamma, sigma_hat, u):
    star = sum([2 * Gamma[j, u] * sigma_hat[j, u]for j in range(len(Gamma)) if j != u])
    return (-star + np.sqrt(star*star + 16*sigma_hat[u, u]))/(4*sigma_hat[u, u])


def CD(X, moral, lam=0.01, MAX_cycles=100, tol=1e-2):
    """
    X: N by P data matrix
    moral: P by P  0-1 matrix as the super-structure. moral[u, v] == 1 means edge u->v might exist
    lam: non-negative value. lam*lam is the regularization parameter
    """
    N, P = X.shape
    sigma = np.cov(X.T)
    # sigma = (X.T@X/N).values
    Gamma = np.eye(P)
    objs = []
    min_obj = float('inf')
    opt_Gamma = None
    support_counter = defaultdict(int)
    for t in range(MAX_cycles):
        # if t % 10 == 0:
        #     print(f"cycle: {t}")
        for u in range(P):
            Gamma[u, u] = gamma_hat_diag(Gamma, sigma, u)
            for v in range(P):
                if u != v and moral[u, v] == 1:
                    temp_gamma = Gamma.copy()
                    temp_gamma -= np.diag(np.diag(temp_gamma))
                    cycle_uv = cycle(temp_gamma, u, v)
                    if cycle_uv:
                        Gamma[u, v] = 0
                    else:
                        Gamma[u, v] = gamma_hat(Gamma, sigma, u, v, lam)
        obj_t = objective(Gamma, sigma, lam)

        support_i = str(np.array(Gamma != 0, dtype=int).flatten())
        support_counter[support_i] += 1

        # spacer step
        if support_counter[support_i] == 5:
            # print("spacer step is working")
            for u, v in np.transpose(np.nonzero(Gamma)):
                if u != v:
                    Gamma[u, v] = gamma_hat(Gamma, sigma, u, v, lam)
                else:
                    Gamma[u, u] = gamma_hat_diag(Gamma, sigma, u)
            support_counter[support_i] = 0
            obj_t = objective(Gamma, sigma, lam)

        if len(objs) > 1 and objs[-1] - obj_t < tol:
            objs.append(obj_t)
            print(f"stop at the {t}-th iteration.")
            break
        if obj_t < min_obj:
            min_obj = obj_t
            opt_Gamma = Gamma.copy()
        objs.append(obj_t)

    return opt_Gamma, min_obj
