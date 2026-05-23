from PIL import Image

Average = 0
list1=[]
output =[]
image_name_lj = input("文件夹路径：(绝对路径，以\结尾)\n")
image_name_start = input("文件名(不含后面的数字)：\n")
image_name_end = input("文件类型（尾缀）如.jpg  .png:\n")
ccdd = int(input("有多少个文件？\n"))
image_name=' '
#image_name_start="image/BadApple"
#image_name_end='.png'

for i in range(ccdd):
    image_name = image_name_lj+image_name_start+str(i)+image_name_end
    img = Image.open(image_name)
    img2 = img.convert('L')
    for yy in range(8):
        for xx in range(8):
            Average=0
            for dy in range(4):
                for dx in range(4):
                    x = 4*xx+dx
                    y=4*yy+dy
                    Average = Average+img2.getpixel((x, y))
                    Average = Average/16
            if Average>127:
                list1.append(1)
            else:
                list1.append(0)
        output.append(list1[7]+(list1[6]*2)+(list1[5]*4)+(list1[4]*8)+(list1[3]*16)+(list1[2]*32)+(list1[1]*64)+(list1[0]*128))
        #print(list1)
        list1=[]
    #print(i)
print("开始写")    
with open('output.txt','w')as file:
    file.write(f'{output}')
print("写完成")

statistics = [0]*256
ysbm = []
dyys = []
#print(ysbm)
for i in output:
    statistics[i] += 1
print("各种显示的可能出现次数：")
print(statistics)
statistics_bf=statistics.copy()#备份统计次数

for i in range(256):
    dyys.append(list([i]))
    ysbm.append([])

def sort():#排序一次
    for n in range(len(statistics)-1):
        if statistics[n]>statistics[n+1]:
            statistics[n],statistics[n+1] = statistics[n+1],statistics[n]
            dyys[n],dyys[n+1] = dyys[n+1],dyys[n]
    return
for m in range(256):
    sort()
    
for i in range(255):
    for m in dyys[0]:#把对应元素的第0项里列出的元素序号
        ysbm[m].append(0)#对应编码全部添加0
    for m in dyys[1]:#第1项里列出的元素序号
        ysbm[m].append(1)#对应编码全部添加1
    #合并第0项和第一项
    statistics[0]=statistics[0]+statistics[1]
    del statistics[1]
    dyys[0] = dyys[0]+dyys[1]
    del dyys[1]
    #排序一次
    sort()
#print(ysbm)    

out_huffman=[]
a=0#有效位计数
temp=0#输出缓存
for i in output:
    for m in ysbm[i]:
        temp += m<<a
        a+=1
    if a>=8:
        a -=8
        out_huffman.append(255&temp)
        temp>>8
with open('压缩后视频数据.txt','w')as file:
    file.write(f'{out_huffman}')
print("压缩完毕")
print("原视频信息长度："+str(len(output)))
print("压缩后："+str(len(out_huffman)))

out_ysbm=[0]*256#元素编码
out_bmcd=[0]*256#编码长度
for i in range(256):
    n=0
    if statistics_bf[i] == 0:
        out_ysbm[i]=1
        out_bmcd[i]=0
    else:
        out_bmcd[i]=len(ysbm[i])
        for m in ysbm[i]:
            out_ysbm[i]+=m<<n
            n +=1            
with open('元素编码.txt','w')as file:
    file.write(f'{out_ysbm}')
print("元素编码数据已存储")
with open('编码长度.txt','w')as file:
    file.write(f'{out_bmcd}')
print("编码长度数据已存储")

aaa=input("按下任意键退出")
#for i in range(statistics.count(0)):
#   del statistics[0]
#    del j[0]
#for i in range(len(statistics)):
#    print(str(j[i]) + ':' + str(statistics[i]))

