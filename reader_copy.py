from pypdf import PdfReader, PdfWriter
import pandas as pd

reader = PdfReader("Case documentation.pdf")
writer = PdfWriter()
df = pd.read_csv("San An Case Data.csv")
caseNumber = 1
pageNumber = 0 
fields = reader.get_fields()

#Initializing and formating dataframe
karlDf=df.loc[(df['Tech Name'] == "Karl Ngantcha-Mbagna") | (df['2nd Tech Name'] == "Karl Ngantcha-Mbagna")]
karlDf = karlDf.reset_index()
karlDf['Times concatenated'] = karlDf['Hospital in'].astype(str)  + '/' + karlDf['Hospital out'].astype(str) 
karlGrouped = karlDf.groupby('Date of services').head(2).reset_index()

#Parsing through pdf pages
for pn in range (2, 9):
    pages = reader.pages[pn-2]
    writer.add_page(pages)
    i = 0
    #Parsing through dataframe rows
    for _, row in karlGrouped.head(22).iterrows():
        fieldNames = ["DATE Of PROCEDURERow", "HOSPITAl NAME PHONE NUMBERRow", "PRIMARy SURGEONRow", "TYPE OF SURGERYRow", "TIME IN OUT OF ROOMRow"]
        dfFieldNames = ["Date of services", "Hospital", "Surgeon", "Procedure Type", "Times concatenated"]
        fieldNumber = 0
        writer.update_page_form_field_values(
                writer.pages[pn-2], {f"NORow{i + 1}_{pn}": caseNumber}
            )
        #Automatically assigning values to their correct form field
        for field in fieldNames:
            writer.update_page_form_field_values(
                writer.pages[pn-2], {f"{field}{i + 1}_{pn}": row [dfFieldNames[fieldNumber]]}
            )
            fieldNumber += 1
        row_ = row
        caseNumber += 1
        i += 1
    #Dropping rows that have been parsed once pdf forms are filled in each page
    karlGrouped = karlGrouped.drop(karlGrouped.head(22).index)

                                                                 
# Ouputing new filled pdf
with open("filled-out.pdf", "wb") as output_stream:
    writer.write(output_stream)

       