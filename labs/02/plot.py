import utils

utils.plot_experiments('.', [
    'partition/k10_p100_g500_x0.8_m0.2_mf0.1_r10(default)',
    'final_bad/k10-p800-g10000-s10-x0.0-m0.00125-mf0.01-ms0.15-dc0.0-r10(tuned)',
    'final_worse/k10-p800-g10000-s10-x0.0-m0.00125-mf0.01-ms0.15-dc0.0-r10(tuned)',
    'final_bad_but_better/k10-p1024-g20480-s10-x0.0-m0.1-mf0.002-ms0.15-dc0.0-r10(tuned)',
    'final_better_9/k10-p500-g10000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned)',
    'final_better_11/k10-p800-g20000-s10-x0.0-m0.001-mf0.02-ms0.15-dc0.05-r10(tuned)'
],
    rename_dict={
        'final_better_11/k10-p800-g20000-s10-x0.0-m0.001-mf0.02-ms0.15-dc0.05-r10(tuned)': 'final_better_11/k10-p800-g20000-s10-x0.0-m0.001-mf0.02-ms0.15-dc0.05-r10(tuned - best found)',
        'final_better_9/k10-p500-g10000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned)': 'final_better_9/k10-p500-g10000-s10-x0.0-m0.002-mf0.05-ms0.33-dc0.1-r10(tuned - enhanced fit)',
        'final_bad/k10-p800-g10000-s10-x0.0-m0.00125-mf0.01-ms0.15-dc0.0-r10(tuned)': 'final_bad/k10-p800-g10000-s10-x0.0-m0.00125-mf0.01-ms0.15-dc0.0-r10(tuned - no special mutations)',
        'final_worse/k10-p800-g10000-s10-x0.0-m0.00125-mf0.01-ms0.15-dc0.0-r10(tuned)': 'final_worse/k10-p800-g10000-s10-x0.0-m0.00125-mf0.01-ms0.15-dc0.0-r10(tuned - no special mut & init)',
        'final_bad_but_better/k10-p1024-g20480-s10-x0.0-m0.1-mf0.002-ms0.15-dc0.0-r10(tuned)': 'final_bad_but_better/k10-p1024-g20480-s10-x0.0-m0.1-mf0.002-ms0.15-dc0.0-r10(tuned - init + low params - no special mut)',
})
