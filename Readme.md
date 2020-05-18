# CC PROJECT

## TEAM NAME

    CC_0085_0133_0171_0289

## TEAM MEMBERS (in inc order of srn)

    JASRAJ ANAND
    RITWIK SINHA
    KESHAV AGRAWAL
    AKASH MUKHOPADHYAY

#### Note : For all the files docker-compose is same, keep only the necessary services!

### IP ADDRESSES

```
52.87.27.206 ORCHESTRATOR
54.166.218.42 USERS
35.153.168.26 RIDES
CC-Project-344747991.us-east-1.elb.amazonaws.com LOAD BALANCER
```

### USERS

```
sudo docker image build -t users .
sudo docker-compose up
```

### RIDES

```
sudo docker image build -t rides .
sudo docker-compose up
```

### ORCHESTRATOR MASTER AND SLAVE

```
sudo docker image build -t orchestrator .
sudo docker image build -t master .
sudo docker image build -t slave .
sudo docker-compose up
```
