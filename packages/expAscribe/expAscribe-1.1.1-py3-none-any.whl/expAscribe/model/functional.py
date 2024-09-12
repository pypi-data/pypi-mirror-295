import torch
import torch.nn as nn
import numpy as np

from expAscribe.model.Utils.input2hidden import Input2Hidden
from expAscribe.model.Utils.hidden2latent import Hidden2Latent
from expAscribe.model.Utils.locally_connected import LocallyConnected
from expAscribe.model.Utils.lbfgsb_scipy import LBFGSBScipy

class SAE(nn.Module):
    def __init__(self,
                 neurons,
                 device,
                 act_func,
                 bias=True):
        super(SAE, self).__init__()
        self.neurons = neurons
        self.device = device
        self.act_func = act_func
        self.bias = bias
        self.d = neurons[0]
        self.q = neurons[-1]

        # encoder
        encoder = nn.Sequential()
        encoder.add_module('fc0', Input2Hidden(num_linear=self.d,input_features=1,output_features=neurons[1],bias=bias))
        encoder.add_module('act0', self.act_func)
        encoder.add_module('fc1', Hidden2Latent(num_linear=self.d,input_features=neurons[1],output_features=neurons[2],bias=bias))
        self.encoder = encoder
        # decoder
        decoder = nn.Sequential()
        decoder.add_module('fc0', nn.Linear(in_features=neurons[-1],out_features=neurons[-2],bias=bias,device=device))
        decoder.add_module('act0', self.act_func)
        decoder.add_module('fc1', nn.Linear(in_features=neurons[-2],out_features=neurons[-3],bias=bias,device=device))
        self.decoder = decoder

        self._init_weights()

    def _init_weights(self):
        for m in self.encoder.modules():
            if isinstance(m, Input2Hidden) or isinstance(m, Hidden2Latent):
                nn.init.uniform_(m.weight.data,-0.1,0.1)
                nn.init.zeros_(m.bias.data)

    def forward(self, x):  # x:[n, d]
        x = x.t().unsqueeze(2)  # [d, n, 1]
        z = torch.sum(self.encoder(x), 0)  # [n, q]
        y = self.decoder(z)  # [n, d]
        return z, y

    def get_l1reg(self):
        l1_reg = 0.
        for l in self.encoder.modules():
            if isinstance(l, Input2Hidden) or isinstance(l, Hidden2Latent):
                l1_reg += torch.sum(torch.abs(l.weight.data))
                l1_reg += torch.sum(torch.abs(l.bias.data))
        return l1_reg

    def get_l2reg(self):
        l2_reg = 0.
        for l in self.encoder.modules():
            if isinstance(l, Input2Hidden) or isinstance(l, Hidden2Latent):
                l2_reg += torch.sum(l.weight.data ** 2)
                l2_reg += torch.sum(l.bias.data ** 2)
        return l2_reg

    def get_path_product(self):  # -> [d, q]
        A = torch.abs(self.encoder[0].weight.data)  # [d, 1, m1]
        A = A.matmul(torch.abs(self.encoder[2].weight.data))  # [d, 1, q] = [d, 1, m1] @ [d, m1, q]
        A = A.squeeze(1)  # [d, q]
        return A

class MLP(nn.Module):
    def __init__(self,
                 neurons,
                 q,
                 device,
                 act_func,
                 bias=True
                 ):
        super(MLP, self).__init__()
        self.neurons = neurons
        self.device = device
        self.act_func = act_func
        self.bias = bias
        d = neurons[0]
        self.d = d
        self.q = q

        # the number of inputs is d+q
        self.fw_pos = nn.Linear(d+q, d*neurons[1], bias=bias)
        self.fw_neg = nn.Linear(d+q, d*neurons[1], bias=bias)
        self.init_bounds = self._bounds()
        self.fw_pos.weight.bounds = self.init_bounds
        self.fw_neg.weight.bounds = self.init_bounds

        # the number of MLPs is d
        layers = []
        for l in range(len(neurons)-2):
            layers.append(self.act_func)
            layers.append(LocallyConnected(d, neurons[l+1], neurons[l+2], bias=bias))
        self.fc = nn.ModuleList(layers)

        # self._init_weights()

    def _bounds(self):
        d = self.d
        q = self.q
        bounds = []
        for j in range(d):
            for m in range(self.neurons[1]):
                for i in range(d+q):
                    if i == j:
                        bound = (0, 0)
                    else:
                        bound = (0, None)
                    bounds.append(bound)
        return bounds

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_uniform_(m.weight.data)

    def forward(self, xz):  # xz:[n, d+q]
        xz = self.fw_pos(xz) - self.fw_neg(xz)  # [n, d*m1]
        xz = xz.view(-1, self.neurons[0], self.neurons[1])  # [n, d, m1]
        for f in self.fc:
            xz = f(xz)
        xz = xz.squeeze(dim=2)  # [n, d]
        return xz

    def get_fw(self):
        return self.fw_pos.weight - self.fw_neg.weight

    def get_abs_fw(self):
        return self.fw_pos.weight + self.fw_neg.weight

    def get_l1reg(self):
        l1_reg = torch.sum(self.get_abs_fw())
        return l1_reg

    def get_l2reg(self):
        l2_reg = torch.sum(self.get_fw() ** 2)
        # l2_reg = 0.
        for f in self.fc:
            if isinstance(f, LocallyConnected):
                l2_reg += torch.sum(f.weight ** 2)
        return l2_reg

    def get_sole(self):
        d, q = self.d, self.q
        fw = self.get_fw()  # [d*m1, d+q]
        fw = fw.view(d, -1, d + q)  # [d, m1, d+q]
        S = torch.sum(fw * fw, dim=1).t()[d:,:]  # [d+q,d]
        reg = torch.sum(S)-torch.sum(torch.max(S,1)[0])
        return reg

    def get_D(self, A):  # D = C.*C
        d, q = self.d, self.q
        fw = self.get_fw()  # [d*m1, d+q]
        fw = fw.view(d, -1, d+q).transpose(1, 2)  # [d, d+q, m1]
        S = torch.matmul(A, fw[:, d:, :])
        S[S<0.3] = 0
        D = S + fw[:, :d, :]  # [d, d, m1]
        D = torch.sum(D * D, dim=2).t()
        return D

    def get_macro_D(self):  # -> S:qxd
        d, q = self.d, self.q
        fw = self.get_fw().data  # [d*m1, d+q]
        fw = fw.view(d, -1, d + q)  # [d, m1, d+q]
        S = torch.sqrt(torch.sum(fw * fw, dim=1).t())[d:,]  # [q,d]
        return S

    def h_func(self, A):
        d = self.d
        D = self.get_D(A)
        from Utils.Acyclic import acyclic
        D[D < 0.01] = 0
        h = acyclic(D)/d
        return h

    def get_penalty(self, A):
        d, q = self.d, self.q
        A = torch.abs(A)
        fw = self.get_abs_fw()  # [d*m1, d+q]
        fw = fw.view(d, -1, d+q).transpose(1, 2)  # [d, d+q, m1]
        return torch.sum(torch.sum(A.matmul(fw[:,d:,:]), dim=2).multiply(torch.sum(fw[:,:d,:], dim=2)))

    def get_macro_adj(self):  # -> S:(d+q)xd
        d, q = self.d, self.q
        fw = self.get_fw()  # [d*m1, d+q]
        fw = fw.view(d, -1, d + q)  # [d, m1, d+q]
        S = torch.sqrt(torch.sum(fw * fw, dim=1).t())  # [d+q,d]
        S = S.cpu().detach().numpy()
        return S

    def get_micro_adj(self, A):
        D = self.get_D(A)
        C = torch.sqrt(D)
        C = C.cpu().detach().numpy()
        return C



class MgCSL(nn.Module):
    def __init__(self,
                 AEneurons,
                 MLPneurons,
                 device_type,
                 device_num=0,
                 macro_graph=False,
                 precision=False,
                 sae_activation='LeakyReLU',
                 mlp_activation='Tanh',
                 bias=True,
                 seed=24,
                 mu=1e-3,
                 gamma=0.,
                 eta=300,
                 max_iter=100,
                 h_tol=0.1,
                 mu_max=1e+16,
                 C_threshold=0.2):
        super(MgCSL, self).__init__()
        self.AEneurons = AEneurons
        self.MLPneuron = MLPneurons
        self.device_type = device_type
        self.device_num = device_num
        self.macro_graph = macro_graph
        self.precision = precision
        self.sae_activation = sae_activation
        self.mlp_activation = mlp_activation
        self.bias = bias
        self.seed = seed
        self.mu = mu
        self.gamma = gamma
        self.eta = eta
        self.max_iter = max_iter
        self.h_tol = h_tol
        self.mu_max = mu_max
        self.C_threshold = C_threshold

        if device_type == 'cpu':
            device = torch.device('cpu')
            if precision:
                torch.set_default_tensor_type('torch.FloatTensor')
            else:
                torch.set_default_tensor_type('torch.DoubleTensor')
        elif device_type == 'gpu' and torch.cuda.is_available():
            torch.cuda.set_device(device_num)
            device = torch.device('cuda:{}'.format(device_num))
            if precision:
                torch.set_default_tensor_type('torch.cuda.FloatTensor')
            else:
                torch.set_default_tensor_type('torch.cuda.DoubleTensor')
        else:
            raise ValueError("GPU is unavailable, please set device_type to 'cpu'")
        self.device = device
        sae_act_func = eval('nn.{}()'.format(sae_activation))
        mlp_act_func = eval('nn.{}()'.format(mlp_activation))
        self.sae_act_func = sae_act_func
        self.mlp_act_func = mlp_act_func
        self.criterion = nn.MSELoss()
        self.d = AEneurons[0]
        self.q = AEneurons[-1]
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.set_num_threads(4)
        import random
        random.seed(seed)
        np.random.seed(seed)

        self.sae = SAE(neurons=AEneurons, device=device, act_func=sae_act_func, bias=bias)
        self.mlp = MLP(neurons=MLPneurons, q=self.q, device=device, act_func=mlp_act_func, bias=bias)

    def forward(self, x):
        z, y = self.sae(x)
        xz = torch.cat([x,z], dim=1)
        x_hat = self.mlp(xz)
        return y, x_hat

    def squared_loss(self, output, target):
        n = target.shape[0]
        loss = 0.5 / n * torch.sum((output - target) ** 2)
        return loss

    def learn(self, x):
        if not isinstance(x, torch.Tensor):
            raise ValueError('Type of x must be tensor!')
        mu, gamma, eta, h = self.mu, self.gamma, self.eta, torch.inf
        max_iter, h_tol, mu_max, C_threshold = self.max_iter, self.h_tol, self.mu_max, self.C_threshold
        optimizer = LBFGSBScipy(self.parameters())
        for _ in range(max_iter):
            while mu < mu_max:
                def closure():
                    optimizer.zero_grad()
                    # loss of auto-encoder
                    A = self.sae.get_path_product()
                    y, x_hat = self(x)
                    encoder_l1reg = 0.1 * self.sae.get_l1reg()
                    L1 = 0.01*self.squared_loss(y, x) + encoder_l1reg
                    # loss of mlp
                    mlp_l1reg = 0.01 * self.mlp.get_l1reg()
                    mlp_l2reg = 0.5 * 0.01 * self.mlp.get_l2reg()
                    h_val = self.mlp.h_func(A)
                    acyclic = 0.5*mu*h_val*h_val + gamma*h_val
                    penalty = 0.01 * self.mlp.get_penalty(A)
                    L2 = self.squared_loss(x_hat, x) + mlp_l1reg + mlp_l2reg + acyclic + penalty + self.mlp.get_sole()
                    obj = L1 + L2
                    obj.backward()
                    return obj
                optimizer.step(closure, self.device)
                with torch.no_grad():
                    self.to(self.device)
                    A = self.sae.get_path_product()
                    h_new = self.mlp.h_func(A).item()
                if h_new > 0.25*h:
                    mu *= eta
                else:
                    break
            gamma += mu*h_new
            h = h_new
            if h_new <= h_tol or mu >= mu_max:
                break
        A = self.sae.get_path_product()
        if self.macro_graph:
            S = self.mlp.get_macro_adj()
            return A, S
        else:
            C = self.mlp.get_micro_adj(A)

            C[C<C_threshold] = 0
            from Utils.is_acyclic import is_acyclic
            with torch.no_grad():
                # Find the smallest threshold that removes all cycle-inducing edges
                thresholds = np.unique(C)
                epsilon = 1e-8
                for step, t in enumerate(thresholds):
                    to_keep = np.array(C > t + epsilon)
                    new_adj = C * to_keep
                    if is_acyclic(new_adj, device=self.device):
                        C = new_adj
                        break
            C[C!=0] = 1
            return C