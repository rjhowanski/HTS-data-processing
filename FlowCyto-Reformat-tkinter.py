# Note: I have made modifications to the scripts on this repository to remove sensitive information 
# and reduce annotations, ensuring they can be shared without risk of confidentiality issues.


# import libraries
import os 
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import * 
from tkinter import messagebox

# message to instruct first file to select
messagebox.showinfo("File 1 of 2", "Please select the ForeCyt experiment .csv file.")

# gui to select forecyt experiment file, assumes proper template used
root = tk.Tk()
root.withdraw()
inputfile=filedialog.askopenfilename(filetypes=[('CSV File','.csv')])
inputfile=os.path.normpath(inputfile)
datafile = pd.read_csv(inputfile,sep=',',skiprows=0,header=0)

# message to instruct second file to select
messagebox.showinfo("File 2 of 2", "Please select your GDB Plate Set .txt file.")

# gui to select gdb plate set file
root = tk.Tk()
root.withdraw()
inputfile2=filedialog.askopenfilename(filetypes=[('Txt File','.txt')])
inputfile2=os.path.normpath(inputfile2)
platefile=pd.read_csv(inputfile2,sep='\t',header=0)

# create key for datafile and platefile
datafile['Reference'] = datafile['Plate'] + "_" + datafile['Well Address']
platefile['Reference'] = platefile['Plate ID'] + "_" + platefile['Well Address']

# keep clones in datafile that exist in GDB platefile
new_df = datafile[datafile['Reference'].isin(platefile['Reference'])]

# drop reference column
new_df = new_df.drop('Reference', axis=1)

# change plate column to 'Plate ID' for proper GDB formatting
new_df.rename(columns = {'Plate':'Plate ID'}, inplace = True)

# count rows in plate set file
ps_count=len(platefile.index)

# count rows in upload file
gdb_count=len(new_df.index)

# provides warning if plate set count doesn't match gdb upload file count
if ps_count != gdb_count:
    messagebox.showwarning("WARNING", "The number of rows in your upload file ("+str(gdb_count)+") doesn't match rows in your plate set file ("+str(ps_count)+").")

# get path of forecyt experiment file
head,tail=os.path.split(inputfile)
name = tail.split('.')[0]

# export gdb upload file as "GDB_Upload_" + experiment file name
# put in same location of experiment file
new_df.to_csv(head+'\\GDB_Upload_'+name+'.txt',header=True,sep='\t')

# message displaying number of data rows in upload file
messagebox.showinfo("Upload Result", "Your .txt file for GDB Upload is ready and contains "+str(gdb_count)+" rows of data")

