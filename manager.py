from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure

def manager_page():

    datatype = [
            "Rental activities",
            "Rents per station",
            "Broken Bike per station"
            ]
      

    Chart_Type = [
            "Bar Chart",
            "Line Chart",
            "Pie Chart"
            ]

    varx = StringVar(window)
    varx.set(datatype[0])
  
    varchart = StringVar(window)
    varchart.set(Chart_Type[0])

    xaxis = OptionMenu(window,varx,*datatype)
    x = Label(text="Data")
    x.grid(row=0,column=0,padx = 90)
    xaxis.grid(row=1,column=0)
    
    chartType = OptionMenu(window,varchart,*Chart_Type)
    chart = Label(text="Chart Types")
    chart.grid(row=0,column=2,padx = 90)
    chartType.grid(row=1,column=2)
    
    plot = Button(window, height = 1, width = 5,text = "Draw",command=lambda: draw(varchart.get(),varx.get()))
    plot.grid(row=2,column=1,pady = 40)

def draw(chartType,datatype):
    
    if chartType == "Line Chart" :
        if datatype =="Rental activities":
            LineChart(["St1","St2","St3"],[1,2,3])
        elif datatype =="Rents per station":
            LineChart(["St1","St2","St3"],[135,346,523])
        elif datatype =="Weekly rental report":
            LineChart(["St1","St2","St3"],[3,2,1])
        else:
            print("Some bullshit")
            
    elif chartType == "Bar Chart":
        if datatype =="Rental activities":
            BarChart(["St1","St2","St3"],[1,2,3],False)
        elif datatype =="Rents per station":
            BarChart(["St1","St2","St3"],[135,346,523],False)
        elif datatype =="Weekly rental report":
            BarChart(["St1","St2","St3"],[3,2,1],True)
        
    elif chartType  == "Pie Chart":
        if datatype =="Rental activities":
            PieChart(["St1","St2","St3"],[1,2,3])
        elif datatype =="Rents per station":
            PieChart(["St1","St2","St3"],[135,346,523])
        elif datatype =="Weekly rental report":
            PieChart(["St1","St2","St3"],[3,2,1])
    else:
        print("you picked the wrong chart fool!")

def LineChart(datasetx,datasety):
    
    fig = Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.plot(datasetx,datasety)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)

def BarChart(datasetx,datasety,stacked):
    
    fig = Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.bar(datasetx,datasety)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)

def PieChart(datasetx,datasety):
    
    fig = Figure(figsize=(5,5))
    a = fig.add_subplot(111)
    a.pie(datasety,labels=datasetx)
    canvas = FigureCanvasTkAgg(fig,master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3,columnspan=3)