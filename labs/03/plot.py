import utils

for graph in ['f01', 'f02', 'f06', 'f08', 'f10']:
    utils.plot_experiments('continuous', [
        '.'.join(['default', graph]),
        '.'.join(['diff-threesome', graph]),
        '.'.join(['diff-threesome-small-F', graph]),
        '.'.join(['diff-threesome-small-CF', graph]),
        '.'.join(['diff-basic-adaptive', graph]),
        '.'.join(['diff-threesome-adaptive', graph]),
        '.'.join(['diff-gangbang-adaptive', graph]),
    ])
