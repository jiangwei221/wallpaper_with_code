import numpy as np
import torch
import torch.nn as nn
import imageio


def init_weights(m):
    if type(m) == nn.Linear:
        torch.nn.init.xavier_normal_(m.weight)


class SimpleMappingNet(nn.Module):
    def __init__(self):
        super(SimpleMappingNet, self).__init__()
        self.mlp = nn.Sequential(
            nn.Linear(2, 32, bias=False),
            nn.Tanh(),
            nn.Linear(32, 128, bias=False),
            nn.Tanh(),
            nn.Linear(128, 128, bias=False),
            nn.Tanh(),
            nn.Linear(128, 3, bias=False),
            nn.Tanh()
        )
        self.mlp.apply(init_weights)

    def forward(self, x):
        return self.mlp(x)


def main():
    BATCH_SIZE = 256
    RESOLUTION = 2000
    VIEW_RANGE = 10
    smn = SimpleMappingNet().cuda()
    x, y = torch.meshgrid(torch.linspace(-VIEW_RANGE, VIEW_RANGE, steps=RESOLUTION),
                          torch.linspace(-VIEW_RANGE, VIEW_RANGE, steps=RESOLUTION))
    x, y = x.flatten(), y.flatten()
    xy = torch.cat([x[:, None], y[:, None]], axis=1).cuda()
    batches = torch.split(xy, BATCH_SIZE, 0)
    color_list = []
    for batch in batches:
        out_color = smn(batch)
        color_list.append(out_color.detach().cpu())
    color_list = torch.cat(color_list, dim=0).numpy()
    color_list = color_list.reshape(RESOLUTION, RESOLUTION, 3)
    color_list = (color_list - color_list.min()) / np.ptp(color_list)
    imageio.imsave('./color.png', color_list)


if __name__ == "__main__":
    main()
