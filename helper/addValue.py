def addValues(bars, ax):
    for bar in bars:
        for b in bar:
            yval = b.get_height()
            ax.text(b.get_x() + b.get_width()/2, yval, f'{round(yval, 1):.1f}', ha='center', va='bottom')