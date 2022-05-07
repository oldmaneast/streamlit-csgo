import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.transforms as mtrans


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