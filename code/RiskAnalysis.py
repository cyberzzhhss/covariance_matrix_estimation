import numpy as np
from sklearn import covariance
from helperCode import pyRMT
from helperCode import rie_estimator


class RiskAnalysis():

    def __init__(self, T_total=5070, T=650, T_out=39, inputRets='returns.txt'):
        self.T_total = T_total
        self.T = T
        self.T_out = T_out
        self.raw_returns = np.loadtxt(inputRets)
        self.sigma_hat = np.sum(self.raw_returns**2, axis=0)**0.5

    '''
    standardizing the returns
    Implementation from the section {Setting the Stage}
    from (Bun, Bouchaud and Potters, 2016) risk paper

    (i)   removing the stock mean across time 
    (ii)  divide by cross-sectional 5min volatility at one time
    (iii) divide by sample estimator of each stock

    INPUT: untreated return matrix
           shape = (N, T) 
                 = (number of tickers, number of time intervals)
    OUTPUT: standardized return matrix
           shape = (N, T) 
                 = (number of tickers, number of time intervals)
    '''

    def standardize_returns(self, raw_returns):
        nTicks, nBins = raw_returns.shape
        # find mean
        stock_mean = raw_returns.mean(axis=1).reshape(nTicks, 1)
        # find cross-sectional 5 min volatility at one time
        # \hat{\sigma}_{it}
        sigma_hat = np.sum(raw_returns**2, axis=0)**0.5
        # step 1 and step 2
        # \tilde{r}_{it}
        tilde_returns = (raw_returns - stock_mean) / sigma_hat
        # find sample estimator
        # ddof=1 means sample estimator
        # \sigma_i
        sample_estimator = np.std(
            tilde_returns, axis=1, ddof=1).reshape(nTicks, 1)
        # step 3
        # standardized return matrix
        X = tilde_returns / sample_estimator
        return X

    # out of sample variance calculation
    '''
        Implementation of eqn(13) from (Bun, Bouchaud and Potters, 2016) risk paper
        out-of-sample variance of the returns of portfolio built
        at time t
        
        oos_var  = out-of-sample variance
        
        INPUTS:
                t : starting time
                T_out : T_out
                w: portfolio weights, 
                   shape = (N, 1) 
                X: rescaled realized returns, 
                   shape = (N, T)
                         = (number of tickers, number of time intervals)
        OUTPUT:
                var (scalar)
                out of sample variance 
        
    '''

    def oos_var(self, t, T_out, w, X):
        nTicks, nBins = X.shape
        res = 0
        for tau in range(t + 1, t + T_out + 1):
            s = 0
            for ii in range(nTicks):
                s = s + w[ii] * X[ii][tau]
            res = res + s ** 2
        var = float(res / T_out)
        return var

    # empirical covariance
    '''
        INPUT:
              X: (T, N) rescaled realized return
        OUTPUT:
              covariance matrix (N, N)
    '''

    def get_empirical_cov(self, input_matrix):
        ret_cov = covariance.empirical_covariance(
            input_matrix, assume_centered=True)
        return ret_cov

    # eigenvalues clipping
    '''
        INPUT:
              X: (T, N) rescaled realized return
        OUTPUT:
              covariance matrix (N, N)
    '''

    def get_ev_clip_cov(self, input_matrix):
        ret_cov = pyRMT.clipped(input_matrix, return_covariance=True)
        return ret_cov

    # optimal shrinkage
    '''
        INPUT:
              X: (T, N) rescaled realized return
        OUTPUT:
              covariance matrix (N, N)
    '''

    def get_os_cov(self, input_matrix):
        ret_cov = rie_estimator.get_rie(input_matrix)
        return ret_cov

    # exponential weighted filtering
    '''
        INPUT:
              X: (T, N) rescaled realized return
        OUTPUT:
              covariance matrix (N, N)
    '''

    # exponential weighted filtering
    def get_expo_weighted_cov(self, input_matrix):
        input_matrix = input_matrix.T  # transpose the input matrix
        N = input_matrix.shape[0]
        T = input_matrix.shape[1]
        input_matrix = input_matrix
        res = np.zeros((N, N))
        alpha = 1 - (1 / (2 * N))
        factor = (1 - alpha)/(1 - alpha**T)
        alpha_arr = [alpha**t for t in range(T)]
        for ii in range(N):
            for jj in range(N):
                s = np.sum(input_matrix[ii]*input_matrix[jj]*alpha_arr)*factor
                res[ii][jj] = s
        return res

    # mean variance weight
    '''
        Implementation of #1 mean variance portfolio
        from (Bun, Bouchaud and Potters, 2016) risk paper
        
        weight is calculated using eqn (14)
        
        INPUT:
              inversed covariance matrix (N, N)
        OUTPUT:
              weight: weight vector (N, 1)
    '''

    def get_mvp_w(self, inv_cov):
        N = len(inv_cov)
        g = np.ones((N, 1))
        weight = (inv_cov @ g) / (g.T @ inv_cov @ g)
        return weight

    # random weight
    '''
        Implementation of #4 random long-short predictors
        from (Bun, Bouchaud and Potters, 2016) risk paper
        
        weight is calculated using eqn (14)
        
        INPUT:
              inversed covariance matrix (N, N)
        OUTPUT:
              weight: weight vector (N, 1)
    '''

    def get_rand_w(self, inv_cov):
        N = len(inv_cov)
        # curly_N = normalization_factor
        normalization_factor = np.sqrt(N)
        v = np.random.uniform(-1, 1, (N, 1))
        g = normalization_factor * v
        weight = (inv_cov @ g) / (g.T @ inv_cov @ g)
        return weight

    '''
    Implementation of #2 omniscient case
    from (Bun, Bouchaud and Potters, 2016) risk paper
    
    weight is calculated using eqn (14)
    
    INPUT:
          inv_cov:  inversed covariance matrix (N, N)
          raw_ret: (T, N) raw return
          T_out: T_out
    OUTPUT:
          weight: weight vector (N, 1)
    '''

    def get_omni_w(self, inv_cov, raw_ret, t, T_out):
        N = len(inv_cov)
        # curly_N = normalization_factor
        normalization_factor = np.sqrt(N)
        r = np.zeros((N, 1))
        curly_r = raw_ret / self.sigma_hat
        for ii in range(N):
            r[ii][0] = np.cumprod(curly_r[ii][t:t+T_out]+1, axis=0)[-1]-1
        g = normalization_factor * r
        weight = (inv_cov @ g) / (g.T @ inv_cov @ g)
        return weight

    def random_select_n_stocks(self,n=300):
        np.random.seed(2022)
        N = self.raw_returns.shape[0]
        choice = np.random.choice(N, size = n, replace=False)
        self.old_raw_returns = self.raw_returns
        self.raw_returns = self.raw_returns[choice]
        self.sigma_hat = np.sum(self.raw_returns**2, axis=0)**0.5
    
    def restore_default_n_stocks(self):
        self.raw_returns = self.old_raw_returns
        self.sigma_hat = np.sum(self.raw_returns**2, axis=0)**0.5
        
    def start_simulation(self):
        np.random.seed(2022)  # ensure the result is replicable
        T_total = self.T_total
        T_out = self.T_out
        T = self.T
        print('Standardizing the returns')
        returns = self.standardize_returns(self.raw_returns)
        X = returns
        var_emp_mvp = []
        var_emp_omni = []
        var_emp_rand = []
        print('Evaluating empirical covariance estimator')
        for t in range(0, T_total - T - T_out, T_out):
            emp_cov = self.get_empirical_cov(returns.T[t:t+T])
            inv_cov = np.linalg.inv(emp_cov)

            mvp_w = self.get_mvp_w(inv_cov)
            omni_w = self.get_omni_w(inv_cov, self.raw_returns, t+T, T_out)
            rand_w = self.get_rand_w(inv_cov)

            var_emp_mvp.append(self.oos_var(t+T, T_out, mvp_w, X))
            var_emp_omni.append(self.oos_var(t+T, T_out, omni_w, X))
            var_emp_rand.append(self.oos_var(t+T, T_out, rand_w, X))

            if t % (T_out*10) == 0:
                param = t / (T_total - T - T_out) * 100
                print('{param:.4}% done'.format(param=param))
        print('100.00% done')
        self.var_emp_mvp = var_emp_mvp
        self.var_emp_omni = var_emp_omni
        self.var_emp_rand = var_emp_rand

        var_ev_clip_mvp = []
        var_ev_clip_omni = []
        var_ev_clip_rand = []
        print('Evaluating eigenvalues clipping estimator')
        for t in range(0, T_total - T - T_out, T_out):
            ev_clip_cov = self.get_ev_clip_cov(returns.T[t:t+T])
            inv_cov = np.linalg.inv(ev_clip_cov)

            mvp_w = self.get_mvp_w(inv_cov)
            omni_w = self.get_omni_w(inv_cov, self.raw_returns, t+T, T_out)
            rand_w = self.get_rand_w(inv_cov)

            var_ev_clip_mvp.append(self.oos_var(t+T, T_out, mvp_w, X))
            var_ev_clip_omni.append(self.oos_var(t+T, T_out, omni_w, X))
            var_ev_clip_rand.append(self.oos_var(t+T, T_out, rand_w, X))

            if t % (T_out*10) == 0:
                param = t / (T_total - T - T_out) * 100
                print('{param:.4}% done'.format(param=param))
        print('100.00% done')
        self.var_ev_clip_mvp = var_ev_clip_mvp
        self.var_ev_clip_omni = var_ev_clip_omni
        self.var_ev_clip_rand = var_ev_clip_rand

        var_os_mvp = []
        var_os_omni = []
        var_os_rand = []
        print('Evaluating optimal shrinkage estimator')
        for t in range(0, T_total - T - T_out, T_out):
            os_cov = self.get_os_cov(returns.T[t:t+T])
            inv_cov = np.linalg.inv(os_cov)

            mvp_w = self.get_mvp_w(inv_cov)
            omni_w = self.get_omni_w(inv_cov, self.raw_returns, t+T, T_out)
            rand_w = self.get_rand_w(inv_cov)

            var_os_mvp.append(self.oos_var(t+T, T_out, mvp_w, X))
            var_os_omni.append(self.oos_var(t+T, T_out, omni_w, X))
            var_os_rand.append(self.oos_var(t+T, T_out, rand_w, X))

            if t % (T_out*10) == 0:
                param = t / (T_total - T - T_out) * 100
                print('{param:.4}% done'.format(param=param))
        print('100.00% done')
        self.var_os_mvp = var_os_mvp
        self.var_os_omni = var_os_omni
        self.var_os_rand = var_os_rand

        var_expo_mvp = []
        var_expo_omni = []
        var_expo_rand = []
        print('Evaluating exponential weighting estimator')
        for t in range(0, T_total - T - T_out, T_out):
            expo_cov = self.get_expo_weighted_cov(returns.T[t:t+T])
            inv_cov = np.linalg.inv(expo_cov)

            mvp_w = self.get_mvp_w(inv_cov)
            omni_w = self.get_omni_w(inv_cov, self.raw_returns, t+T, T_out)
            rand_w = self.get_rand_w(inv_cov)

            var_expo_mvp.append(self.oos_var(t+T, T_out, mvp_w, X))
            var_expo_omni.append(self.oos_var(t+T, T_out, omni_w, X))
            var_expo_rand.append(self.oos_var(t+T, T_out, rand_w, X))

            if t % (T_out*10) == 0:
                param = t / (T_total - T - T_out) * 100
                print('{param:.4}% done'.format(param=param))
        print('100.00% done')
        self.var_expo_mvp = var_expo_mvp
        self.var_expo_omni = var_expo_omni
        self.var_expo_rand = var_expo_rand

        print("Finish the simulation for all covariance estimators")