#!/usr/bin/python3
import subprocess as sp 
import os
def aws():


    def  iamuser(name):
        a = sp.getstatusoutput('aws iam create-user --user-name {}'.format(name))
        if a[0] != 0:
            print("Can't Create the User : {}".format(a[1]))
            return
        print("Iam user {} created Successfully".format(name))


    def s3bucket(name):
        a = sp.getstatusoutput("aws s3 mb s3://{}".format(name))
        if a[0] != 0:
            print("Can't Create the Bucket : {}".format(a[1]))
            return
        print("Bucket {} created Successfully".format(name))


    def s3list():
        a = sp.getstatusoutput("aws s3 ls")
        if a[0] != 0:
            print("Can't List Buckets : {}".format(a[1]))
            return
        print("Available Buckets :-  \n{}".format(a[1]))


    def s3object(path, bucket, public=True):
        if public:
            a = sp.getstatusoutput("aws s3 cp --acl public-read {} s3://{}".format(path, bucket))
        else :
            a = sp.getstatusoutput("aws s3 cp {} s3://{}".format(path, bucket))

        if a[0] != 0:
            print("Can't Upload The Object : {}".format(a[1]))
            return
        print("Object {} Uploaded Successfully To The Bucket {}".format(path, bucket))


    def cloudfront(origin):
        a = sp.getstatusoutput("aws cloudfront create-distribution --origin-domain-name {}.s3.apsouth1.amazonaws.com".format(origin))
        if a[0] != 0:
            print("\nCan't Create The CDN : {}".format(a[1]))
            return
        print("\nCDN Created Successfully With Origin {}".format(origin))


    def  ec2launch(ami, keypair, sg, count=1, instance="t2.micro", sid=""):
        if sid == "":
            a = sp.getstatusoutput("aws ec2 run-instances --image {} --instance-type {} --key-name {} --security-group-ids {} --count {}".format(ami, instance, keypair, sg, count))
    
        else :
            a = sp.getstatusoutput("aws ec2 run-instances --image {} --instance-type {} --key-name {} --security-group-ids {} --count {} --subnet-id {}".format(ami, instance, keypair, sg, count, sid))

        if a[0] != 0:
            print("Can't Launch the instance: {}".format(a[1]))
            return

        print("Instance Launched Succesfully!!")


    def viewinstances():
        a = sp.getstatusoutput('aws ec2 describe-instances')
        print("Instance Status : {}".format(a[1]))


    def stopec2(id):
        a = sp.getstatusoutput("aws ec2 stop-instances --instance-ids {}".format(id))
        if a[0] != 0:
            print("Can't Stop the instance: {}".format(a[1]))
            return
        print("Instance Stopped Succesfully!!")

    def configure():
        try:
            os.system("aws configure")

        except KeyboardInterrupt  :
            print("User Interrupt Detected Aborting... ")
        return


    def switch():
        cur = sp.getoutput('aws configure get default.region')
        new = input('\nEnter the code for New Region (Current : {}) : '.format(cur))
        if new == '':
            print('\nNo Input Provided Defaulting to {} ..'.format(cur))
            return
        b = sp.getstatusoutput('aws configure set default.region {}'.format(new))
        a = sp.getstatusoutput('aws ec2 describe-instances')
        if a[0] != 0 or b[0] != 0:
            print('\nRegion {} Does Not Exist..'.format(new))
            sp.run('aws configure set default.region {}'.format(cur))
            return
        print('\nRegion Changed to {} Successfully ! '.format(new))



    def ebslaunch(az="ap-south-1a", size=1):
        a = sp.getstatusoutput("aws ec2 create-volume --availability-zone {} --size {}".format(az, size))
        if a[0] != 0:
            print("Can't Launch the Volume: {}".format(a[1]))
            return
        print("Ebs Volume Launched Succesfully!!")


    def attach(vol_id, ins_id):
        a = sp.getstatusoutput("aws ec2 attach-volume --instance-id {} --volume-id {} --device /dev/sdb".format(ins_id, vol_id))
        if a[0] != 0:
            print("Can't Attach the Volume: {}".format(a[1]))
            return
        print("Ebs Volume Attached Succesfully!!")


    def keypair(name):
        a = sp.getstatusoutput("aws ec2 create-key-pair --key-name {}".format(name))
        if a[0] != 0:
            print("Can't Create the Keyfile: {}".format(a[1]))
            return
        print("Key pair created successfully,  {}".format(a[1]))


    def security(name, desc):
        a = sp.getstatusoutput('aws ec2 create-security-group --group-name {} --description "{}"'.format(name, desc))
        if a[0] != 0:
            print("\nCan't Create Security Group : {}".format(a[1]))
            return
        print('\nSecurity Group {} created Successfully!'.format(name))


    def prereq():
        a = sp.getstatusoutput('aws help')
        if a[0] != 0:
            print('\nOops Looks like Aws Cli Command is Not Available...')
            exit()

    def snap(vol, desc):
        a = sp.getstatusoutput('aws ec2 create-snapshot --volume-id {} --description "{}"'.format(vol, desc))
        if a[0] != 0:
            print("\nCan't Create Snap : {} ".format(a[1]))
            return
        print('\nSnapshot Created Successfully!')
    


    prereq()



    ami = ('ami-0e306788ff2473ccb', ' ami-052c08d70def0ac62', 'ami-0cda377a1b884a1bc')

    col, lines = os.get_terminal_size()
    welcome = "-----Welcome To AWS Automation Service-----".center(col)


    while True :
        os.system('cls')
        print(welcome)

        print("""\n\n   1) Configure Aws 
    2) Switch Region
    3) Launch an Ec2 Instance
    4) View All Ec2 Instances
    5) Stop An Instance
    6) Launch an Ebs Volume 
    7) Attach Volume To an Instance
    8) Create Snapshot
    9) Create a s3 Bucket
    10) List All s3 buckets
    11) Upload An Object To a Bucket
    12) Create a CDN Using Cloudfront
    13) Create a KeyPair
    14) Create a new Iam User
    15) Create a Security Group
    16) Quit\n""")

        try:
            choice = int(input("Please Choose an Option To Continue : "))

        except ValueError:
            print("\n\nwhoops Please Enter the Choice in Number, for eg. 2 for Launching Ec2 Instance.. ")
            input('\nPress Enter to continue..')
            continue

        if choice == 1:
            configure()
            input('\nPress Enter to Continue')

        elif choice == 2:
            switch()
            input('\nPress Enter To Continue..')

        elif choice == 3:
            img = int(input("""\n  Please Choose Your os\n
        1) Amazon-Linux-2
        2) RHEL8
        3) Ubuntu\n\nYour Choice : """))

            key = input("\nEnter Your KeyPair Name : ")

            sg = input("\nEnter Security Group : ")


            inp = input('\nDo You Wish To use Advanced Options ?(y/n) : ')

            if inp == 'y'.casefold():
                subnetid = ''
                inst = 't2.micro'
                count = input('\nEnter No. Of Instances You Want : ')
                instance = input('\nEnter Desired Instance Type (t2.micro by default) : ')
                sid = input('\nEnter a Subnet id (press Enter for default Subnet) : ')
                if sid != '':
                    subnetid = sid
                if instance != '':
                    inst = instance
                ec2launch(ami[img], key, sg, count, inst, subnetid)

            else:
                ec2launch(ami[img], key, sg)

            input('\nPress Enter To Continue..')

        elif choice == 4:
            viewinstances()
            input('\nPress Enter To Continue..')

        elif choice == 5:
            id = input('\nPlease Enter The Id of The Instance You Wish To Stop : ')
            stopec2(id)
            input('\nPress Enter To Continue..')

        elif choice == 6:
            az = input('\nName Of The Availability Zone to launch the instance in : ')
            size = int(input('\nSize Of The Volume in GB : '))
            ebslaunch(az, size)
            input('\nPress Enter To Continue..')

        elif choice == 7:
            vol = input('\nEnter The Volume ID : ')
            id = input('\nEnter The Instance ID : ')
            attach(vol, id)
            input('\nPress Enter To Continue..')


        elif choice == 8:
            vol = input('\nEnter The Volume ID : ')
            desc = input('\nEnter Description For This Snapshot : ')
            snap(vol, desc)
            input('\nPress Enter To Continue..')

    
        elif choice == 9:
            name = input('\nEnter a Globally Unique Bucket Name : ')
            s3bucket(name)
            input('\nPress Enter To Continue..')
        
    
        elif choice == 10:
            s3list()
            input('\nPress Enter To Continue..')

        elif choice == 11:
            path = input('\nEnter Complete Path To The Object : ')
            bucket = input('\nEnter Name of The Bucket : ')
            b = input('\nDo You want To Make The Object Public? (y/n) : ')
            if b == 'y'.casefold() :
                s3object(path, bucket)
            else:
                s3object(path, bucket, False)
            input('\nPress Enter To Continue..')


        elif choice == 12:
            s3list()
            origin = input('\nEnter the bucket You want to make origin : ')
            cloudfront(origin)
            input('\nPress Enter To Continue..')
        

        elif choice == 13:
            name = input('\nEnter The Name Of The Keypair : ')
            keypair(name)
            input('\nPress Enter To Continue..')

    
        elif choice == 14:
            name = input('\nEnter The Name of Iam User : ')
            iamuser(name)
            input('\nPress Enter To Continue..')

    
        elif choice == 15:
            nm = input('\nEnter Name Of Security Group : ')
            desc = input('\nEnter a Description For The Security Group : ')
            security(nm, desc)
            input('\nPress Enter To Continue..')


        elif choice == 16:
            print('THANKS FOR USING THIS SERVICE'.center(col))
            input('\n\nPress Enter To Exit..')
            os.system('cls')
            break 



def hadoop():
    os.system("tput setaf 3")
    print("\n\t--------------**------------------Hadoop Automation Console---------------------**----------")
    os.system("tput setaf 7")
    while True:
        print("\n\n************************************** Menu List ************************************************")
        print("""
\n\t\t
Press 1: Install Hadoop Requirements
press 2: Configure Name Node
press 3: Configure Data Node
press 4: Configure Hadoop Client
press 5: Limit The Data Node Storage
press 6: Upload Data To Hadoop Cluster
press 7: Read Client Data from Hadoop Cluster
press 8: Delete Client Data
press 9: Stop Name Node
press 10: Stop Data Node
press 11: Exit
""")
        ch = input("\n\t\t\t\tEnter your choice : ") 
        print("\n\t-----------------------------------------------------------------------------------")

        if int(ch) == 1:
           os.system('rpm -ivh /root/jdk-8u171-linux-x64.rpm')
           os.system('rpm -ivh /root/hadoop-1.2.1-1.x86_64.rpm  --force')
           print("\n\tHadoop Requirements Sucessfully Installed In Name Node")
           print("\n\t---------------------------------------------------------------------")
           ab = input("Enter Your Data Node IP :")
           os.system('ssh {} rpm -ivh jdk-8u171-linux-x64.rpm'.format(ab))
           os.system('ssh {} rpm -ivh  hadoop-1.2.1-1.x86_64.rpm  --force'.format(ab))
           print("\n\tHadoop Requirements Sucessfully Installed In Data Node")
           print("\n\t---------------------------------------------------------------------")
           bb = input("Enter Your Client Node IP :")
           os.system('ssh {} rpm -ivh jdk-8u171-linux-x64.rpm'.format(bb))
           os.system('ssh {} rpm -ivh  hadoop-1.2.1-1.x86_64.rpm  --force'.format(bb))
           print("\n\tHadoop Requirements Sucessfully Installed In Client Node")
           print("\n\t---------------------------------------------------------------------")
           
        elif int(ch) == 2:
           dir = input("\n\t\tEnter your Name Node directory name : ")
           print("\t\t\t\tConfiguring hdfs-site.xml file ............")
           os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/hdfs-site.xml")
           os.system("echo -e '\n<!-- Put site-specific property overrides in this file. -->' >> /root/hdfs-site.xml")
           os.system('echo -e "\n<configuration>" >> /root/hdfs-site.xml')
           os.system('echo -e "\n<property>" >> /root/hdfs-site.xml')
           os.system('echo -e "<name>dfs.name.dir</name>" >> /root/hdfs-site.xml')
           os.system('echo -e "<value>{}</value>" >> /root/hdfs-site.xml'.format(dir))
           os.system('echo -e "</property>" >> /root/hdfs-site.xml')
           os.system('echo -e "\n</configuration>" >> /root/hdfs-site.xml')
           os.system('rm -rf /etc/hadoop/hdfs-site.xml')
           os.system('cp  /root/hdfs-site.xml  /etc/hadoop')
           os.system('rm -rf /root/hdfs-site.xml')
           print("\n\tFormatting the Name Node ..............................")
           print()
           os.system('hadoop namenode -format')
           print()
           print()
           nip = input("Enter Name Node IP :")
           print("\t\t\t\tConfiguring core-site.xml file ...........")
           os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/core-site.xml")
           os.system('echo -e "\n<!-- Put site-specific property overrides in this file. -->" >> /root/core-site.xml')
           os.system('echo -e "\n<configuration>" >> /root/core-site.xml')
           os.system('echo -e "\n<property>" >> /root/core-site.xml')
           os.system('echo -e "<name>fs.default.name</name>" >> /root/core-site.xml')
           os.system('echo -e "<value>hdfs://{}:9001</value>" >> /root/core-site.xml'.format(nip))
           os.system('echo -e "</property>" >> /root/core-site.xml')
           os.system('echo -e "\n</configuration>" >> /root/core-site.xml')
           os.system('rm -rf /etc/hadoop/core-site.xml')
           os.system('cp  /root/core-site.xml  /etc/hadoop')
           os.system('rm -rf /root/core-site.xml')
           print("\n\t--------------------------------------------------------------")
           print("\n\t Starting Hadoop Name Node Services .............................")
           os.system('hadoop-daemon.sh start namenode') 
           os.system('jps')

        elif int(ch) == 3:
           dip = input("\t\tEnter Data Node IP : ")
           dio = input("\t\tEnter your Data Node directory name : ")
           print("\t\t\t\tConfiguring hdfs-site.xml file ............")
           os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/hdfs-site.xml")
           os.system("echo -e '\n<!-- Put site-specific property overrides in this file. -->' >> /root/hdfs-site.xml")
           os.system('echo -e "\n<configuration>" >> /root/hdfs-site.xml')
           os.system('echo -e "\n<property>" >> /root/hdfs-site.xml')
           os.system('echo -e "<name>dfs.data.dir</name>" >> /root/hdfs-site.xml')
           os.system('echo -e "<value>{}</value>" >> /root/hdfs-site.xml'.format(dio))
           os.system('echo -e "</property>" >> /root/hdfs-site.xml')
           os.system('echo -e "\n</configuration>" >> /root/hdfs-site.xml')
           os.system('scp  /root/hdfs-site.xml  {}:/etc/hadoop'.format(dip))
           os.system('rm -rf /root/hdfs-site.xml')
           niq = input("Enter Name Node IP :")
           print("\t\t\t\tConfiguring core-site.xml file ...........")
           os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/core-site.xml")
           os.system('echo -e "\n<!-- Put site-specific property overrides in this file. -->" >> /root/core-site.xml')
           os.system('echo -e "\n<configuration>" >> /root/core-site.xml')
           os.system('echo -e "\n<property>" >> /root/core-site.xml')
           os.system('echo -e "<name>fs.default.name</name>" >> /root/core-site.xml')
           os.system('echo -e "<value>hdfs://{}:9001</value>" >> /root/core-site.xml'.format(niq))
           os.system('echo -e "</property>" >> /root/core-site.xml')
           os.system('echo -e "\n</configuration>" >> /root/core-site.xml')
           os.system('scp  /root/core-site.xml  {}:/etc/hadoop'.format(dip))
           os.system('rm -rf /root/core-site.xml')
           print("\n\t--------------------------------------------------------------")
           print("\n\t Starting Hadoop Data Node Services .............................")
           os.system('ssh {} hadoop-daemon.sh start datanode'.format(dip))
           os.system('ssh {} jps'.format(dip))
           print("\n\t--------------------------------------------------------------")
           print("\n\t Showing Hadoop Cluster Report ..............................")
           os.system('ssh {} hadoop dfsadmin -report'.format(dip))

      
        elif int(ch) == 4:
           yu = input("Enter Name Node IP : ")
           print("\t\t\t\tConfiguring core-site.xml file ...........")
           ip = input("\n\t\tEnter Client IP : ")
           os.system("echo -e '<?xml version=\"1.0\"?> \n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>' > /root/core-site.xml")
           os.system('echo -e "\n<!-- Put site-specific property overrides in this file. -->" >> /root/core-site.xml')
           os.system('echo -e "\n<configuration>" >> /root/core-site.xml')
           os.system('echo -e "\n<property>" >> /root/core-site.xml')
           os.system('echo -e "<name>fs.default.name</name>" >> /root/core-site.xml')
           os.system('echo -e "<value>hdfs://{}:9001</value>" >> /root/core-site.xml'.format(yu))
           os.system('echo -e "</property>" >> /root/core-site.xml')
           os.system('echo -e "\n</configuration>" >> /root/core-site.xml')
           os.system('scp  /root/core-site.xml  {}:/etc/hadoop'.format(ip))
           print("\t\tHadoop Client Sucessfully Configured.........")

        elif int(ch) == 5:
           ip = input("\n\tEnter Data Node IP : ")
           si = input("\n\tDo You want to extend/reduce Data Node Storage? : ")
           if si == "extend":
               os.system('ssh {} df -hT'.format(ip))
               ex = input("\n\t\tHow much you want to extend? : ")
               vg = input("\t\tEnter Your Volume Group Name : ")
               lv = input("\t\tEnter Your Logical Volume Name : ")
               os.system('ssh {} lvextend --size {} /dev/{}/{}'.format(ip , ex , vg , lv))
               print("\t\t\tSucessfully Extended the  Data Node Storage ")
               os.system('ssh {} resize2fs  /dev/{}/{}'.format(ip , vg ,lv))
               print("------------------------------------------------------------")
               os.system('ssh {} df -hT'.format(ip))
           elif si == "reduce":
               os.system('ssh {} df -hT'.format(ip))
               ex = input("\n\t\tHow much you want to reduce? : ")
               vg = input("\t\tEnter Your Volume Group Name : ")
               lv = input("\t\tEnter Your Logical Volume Name : ")
               os.system('ssh {} lvextend --size {} /dev/{}/{}'.format(ip , ex , vg , lv))
               print("\t\t\tSucessfully Reduced Data Node Storage ")
               os.system('ssh {} resize2fs  /dev/{}/{}'.format(ip , vg ,lv))
               print("------------------------------------------------------------")
               os.system('ssh {} df -hT'.format(ip))
       
        elif int(ch) == 6:
           ci = input("\t\tEnter Client IP : ")
           fiz = input("\t\tEnter The Name of File You want to upload on Hadoop Cluster : ")
           os.system('ssh {} hadoop fs -put {} /'.format(ci , fiz))
           print("\t\t\tFile Sucessfully Uploaded .......................")
           os.system('ssh {} hadoop fs -ls /'.format(ci))
       
        elif int(ch) == 7:
           co = input("\t\tEnter Client IP : ")
           fii = input("\t\tEnter Your File Name : ")
           os.system('ssh {} hadoop fs -cat /{}'.format(co , fii))

        elif int(ch) == 8:
           ty = input("\t\tEnter Client IP : ")
           foi = input("\t\tEnter Your File Name : ")
           os.system('ssh {} hadoop fs -rm /{}'.format(ty , foi))
           print("\t\tSucessfully Deleted File {} ".format(foi))
       
        elif int(ch) == 9:
           os.system('hadoop-daemon.sh stop namenode')
           os.system('jps')

        elif int(ch) == 10:
           ip = input("\n\tEnter Data Node IP : ")
           os.system('ssh {} hadoop-daemon.sh stop datanode'.format(ip))
           os.system('ssh {} jps'.format(ip))
       
        elif int(ch) == 11:
           break



def basic():
    print("\t--------------------WELCOME USER--------------")
    ch = 'Y'
    while ch == 'Y':
        print("\tCHOOSE ANY OF THE BELOW OPTION:")
        print("\tPress 1 : To run Linux basic commands")
        print("\tPress 2 : To configure webserver")
        base = input("\tEnter your choice: ")
        if base=="1":
            print("PLEASE ENTER ONE OF THE FOLLOWING COMMAND TO RUN:")
            print("""1 : cal
2 : date
3 : ls""")
            x = input()
            if(x=='1'):
                res = input("\tWould you like to see calendar of particular date?[Y/N]")
            if(res == 'Y'):
               print("\tPlease type date to see")
               date = input()
               op = sp.getoutput("cal {}".format(date))
               print(op)
            
            elif(x=='2'):
                output = sp.getoutput("date")
                print(output)
            elif(x=='3'):
                output = sp.getoutput("ls")
                detail = input("\tWould you like to see detailed info of all content?[Y/N]")
                if detail == 'Y':
                    op2 = sp.getoutput("ls -l")
                    print(op2)
                else:
                    print(output)
            else:
                output = sp.getoutput("cal")
                print(output)

        elif base == "2":
            output = sp.getoutput("yum install httpd -y")
            print(output)
            print("\tAPACHE WEBSERVER IS SUCCESSFULLY INSTALLED")
            webpage=input("\tENTER WEBPAGE NAME: ")
            print("\tin progress....")
            content = input("\tENTER CONTENT: ")
            savefile = open(webpage,'w')
            savefile.write(content)
            savefile.close()
            op2 = sp.getoutput("mv {} /var/www/html/".format(webpage))
            output = sp.getoutput("systemctl start httpd")
        else:
            print("INVALID INPUT")
        ch = input("WOULD YOU LIKE TO CONTINUE?[Y/N]")
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
               status,output=sp.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)
               
           
        if(x==2):
           
               m="sudo systemctl status docker"
               status,output=sp.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)
        if(x==3):
           
               m="sudo docker images"
               status,output=sp.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)                   
        if(x==4):
           
               m="sudo docker ps -a"
               status,output=sp.getstatusoutput(m)
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
                status,output=sp.getstatusoutput(m)
                if(status!=0):
                  print("error!!!")
                else:
               
                   print(output)
               else:
                m="sudo docker run -dit --name {} {}".format(cname,iname)
                status,output=sp.getstatusoutput(m)
                if(status!=0):
                  print("error!!!")
                else:
               
                   print(output)
        if(x==6):
           
               m="sudo docker ps"
               status,output=sp.getstatusoutput(m)
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

                   status,output=sp.getstatusoutput(m)
                   if(status!=0):
                       print("error!!!")
                   else:
               
                       print(output)  
                elif(inn==2):
                    m="docker logout"
                    status,output=sp.getstatusoutput(m)
                    if(status!=0):
                       print("error!!!")
                    else:
               
                       print(output)  

        if(x==8):
               cid=input("enter container name")
               m="sudo docker logs {}".format(cid)
               status,output=sp.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)

        if(x==9):
               cid=input("Enter container name : ")
               cmd=input("enter the command : ")

               
               m="sudo docker exec -it {} {}".format(cid,cmd)
               status,output=sp.getstatusoutput(m)
               if(status!=0):
                  print("error!!!")
               else:
               
                   print(output)  
        if(x==10):
                val=int(input("Enter 1. to remove container 2. to remove all the container 3. to remove Image"))
                if(val==1):
                  contid=input("enter the container name:")
                  m="sudo docker rm -f {}".format(contid)
                  status,output=sp.getstatusoutput(m)
                  if(status!=0):
                     print("error!!!")
                  else:
               
                     print(output)  
                elif(val==2):
                    print("\n\t\t!! Attention !!\n\t\t## Not Recommended ##")
                    x=input("If you want to delete all the containers then press 1 ")
                    if(x==1):
                        m="sudo docker rm -f $(sudo docker container ls -a -q"
                        status,output=sp.getstatusoutput(m)
                        if(status!=0):
                             print("error!!!")
                        else:
                             print(output)
                    else:
                        pass
                elif(val==3):
                        Iid=input("enter the Image name:")
                        m="sudo docker rmi  {}".format(Iid)
                        status,output=sp.getstatusoutput(m)
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
        print("2.aws") 
        print("3.hadoop")
        print("4.basic command/web-server")

        print("0.EXIT")

        x=input()
        x=int(x)
        if(x==1):
            docker()
        elif(x==2):
            aws()
        elif(x==3):
            hadoop()
        elif(x==4):
            basic()
        elif(x==0):
            flag=0
            break
print("program completed")
     
