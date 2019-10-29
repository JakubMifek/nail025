import utils

utils.plot_experiments('.', [
    'partition/k10_p100_g500_x0.8_m0.2_mf0.1_r10(default)',
    'final/k10-p200-g20000-s10-x0.0-m0.0-mf0.05-ms0.33-dc0.4-r10(tuned)',
    'final_better_9/k10-p500-g10000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned)',
    'final_better_10/k10-p500-g20000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned)'
    ],
    rename_dict={
        'final/k10-p200-g20000-s10-x0.0-m0.0-mf0.05-ms0.33-dc0.4-r10(tuned)': 'final/k10-p200-g20000-s10-x0.0-m0.0-mf0.05-ms0.33-dc0.4-r10(tuned - default fit)',
        'final_better_9/k10-p500-g10000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned)': 'final_better_9/k10-p500-g10000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned - enhanced fit)',
        'final_better_10/k10-p500-g20000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned)': 'final_better_10/k10-p500-g20000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned - enhanced longer)'
    })

