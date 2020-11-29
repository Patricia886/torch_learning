import torchvision as tv
import torchvision.transforms as transforms
from torchvision.transforms import ToPILImage
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import torch as t
from torch.autograd import Variable


show = ToPILImage() #可以把Tensor转成Image，方便可视化


#定义对数据的预处理
transform = transforms.Compose([transforms.ToTensor(),#转为Tensor
        transforms.Normalize((0.5,0.5,0.5),(0.5,0.5,0.5))])#归一化


#训练集
trainset = tv.datasets.CIFAR10(root="./data",train=True,download=True,transform=transform)
trainloader = t.utils.data.DataLoader(
    trainset,batch_size=4,shuffle=True,num_workers=0)

#测试集
testset = tv.datasets.CIFAR10("./data",train=False,download=True,
            transform=transform)
testloader = t.utils.data.DataLoader(testset,batch_size=4,shuffle=False,
            num_workers=0)
            
classes = ('plane','car','bird','cat',
            'deer','dog','frog','horse','ship','truck')


class Net(nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.conv1 = nn.Conv2d(3,6,5)
        self.conv2 = nn.Conv2d(6,16,5)
        self.fc1 = nn.Linear(16*5*5,120)
        self.fc2 = nn.Linear(120,84)
        self.fc3 = nn.Linear(84,10)

    def forward(self,x):
        x = F.max_pool2d(F.relu(self.conv1(x)),(2,2))
        x = F.max_pool2d(F.relu(self.conv2(x)),2)
        x = x.view(x.size()[0],-1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()

criterion = nn.CrossEntropyLoss()#交叉熵损失函数
optimizer = optim.SGD(net.parameters(),lr=0.001,momentum=0.9)

#训练网络
for epoch in range(10):

    running_loss = 0.0
    for i,data in enumerate(trainloader,0):

        #输入数据
        inputs, labels = data
        inputs, labels = Variable(inputs),Variable(labels)

        #梯度清零
        optimizer.zero_grad()

        #forward+backward
        outputs = net(inputs)
        loss = criterion(outputs,labels)
        loss.backward()

        #更新参数
        optimizer.step ()

        #打印log信息
        running_loss += loss.data
        if i % 2000 == 1999: #每2000个batch打印一次训练状态
            print('[%d, %5d] loss: %.3f'%(epoch+1, i+1, running_loss / 2000))
            running_loss = 0.0
print('Finished Training')

#测试
dataiter = iter(testloader)
correct = 0
total = 0
for data in testloader:
    images, labels = data
    outputs = net(Variable(images))
    _, predicted = t.max(outputs.data, 1)
    total +=labels.size(0)
    correct +=(predicted == labels).sum()

print('10000张测试集中的准确率为：%d %%'%(100*correct/total))