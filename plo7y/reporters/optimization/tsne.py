"""
t-distributed Stochastic Neighbor Embedding (t-SNE) visualization of classes
in hyperplane.

**Please** read more about t-SNE [here](https://distill.pub/2016/misread-tsne/)
to help with interpreting the results.

Based on: https://blog.applied.ai/visualising-high-dimensional-data/
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import seaborn as sns
from sklearn.preprocessing import StandardScaler


print(__doc__)


def base16(number):
    """0-255 -> 00-FF"""
    return number.to_bytes(1, 'little').hex()


def main(df, var1, var2, var3, saveFigPath=None):
    # master_dataframe_ is exported by class_subset_vs_all_dists
    df = df.dropna()

    tsne = TSNE(
        n_components=2, random_state=0,
        perplexity=30  # should be ~ size of smallest expected cluster
    )

    assert len(df["score"]) > 0
    dfsvd = df.copy()
    dfsvd.pop("score")
    print(dfsvd.shape)
    print("building tsne using :")
    print(dfsvd.head())

    # TODO: should we scale here or use raw values?
    X = StandardScaler().fit_transform(dfsvd.values)
    # X = dfsvd.values
    Z = tsne.fit_transform(X)
    dftsne = pd.DataFrame(Z, columns=['x', 'y'], index=dfsvd.index)
    # === calc 3 color components from selected variables in df
    MAX_COLOR = 255
    dftsne['r'] = (
        MAX_COLOR * (df[var1] - min(df[var1]))/(max(df[var1]) - min(df[var1]))
    ).apply(round).apply(int)
    dftsne['g'] = (
        MAX_COLOR * (df[var2] - min(df[var2]))/(max(df[var2]) - min(df[var2]))
    ).apply(round).apply(int)
    dftsne['b'] = (
        MAX_COLOR * (df[var3] - min(df[var3]))/(max(df[var3]) - min(df[var3]))
    ).apply(round).apply(int)
    dftsne['color'] = (  # hexidecimal color code
        '#' + dftsne['r'].apply(base16).apply(str) +
        dftsne['g'].apply(base16).apply(str) +
        dftsne['b'].apply(base16).apply(str)
    )
    MIN_SIZE = 1
    MAX_SIZE = 10
    dftsne['size_float'] = (
        MAX_SIZE * (df['score'] - min(df['score']))/max(df['score']) + MIN_SIZE
    )
    dftsne['size'] = dftsne['size_float'].apply(round).apply(int)
    print(dftsne)
    g = sns.lmplot(
        'x', 'y', dftsne, hue='color', palette=list(dftsne['color']),
        fit_reg=False,
        scatter_kws={'alpha': 0.7, 's': 60},
        # size=list(dftsne['size'])
        # size='size'  # TODO: is this supported?
    )
    g.axes.flat[0].set_title(
        'Scatterplot of data reduced to 2D using t-SNE ' +
        'Colorized R={} G={} B={}. '.format(var1, var2, var3) +
        'Point size is score.'
    )

    if (saveFigPath is None):
        plt.show()
    else:
        plt.savefig(str(saveFigPath), bbox_inches='tight')

if __name__ == "__main__":
    dta = pd.read_csv('sample_data.csv')
    main(dta, 'var1', 'var2', 'var3')
