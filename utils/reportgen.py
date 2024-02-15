import streamlit as st
import xhtml2pdf.pisa as pisa
import plotly.express as px
import plotly.io as pio
import folium
from tabulate import tabulate
from io import BytesIO
import base64
import pandas as pd

# ensure the plotly chart is rendered as an image with the right colors. 
pio.templates.default = "plotly"

#Sample data
df = px.data.gapminder() 

# # Plotly chart
fig = px.scatter(df.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

# # Folium map
map_center = [40.7128, -74.0060]  # New York City 
my_map = folium.Map(location=map_center, zoom_start=10)
folium.Marker(map_center, tooltip='NYC').add_to(my_map)

# Streamlit app
st.title("PDF Generation Demo")
st.plotly_chart(fig)
st.subheader("Folium Map")

img_bytes = BytesIO()
fig.write_image(img_bytes, format='png') 
img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

df = pd.DataFrame({'color': ['blue', 'green', 'red', 'blue'], 
                   'size': ['S', 'M', 'M', 'L']})

df_dummies = pd.get_dummies(df)
df_html = tabulate(df_dummies, headers='keys', tablefmt='html') 


# PDF generation logic
def create_pdf():
    
    
    html = f"""
        <html>
        <head>
            <title>My Report</title>
              <style>
          img {{ max-width: 100%; }} 
          table {{ border-collapse: collapse; width: 80%;}}  
          th, td {{ border: 1px solid black; padding: 5px;}}
        </style>
        </head>
        <body>
            <h1>My Report</h1>
            <img src="data:image/png;base64,{img_base64}" alt="Plotly Chart"> 
             {df_html} 
        </body>
        </html>
        """
    
    with open("/Users/ivanthung/code/mock-up-umdashboard/test_files/test.html", "w", encoding='utf-8') as file:
        file.write(html)

    pdf = pisa.CreatePDF(html, dest=open('report.pdf', 'wb'))
    
    if not pdf.err:
        pdf.dest.close()  #  Write the PDF content and close the file  
        st.success("PDF Generated Successfully!")
        with open('report.pdf', 'rb') as file:
            st.download_button(label="Download PDF", data=file, file_name='report.pdf', mime='application/pdf')
    else:
        st.error("Error generating PDF.")
        

st.button("Generate PDF", on_click=create_pdf)

