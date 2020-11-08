#!/usr/bin/python3

import os
print("Welcome to Menu Program")
loc = input("\nDo you wish to run commands locally or remote?\n")

print("\nGreat!")
while(True):
    print("""        Here are your options:
        ----------------------
        
        PRESS 0 TO EXIT

        COMMON COMMANDS
        ---------------
        S1. Date
        S2. Calender
        S3. NIC

        CONFIGURATIONS
        --------------
        C1. Configure yum
        C2. Configure Webserver
        C3. Configure Docker

        ADDITIONAL STORAGE /  DRIVES
        ----------------------------
        M1. Create Static Partition
        M2. Delete Static Partition
        M3. Format partition
        M4. Mount to folder
        M5. Unmount from folder
        M6. Create VG - LVM (Dynamic Partition)
        M7. Extend LVM size

        DOCKER
        ------
        D1. Run container
        D2. Stop container
        D3. Restart container and get shell access
        D4. Delete container
        D5. Show running containers
        D6. Show stopped containers
        
        HADOOP
        ------
        H1. Configure Client
        H2. Configure NameNode
        H3. Configure DataNode
        H4. Report
        H5. List Data
        H5. Put Data
        H6. Get Data
        H7. Remove Data
        """)

    choice = input("Enter your option: ")
    if(choice == "0"):
        exit()
    elif(choice == "C1"):
        os.system("cp ishan.repo /etc/yum.repos.d/")
        os.system("yum repolist")
    elif(choice == "C2"):
        os.system("yum install httpd -y")
        os.system("systemctl start httpd")
        os.system("systemctl enable httpd")
        os.system("ifconfig enp0s3")
        print("Put your files in /var/www/html/ and open browser to system IP")
    elif(choice == "C3"):
        os.system("cp docker.repo /etc/yum.repos.d/")
        os.system("yum install docker-ce --nobest -y")
        os.system("systemctl start docker")
        os.system("systemctl enable docker")
    elif(choice == "M1"):
        os.system("fdisk -l")
        diskname = input("Check your drive name and input: ")
        os.system("""echo -e "n\np\n1\n\n\nw\n" | fdisk {}""".format(diskname))
    elif(choice=="M2"):
        diskname = input("Input disk name: ")
        os.system("""echo -e "d\nw\n" | fdisk {}""".format(diskname))
    elif(choice == "M3"):
        pname = input("Enter partition name: ")
        os.system("mkfs.ext4 {}".format(pname))
    elif(choice == "M4"):
        os.system("fdisk -l")
        pname = input("Enter partition name: ")
        fname = input("Enter folder name: ")
        os.system("mount {} {}".format(pname,fname))
    elif(choice == "M5"):
        name = input("Enter folder location/name :")
        os.system("umount {}".format(name))
    elif(choice == "M6"):
        dname = input("Enter drive name: ")
        vname = input("Enter VG name you want: ")
        lname = input("Enter LV name: ")
        lsize = input("Enter LV size (eg 30G) :")
        floc = input("Enter folder location/name")
        os.system("pvcreate {}".format(dname))
        os.system("vgcreate {} {}".format(vname,dname))
        os.system("lvcreate --size {} --name {} {}".format(lsize,lname,vname))
        os.system("mkfs.ext4 /dev/{}/{}".format(vname,lname))
        os.system("mount /dev/{}/{} {}".format(vname,lname,floc))
    elif(choice == "M7"):
        vname = input("Enter VG name")
        lname = input("Enter LV name")
        addsize = input("How much to extend by? :")
        os.system("lvextend --size +{} /dev/{}/{}".format(addsize,vname,lname))
        os.system("resize2fs /dev/{}/{}".format(vname,lname))
    elif(choice == "D1"):
        name = input("Enter name: ")
        image = input("Enter OS: ")
        os.system("docker run -it --name {} {}".format(name,image))
    elif(choice == "D2"):
        name = input("Enter container name: ")
        os.system("docker stop {}".format(name))
    elif(choice == "D3"):
        name = input("Enter container name: ")
        os.system("docker start {}".format(name))
        os.system("docker attach {}".format(name))
    elif(choice == "D4"):
        name = input("Enter container name :")
        os.system("docker rm -f {}".format(name))
    elif(choice == "D5"):
        os.system("docker ps")
    elif(choice == "D6"):
        os.system("docker ps -a")
    elif(choice == "H1"):
        ip = input("Input NameNode IP: ")
        os.system("sed -i 's/0.0.0.0/{}/g' core-site.xml".format(ip))
        os.system("cp -rf core-site.xml /etc/hadoop/")
        os.system("sed -i 's/{}/0.0.0.0/g' core-site.xml".format(ip))
    elif(choice == "H2"):
        ip = input("Input IP: ")
        os.system("mkdir /nn")
        os.system("cp -rf hdfs-site.xml /etc/hadoop/")
        os.system("cp -rf core-site.xml /etc/hadoop/")
        os.system("""echo -e "yes\n" | hadoop namenode -format""")
        os.system("hadoop-daemon.sh start namenode")
    elif(choice == "H3"):
        ip = input("Input NameNode IP")
        os.system("mkdir /dn")
        os.system("sed -i 's/dfs.name.dir/dfs.data.dir/g' hdfs-site.xml")
        os.system("sed -i 's/nn/dn/g' hdfs-site.xml")
        os.system("cp -rf hdfs-site.xml /etc/hadoop/")
        os.system("sed -i 's/dfs.data.dir/dfs.name.dir/g' hdfs-site.xml")
        os.system("sed -i 's/dn/nn/g' hdfs-site.xml")
        os.system("sed -i 's/0.0.0.0/{}/g' core-site.xml".format(ip))
        os.system("cp -rf core-site.xml /etc/hadoop/")
        os.system("sed -i 's/{}/0.0.0.0/g' core-site.xml")
        os.system("hadoop-daemon.sh start datanode")
    elif(choice == "H4"):
        os.system("hadoop dfsadmin -report")
    elif(choice == "H5"):
        os.system("hadoop fs -ls /")
    elif(choice == "H6"):
        floc = input("Enter file location/name: ")
        bsize = input("Enter block size: ")
        brep = input("Enter number of replications: ")
        os.system("hadoop fs -Ddfs.block.size={} -Ddfs.replications={} -put {} /".format(bsize,brep,floc))
    elif(choice == "H7"):
        floc = input("Enter file location/name: ")
        os.system("hadoop fs -get {}".format(floc))
    elif(choice == "H8"):
        floc = input("Enter file location/name: ")
        os.system("hadoop fs -rm {}".format(floc))
    else:
        print("Incorrect Option")
