
from torch import nn

class Autoencoder(nn.Module):
    def __init__(self, input_dim, xcode_dim=2, act_fn=nn.ELU, with_bn=False):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 14),
            act_fn(),
            nn.BatchNorm1d(14) if with_bn else nn.Identity(),

            nn.Linear(14, 10),
            act_fn(),
            nn.BatchNorm1d(10) if with_bn else nn.Identity(),

            nn.Linear(10, 8),
            act_fn(),
            nn.BatchNorm1d(8) if with_bn else nn.Identity(),

            nn.Linear(8, 4),
            act_fn(),
            nn.BatchNorm1d(4) if with_bn else nn.Identity(),

            nn.Linear(4, xcode_dim),
            nn.Sigmoid(),
            # nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(xcode_dim, 4),
            act_fn(),
            nn.BatchNorm1d(4) if with_bn else nn.Identity(),

            nn.Linear(4, 8),
            act_fn(),
            nn.BatchNorm1d(8) if with_bn else nn.Identity(),

            nn.Linear(8, 10),
            act_fn(),
            nn.BatchNorm1d(10) if with_bn else nn.Identity(),

            nn.Linear(10, 14),
            act_fn(),
            nn.BatchNorm1d(14) if with_bn else nn.Identity(),

            nn.Linear(14, input_dim),
        )

    def get_xcode(self, x):
        return self.encoder(x)

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x