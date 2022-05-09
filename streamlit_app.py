import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.transforms as mtrans
from heapq import nlargest, nsmallest


@st.cache
def load_data():
    detailed_df = pd.read_csv('detailed_top_10.csv', converters={'Kills': pd.eval, 'Assists' : pd.eval,
                                'Deaths' : pd.eval, 'MVPs' : pd.eval, 'Score' : pd.eval})
    return detailed_df


st.title("CS:GO Stats")
st.markdown("Data from all my CS:GO competitive matches.")
data = load_data()


# Display the tabled data
df = pd.read_csv('top_10.csv')
if 'Unnamed: 0' in df.columns:
    del df['Unnamed: 0']
st.dataframe(df)


# First chart area, will display a simple boxplot
# of each of the players in the detailed df
st.subheader('Player Averages')
option = st.selectbox('Select stat to view',
                        ("Kills", "Assists", "Deaths", "MVPs", "Score"), index=0)


fig, ax = plt.subplots()
ax = sns.boxplot(data=data[option])
ax.set_xticklabels(data['Name'].to_list(), rotation=45)
trans = mtrans.Affine2D().translate(-40, 0)
for t in ax.get_xticklabels():
    t.set_transform(t.get_transform()+trans)
fig.tight_layout()
st.pyplot(fig)


# Best/Worst comparison
# Grab the index of the top or bottom 10 scores of selected
# players, plot on a scatter chart for comparison
st.subheader('Best/Worst Comparison')
names = data['Name'].to_list()
player1_name = st.selectbox('Select Player 1',
                                names)
player1_best_worst = st.select_slider(f'{player1_name} at their best or worst?',
                                        options=['Best', 'Worst'])
player2_name = st.selectbox('Select Player 2',
                                names)
player2_best_worst = st.select_slider(f'{player2_name} at their best or worst? ',
                                        options=['Best', 'Worst'])

idx = data.index[data['Name']==player1_name]
idx2 = data.index[data['Name']==player2_name]

if player1_best_worst == 'Worst':
    p1_x_data = nsmallest(10, data['Kills'][idx[0]])
    p1_y_data = nsmallest(10, data['Score'][idx[0]])
if player1_best_worst == 'Best':
    p1_x_data = nlargest(10, data['Kills'][idx[0]])
    p1_y_data = nlargest(10, data['Score'][idx[0]])

if player2_best_worst == 'Worst':
    p2_x_data = nsmallest(10, data['Kills'][idx2[0]])
    p2_y_data = nsmallest(10, data['Score'][idx2[0]])
if player2_best_worst == 'Best':
    p2_x_data = nlargest(10, data['Kills'][idx2[0]])
    p2_y_data = nlargest(10, data['Score'][idx2[0]])

fig2, ax2 = plt.subplots()
ax2 = plt.scatter(p1_x_data, p1_y_data, marker="X")
ax2 = plt.scatter(p2_x_data, p2_y_data, marker="X")
plt.xlabel("Kills")
plt.ylabel("Score")
plt.legend([player1_name, player2_name])
st.pyplot(fig2)