import utils

for graph in ['f01', 'f02', 'f06', 'f08', 'f10']:
    utils.plot_experiments('continuous', [
        '.'.join(['default', graph]),
        '.'.join(['random', graph]),
        '.'.join(['intelligent', graph]),
        '.'.join(['coin', graph]),
        '.'.join(['random_adaptive', graph]),
        '.'.join(['intelligent_adaptive', graph]),
        '.'.join(['coin_adaptive', graph])
    ])
