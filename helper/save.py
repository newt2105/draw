import os
def savePlot(fig, filename, folder='fig'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    fig.tight_layout()
    fig.savefig(filepath)
    print(f"Figure saved as {filepath}")