import subprocess as sp
import os


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

