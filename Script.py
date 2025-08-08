import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# GitHub Link : https://github.com/0-mazooon-0/No-show-Appointments-Dataset-Dashboard

# === Load and preprocess data ===
df = pd.read_csv(r"D:\DEPI\3- Preprocessing & Visualization\Dash project\modified.csv")

# === Figure 1: Gender ===
gender_groups = df.groupby('No-show')['Gender'].value_counts().reset_index(name='count')
total_f = gender_groups['count'][gender_groups['Gender'] == 0].sum()
total_m = gender_groups['count'][gender_groups['Gender'] == 1].sum()
gender_groups['%OutOfGender'] = gender_groups.apply(
    lambda x: (x['count']/total_f)*100 if x['Gender'] == 0 else (x['count']/total_m)*100, axis=1
)
fig1 = px.bar(
    x=['Female', 'Male', 'Female', 'Male'],
    y=gender_groups['count'],
    color=['Attend', 'Attend', "Didn't attend", "Didn't attend"],
    hover_name=['Attend', 'Attend', "Didn't attend", "Didn't attend"],
    hover_data={'%OutOfGender': gender_groups['%OutOfGender'].values}
)
fig1.update_layout(title="Attendance by Gender", xaxis_title="Gender", yaxis_title="Attendance")

# === Figure 2: ScheduledMonth ===
month_gp = df.groupby('ScheduledMonth')['No-show'].value_counts().reset_index(name='count')
fig2 = px.bar(
    x=month_gp['ScheduledMonth'],
    y=month_gp['count'],
    color=month_gp['No-show'],
    color_continuous_scale='Viridis'
)
fig2.update_layout(title="Attendance by Scheduled Month", xaxis_title="Month", yaxis_title="Count")

# === Figure 3: AppointmentMonth ===
month_gp = df.groupby('AppointmentMonth')['No-show'].value_counts().reset_index()
fig3 = px.bar(x = month_gp['AppointmentMonth'], y = month_gp['count'], color = month_gp['No-show'], color_continuous_scale = 'Viridis')
fig3.update_layout(
    title = "Attendance by AppointmentMonth",
    xaxis_title="Months",
    yaxis_title="Count"
)

# === Figure 4: Age ===
age_group = df.groupby('Age')['No-show'].value_counts().reset_index(name='count')
fig4 = px.line(
    x=age_group['Age'],
    y=age_group['count'],
    facet_col=age_group['No-show'].apply(lambda x: "Attended" if x == 0 else "Didn't")
)
fig4.update_layout(title="Attendance by Age", xaxis_title="Age", yaxis_title="Count")

# === Figure 5: Neighbourhood ===
neigh_gp = df.groupby('Neighbourhood')['No-show'].value_counts().sort_values().reset_index(name='count')
fig5 = px.bar(
    x=neigh_gp['Neighbourhood'],
    y=neigh_gp['count'],
)
fig5.update_layout(
    xaxis=dict(dtick=2),
    title="Attendance by Neighbourhood",
    xaxis_title="Neighbourhood",
    yaxis_title="Count"
)

# === Figure 6: Scheduled Day of Week ===
dow_gp = df.groupby('ScheduledDayofWeek')['No-show'].value_counts().reset_index(name='count')
fig6 = px.bar(
    x=dow_gp['ScheduledDayofWeek'],
    y=dow_gp['count'],
    facet_col=dow_gp['No-show'].apply(lambda x: "Attended" if x == 0 else "Didn't"),
    color=dow_gp['ScheduledDayofWeek'].map({
        0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
        4: 'Friday', 6: 'Sunday'
    })
)
fig6.update_layout(title="Attendance by Day of Week Scheduled", xaxis_title="Day of Week", yaxis_title="Count")

# === Figure 7: Appointment Day of Week ===
day_of_week_gp = df.groupby('AppointmentDayofWeek')['No-show'].value_counts().reset_index()
fig7 = px.bar(x = day_of_week_gp['AppointmentDayofWeek'], y = day_of_week_gp['count'], facet_col = day_of_week_gp['No-show'].apply(lambda x : "Attended" if x == 0 else "Didn't"), color = day_of_week_gp['AppointmentDayofWeek'].map({0: 'Monday', 1: 'Tuesday',
2: 'Wednesday', 3: 'Thursday',
4: 'Friday', 6: 'Sunday'}))

fig7.update_layout(
    title = "Attendance by Day of Week Appointed",
    xaxis_title="Day of week number",
    yaxis_title="Count",

)

# === Figure 8: Difference ===
by_difference = df.groupby('Difference')['No-show'].value_counts().reset_index().sort_values('Difference')
by_difference['Difference'] = by_difference['Difference']
fig8 = px.line(by_difference,x = 'Difference', y = 'count', facet_col = by_difference['No-show'].apply(lambda x : "Attended" if x == 0 else "Didn't"))

fig8.update_layout(
    title = "Number of pepole attended/not grouped by the difference between the 2 dates",
    xaxis_title="Day of week number",
    yaxis_title="Count",
)


# === Build Dash App ===
app = Dash(__name__)

app.layout = html.Div([
    html.H1("No-show Appointments Dashboard", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    html.H2("Observations: " 
    "As we can see people barely scheduled appointments on January and Feburary. Also people on March and June barely missed appointments "
    ),
    dcc.Graph(figure=fig3),
    html.H2("Observations: " 
    "As we can see people didn't appoint appointments on January and Feburary and March. Also barely missed appointments on April"
    ),
    html.H2("Final Observation: " 
    "May is a busy month with the highest rate and count of people missing their appointments"
    ),
    dcc.Graph(figure=fig4),
    html.H2("Observation: " 
    "As we can see the age affects absence of people. Where the more the patient is older the more likely they didn't miss their appointment"
    ),
    dcc.Graph(figure=fig5),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7),
    html.H2("Final Observation: " 
    "People are more likely to be absent on Tuesday and Wednesday"
    ),
    dcc.Graph(figure=fig8),
    html.H2("Observation: " 
    "As we can see difference affects attendance and absecne. Where the more the difference in days is bigger the less people show-up in appointmnets"
    ),
])

if __name__ == '__main__':
    app.run(debug=True)

