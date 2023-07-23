from PIL import ImageFont, ImageDraw, Image  
import cv2  
import numpy as np 

random_num = np.random.randint(1, 7)
cap = cv2.VideoCapture(f'template_videos/{random_num}.mp4')

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
result = cv2.VideoWriter(f'exported_videos/exported_video{random_num}.mp4', 0, 0, size)

font_size = 30

while(True):
      
    # Capture frames in the video
    ret, frame = cap.read()
  
    # describe the type of font
    # to be used.
    font = ImageFont.truetype("THEBOLDFONT.ttf", font_size)
    
    # Convert the image to RGB (OpenCV uses BGR)  
    cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
   
    # Pass the image to PIL  
    pil_im = Image.fromarray(cv2_im_rgb) 

    draw = ImageDraw.Draw(pil_im)
    W = cap.get(3)
    H = cap.get(4)

    draw.text(((W-font_size)/2,(H-font_size)/2), "One day, or day one.", font=font)
    
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  

    cv2.imshow('video', cv2_im_processed)
  
    # creating 'q' as the quit 
    # button for the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# release the cap object
cap.release()
result.release()
# close all windows
cv2.destroyAllWindows()