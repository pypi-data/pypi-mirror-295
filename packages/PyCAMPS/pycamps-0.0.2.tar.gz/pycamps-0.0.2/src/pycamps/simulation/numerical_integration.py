import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp
from pycamps.logger import configure_logging

logger = configure_logging()
global_flag = 0

class NumericalIntegration:
    def __init__(self, dynamics_fn, time_dep=False):
        if time_dep:
            # Not sure what timedep is supposed to do
            # The function must take in input states and return their derivatives
            self.fhandle = lambda t, x: dynamics_fn(t, *x)
        else:
            self.fhandle = lambda t, x: dynamics_fn(*x)

    def integrate(self, tspan, xf, method='trapezoid_adaptive'):
        if method == 'trapezoid_adaptive':
            return self.trapezoid_adaptive(tspan, xf)
        elif method in ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA']:
            return self.solve_ivp(tspan, xf, method)
        else:
            logger.error(f"Method {method} not supported")
            raise ValueError(f"Method {method} not supported")

    def trapezoid_adaptive(self, tspan, x0, delt=1e-6, tolr=1e-6):
        """
        Solves dynamic system of equations using adaptive trapezoid method.

        Parameters:
        - fhandle: function handle
        - tspan: time of integration (start and end time)
        - x0: initial values
        - time_dep: True if time-dependent dynamics, False otherwise
        - delt: time step
        - tolr: acceptable infinite norm tolerance

        Returns:
        - time: vector of time instants
        - xspan: vector of values of x at different time instants
        - delt: adapted time step
        """
        logger.debug(f"Using adaptive trapezoid method with delt={delt} and tolr={tolr}")
        t = tspan[0] # Initial time
        logger.info(f"Beginning simulation at t = {t}")
        xspan, time = [], [] # Initialize the vectors to store states and output
        while t < tspan[1]:
            # State and output after one time step
            def newf(x):
                dxexp = np.array(self.fhandle(t, x0))
                logger.debug(f"t={t}, dxexp={dxexp}")
                dximp = np.array(self.fhandle(t, x))
                logger.debug(f"t={t}, dximp={dximp}")
                return x - x0 - delt / 2 * (dxexp + dximp)

            # Set options for fsolve
            options = {'maxfev': 50}
            x1, info, ier, mesg = fsolve(newf, x0, full_output=True, xtol=tolr, **options)
            logger.debug(f"t={t}, x1={x1}")
            nf = newf(x1)
            logger.debug(f"t={t}, nf={nf}")

            # Adaptive time step chosen for next time instant
            delt = 0.9 * (tolr / np.linalg.norm(nf, np.inf)) ** (1 / 3) * delt
            logger.debug(f"t={t}, delt={delt}")

            # If smooth response needed
            if delt > 1e-2:
                delt = 1e-2
                logger.debug(f"t={t}, clipped delt={delt}")

            if ier == 2:
                x1 = x0
                logger.debug(f"t={t}, reached maxfev, x1={x1}")
            else:
                t += delt
                logger.debug(f"Next time: {t}")
                if t > tspan[1]:
                    t = tspan[1]

            # In case of simulating faults or events - flag to be assigned a value 1 by the
            # program that calls this function - Logic for how long flag is 1 is dictated by
            # the program that calls this function 
            if global_flag == 1:
                delt = 1e-6

            x0 = x1

            xspan.append(x0)
            time.append(t)

        logger.info(f"Ending simulation at t = {t}")
        return np.array(time), np.array(xspan), delt

    def solve_ivp(self, tspan, x0, method):
        '''
        Solve the differential equation using the specified method
        '''
        logger.debug(f"Using {method} method")
        # Integrate the differential equation
        sol = solve_ivp(fun=self.fhandle,
                        t_span=tspan,
                        y0=x0,
                        method=method)

        # Handle the results
        time = sol.t
        xspan = sol.y.T

        # Check if the event was triggered
        if sol.status == 1:
            logger.info(f"Event triggered at t = {sol.t_events[0][0]}")

        # Handle global flag for faults or events
        if global_flag == 1:
            delt = 1e-6
        else:
            delt = (tspan[1] - tspan[0]) / len(time)

        logger.info(f"Ending simulation at t = {time[-1]}")
        return time, xspan, delt