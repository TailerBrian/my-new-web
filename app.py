import pandas as pd
import scipy.stats
import streamlit as st
import time

# estas são variáveis persistentes preservadas à medida que o Streamlit executa novamente esse script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Jogando uma moeda')

chart = st.line_chart([[0.5]])

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
start_button = st.button('Executar')

if start_button:
    st.session_state['experiment_no'] += 1
    st.write(f'Executando o experimento nº {st.session_state["experiment_no"]} de {number_of_trials} tentativas.')
    
    mean = toss_coin(number_of_trials)
    
    # Guarda os resultados do teste atual na tabela de histórico
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame([{'no': st.session_state['experiment_no'], 'iterations': number_of_trials, 'mean': mean}])
    ], ignore_index=True)

# Exibe a tabela com o histórico de todos os testes feitos abaixo do gráfico
st.dataframe(st.session_state['df_experiment_results'])
