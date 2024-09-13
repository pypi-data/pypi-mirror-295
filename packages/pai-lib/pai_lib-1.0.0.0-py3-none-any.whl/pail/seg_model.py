from email.mime import base
import torch 
import torch.nn as nn

import torch.nn.functional as F

class Seg_Network(nn.Module):
    def __init__(self,in_channels=3, out_channels=3, base_width=128):
        super(Seg_Network, self).__init__()
        self.encoder = Encoder(in_channels, base_width)
        self.decoder = Decoder(base_width, out_channels=out_channels)

    def forward(self, x):
        b3 = self.encoder(x)
        output = self.decoder(b3)
        return output

    def get_n_params(model):
        pp=0
        for p in list(model.parameters()):
            nn=1
            for s in list(p.size()):
                nn = nn*s
            pp += nn
        return pp


class Encoder(nn.Module):
    def __init__(self, in_channels, base_width):
        super(Encoder, self).__init__()
        
        self.block1 = nn.Sequential(
            nn.Conv2d(in_channels, base_width,kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width),
            nn.ReLU(inplace=True),
            nn.Conv2d(base_width, base_width, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width),
            nn.ReLU(inplace=True)
            )
        ''' self.block1_conv_1          =   nn.Conv2d(in_channels, base_width,kernel_size=3, padding=1)
        self.block1_batch_norm_1    =   nn.BatchNorm2d(base_width)
        self.block1_relu_1          =   nn.ReLU(inplace=True)
        self.block1_conv_2          =   nn.Conv2d(base_width, base_width,kernel_size=3, padding=1)
        self.block1_batch_norm_2    =   nn.BatchNorm2d(base_width)
        self.block1_relu_1          =   nn.ReLU(inplace=True) '''
        
        # self.mp1    = nn.Sequential(nn.MaxPool2d(2))
        self.block2 = nn.Sequential(
            nn.Conv2d(base_width,base_width*2,kernel_size=3,padding=1),
            nn.BatchNorm2d(base_width*2),
            nn.ReLU(inplace=True),
            nn.Conv2d(base_width*2, base_width*2, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*2),
            nn.ReLU(inplace=True)
            )
        ''' self.block2_conv_1          =   nn.Conv2d(base_width,base_width*2,kernel_size=3,padding=1)
        self.block2_batch_norm_1    =   nn.BatchNorm2d(base_width*2)
        self.block2_relu_1          =   nn.ReLU(inplace=True)
        self.block2_conv_2          =   nn.Conv2d(base_width*2, base_width*2,kernel_size=3, padding=1)
        self.block2_batch_norm_2    =   nn.BatchNorm2d(base_width*2)
        self.block2_relu_1          =   nn.ReLU(inplace=True) '''
        # self.mp2    = nn.Sequential(nn.MaxPool2d(2))
        self.block3 = nn.Sequential(
            nn.Conv2d(base_width*2,base_width*4,kernel_size=3,padding=1),
            nn.BatchNorm2d(base_width*4),
            nn.ReLU(inplace=True),
            nn.Conv2d(base_width*4, base_width*4, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*4),
            nn.ReLU(inplace=True)
            )
        #self.mp3    = nn.Sequential(nn.MaxPool2d(2))
    
    def forward(self,x):
        
        #start = torch.cuda.memory_allocated()
        if x.shape==3:
            x = x.view(1,x.shape[0],x.shape[1],x.shape[2])
               
        ''' 
        b1          =   self.block1_conv_1(x)          
        b1          =   self.block1_batch_norm_1(b1)
        b1          =   self.block1_relu_1(b1)          
        b1          =   self.block1_conv_2(b1)          
        b1          =   self.block1_batch_norm_2(b1)
        b1_         =   self.block1_relu_1(b1)
  
        print("memory allocated: ", end)
        b2          =   self.block2_conv_1(b1_)          
        b2          =   self.block2_batch_norm_1(b2)
        b2          =   self.block2_relu_1(b2)          
        b2          =   self.block2_conv_2(b2)          
        b2          =   self.block2_batch_norm_2(b2)
        b2          =   self.block2_relu_1(b2)
        '''
        b1          = self.block1(x)
        #mp1         = self.mp1(b1)
        b2          = self.block2(b1)
        #mp2         = self.mp2(b2)
        b3          =   self.block3(b2)
        return b3


class Decoder(nn.Module):
    def __init__(self,base_width,out_channels=144):
        super(Decoder, self).__init__()

        self.up1    = nn.Sequential(
            nn.Conv2d(base_width*4, base_width*4, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*4),
            nn.ReLU(inplace=True)
            ) # nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
        
        self.db1    = nn.Sequential(
            nn.Conv2d(base_width*4, base_width*4, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*4),
            nn.ReLU(inplace=True),
            nn.Conv2d(base_width*4, base_width*2, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*2),
            nn.ReLU(inplace=True)
            )

        self.up2    = nn.Sequential(
            nn.Conv2d(base_width*2,base_width*2, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*2),
            nn.ReLU(inplace=True)
            ) # nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True),
        
        self.db2    = nn.Sequential(
            nn.Conv2d(base_width*2, base_width*2, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width*2),
            nn.ReLU(inplace=True),
            nn.Conv2d(base_width*2, base_width, kernel_size=3, padding=1),
            nn.BatchNorm2d(base_width),
            nn.ReLU(inplace=True)
            )
        
        self.fin_out = nn.Sequential(nn.Conv2d(base_width,out_channels,kernel_size=3, padding=1)) #nn.Sigmoid(inplace=True)
    
    def forward(self, b3):
        up1         = self.up1(b3)
        db1         = self.db1(up1)
        up2         = self.up2(db1)
        db2         = self.db2(up2)

        out         = self.fin_out(db2)

        return out






class Seg_Network_small(nn.Module):
    def __init__(self,in_channels=3, out_channels=3, base_width=128):
        super(Seg_Network_small, self).__init__()
        self.conv_1             =   nn.Conv2d(in_channels, base_width,kernel_size=3, padding=1)
        self.conv_output_1      =   nn.Conv2d(base_width, out_channels,kernel_size=3, padding=1)
        
        self.conv_2             =   nn.Conv2d(out_channels, int(base_width/2),kernel_size=3, padding=1)
        self.conv_output_2      =   nn.Conv2d(int(base_width/2), out_channels,kernel_size=3, padding=1)
        
        self.conv_3             =   nn.Conv2d(out_channels, int(base_width/3),kernel_size=3, padding=1)
        self.conv_output_3      =   nn.Conv2d(int(base_width/3), out_channels,kernel_size=3, padding=1)
        
        self.conv_4             =   nn.Conv2d(out_channels, int(base_width/4),kernel_size=3, padding=1)
        self.conv_output_4      =   nn.Conv2d(int(base_width/4), out_channels,kernel_size=3, padding=1)
        
        self.conv_1_up          =   nn.Conv2d(out_channels, int(base_width/3),kernel_size=3, padding=1)
        self.conv_output_5      =   nn.Conv2d(int(base_width/3), out_channels,kernel_size=3, padding=1)
        
        self.conv_2_up          =   nn.Conv2d(out_channels, int(base_width/2),kernel_size=3, padding=1)
        self.conv_output_6      =   nn.Conv2d(int(base_width/2), out_channels,kernel_size=3, padding=1)
        
        self.conv_3_up          =   nn.Conv2d(out_channels, base_width,kernel_size=3, padding=1)
        self.conv_output        =   nn.Conv2d(base_width, out_channels,kernel_size=3, padding=1)
        
        self.relu               =   nn.ReLU(inplace=True)
        self.sig                =   nn.Sigmoid()
    def forward(self, x):
        
        x   =   self.relu(self.conv_1(x))
        x   =   self.conv_output_1(x)
        
        x   =   self.relu(self.conv_2(x))
        x   =   self.conv_output_2(x)
        
        x   =   self.relu(self.conv_3(x))
        x   =   self.conv_output_3(x)
        
        x   =   self.relu(self.conv_4(x))
        x   =   self.conv_output_4(x)
        
        x   =   self.relu(self.conv_1_up(x))
        x   =   self.conv_output_5(x)
        
        x   =   self.relu(self.conv_2_up(x))
        x   =   self.conv_output_6(x)
        
        x   =   self.relu(self.conv_3_up(x))
        x   =   self.sig(self.conv_output(x))
        
        return x

    def get_n_params(model):
        pp=0
        for p in list(model.parameters()):
            nn=1
            for s in list(p.size()):
                nn = nn*s
            pp += nn
        return pp

