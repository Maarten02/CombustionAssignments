import matplotlib.pyplot as plt

def plot_A_vs_fblrg(fig, ax, data, r):
    ax.scatter(data['FBLGR'], data['A'], label=f'r/d = {r}')

    return fig, ax

def plot_layout_2bi(fig, ax, x):

    ax.set_xlabel('FBLGR [-]')
    ax.set_ylabel('A [-]')
    ax.set_title(f'A vs. FBLGR for various r/d positions at x/d = {x}')

    ax.legend()
    ax.grid()

    ax.legend(loc='center left', bbox_to_anchor=(-0.42, 0.5))
    fig.savefig(f'./figures/A_vs_FBLGR_x_{int(x*10):03}.pdf', bbox_inches='tight', pad_inches=0.2)


def plot_2bii(data, bins, x):

    fig, ax = plt.subplots()

    FBLRG_arr = []
    A_mean_arr = []

    for i in range(len(bins) - 1):
        filtered_df = data[(data['FBLGR'] >= bins[i]) & (data['FBLGR'] <= bins[i+1])]
        FBLRG_arr.append(0.5 * (bins[i] + bins[i+1]))
        A_mean_arr.append(filtered_df['A'].mean())

    ax.plot(FBLRG_arr, A_mean_arr, marker='.')

    ax.set_xlabel('FBLGR [-]')
    ax.set_ylabel('A [-]')
    ax.set_title(f'averaged A vs. FBLGR using various r/d positions at x/d = {x}')

    ax.grid()

    fig.savefig(f'./figures/A_mean_vs_FBLGR_x_{int(x*10):03}.pdf', bbox_inches='tight', pad_inches=0.2)