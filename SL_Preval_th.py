import streamlit as st

import pandas as pd
import numpy as np
import plotly
import altair as alt

from scipy.stats import binom

st.title("Covid Prevalence Calculator")

population = int(st.text_input("Population Size", value = 69984915))
total_case = st.text_input("Cumulative Case", value = 481967)
cured = st.text_input("Recovered", value = 327789)
active_case = int(total_case) - int(cured)

#death = 3811

st.write("Active Case: " + str(active_case))

preval_rate = active_case / population

st.header("Prevalence Rate: *"+str(preval_rate)+"*")

max_pop = st.slider("Max Population", 0, 10000, value = 4000)

pop = []
for i in range(0, max_pop):
    pop.append(i)

#Graph itself

graph = pd.DataFrame()
graph["Population"] = pop

atleastone = []
for y in range(0,len(pop)):
    atleastone.append(1 - binom.pmf(0, graph["Population"].iloc[y], preval_rate))

graph["Chance at least 1 is infected"] = atleastone
graph.set_index("Population", inplace = True)
st.title("Within *"+str(max_pop)+"* people, "+"approximately *"+str(round(preval_rate * max_pop))+"* people is infected.")

st.subheader("Chance *at least 1* person is infected (Probability/ Population)")
st.line_chart(graph)

st.write(graph)

#vaccine success rate, 2 dose, PREVENTING SEVERE DISEASE
pfizer = .95
moderna =  .941
jj = .86
az = .76
sinovac = .51

vax_list = (pfizer, moderna, jj, az, sinovac)
vax_names = ("pfizer", "moderna", "jj", "az", "sinovac")

pop = []
for i in range(0, 10000):
    pop.append(i)

graph = pd.DataFrame()
graph["Population"] = pop

for i in range(0, len(vax_list)):
    infected = []
    for y in range(0,len(pop)):
        infected.append( 1 - binom.pmf( 0 , graph["Population"].iloc[y] , ((1 - vax_list[i]) * preval_rate) ) )

    graph[str(vax_names[i])] = infected

graph.set_index("Population", inplace = True)

st.title("Chance of being infected with each vaccine")

st.subheader("Probability/ Population")
st.line_chart(graph)
st.write('''
Vaccine efficiency according to https://www.yalemedicine.org/news/covid-19-vaccine-comparison and https://www.who.int/news-room/feature-stories/detail/the-sinovac-covid-19-vaccine-what-you-need-to-know
''')