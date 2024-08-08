# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 18:06:53 2024

@author: waleed emad yaya
@project: script for verilog module and test_bench generation
"""

#IMPORT NEEDE LIBRARY FOR VALIDATION THE INPUT DIRECTORY AND IDENTIFIERS FROM THE USERS
import os
import re

#BOOLEAN VARIABLES FOR SELECTION THE TYPE OF THE MODULE ONLY ONE OF THEM WILL BE TRUE#
comb_struc  = False;
comb_behav  = False;
comb_RTL    = False;
sequ_synch  = False;
sequ_asynch = False;
param_exist = False;
valid_directory = False;

#INTEGER VARIABLES FOR SOME INPUT DATA ABOUT THE MODULE TO CAPTURE THE DATA FROM THE USER ABOUT DESIRED MODULE#
parameters_num  = 0;
variables_num   = 0;
inputports_num  = 0;
outputports_num = 0;
inoutports_num  = 0;
intrnalREG_num  = 0;
intrnalWIR_num  = 0;

#STRING VARIABLES FOR STORING THE VALUE INPUT FROM THE USER ABOUT SOME IDENTIFERS AND DIRECTORY#
directory   = "";
module_name = "";
clk_name    = "";
rst_name    = "";

#DICTIONARIES FOR STORING DATA IN THE RIGHT FORM AND REUSE THEM IN WRITING THE MODULE AND THE TEST BENCH#
parameters_dic  = {};
variables_dic   = {};
inputports_dic  = {};
outputports_dic = {};
inoutports_dic  = {};
intrnalREG_dic  = {};
intrnalWIR_dic  = {};

#STORING VERILOG KEYWORDS IN ARRAYS OF STRINGS FOR CHECK IF THE USER INPUT IS INVALID#
reserved_words = [
    'module', 'endmodule', 'input', 'output', 'inout', 'wire', 'reg','assign',
    'always', 'initial', 'if', 'else', 'case', 'endcase','for', 'endfor', 'while',
    'endwhile', 'repeat', 'endrepeat',
    'begin', 'end', 'task', 'endtask', 'function', 'endfunction',
    'integer', 'real', 'time', 'realtime', 'event', 'genvar',
    'parameter', 'localparam', 'specify', 'endspecify', 'posedge', 'negedge',
    'or', 'and', 'nand', 'nor', 'xor', 'xnor', 'not', 'buf', 'bufif0', 'bufif1',
    'notif0', 'notif1', 'tran', 'rtran', 'tranif0', 'tranif1', 'rtranif0', 'rtranif1',
    'pullup', 'pulldown', 'cmos', 'rcmos', 'nmos', 'pmos', 'rnmos', 'rpmos',
    'tranif0', 'tranif1', 'rtranif0', 'rtranif1', 'pullup', 'pulldown',
    'cmos', 'rcmos', 'nmos', 'pmos', 'rnmos', 'rpmos', 'cell', 'endcell',
    'config', 'endconfig', 'design', 'enddesign', 'instance', 'endinstance',
    'primitive', 'endprimitive', 'table', 'endtable', 'default', 'defparam',
    'disable', 'edge', 'else', 'end', 'endcase', 'endconfig', 'endfunction',
    'endgenerate', 'endmodule', 'endprimitive', 'endspecify', 'endtable',
    'endtask', 'event', 'for', 'force', 'forever', 'fork', 'function', 'generate',
    'genvar', 'highz0', 'highz1', 'if', 'ifnone', 'incdir', 'include', 'initial',
    'inout', 'input', 'instance', 'integer', 'join', 'large', 'liblist', 'library',
    'localparam', 'macromodule', 'medium', 'module', 'nand', 'negedge', 'nmos',
    'nor', 'noshowcancelled', 'not', 'notif0', 'notif1', 'or', 'output', 'parameter',
    'pmos', 'posedge', 'primitive', 'pull0', 'pull1', 'pulldown', 'pullup', 'pulsestyle_onevent',
    'pulsestyle_ondetect', 'rcmos', 'real', 'realtime', 'reg', 'release', 'repeat',
    'rnmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared', 'showcancelled',
    'signed', 'small', 'specparam', 'strength', 'strong0', 'strong1', 'supply0',
    'supply1', 'table', 'task', 'time', 'tran', 'tranif0', 'tranif1', 'tri',
    'tri0', 'tri1', 'triand', 'trior', 'trireg', 'unsigned', 'use', 'uwire',
    'vectored', 'wait', 'wand', 'weak0', 'weak1', 'while', 'wire', 'wor', 'xnor',
    'xor'
]
#FUNCTION FOR VALIDATION OF USER INPUT IDENTIFIER DEPENDING ON SOME CONSTRAINS ON THEM#
def validate_identifier(s):
    """
    Validates a string based on the following rules:
        1. Does not start with digits
        2. Does not contain spaces
        3. Does not contain special characters except underscore (_)

    """
    # Rule 1: Does not start with digits
    if s[0].isdigit():
        return False
    # Rule 2: Does not contain spaces
    if ' ' in s:
        return False
    # Rule 3: Does not contain special characters except underscore
    if not re.match(r'^[a-zA-Z0-9_]*$', s):
        return False
    return True

#READING THE DIRICTORY FROM THE USER AND CHECK THE VALIDATION #
print("Welcom");
while( not(valid_directory) ):
     directory = input("Enter the directry in which generated files to be saved: ");
     #valid_directory = check validity of directory pleas
     if( os.path.isdir(directory) ): #valid directory
         valid_directory = True;
     else:
         print("!!!!!!!Invalid directory pleas enter valid one!!!!!!!");

#READING THE MODULE NAME FROM THE USER AND CHECK THE VALIDATION #
while(True):
    module_name = input("Enter valid module name pleas : ");
    if (not(validate_identifier(module_name)) or (module_name in reserved_words)):
        print ("!!!!!!!!INVALID IDENTIFIER NAME PLEASE ENTER VALID ONE!!!!!!!!")
        continue;
    else:
        reserved_words.append (module_name);
        break;

#STORING THE DIRECTORIES OF MODULE AND TEST BENCH FILES IN VARIABLES FOR USING IN OPENNING AND WRITING ON THEM#
directory_module = directory + "/" + module_name +".v";
directory_TB = directory + "/" + module_name +"_TB.v";

#SELECTION OF THE TYPE OF THE MODULE FROM 5 POSSIBLE TYPE FOR DESCRIPING ANY MODULE ( FIRST COM OR SEQ) #
while(True):
    print ("1- COMBINATIONAL");
    print ("2- SEQUENTIAL   ");
    comb_seq = (input ("Choose only ( 1 ) or ( 2 ) :"));
    if (comb_seq == "1"):
        break;
    elif (comb_seq == '2'):
        break;
    else :
        continue;

#SELECTION OF THE TYPE OF THE MODULE FROM 5 POSSIBLE TYPE FOR DESCRIPING ANY MODULE (COMBINATIONAL) ( SECOND STRUC OR BEHAV OR RTL) #
if (comb_seq == "1"):
    while(True):
        print ("1- STRUCYURAL");
        print ("2- BEHAVIORAL");
        print ("3- RTL       ");
        comb_seq = int(input ("Choose only ( 1 ) or ( 2 ) or ( 3 ) :"));
        if (comb_seq == 1):
            comb_struc = True;
            break;
        elif (comb_seq == 2):
            comb_behav = True;
            break;
        elif (comb_seq == 3):
            comb_RTL = True;
            break;
        else :
            continue;
#SELECTION OF THE TYPE OF THE MODULE FROM 5 POSSIBLE TYPE FOR DESCRIPING ANY MODULE (SEQUENTIAL) ( THIRD SYNCH OR ASYNCH) #
elif (comb_seq == "2"):
    while(True):
        print ("1- SYNCHROUNES ");
        print ("2- ASYNCHROUNES");
        comb_seq = int(input ("Choose only ( 1 ) or ( 2 ) :"));
        if (comb_seq == 1):
            sequ_synch = True;
            break;
        elif (comb_seq == 2):
            sequ_asynch = True;
            break;
        else :
            continue;
#CHECK IF THE DESIRED MODULE IS PARAMETRIZED OR NOT#
while(True):
    is_parametrized = input("There is parameters?(y,Y,1) or (n,N,0): ");
    if(is_parametrized == "y" or is_parametrized == "Y" or is_parametrized == "1"):
        param_exist = True;
        break
    elif(is_parametrized == "n" or is_parametrized == "N" or is_parametrized == "0"):
        param_exist = False;
        break;
    else:
        continue;
""""
IF PARAMETERS EXIST CAPTURE THE DATA OF THE PARAMETERS FROM THE USER
AND APPLY SOME CONSTRAINA ON THE IDENTIFIER AND THE VALULE OF EACH PARAMETER
"""
if (param_exist):
    while (True):
        temp_param_num = input("Enter number of parameters (only digits) : ");
        if (temp_param_num.isdigit() and not temp_param_num.isspace()):
            parameters_num = int(temp_param_num);
            break;
        else:
            print ("!!!!!!!!INVALID INPUT PLEAS ENTER A DIGIT NUMBER!!!!!!!!")
            continue;

index = 1;
while(index <= parameters_num):
    while(True):
        while(True):
            param_name = input("Enter parameter number (%d) name (write valid one): "%index);
            if (not(validate_identifier(param_name)) or (param_name in reserved_words
        )):
                print ("!!!!!!!!INVALID IDENTIFIER NAME PLEASE ENTER VALID ONE!!!!!!!!")
                continue;
            else:
                reserved_words.append (param_name);
                break;
        if (param_name.isalnum() and not param_name.isspace()):
            break;
        else:
            continue;
    while (True):
        param_value = input("Enter vlaue of (%s) parameter (write valid one): "%param_name);
        if (param_value.isdigit() and not param_value.isspace()):
            break;
        else:
            continue;
    index = index + 1;
    new_data = {param_name: param_value};
    # Update the existing dictionary
    parameters_dic.update(new_data);

#CLOCK AND REST SIGNAL DECLARATION IF THE MODE IS SEQUENTIOAL OR RTL#
if (sequ_asynch or sequ_synch or comb_RTL):
    
    while(True):
        clk_name = input("Enter clock signal name pleas: ");
        if (not(validate_identifier(clk_name)) or (clk_name in reserved_words
    )):
            print ("!!!!!!!!INVALID IDENTIFIER NAME PLEASE ENTER VALID ONE!!!!!!!!")
            continue;
        else:
            reserved_words.append (clk_name);
            break;
    while(True):
        print ("1- Rising Edge Clock \n2- Falling Edge Clock")
        clk_type = input("Enter clock mode (write valid one): ");
        if (clk_type == "1"):
            pos_neg_edge = "posedge";
            break;
        elif (clk_type == "2"):
            pos_neg_edge = "negedge";
            break;
        else:
            continue;
   
    while(True):
        rst_name = input("Enter reset signal name pleas: ");
        if (not(validate_identifier(rst_name)) or (rst_name in reserved_words
    )):
            print ("!!!!!!!!INVALID IDENTIFIER NAME PLEASE ENTER VALID ONE!!!!!!!!")
            continue;
        else:
            reserved_words.append (rst_name);
            break;

#CAPTURE THE DATA OF INPUTS PINS AND STORING VALUES ISIDE THE DICTIONARIES#   
while (True):
    temp_port_num = input("Enter number of input ports (only digits) : ");
    if (temp_port_num.isdigit() and not temp_port_num.isspace()):
        temp_port_num = int(temp_port_num);
        break;
    else:
        continue;

index = 1;
while(index <= temp_port_num):
    while(True):
        port_name = input("Enter port number (%d) name (write valid one): "%index);
        if (not(validate_identifier(port_name)) or (port_name in reserved_words)):
            print ("!!!!!!!!INVALID IDENTIFIER NAME PLEASE ENTER VALID ONE!!!!!!!!")
            continue;
        else:
            reserved_words.append (port_name);
            break;
    
    while(True):
        in_is_param = False;
        #CHECK THE PARAMETRIZED INPUT DATA AND STOR THE SPECIFIC PARAMETER#
        if (param_exist and (parameters_num != 0)):
            is_param_input = input("Is %s is parametrized (y,Y,1) or (n,N,0)? "%port_name);
            if(is_param_input == "y" or is_param_input == "Y" or is_param_input == "1"):
                in_is_param = True;
                break
            elif(is_param_input == "n" or is_param_input == "N" or is_param_input == "0"):
                in_is_param = False;
                break;
            else:
                continue;
        else:
                break;
    #IF THE MODULE HAVE PARAMETERS AND ONE OF THE INPUTS IS PARAMETRIZED CHOOSE ON FROM THE VALID PARAMETERS STORED IN THE DICTIONARY OF 
    #PARAMETERS 
    if(in_is_param):
        while(True):
            in_port_param = str(input("Enter valid name of the parameter: "));
            if in_port_param in parameters_dic:
                port_value = in_port_param;
                break;
            else:
                continue;
    #IF THE INPUT IS NOT PARAMETRIZED OR THE MODULE DOSE NOT HAVE PARAMETERS AT ALL THE DIMENTION OF THE PORT IS CAPTURED FROM THE USER
    else:
        while (True):
            port_value = input("Enter vlaue of port dimension (%d) name (write valid one): "%index);
            if (port_value.isdigit() and not port_value.isspace()):
                break;
            else:
                continue;
    index = index + 1;
    new_data = {port_name: port_value};
    # Update the existing dictionary
    inputports_dic.update(new_data);

#CAPTURE THE DATA OF INPUTS PINS AND STORING VALUES ISIDE THE DICTIONARIES#   
while (True):
    temp_port_num = input("Enter number of output ports (only digits) : ");
    if (temp_port_num.isdigit() and not temp_port_num.isspace()):
        temp_port_num = int(temp_port_num);
        break;
    else:
        continue;

index = 1;
while(index <= temp_port_num):
    while(True):
        port_name = input("Enter port number (%d) name (write valid one): "%index);
        if (not(validate_identifier(port_name)) or (port_name in reserved_words
    )):
            print ("!!!!!!!!INVALID IDENTIFIER NAME PLEASE ENTER VALID ONE!!!!!!!!")
            continue;
        else:
            reserved_words.append (port_name);
            break;
    
    while(True):
        print ("1- wire \n2- reg")
        port_type = input("Enter port number (%d) type (write valid one): "%index);
        if (port_type == "1"):
            out_is = "wire";
            break;
        elif (port_type == "2"):
            out_is = "reg";
            break;
        else:
            continue;
    
    while(True):
        in_is_param = False;
        if (param_exist and (parameters_num != 0)):
            is_param_out = input("Is %s is parametrized (y,Y,1) or (n,N,0)? "%port_name);
            if(is_param_out == "y" or is_param_out == "Y" or is_param_out == "1"):
                in_is_param = True;
                break
            elif(is_param_out == "n" or is_param_out == "N" or is_param_out == "0"):
                in_is_param = False;
                break;
            else:
                continue;
        else: 
            break;

    if(in_is_param):
        while(True):
            out_port_param = str(input("Enter valid name of the parameter: "));
            if out_port_param in parameters_dic:
                port_value = out_port_param;
                break;
            else:
                reserved_words.append (out_port_param);
                continue;
    else:
        while (True):
            port_value = input("Enter vlaue of port dimension (%d) name (write valid one): "%index);
            if (port_value.isdigit() and not port_value.isspace()):
                break;
            else:
                continue;
    
    new_data = {port_name: [port_value,out_is]};
    # Update the existing dictionary
    outputports_dic.update(new_data);    
    index = index + 1;
###############################################################################
#internal signals
###############################################################################
#variables and wires 

#LINES TO BE WRITEN IN THE MODULE FILE DEPENDING ON THE STORED DATA CAPTURED FORM THE USER#
in_port_names = "";
for x in inputports_dic :
    in_port_names = in_port_names + x + " , ";

out_port_names = ""
for x in outputports_dic :
    out_port_names = out_port_names + x + " , ";

out_port_names = out_port_names[:-1];
out_port_names = out_port_names[:-1];
    
line1 = "module " + module_name + " (" + in_port_names  +  "\n" ;
line2 = "            " + out_port_names + ");\n" ;
line3 = "\n/********************** parameters **********************/\n";
parameters = [];
for i in parameters_dic :
    line = "parameter " + i + " = " + parameters_dic[i] + ";\n";
    parameters.append(line);
line4 = "\n/********************** input declaration **********************/\n";
inputs = [];
for i in inputports_dic :
    if (param_exist and not(inputports_dic[i].isdigit()) ):
        line = "input " + "wire " + "[" + inputports_dic[i] +"-1 : " + "0] " + i + ";\n";
    elif (int(inputports_dic[i][0]) > 1) :
        temp = (int(inputports_dic[i][0]) - 1);
        line = "input " + "wire " + "[" + str(temp) + " : 0] " + i + ";\n";
    else:
        line = "input " + "wire " +  i + ";\n";
    inputs.append(line);
line12 = "\n/********************** output declaration **********************/\n";
outputs = [];
for i in outputports_dic:
    if (param_exist and not(outputports_dic[i][0].isdigit())):
        line = "output " + "wire " + "[" + outputports_dic[i][0] +"-1 : " + "0] " + i + ";\n";
    elif (int(str(outputports_dic[i][0])) > 1) :
        temp = (int(outputports_dic[i][0]) - 1);
        line = "output " + outputports_dic[i][1] + " ["+ str(temp) + " : " + "0] " + i + ";\n";
    else:
        line = "output " + outputports_dic[i][1] + " " +  i + ";\n";
    
    outputs.append(line);
line5 = "\n/********************** internal wires **********************/\n\n";
line6 = "\n/**********************   descriptin   **********************/\n";

line7 = "\n";
line8 = "\n";
line9 = "\n";
line10 = "\n";

if (sequ_asynch or sequ_synch or comb_RTL):
    line7 = "\nalways @ (" + pos_neg_edge +" "+ clk_name +" )\n"
    line8 = "begin\n";
    line9 = "\n";
    line10 = "end\n";
    
if (sequ_asynch):
    line7 = "\nalways @ (" +pos_neg_edge + " " + clk_name + " , " + rst_name + " )\n"
    line8 = "begin\n";
    line9 = "\n";
    line10 = "end\n";

if (comb_behav):
    line7 = "\nalways @ (*)\n"
    line8 = "begin\n";
    line9 = "\n";
    line10 = "end\n";

line11 = "\nendmodule\n"

file = open(directory_module,"w")

file.write(line1);
file.write(line2);
file.write(line3);
for ln in parameters :
    file.write(ln);
file.write(line4);
for ln in inputs :
    file.write(ln);
file.write(line12);
for ln in outputs :
    file.write(ln);
file.write(line5);
file.write(line6);
file.write(line7);
file.write(line8);
file.write(line9);
file.write(line10);
file.write(line11);
file.close();


#LINES TO BE WRITEN IN THE TEST BENCH FILE DEPENDING ON THE STORED DATA CAPTURED FORM THE USER#

line1 = "module " + module_name + "_TB" + " (    "  + ");\n" ;
line2 = "\n/********************** parameters **********************/\n";
parameters = [];
for i in parameters_dic :
    line = "parameter " + i + " = " + parameters_dic[i] + ";\n";
    parameters.append(line);
line3 = "\n/********************** input reg declaration **********************/\n";
inputs = [];
for i in inputports_dic :
    if (param_exist and not(inputports_dic[i].isdigit()) ):
        line = "reg " + "[" + inputports_dic[i] +"-1 : " + "0] " + i + "_TB" + ";\n";
    elif (int(inputports_dic[i][0]) > 1) :

        temp = (int(inputports_dic[i][0]) - 1)
        line = "reg " + "[" + str(temp) + " : 0] " + i + "_TB" + ";\n";
    else:
        line = "reg " + i + "_TB" + ";\n";
    
    
    inputs.append(line);
line4 = "\n/********************** output wire declaration **********************/\n";
outputs = [];
for i in outputports_dic:
    if (param_exist  and not(outputports_dic[i][0].isdigit())):
        line = "wire " + "[" + outputports_dic[i][0] +"-1 : " + "0] " + i +"_TB" + ";\n";
    elif (int(outputports_dic[i][0]) > 1) :
        temp = int(outputports_dic[i][0]) - 1;
        line = "wire " + "[" + str(temp) + " : 0] " + i +"_TB" + ";\n";
    else:
        line = "wire " + i +"_TB" + ";\n";
    
    
    outputs.append(line);
line5 = "\n/********************** internal wires **********************/\n\n\n\n\n\n";
line6 = "\n/********************** DUT instantiation **********************/\n\n";
line7 = module_name + " DUT" + "( " ;
in_port_TB = "";
for x in inputports_dic :
    in_port_TB = in_port_TB + "." + x + "( " + x + "_TB" + ") , ";
out_port_TB = ""
for y in outputports_dic :
    out_port_TB = out_port_TB + " ." + y + "( " + y + "_TB" + ") , ";
out_port_TB = out_port_TB[:-1];
out_port_TB = out_port_TB[:-1];
line8 = " );"
line9 = "\n";
line10 = "\n";
line11 = "\n";
line12 = "\n";
line13 = "\n";
if (sequ_asynch or sequ_synch or comb_RTL):
    line9 = "\n/**********************   clock generation    **********************/\n"
    line10 = "always  #10 " + clk_name + " = ~" + clk_name +";\n" ;
    line11 = "";
    line12 = "";
    line13 = "        " + clk_name +" = " + "0 ;\n\n\n\n\n\n\n\n\n\n\n"
line14 = "\n/**********************   INTIALIZATION    **********************/\n    initial begin \n"
line15 = "    end"
line16 = "\nendmodule\n"


file = open(directory_TB,"w")

file.write(line1);
file.write(line2);
for ln in parameters :
    file.write(ln);
file.write(line3);
for ln in inputs :
    file.write(ln);
file.write(line4);
for ln in outputs :
    file.write(ln);
file.write(line5);
file.write(line6);
file.write(line7);
file.write(in_port_TB);
file.write(out_port_TB);
file.write(line8);
file.write(line9);
file.write(line10);
file.write(line11);
file.write(line12);
file.write(line14);
file.write(line13);
file.write(line15);
file.write(line16);

file.close();

        
    





