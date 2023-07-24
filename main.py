from PIL import ImageFont, ImageDraw, Image  
import cv2  
import requests
import numpy as np 
import moviepy.editor as mpe
from moviepy.editor import *
import os

random_num = np.random.randint(1, 7)
random_music = np.random.randint(1, 6)
cap = cv2.VideoCapture(f'template_videos/{random_num}.mp4')

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
   
size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
result = cv2.VideoWriter(f'exported_videos/exported_video{random_num}.avi', fourcc, 30, size)

font_size = 43

QUOTE_DATA = {
    "limit": 1,
    "maxLength": 30,
    "minLength": 10,
}

def get_motivational_quote(max_length=30):
    try:
        response = requests.get("https://api.quotable.io/quotes/random", QUOTE_DATA)
        data = response.json()
        print(data)
        quote = data[0]["content"]

        return quote
            
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except (KeyError, IndexError):
        return "Error: Unable to fetch quote"

# Example usage:
text = get_motivational_quote(max_length=30)
    

while(True):
    
    ## MAIN FRAME HANDLING
    # Capture frames in the video
    ret, frame = cap.read()
    if ret == None:
        break
    font = ImageFont.truetype("THEBOLDFONT.ttf", font_size)
    
    # Convert the image to RGB (OpenCV uses BGR) to use for pillow:
    try:
        cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    except:
        print("Reached end")
        break
   
    # Pass the image to PIL  
    pil_im = Image.fromarray(cv2_im_rgb) 
    draw = ImageDraw.Draw(pil_im)

    # MAIN TEXT
    W = cap.get(3)
    H = cap.get(4)

    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (W - text_width) // 2
    text_y = (H - text_height) // 2
    
    # OUTLINE
    outline_color = (0, 0, 0)

    # Outline created with multiple text with slight offsets
    outline_offsets = [
        (-3, -3), (-3, 3), (3, -3), (3, 3),
        (-2, -2), (-2, 2), (2, -2), (2, 2),
        (-1, -1), (-1, 1), (1, -1), (1, 1)
    ]
    for offset_x, offset_y in outline_offsets:
        draw.text((text_x + offset_x, text_y + offset_y), text, fill=outline_color, font=font)

    draw.text((text_x,text_y),  text, fill=(255, 255, 255), font=font)
    
    ## MAIN VIDEO HANDLING
    cv2_im_processed = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  

    cv2.imshow('video', cv2_im_processed)
    result.write(cv2_im_processed)
  
    # creating 'q' as the quit 
    # button for the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# release the cap object
cap.release()
result.release()
# close all windows
cv2.destroyAllWindows()

# Add Music
clip = mpe.VideoFileClip(f'exported_videos/exported_video{random_num}.avi')
sped_up_clip = clip.fx(vfx.speedx, 2)
audio_bg = mpe.AudioFileClip(f'music/{random_music}.MP3')
final_clip = sped_up_clip.set_audio(audio_bg)
final_clip.write_videofile(f'finished_videos/exported_video{random_num}.mp4')

# Remove exported video
os.remove(f'exported_videos/exported_video{random_num}.avi')

