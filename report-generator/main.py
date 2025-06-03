from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
import matplotlib.pyplot as plt
import pandas as pd
import os

def df_to_table(df):
    table_data = [df.columns.values.tolist()] + df.values.tolist()
    index = [""] + list(df.index)
    i = 0
    while i < len(table_data):
        table_data[i].insert(0, index[i])
        i += 1
    table = Table(table_data)
    return table

def dynamic_pdf(output_path, items):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    content = cover_page("Project 2 Report", "Alex Murad", "logo.png")
    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]
    text_style = styles["Normal"]
    table_title_style = ParagraphStyle("TableTitle", parent=styles["Heading4"], alignment=TA_CENTER)
    table_style = TableStyle([('BACKGROUND', (1, 0), (-1, 0), colors.grey),
            ('BACKGROUND', (0, 1), (0, -1), colors.grey),
            ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ('BACKGROUND', (1, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (1, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 1), (0, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (1, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    for item in items:
        if type(item) == tuple:
            header, text = item
            content.append(Paragraph(header, header_style))
            content.append(Paragraph(text, text_style))
            content.append(Spacer(1, 10))
        elif type(item) == str:
            content.append(Image(f"Figures/{item}", width=450, height=300))
        else:
            content.append(Paragraph(item.attrs["title"], table_title_style))
            table = df_to_table(item)
            table.setStyle(table_style)
            content.append(table)
            content.append(Spacer(1, 10))
    doc.build(content)
    print(f"PDF created successfully at {output_path}")

def cover_page(title, subtitle, logo):
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Heading3"], alignment=TA_CENTER)
    content = []
    content.append(Paragraph(title, title_style))
    content.append(Image(logo, width=400, height=400))
    content.append(Paragraph(subtitle, subtitle_style))
    content.append(PageBreak())
    return content

def create_plots(csv):
    df = pd.read_csv(csv)
    plt.figure(figsize=(6, 4))
    plt.hist(df["Operating Temperature (K)"], edgecolor="k")
    plt.xlabel("K")
    plt.ylabel("Frequency")
    plt.title("Figure 1: Operating Temperature")
    plt.savefig("Figures/plot1.png")
    plt.close()
    plt.figure(figsize=(6, 4))
    plt.hist(df["Annual Revenue (USD/yr)"], edgecolor="k")
    plt.xlabel("USD/yr")
    plt.ylabel("Frequency")
    plt.title("Figure 2: Annual Revenue")
    plt.savefig("Figures/plot2.png")
    plt.close()
    plt.figure(figsize=(6, 4))
    plt.scatter(df["Throughput (kg/hr)"], df["Annual Revenue (USD/yr)"])
    plt.xlabel("Throughput (kg/hr)")
    plt.ylabel("Annual Revenue (USD/yr)")
    plt.title("Figure 3: Throughput vs Annual Revenue")
    plt.savefig("Figures/plot3.png")
    plt.close()
    plt.figure(figsize=(6, 4))
    plt.scatter(df["Residence Time (sec)"], df["Equipment Cost (USD)"])
    plt.xlabel("Residence Time (sec)")
    plt.ylabel("Equipment Cost (USD)")
    plt.title("Figure 4: Residence Time vs Equipment Cost")
    plt.savefig("Figures/plot4.png")
    plt.close()
    data = df.groupby("Construction Material")["Operating Temperature (K)"].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(data.index, data, edgecolor="k")
    plt.xlabel("Construction Material")
    plt.ylabel("Operating Temperature (K)")
    plt.title("Figure 5: Average Operating Temperature by Construction Material")
    plt.savefig("Figures/plot5.png")
    plt.close()
    return "plot1.png", "plot2.png", "plot3.png", "plot4.png", "plot5.png"

def create_text(csv):
    df = pd.read_csv(csv)
    series = df["Reactor Type"].value_counts()
    x0 = series["CSTR"]
    x1 = series["PBR"]
    x2 = series["Batch"]
    x3 = series["PFR"]
    string1 = f"CSTR ({x0}), PBR ({x1}), Batch ({x2}), and PFR ({x3})"
    series = df["Target Chemical"].value_counts()
    x0 = series["Acetic Acid"]
    x1 = series["Benzene"]
    x2 = series["Nitric Acid"]
    x3 = series["Acetone"]
    x4 = series["IPA"]
    x5 = series["Propylene"]
    string2 = f"Acetic Acid ({x0}), Benzene ({x1}), Nitric Acid ({x2}), Acetone ({x3}), IPA ({x4}), Propylene ({x5})"
    series = df["Construction Material"].value_counts()
    x0 = series["Stainless Steel"]
    x1 = series["Titanium"]
    x2 = series["Carbon Steel"]
    string3 = f"Stainless Steel ({x0}), Titanium ({x1}), and Carbon Steel ({x2})"
    return (("Introduction", "This report is intended to analyze chemical plant reaction data to provide companies with information that they can use to make informed decisions about chemical processes. The example data set was obtained from a program that was generated by the NaviGator AI provided by the University of Florida, and has been tested to ensure that it accurately represents all of the expected trends."),
        ("Qualitative Summary", f"The data set contained three different qualitative variables, which were reactor type, target chemical, and material of construction. There were four different reactor types, each of which had a similar number of occurrences throughout the data set. These were {string1}. The number shown in parentheses is the number of occurrences of the given type that were present in the data set. Additionally there were six different target chemicals in the data set with a similar number of occurrences: {string2}. This shows that the data set contained a wide array of reactor types and target chemicals, and thus provides sufficient sample sizes to make informed decisions with regards to either one. Lastly, there were three different materials of construction, which were {string3}. This shows that there are fewer Carbon Steel reactors than Stainless Steel or Titanium. This is due to the high temperature requirements often seen in the data set, which require a stronger material of construction to withstand those temperatures."),
        ("Member Contributions", "Every component of this project was completed by me, Alex Murad, as I chose to work independently."),
        ("Quantitatve Analysis", "For this data set, there were seven different quantitative variables. These variables, along with their means, medians, and standard deviations can be found in Table 1 above. Some of these had observable trends with respect to other variables, while others were independent. Operating temperature, operating pressure, and throughput were all independent of other variables and had an even array of results, as can be seen for operating temperature in Figure 1. Annual revenue, residence time, utility cost, and equipment cost were dependent on other variables, and thus often showed weighted results, as can be seen for annual revenue in Figure 2. Figure 3 demonstrated the trend between annual revenue and throughput, showing that as throughput increases, so does the annual revenue. Figure 4 shows a very similar trend between residence time and equipment cost where, as residence time increases the equipment cost increases as well. Lastly, Figure 5 shows a trend between the qualitative variable of construction material and the quantitative variable of operating temperature. Since the construction material is dependent on the operating temperature, Titanium has the highest average operating temperature and Carbon Steel has the lowest average operating temperature. Table 2 summarizes this trend. Additionally, Table 3 demonstrates how Titanium was the most expensive material of construction, and carbon steel was the cheapest material of construction, based on their average equipment cost."))

def create_dfs(csv):
    source_df = pd.read_csv(csv)
    df = source_df.filter(["Operating Pressure (kPa)", "Operating Temperature (K)", "Throughput (kg/hr)", "Annual Revenue (USD/yr)", "Equipment Cost (USD)", "Residence Time (sec)", "Utility Cost (USD/hr)"])
    data = {}
    for column in df:
        data[column] = [df[column].mean(), df[column].median(), df[column].std()]
    quantitative_df = pd.DataFrame(data, index=["Mean", "Median", "Standard Deviation"]).T.map(lambda x: f"{x:.4g}")
    quantitative_df.attrs["title"] = "Table 1: Quantitatve Data"
    temperature_df = source_df.filter(["Construction Material", "Operating Temperature (K)"]).groupby("Construction Material").mean().map(lambda x: f"{x:.4g}")
    temperature_df.attrs["title"] = "Table 2: Average Operating Temperature by Construction Material"
    cost_df = source_df.filter(["Construction Material", "Equipment Cost (USD)"]).groupby("Construction Material").mean().map(lambda x: f"{x:.4g}")
    cost_df.attrs["title"] = "Table 3: Average Equipment Cost by Construction Material"
    return (quantitative_df, temperature_df, cost_df)

def generate_list(csv):
    text1, text2, text3, text4 = create_text(csv)
    df1, df2, df3 = create_dfs(csv)
    plot1, plot2, plot3, plot4, plot5 = create_plots(csv)
    items = []
    items.append(text1)
    items.append(df1)
    items.append(text4)
    items.append(plot1)
    items.append(plot2)
    items.append(plot3)
    items.append(plot4)
    items.append(plot5)
    items.append(df2)
    items.append(df3)
    items.append(text2)
    items.append(text3)
    return items

def report_tables(csv):
    items = generate_list(csv)
    new_items = []
    for item in items:
        if not (type(item) == tuple or type(item) == str):
            new_items.append(item)
    dynamic_pdf("Project2Report.pdf", new_items)

def report_plots(csv):
    items = generate_list(csv)
    new_items = []
    for item in items:
        if type(item) == str:
            new_items.append(item)
    dynamic_pdf("Project2Report.pdf", new_items)

def qualitative_summary(csv):
    text1, text2, text3, text4 = create_text(csv)
    items = []
    items.append(text2)
    items.append(text3)
    dynamic_pdf("Project2Report.pdf", items)

def quantitative_summary(csv):
    text1, text2, text3, text4 = create_text(csv)
    df1, df2, df3 = create_dfs(csv)
    plot1, plot2, plot3, plot4, plot5 = create_plots(csv)
    items = []
    items.append(text1)
    items.append(df1)
    items.append(text4)
    items.append(plot1)
    items.append(plot2)
    items.append(plot3)
    items.append(plot4)
    items.append(plot5)
    items.append(df2)
    items.append(df3)
    items.append(text3)
    dynamic_pdf("Project2Report.pdf", items)

def full_report(csv):
    items = generate_list(csv)
    dynamic_pdf("Project2Report.pdf", items)

def dimensions(csv):
    df = pd.read_csv(csv)
    row_count = len(df)
    col_count = len(df.columns)
    print(f"CSV File: {csv}, Rows: {row_count}, Columns: {col_count}")

def find_in_data(csv):
    df = pd.read_csv(csv)
    loop = True
    while loop:
        for key in df.columns:
            print(key)
        print("Please select a column:")
        user_input = input()
        if user_input in df.columns:
            column = user_input
            loop = False
        else:
            print("Invald input.")
    loop = True
    while loop:
        print("Please select a row (1-500):")
        user_input = input()
        try:
            user_input = int(user_input)
        except:
            print("Invald input.")
            continue
        if 1 <= user_input and user_input <= 500:
            row = user_input - 1
            loop = False
        else:
            print("Please enter a number between 1 and 500.")
    print(df[column][row])

def add_rows(csv, other_csv):
    df1 = pd.read_csv(csv)
    df2 = pd.read_csv(other_csv)
    df3 = pd.concat([df1, df2])
    print("Please enter the destination file name:")
    file_name = input()
    df3.to_csv(file_name, index=False)

if __name__ == "__main__":
    loop = True
    while loop:
        inner_loop = True
        while inner_loop:
            print("Please enter a file name:")
            user_input = input()
            if os.path.exists(user_input):
                inner_loop = False
                file_name = user_input
            else:
                print(f"Cannot find file \"{user_input}\".")
        inner_loop = True
        while inner_loop:
            print("[1] Generate Report Tables")
            print("[2] Generate Report Plots")
            print("[3] Generate Quantitative Summary")
            print("[4] Generate Qualitative Summary")
            print("[5] Generate Full Report")
            print("[6] Obtain Data Dimensions")
            print("[7] Find Data Point")
            print("[8] Add Rows")
            print("Please select an option:")
            user_input = input()
            if user_input == "1":
                report_tables(file_name)
            elif user_input == "2":
                report_plots(file_name)
            elif user_input == "3":
                quantitative_summary(file_name)
            elif user_input == "4":
                qualitative_summary(file_name)
            elif user_input == "5":
                full_report(file_name)
            elif user_input == "6":
                dimensions(file_name)
            elif user_input == "7":
                find_in_data(file_name)
            elif user_input == "8":
                inner_loop = True
                while inner_loop:
                    print("Please enter the second file name:")
                    user_input = input()
                    if os.path.exists(user_input):
                        inner_loop = False
                        other_file_name = user_input
                    else:
                        print(f"Cannot find file \"{user_input}\".")
                add_rows(file_name, other_file_name)
            else:
                print("Invalid input.")
                continue
            inner_loop = False
        inner_loop = True
        while inner_loop:
            print("Would you like to continue? (Y/N)")
            user_input = input()
            if user_input.upper() == "N":
                loop = False
                inner_loop = False
            elif user_input.upper() == "Y":
                inner_loop = False
                os.system("clear")
            else:
                print("Invalid input.")
