# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 09:13:10 2020

@author: Eric Buehler
"""
import sys
import os

global code
code={}
linenum=0
end=False
line=0
variables={}
sys_flag=False
version=1.2

commands_list=["#","ss","sd",".prg","gosub","return","end","quit","print","printvar","input","goto","if","var","add","subtract","multiply","divide","exponent","increment","decrement"]
terminal_command=["rename","run","ls","cat","mkdir","cd","cwd","list","del","save","load","exit","version","rmfile","rmdir","rmallfiles","rmdirfiles","mov"]

def loop():
    try:
        a=input(">>>")
    except KeyboardInterrupt:
        x=input("\nDo you want to exit?(y/n): ").lower()
        if x=="y":
            sys.exit()
        
        return None
            
    return a

def maxline_function(code):
    keys=code.keys()
    return max(keys)

def minline_function(code):
    keys=code.keys()
    return min(keys)

def decode(line,comm,param,code,variables,stack):
    try:
        line=int(line)
        comm=str(comm)
        param=str(param)
        stack=list(stack)
        
        if comm=="end":
            end=True
            return end
        
        if comm=="quit":
            sys.exit()
        
        if comm=="print":
            param_out=param.split(',')
            
            count=len(param_out)
            
            if count>2: #text to print includes extra commas
                text=str(param_out[0:len(param_out)-1]).replace("'","").replace("[","").replace("]","").replace(", ",",")
                end_out=str(param_out[len(param_out)-1]) #newline/sameline
                
            if count==2: #text to print only contains the comma associated with newline/sameline
                text=str(param_out[0])
                end_out=str(param_out[1]) #newline/sameline
                
            if count==1: #no parameters other than text to print
                text=str(param_out[0])
                end_out="nl" #newline default
    
            
            if end_out=="nl":
                print(text)
            if end_out=="sl":
                print(text,end='')
                
            return
        if comm=="printvar":
            param_out=param.split(',')
            
            var=str(param_out[0])
            try:
                end_out=str(param_out[1]) #newline/sameline
            except IndexError:
                end_out="nl"
            
            try:
                if end_out=="nl":
                    print(str(variables[var]))
                if end_out=="sl":
                    print(str(variables[var]),end='')   
            except KeyError:
                print("InvalidKeyError: The parameter of printvar must be a valid key. Line: ",str(line))
                
            return
            
        if comm=="input":
            param_out=param.split(',')
            
            prompt=str(param_out[0:len(param_out)-1]).replace("'","").replace("[","").replace("]","").replace(", ",",") #prompt
            var=str(param_out[len(param_out)-1]) #variable to save to
            
            var_out=input(prompt)
            
            variables.update({var:var_out})
            
            return variables
        if comm=="goto" or comm==".prg":
            try:
                keys=list(sorted(code.keys()))
                maxline=maxline_function(code)
                if int(param)>maxline:
                    print("\nMaxlineError: Command jumps to line number outside maximum. Line: ",str(line))
                    end=True
                    return end
                if int(param) not in keys:
                    print("\nLineNotFoundError: Command jumps to line number that does not exist. Line: ",str(line))
                    end=True
                    return end
                if int(param)<=maxline and int(param) in keys:
                    line=int(param)
                    return line
            except ValueError:
                print("\nParameterError: No parameter. Line: ",str(line))
                end=True
                return end
            return 
        if comm=="if":
            #Parse parameter
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            var2_out=str(param_out[1]) #var2
            param3=param_out[2].lower() #Operation
            param4=int(param_out[3]) #line to go to
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
            try:
                var2=variables[str(var2_out)]
            except ValueError:
                var2=int(var2_out)
            except KeyError:
                var2=str(var2_out)
            
            if param3=="eq": #Equal
                if var1==var2:
                    line=param4
                    return line
            if param3=="ne": #Not equal
                if var1!=var2:
                    line=param4
                    return line
            if param3=="gt": #num1>num2
                try:
                    if int(var1)>int(var2):
                        line=param4
                        return line
                except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when using gt, lt, gte, or lte operands. Line: ",str(line))
                    end=True
                    return end
            if param3=="lt": #num1<num2
                try:
                    if int(var1)<int(var2):
                        line=param4
                        return line
                except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when using gt, lt, gte, or lte operands. Line: ",str(line))
                    end=True
                    return end
            if param3=="gte": #num1>=num2
                try:
                    if int(var1)>=int(var2):
                        line=param4
                        return line
                except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when using gt, lt, gte, or lte operands. Line: ",str(line))
                    end=True
                    return end
            if param3=="lte": #num1<=num2
                try:
                    if int(var1)<=int(var2):
                        line=param4
                        return line
                except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when using gt, lt, gte, or lte operands. Line: ",str(line))
                    end=True
                    return end
            
            return
                
        if comm=="var":
            y=0
            for n in range(0,len(param)):
                x=param[n]
                if x=="," and y==0:
                    param1=param[0:n].lower()
                    y=n
                    param2=param[y+1:len(param)].lower()
                    break
                
            variables.update({param1:param2})
            return variables
        
        if comm=="add":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            var2_out=str(param_out[1]) #var2
            var3=param_out[2].lower() #var to save to
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
            try:
                var2=variables[str(var2_out)]
            except ValueError:
                var2=int(var2_out)
            except KeyError:
                var2=str(var2_out)
             
            try:
                var_out=int(var1)+int(var2)
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when adding. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({var3:var_out})
            
            return variables
        
        if comm=="subtract":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            var2_out=str(param_out[1]) #var2
            var3=param_out[2].lower() #var to save to
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
            try:
                var2=variables[str(var2_out)]
            except ValueError:
                var2=int(var2_out)
            except KeyError:
                var2=str(var2_out)
             
            try:
                var_out=int(var1)-int(var2)
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when subtracting. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({var3:var_out})
            
            return variables
        
        if comm=="divide":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            var2_out=str(param_out[1]) #var2
            var3=param_out[2].lower() #var to save to
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
            try:
                var2=variables[str(var2_out)]
            except ValueError:
                var2=int(var2_out)
            except KeyError:
                var2=str(var2_out)
             
            try:
                var_out=int(var1)/int(var2)
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when dividing. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({var3:var_out})
            
            return variables
        
        if comm=="multiply":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            var2_out=str(param_out[1]) #var2
            var3=param_out[2].lower() #var to save to
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
            try:
                var2=variables[str(var2_out)]
            except ValueError:
                var2=int(var2_out)
            except KeyError:
                var2=str(var2_out)
             
            try:
                var_out=int(var1)*int(var2)
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when multiplying. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({var3:var_out})
            
            return variables
        
        if comm=="exponent":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            var2_out=str(param_out[1]) #var2
            var3=param_out[2].lower() #var to save to
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
            try:
                var2=variables[str(var2_out)]
            except ValueError:
                var2=int(var2_out)
            except KeyError:
                var2=str(var2_out)
             
            try:
                var_out=int(var1)**int(var2)
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when using exponents. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({var3:var_out})
            
            return variables
        
        if comm=="increment":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            
            output=str(var1_out)
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
             
            try:
                var_out=int(var1)+1
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when incrementing. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({output:var_out})
            
            return variables
        
        if comm=="decrement":
            param_out=param.split(',')
            
            var1_out=str(param_out[0]) #var1
            
            output=str(var1_out)
            
            #Check if var inputs are int to variable.
            try:
                var1=variables[str(var1_out)]
            except ValueError:
                var1=int(var1_out)
            except KeyError:
                var1=str(var1_out)
             
            try:
                var_out=int(var1)-1
            except ValueError:
                    print("\nValueError: Var1 and Var2 must be a number when decrementing. Line: ",str(line))
                    end=True
                    return end
            
            variables.update({output:var_out})
            
            return variables
        
        if comm=="gosub":
            try:
                keys=list(sorted(code.keys()))
                maxline=maxline_function(code)
                if int(param)>maxline:
                    print("\nMaxlineError: Command jumps to line number outside maximum. Line: ",str(line))
                    end=True
                    return end
                if int(param) not in keys:
                    print("\nLineNotFoundError: Command jumps to line number that does not exist. Line: ",str(line))
                    end=True
                    return end
                if int(param)<=maxline and int(param) in keys:
                    line_to=int(param)
                    stack.append(line)
                    return list([line_to,stack])
            except ValueError:
                print("\nValueError: Enter a number. Line: ",str(line))
                end=True
                return end
            return 
        
        if comm=="return":
            try:
                if stack==[]:
                    return
                line=float(int(stack.pop())+0.5)
                return line
            except ValueError:
                print("\nValueError: Enter a number. Line: ",str(line))
                end=True
                return end
            return         
        
        #Command not found.
        print("\nError: Command not found. Line: ",str(line))
        end=True
        return end
    except KeyboardInterrupt:
        print("\nBreak in line ",str(line))
        end=True
        return end

print("\nWelcome to FPL v"+str(version)+"!")
print("Created October 2020, Eric L Buehler.")

while True:
    line_of_code=loop()
    
    if line_of_code==None:
        continue
    
    y=0
    
    sys_flag=True

    if line_of_code.lower()=="run":
        line=int(minline_function(code))
        stack=[]
        
        sub=False
        
        try:
            try:
                maxline=int(maxline_function(code))
            except ValueError:
                print("\nProgramEmptyError: No program. Load or write a program before running")
                continue
            
            
            
            while True:
                code=code
                variables=variables
                if line>int(maxline_function(code)):
                    break                
                if line in code: 
                    comm=code.get(line)[0]
                    param=code.get(line)[1]
                    
                    if comm=="#" or comm.count("#")>=1: #Comment
                        line+=0.5
                        continue
                    
                    if comm=="ss":
                        sub=True
                    
                    if comm=="sd":
                        sub=False
                        line+=0.5
                        continue
                    
                    if sub:
                        line+=0.5
                        continue

                    returned=decode(line,comm,param,code,variables,stack)
                    
                    if type(returned)==dict:
                        returned=variables
                        line+=0.5
                        continue
                    if type(returned)==float or type(returned)==int:
                        line=float(returned)
                        continue
                    if type(returned)==bool:   
                        end=returned
                        if end:
                            end=False
                            break
                    if type(returned)==list:
                        stack=list(returned[1])
                        line=float(returned[0])
                        continue
                    
                    #print(stack)
                
                line+=0.5
                
            continue
                
                
        except KeyboardInterrupt:
            print("\nBreak in line ",str(line))
            end=True
            continue
        
    if line_of_code.lower()=="version":
        print("\nFPL v"+str(version)+", created October 2020 by Eric L Buehler.")
        continue
    
    if "mov" in line_of_code.lower():
        try:
            param=line_of_code.lower().split(" ")[1]
            param=param.split(",")
            line1=param[0]
            line2=param[1]
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        line=[]
        
        try:
            line.append(code.get(int(line1))[0]) 
            line.append(code.get(int(line1))[1])
        except TypeError:
            print("\nLineNumberError: The first parameter is not valid")
            continue
        
        code.update({int(line2):line})
        code.pop(int(line1))
        
        continue

        
    if line_of_code.lower()=="ls":  
        basepath=os.getcwd()
        
        files=[]
        dirs=[]
        
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                files.append(entry)
                
        for entry in os.listdir(basepath):
            if os.path.isdir(os.path.join(basepath, entry)):
                dirs.append(entry)
                
        if len(files)>0:
            print("\nFiles: ")
            for n in range(0,len(files)):
                print(files[n])
                
        if len(files)==0:
            print("\nNo files.")
                
        if len(dirs)>0:
            print("\nDirectories: ")
            for n in range(0,len(dirs)):
                print(dirs[n])
                
        if len(dirs)==0:
            print("\nNo directories.")
        
        continue
    
    if "rmallfiles"==line_of_code.lower():
        basepath=os.getcwd()
        
        files=[]
        
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                files.append(entry)
                
        if len(files)==0:
            print("\nNo files to delete. This directory is empty.")
            continue
                
        for n in range(0,len(files)):
            os.remove(files[n])
            
        continue
    
    if "rename" in line_of_code.lower():
        try:
            filename=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                filename+=line_of_code.split(" ")[n+1]
                filename+=" "
                
            filename=filename[:-1]  
            filename=filename.split(",")
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        basepath=os.getcwd()
        
        try:
            os.rename(os.path.join(basepath, filename[0]),os.path.join(basepath, filename[1]))
            continue
        except FileNotFoundError:
            print("\nFileNotFoundError: Please enter a valid file name")
            continue 
   
    if "rmfile" in line_of_code.lower():
        try:
            filename=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                filename+=line_of_code.split(" ")[n+1]
                filename+=" "
                
            filename=filename[:-1] 
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        basepath=os.getcwd()
        
        if os.path.exists(filename) and os.path.isfile(os.path.join(basepath, filename)):
            os.remove(filename)
            continue
        else:
            print("\nFileNotFoundError: Please enter a valid file name")
            continue   
        
    if "rmdir" in line_of_code.lower():
        try:
            filename=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                filename+=line_of_code.split(" ")[n+1]
                filename+=" "
                
            filename=filename[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        try:
            directory=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                directory+=line_of_code.split(" ")[n+1]
                directory+=" "
                
            directory=directory[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        basepath=os.getcwd()
        
        if os.path.exists(filename) and os.path.isdir(os.path.join(basepath, filename)):
            try:    
                os.rmdir(filename)
            except OSError:
                print("\nDirectoryError: The directory "+filename+" is not empty")
            continue
        else:
            print("\nFileNotFoundError: Please enter a valid file name")
            continue 
        
    if "rmdirfiles" in line_of_code.lower():
        try:
            filename=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                filename+=line_of_code.split(" ")[n+1]
                filename+=" "
                
            filename=filename[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        try:
            directory=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                directory+=line_of_code.split(" ")[n+1]
                directory+=" "
                
            directory=directory[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        basepath=os.getcwd()
        
        #### DELETE ALL THE FILES IN THIS DIRECTORY ####
        
        files=[]
        
        for entry in os.listdir(basepath):
            if os.path.isfile(os.path.join(basepath, entry)):
                files.append(entry)
                
        if len(files)==0:
            print("\nNo files to delete. This directory is empty.")
            continue
        
        for n in range(0,len(files)):
            os.remove(files[n])
            
        ################################################
            
        
        if os.path.exists(filename) and os.path.isdir(os.path.join(basepath, filename)):
            try:    
                os.rmdir(filename)
            except OSError:
                print("\nDirectoryError: The directory "+filename+" is not empty")
            continue
        else:
            print("\nFileNotFoundError: Please enter a valid file name")
            continue 
    
    if "cat" in line_of_code.lower():
        try:
            filename=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                filename+=line_of_code.split(" ")[n+1]
                filename+=" "
                
            filename=filename[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        if filename=="":
            print("\nParameterError: No parameter")
            continue
        
        try:
            file=open(filename,"r")
            file_out=file.read()
            file.close()   
        except FileNotFoundError:
            print("\nFileNotFoundError: Please enter a valid file name")
            continue              
        
        print(file_out)   
        continue
            
    
    if "mkdir" in line_of_code.lower():
        try:
            directory=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                directory+=line_of_code.split(" ")[n+1]
                directory+=" "
                
            directory=directory[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        if directory!="":
            os.mkdir(directory)
            continue
        if directory=="":
            print("\nParameterError: No parameter")
            continue
    
    if "cd" in line_of_code.lower():
        try:
            directory=""
            for n in range(0,len(line_of_code.lower().split(" "))-1):
                directory+=line_of_code.split(" ")[n+1]
                directory+=" "
                
            directory=directory[:-1]          
        except IndexError:
            print("\nParameterError: No parameter")
            continue
        
        if directory!="":
            try:
                os.chdir(directory)
            except FileNotFoundError:
                print("\nFileNotFoundError: Please enter a valid file name")
                continue    
                
        if directory=="":
            print("\nParameterError: No parameter")
            continue
            
        continue
    
    if line_of_code.lower()=="cwd":  
        basepath=os.getcwd()
        print(basepath)
        continue

    if line_of_code.lower()=="list":
        if code=={}:
            print("No program.")
            continue
        keys=list(sorted(code.keys()))
        for n in range(0,len(keys)):
            print(str(keys[n])+" "+str(code[keys[n]][0])+" "+str(code[keys[n]][1]))
            
        continue
    #After list command. This is important
    if "list" in line_of_code.lower():
        keys=list(sorted(code.keys()))
        list_out=line_of_code.lower().split(" ")
        try:
            param=int(list_out[1])
        except ValueError:
            print("\nValueError: list parameter must be an integer")
            continue
        try:
            index=keys.index(param)
        except ValueError:
            print("\nValueError: list parameter must be a valid line number")
            continue
        
        print(str(keys[index])+" "+str(code[keys[index]][0])+" "+str(code[keys[index]][1]))
            
        continue
    
    if line_of_code.lower()=="del":
        code={}            
        continue
    
    #After del command. This is important
    if "del" in line_of_code.lower():
        keys=list(code.keys())
        max_key=maxline_function(code)
        del_out=line_of_code.lower().split(" ")
        try:
            if int(del_out[1])>max_key:
                print("\nValueError: del parameter must be a valid line number")
                continue
            if int(del_out[1])<=max_key:
                code.pop(int(del_out[1]),None)
        except ValueError:
            print("\nValueError: del parameter must be an integer")
            continue
    
        continue
    
    if "save" in line_of_code.lower():
        save_out=line_of_code.split(" ")
        code_in=""
        keys=list(code.keys())
        for n in range(0,len(keys)):
            code_in+=str(keys[n])
            code_in+="~"
            data=code.get(keys[n])
            code_in+=str(data[0])
            code_in+="~"
            code_in+=str(data[1])
            code_in+="|"
        code_in=code_in[:-1]
        
        try:        
            param=""
            for n in range(0,len(save_out)-1):
                param+=save_out[n+1]
                param+=" "
                
            param=param[:-1]
        except IndexError:
            print("\nParameterError: No parameter")
            continue
            
        if param=="":
            print("\nParameterError: No parameter")
            continue
            
        
        file=open(param+".falcon","w")
        file.write(code_in)
        file.close()
        
        print("File '"+str(param)+"' saved.")
        
        continue

    if "load" in line_of_code.lower():
        try:
            save_out=line_of_code.split(" ")
            try:
                param=""
                for n in range(0,len(save_out)-1):
                    param+=save_out[n+1]
                    param+=" "
                    
                param=param[:-1]
            except IndexError:
                print("\nParameterError: No parameter")
                continue
            
            if param=="":
                print("\nParameterError: No parameter")
                continue
            
            file=open(param+".falcon","r")
            file_out=file.read()
            file.close()
            
            file_final=file_out.split("|")
            code={}
            for n in range(0,len(file_final)):
                individual=file_final[n].split("~")
                try:
                    code.update({int(individual[0]):[str(individual[1]),str(individual[2])]})
                except ValueError:
                    print("\nFileTypeError: This file is not a .falcon file, or it is not a file from FPL v"+str(version))
                    break
                    
        except FileNotFoundError:
            print("\nFileNotFoundError: Please enter a valid file name")
            continue
        continue
    
    if "exit"==line_of_code.lower() or "quit"==line_of_code.lower() or "end"==line_of_code.lower():
        sys.exit()  
                
    sys_flag=False #The command entered is not a sys command
                   
    for n in range(0,len(line_of_code)):
        x=line_of_code[n]
                
        if line_of_code.count(" ")==1 and y!=0:
            command=line_of_code[y+1:len(line_of_code)].lower() 
            parameter=''
            break
        
        if x==" " and y==0:
            try:
                linenum=int(line_of_code[0:n])
            except ValueError:
                print("\nLineNumberError: Make sure you include line numbers")
                break
        
            y=n
            continue
    
        if x==" ":
            command=line_of_code[y+1:n].lower() 
            parameter=line_of_code[n+1:len(line_of_code)]
            break
        
    try:
        commandx=command 
    except NameError:
        if sys_flag==False:
            print("\nMake sure you enter an allowed FPL terminal command.")      
            continue
        
   
    if command not in commands_list and command.count('#')==0:
        print("\nMake sure you enter an allowed FPL command.")      
        continue
            
    code.update({linenum:[command,parameter]})     