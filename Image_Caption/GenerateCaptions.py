
#Upload fake images to imgur
#Save imgur links to excel file, also save original image name here for reference.



import glob
import csv
import requests


#Creates csv with the list of fake image names from the Fake_Images folder produced with DCGAN
#URLs are manually added from imgur. Static file provided in folder
def create_img_csv():
    images = glob.glob('Image_Caption/Fake_Images/*.jpeg')+glob.glob('Image_Caption/Fake_Images/*.png')+glob.glob('Image_Caption/Fake_Images/*.jpg')
    Image_Name_lst=[]
    for i in images:
        name=i.split("/")
        Image_Name_lst.append(name[1])

    Image_Name_lst= sorted(Image_Name_lst)

    fake_csv=open('Fake_Images.csv', "w")
    writer = csv.writer(fake_csv)
    for name in Image_Name_lst:
        writer.writerow([name])


#Function to extract captions from inception link
def get_caption(image_url):
    host_link= "http://0.0.0.0:8764/inception/v3/caption/image?url="
    content = requests.get(host_link+image_url)
    js_cont=content.json()
    first_item=js_cont["captions"][0]
    caption=first_item["sentence"].replace(" .", "")
    caption=caption.title()
    return caption


#Iterate through the URLs provided, get caption and save them to a list and dictionary
def save_captions(csv_file):
    fake_csv=open(csv_file, encoding='utf-8-sig')
    read_csv= csv.reader(fake_csv)

    fake_images=[]
    for row in read_csv:
        fake_images.append([row[0], row[1]])

    Caption_Dict={}

    #read excel csv
    for img in fake_images:
        capt=get_caption(img[1])
        Caption_Dict[img[0]]=capt
        img.append(capt)

    return Caption_Dict, fake_images

#write new csv with captions
def output_caption_csv(fake_images, output_file):
    
    try:
        fake_csv_read=open(output_file, encoding='utf-8-sig')
        current_csv=csv.reader(fake_csv_read)
        
        existing_rows=[]
        #Read Fake_Images csv
        for row in current_csv:
            existing_rows.append([row[0], row[1], row[2]])
            #print(row[0])
    
    except:
        existing_rows=[]

    for i in fake_images:
        existing_rows.append(i)
        
    #Write new csv
    fake_csv_final=open(output_file, "w")
    writer = csv.writer(fake_csv_final)
    for row in existing_rows:
        writer.writerow([row[0],row[1],row[2]])



	