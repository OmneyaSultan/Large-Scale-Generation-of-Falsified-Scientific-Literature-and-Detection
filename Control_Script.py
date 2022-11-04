#Group: Sieze The Data
#Course: DSCI 550 - Spring 2022

import Image_Caption.GenerateCaptions as Captions
import step7_8_9.fake_name_gen as fake_names
import step7_8_9.fake_paper_gen as fake_pdf
import step7_8_9.final_tsv_gen as final_tsv
import sys


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please Run --Generate_Captions --Test_Captions")

    elif sys.argv[1] == '--Generate_Captions':
        #must have tika dockers running to run this code
        #This goes through the entire list of Image names and URLs for the images
        #Possibility of crashing due to so many entries
        Caption_Dict_1, fake_images_1= Captions.save_captions("Image_Caption//Fake_Images_pt1.csv")
        Captions.output_caption_csv(fake_images_1, 'Fake_Images_Final.csv')

        Caption_Dict_2, fake_images_2= Captions.save_captions("Image_Caption//Fake_Images_pt2.csv")
        Captions.output_caption_csv(fake_images_2, 'Fake_Images_Final.csv')

        Caption_Dict_3, fake_images_3= Captions.save_captions("Image_Caption//Fake_Images_pt3.csv")
        Captions.output_caption_csv(fake_images_3, 'Fake_Images_Final.csv')

        Caption_Dict_4, fake_images_4= Captions.save_captions("Image_Caption//Fake_Images_pt4.csv")
        Captions.output_caption_csv(fake_images_4, 'Fake_Images_Final.csv')



    elif sys.argv[1] == '--Test_Captions':
        #must have tika dockers running to run this code
        #This goes through only 1/4 of the image names and URLs for the images
        Caption_Dict_1, fake_images_1= Captions.save_captions("Image_Caption//Fake_Images_pt1.csv")
        Captions.output_caption_csv(fake_images_1, 'Fake_Images_Batch1.csv')
        
        
    elif sys.argv[1] == '--fake_names':
        #must have faker library installed. use pip install faker
        #generates fake names and creates csv to be used for generating fake pdf
        fake_names.gen_fake_names()
        

    elif sys.argv[1] == '--fake_pdf':
        #must have pylatex installed. use pip install pylatex
        #must have miktex installed from miktex.org (for windows - may be different for other OS)
        fake_pdf.gen_fake_pdf()
        
        
    elif sys.argv[1] == '--final_tsv':
        final_tsv.gen_fake_tsv()

    #Accounts for any naming errors
    else:
        print("Please Run --Generate_Captions")
