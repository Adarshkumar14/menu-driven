#!/usr/bin/python3
import subprocess
def docker():
    flag=1
    while(flag):
        print("Enter your choice:")
        print("1. To start docker")
        print("2.To check docker status")
        print("3.To See Image list")
        print("4. to see container list")
        print("5. to launch  new container")
        print("6. to see running container")
        print("7. to docker login/logout")
        print("8. to check log of container")
        print("9.to execute command on container")
        print("10. to delete container / Image")
        print("0. EXIT DOCKER")
        x=input()
        x=int(x)
        if(x==1):
               
               m="sudo systemctl start docker"
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)
               
           
        if(x==2):
           
               m="sudo systemctl status docker"
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)
        if(x==3):
           
               m="sudo docker images"
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)                   
        if(x==4):
           
               m="sudo docker ps -a"
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)
        if(x==5):
               print("enter Image name")
               iname=input()
               print("enter container name") 
               cname=input()
               volume=""
               port=""
               print("Do You want to attach volume or port ??\t press 1 for YES!!")
               x=input()
               x=int(x)
               if(x==1):
                print("enter source address:destination address")
                v=input()
                volume="-v "+v
                print("enter source port:destination port")
                p=input()
                port="-p "+p
                m="sudo docker run -dit --name {} {} {} {}".format(cname,volume,port,iname)
                status,output=subprocess.getstatusoutput(m)
                if(status!=0):
                  print("error!!!")
                else:
               
                   print(output)
               else:
                m="sudo docker run -dit --name {} {}".format(cname,iname)
                status,output=subprocess.getstatusoutput(m)
                if(status!=0):
                  print("error!!!")
                else:
               
                   print(output)
        if(x==6):
           
               m="sudo docker ps"
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)      
        if(x==7):
                inn=int(input("Enter 1. to login to docerhub and 2. to logout:"))
                if(inn==1):
                   username=input("enter userid")
                   passwd=input("password")
                   m="docker login -u {} -p {}".format(username,passwd)

                   status,output=subprocess.getstatusoutput(m)
                   if(status!=0):
                       print("error!!!")
                   else:
               
                       print(output)  
                elif(inn==2):
                    m="docker logout"
                    status,output=subprocess.getstatusoutput(m)
                    if(status!=0):
                       print("error!!!")
                    else:
               
                       print(output)  

        if(x==8):
               cid=input("enter container name")
               m="sudo docker logs {}".format(cid)
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)

        if(x==9):
               cid=input("Enter container name : ")
               cmd=input("enter the command : ")

               
               m="sudo docker exec -it {} {}".format(cid,cmd)
               status,output=subprocess.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)  
        if(x==10):
                val=int(input("Enter 1. to remove container 2. to remove all the container 3. to remove Image"))
                if(val==1):
                  contid=input("enter the container name:")
                  m="sudo docker rm -f {}".format(contid)
                  status,output=subprocess.getstatusoutput(m)
                  if(status!=0):
                     print("error!!!")
                  else:
               
                     print(output)  
                elif(val==2):
                    print("\n\t\t!! Attention !!\n\t\t## Not Recommended ##")
                    x=input("If you want to delete all the containers then press 1 ")
                    if(x==1):
                        m="sudo docker rm -f $(sudo docker container ls -a -q"
                        status,output=subprocess.getstatusoutput(m)
                        if(status!=0):
                             print("error!!!")
                        else:
                             print(output)
                    else:
                        pass
                elif(val==3):
                        Iid=input("enter the Image name:")
                        m="sudo docker rmi  {}".format(Iid)
                        status,output=subprocess.getstatusoutput(m)
                        if(status!=0):
                           print("error!!!")
                        else:
               
                           print(output)  

        if(x==0):
           flag=0
           break
               
    
flag=1
while(flag):
    print("Enter your choice")
    print("1. Docker")
    print("0.EXIT") 
    x=input()
    x=int(x)
    if(x==1):
        docker()
    elif(x==0):
        flag=0
        break
print("program completed")
     
