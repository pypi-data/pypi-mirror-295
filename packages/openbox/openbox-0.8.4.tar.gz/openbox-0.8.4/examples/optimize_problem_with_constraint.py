# License: MIT

import numpy as np
import matplotlib.pyplot as plt
from openbox import Optimizer, space as sp


def mishra(config: sp.Configuration):
    X = np.array([config['x%d' % i] for i in range(2)])
    x, y = X[0], X[1]
    t1 = np.sin(y) * np.exp((1 - np.cos(x))**2)
    t2 = np.cos(x) * np.exp((1 - np.sin(y))**2)
    t3 = (x - y)**2

    result = dict()
    result['objectives'] = [t1 + t2 + t3, ]
    result['constraints'] = [np.sum((X + 5)**2) - 25, ]
    return result


if __name__ == "__main__":
    params = {
        'float': {
            'x0': (-10, 0, -5),
            'x1': (-6.5, 0, -3.25)
        }
    }
    space = sp.Space()
    space.add_variables([
        sp.Real(name, *para) for name, para in params['float'].items()
    ])

    opt = Optimizer(
        mishra,
        space,
        num_constraints=1,
        num_objectives=1,
        surrogate_type='gp',
        acq_optimizer_type='random_scipy',
        max_runs=50,
        task_id='soc',
        # Have a try on the new HTML visualization feature!
        # visualization='advanced',  # or 'basic'. For 'advanced', run 'pip install "openbox[extra]"' first
        # auto_open_html=True,  # open the visualization page in your browser automatically
    )
    history = opt.run()

    print(history)

    history.plot_convergence(true_minimum=-106.7645367)
    plt.show()

    # install pyrfr to use get_importance()
    # print(history.get_importance())

    # Have a try on the new HTML visualization feature!
    # You can also call visualize_html() after optimization.
    # For 'show_importance' and 'verify_surrogate', run 'pip install "openbox[extra]"' first
    # history.visualize_html(open_html=True, show_importance=True, verify_surrogate=True, optimizer=opt)
