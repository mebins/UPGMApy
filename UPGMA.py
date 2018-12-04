from tkinter import filedialog
from tkinter import *
import numpy as np
import re
root = Tk()
root.title("UPGMA")
matrix_filepath = ""
T = Text(root, height=30, width=180)
def select():
	root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
	global matrix_filepath
	matrix_filepath = root.filename
	generate()

def generate():
	(name, label, matrix) = read_matrix()

	for i in range(len(name)):
		res = ""
		res += name[i]
		formatted_m = format_matrix(matrix[i])
		res += "\n"
		res += UPGMA(formatted_m, label[i])
		res += "\n\n\n\n"
		T.insert(END, res)


#generates table
def read_matrix():
	with open(matrix_filepath, "r") as f:
		lines = f.readlines()
		matrix_name = ""
		name_pattern = re.compile('\[.*\]')
		col_number = re.compile('\d')
		data_pattern = re.compile('\*\S*')
		entry_pattern = re.compile('-?\d\.\d\d\d\d')
		all_tables = []
		all_labels = []
		all_names = []
		labels = []
		table_ref = []
		current_index = 0
		col_i = 0
		row_i = 0
		first_loop = True
		for line in lines:
			name = re.search(name_pattern, line)
			col = re.search(col_number, line)
			data = re.match(data_pattern,line)
			entry_val = re.findall(entry_pattern, line) #gets the whole row
			if name:
				matrix_name = name.group(0)
				rows = int(col.group(0))
				table_ref = [[0 for y in range(rows)] for x in range(rows)]
				all_names.append(matrix_name)
				all_tables.append(table_ref)
				all_labels.append(labels)
				del labels[:]
			if data:
				labels.append(data.group(0))
			if entry_val:
				for vals in entry_val:
					table_ref[col_i][row_i] = float(vals)
					col_i+= 1
				row_i+= 1;
				if row_i >= rows:
					row_i = 0;
				if col_i >= rows:
					col_i = 0;
		return (all_names, all_labels, all_tables)

def format_matrix(table):
	proper_matrix = np.tril(table)
	res = [[]for x in range(len(proper_matrix))]
	for x in range(len(proper_matrix)):
		res[x].extend(proper_matrix[x][0:x].tolist())
	return res

#returns index with the smallest min val.
def min_val_cluster(table):
	min_cell = float("inf");
	x, y = -1,-1

	for i in range(len(table)):
		for j in range(len(table[i])):
			if table[i][j] < min_cell:
				min_cell = table[i][j]
				x, y = i, j
	return x,y


def join_labels(labels, a, b):
	if b < a:
		a, b = b, a
		labels[a] = "(" + labels[a] + "," + labels[b] + ")"
		del labels[b]

def join_table(table, a, b):
	if b < a:
		a, b = b, a
	row = []
	for i in range(0, a):
		row.append((table[a][i] + table[b][i])/2)
	table[a] = row
	for i in range(a+1, b):
		table[i][a] = (table[i][a] + table[b][i])/2
	for i in range(b+1, len(table)):
		table[i][a] = (table[i][a] + table[i][b]/2)
		del table[i][b]
		#np.delete(table[i],b)
	del table[b]
	#np.delete(table,b)

def UPGMA(table, labels):
	while len(labels) > 1:
		x, y = min_val_cluster(table)

		join_table(table, x, y)

		join_labels(labels, x, y)

	return labels[0]

'''
# alpha_labels:
#   Makes labels from a starting letter to an ending letter
def alpha_labels(start, end):
    labels = []
    for i in range(ord(start), ord(end)+1):
        labels.append(chr(i))
    return labels

# Test table data and corresponding labels
M_labels = alpha_labels("A", "G")   #A through G
M = [
    [],                         #A
    [19],                       #B
    [27, 31],                   #C
    [8, 18, 26],                #D
    [33, 36, 41, 31],           #E
    [18, 1, 32, 17, 35],        #F
    [13, 13, 29, 14, 28, 12]    #G
    ]

KIMURA_labels = ["BK001410.1","AY350716.1","AY350722.1","AY350721.1",
"AY350720.1","AY350719.1","AY350717.1","AY350718.1"]
KIMURA_M = [
			[],
			[0.0858],
			[0.0117, 0.0713],
			[0.0117, 0.0713, 0.0000],
			[0.0117, 0.0713, 0.0000, 0.0000],
			[0.0117, 0.0713, 0.0000, 0.0000, 0.0000],
			[0.0235, 0.0591, 0.0114, 0.0114, 0.0114, 0.0114],
			[0.0235, 0.0591, 0.0114, 0.0114, 0.0114, 0.0114, 0.0000]]
print(UPGMA(M, M_labels))
print(UPGMA(KIMURA_M, KIMURA_labels))
'''
T.pack()
B = Button(root, width = 30, height = 30, text="select file", command=select)
B.pack()
mainloop()
