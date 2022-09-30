'''
Trying to run a Salabim model with animation from within a Streamlit application.

Requirements:
    pip install salabim streamlit

Run example:
    streamlit run streamsalabim.py

'''
import salabim as sim
from numpy.random import randint


class X(sim.Component):
    def setup(self, server):
        self.server = server

    def process(self):
        yield self.request(self.server)
        yield self.hold(sim.Exponential(1))


def simulate(seed, till=30, animate=True):
    sim.reset()
    env = sim.Environment(random_seed=seed)
    env.animate(animate)

    server = sim.Resource()
    sim.ComponentGenerator(X, iat=sim.Exponential(1), server=server)
    sim.AnimateQueue(server.requesters(), x=700, y=200)
    sim.AnimateQueue(server.claimers(), x=700, y=100)
    sim.AnimateText('requesters', x=750, y=200)
    sim.AnimateText('claimers', x=750, y=100)

    try:
        env.run(till=till)
    except sim.SimulationStopped:
        msg = f'simulation stopped, t={env.now()}'
    except Exception as e:
        msg = f'another exception: {e}'
    else:
        msg = f'simulation ended, t={env.now()}'

    return {
        'seed': seed,
        'msg': msg,
        'occupancy': server.occupancy.mean(),
        'waiting_time': server.requesters().length_of_stay.mean(),
    }


if __name__ == '__main__':
    import streamlit as st
    from multiprocessing import Pool

    st.title('Salabim')

    if st.button('without animation'):
        result = simulate(randint(100000), animate=False)
        st.write(result)

    if st.button('with animation'):
        with Pool(1) as p:
            results = p.map(simulate, [randint(100000)])
        st.write(results[0])
