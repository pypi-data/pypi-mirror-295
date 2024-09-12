# -*- coding: utf-8 -*-

import cv2
import numpy as np
import matplotlib.colors as mcolors
import io
import base64
import os

from PIL import Image
from robot.libraries.BuiltIn import BuiltIn


class ImageProcessing:
    def __init__(self):
        pass
    #KeyWord

    def detect_and_mask_objects(self, image_path , contour_area = None, hsv_array_lower = None, hsv_array_upper = None):
        """
        ***|    Description     |***
        |   *`Detect And Mask Objects`*   |   ส่ง path รูปภาพ และ สี เพื่อไป mask object ที่เป็นสีดังกล่าวภายในภาพ |
 
        ***|    Example     |***
        | *`Detect And Mask Objects`* | image_path | color = String | contour_area = Int
 
        ***|    Parameters     |***
        -  image_path
        -  color (ณ ปัจจุบัน มีให้ทดสอบเฉพาะ color = green)
        -  contour_area (Minimum area to consider a contour valid | หากสนใจพวกเส้นหรือตัวอักษร min_contour_area = 50-100 
        หรือหากสนใจสิ่งที่ใหญ่กว่าเช่นกรอบหรือกล่อง Text Field ให้ min_contour_area = 3500 - 5000++)
        -  hsv_array_lower ค่า min hsv 
        -  hsv_array_upper ค่า max hsv
 
        *`ทดสอบได้เฉพาะบางหน้าเท่านั้น บางรูปอาจจะไม่สามารถจับ mask ต้องกำหนดค่าเฉพาะ`*
        """
        if contour_area == None or hsv_array_lower == None or hsv_array_upper == None:
            raise ValueError("Error Argument contour_area or hsv_array_lower or hsv_array_upper is None ")
        #read image with cv2.imread
        image = cv2.imread(image_path)
        image_old = cv2.imread(image_path)
        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        #np set hsv lower , upper
        h_lower = hsv_array_lower[0]
        s_lower = hsv_array_lower[1]
        v_lower = hsv_array_lower[2]
        h_upper = hsv_array_upper[0]
        s_upper = hsv_array_upper[1]
        v_upper = hsv_array_upper[2]

        # Define the green color range for the mask
        lower_color = None
        upper_color = None
        if contour_area != None and hsv_array_lower != None and hsv_array_upper != None:
            lower_color = np.array([h_lower, s_lower, v_lower])
            upper_color = np.array([h_upper, s_upper, v_upper])

            # Create the mask
            mask = cv2.inRange(hsv,lower_color,upper_color)

            # Find contours in the binary image
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours based on their size
            min_contour_area = contour_area  # Minimum area to consider a contour valid
 
            # Filter contours with an area greater than or equal to min_contour_area | กรอง contour ที่มีพื้นที่มากกว่าหรือเท่ากับ min_contour_area
            filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

            # Draw contours on the original image with a thin red line | วาดเส้น ตาม filtered_contours ที่มี
            draw_contour_image = cv2.drawContours(image, filtered_contours, -1, (255, 0, 0), 2)  

            # Convert image back to PIL format  | หากต้องการดูรูปให้เปิด image_pil.show()  | COLOR_BGR2RGB , cv2.COLOR_BGR2RGB , cv2.COLOR_HSV2RGB
            # image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))   #(กรณีทดสอบดูรูปแรกสุด)
            # image_pil.show()
            image_new_pil = Image.fromarray(image)
            # image_pil.show()

            # แปลงภาพ PIL เป็น base64
            image_old_pil = Image.fromarray(cv2.cvtColor(image_old, cv2.COLOR_BGR2RGB))
            buffered_old = io.BytesIO()
            image_old_pil.save(buffered_old, format="PNG")
            old_image_base64 = base64.b64encode(buffered_old.getvalue()).decode('utf-8')

            buffered_new = io.BytesIO()
            image_new_pil.save(buffered_new, format="PNG")
            new_image_base64 = base64.b64encode(buffered_new.getvalue()).decode('utf-8')

            #แสดงผลบน log.html 
            BuiltIn().log(f'''
            <table>
                <tr>
                    <td style="padding-right: 35px;"><h3>Old Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                    <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#11162;</h2></td>
                    <td><h3>New Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                </tr>
            </table>
            ''', html=True)


            return  len(filtered_contours) , filtered_contours
        
        
        
    def highlight_contours_objects(self, image_path , contours, indices):
        """
        ***|    Description     |***
        |   *`Highlight Contours Objects`*   |   ส่ง path รูปภาพ , contours และ indices เพื่อไป highlight object ที่ต้องการตาม indices ที่กำหนด |
 
        ***|    Example     |***
        | *`Highlight Contours Objects`* | image_path = path | contours = data filtered_contours | indices  = [array or list contours]
        | *`Highlight Contours Objects`* | image_path = C/domain/log.png | contours = data filtered_contours | indices  = 0 

        ***|    Parameters     |***
        -  image_path
        -  contours (data filtered_contours ที่ได้จาก keyword : 'Detect And Mask Objects')
        -  indices (array or list ของตัวที่ต้องการ ภายใน data filtered_contours )
 
        *`ทดสอบได้เฉพาะบางหน้าเท่านั้น ค่าบางค่าอาจเอาออกมาไม่ได้เนื่องจากขนาดใหญ่เกินไป`*
        """
        #read image with cv2.imread
        image = cv2.imread(image_path)
        image_old = cv2.imread(image_path)
        indices = [int(indices)]
        # Draw specified contours on the image with different colors
        for index in indices:
            color = (0, 0, 255)
            result_image = cv2.drawContours(image, contours, index, color, 3)

        # Convert image back to PIL format
        image_new_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # result_image.show()

        # แปลงภาพ PIL เป็น base64
        image_old_pil = Image.fromarray(cv2.cvtColor(image_old, cv2.COLOR_BGR2RGB))
        buffered_old = io.BytesIO()
        image_old_pil.save(buffered_old, format="PNG")
        old_image_base64 = base64.b64encode(buffered_old.getvalue()).decode('utf-8')

        buffered_new = io.BytesIO()
        image_new_pil.save(buffered_new, format="PNG")
        new_image_base64 = base64.b64encode(buffered_new.getvalue()).decode('utf-8')

        #แสดงผลบน log.html 
        BuiltIn().log(f'''
            <table>
                <tr>
                    <td style="padding-right: 35px;"><h3>Old Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                    <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#11162;</h2></td>
                    <td><h3>New Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                </tr>
            </table>
        ''', html=True)

        return image_new_pil

    def get_average_bgr_color_within_contour(self, image_path , contour):
        """
        ***|    Description     |***
        |   *`Get Average Bgr Color Within Contour`*   |   ส่ง path รูปภาพ , contours เพื่อไปคำนวณค่าสีเฉลี่ยภายใน contour โดยใช้ mask ค่าที่ได้จะเป็น B , G , R , Alpha|
 
        ***|    Example     |***
        | *`Highlight Contours Objects`* | image_path = C/domain/log.png | contours = contour[0] (เลือกเฉพาะ array contour ที่ต้องการจะส่ง)

        ***|    Parameters     |***
        -  image_path
        -  contours (data filtered_contours ที่ได้จาก Keyword : 'Detect And Mask Objects')

        *`ทดสอบได้เฉพาะบางหน้าเท่านั้น ค่าบางค่าอาจเอาออกมาไม่ได้เนื่องจากขนาดใหญ่เกินไป`*
        """
        #read image with cv2.imread
        image = cv2.imread(image_path)
        image_old = cv2.imread(image_path)
        # สร้าง mask ที่มีขนาดเท่ากับภาพ โดยมีค่าเริ่มต้นเป็นสีดำ (ค่า 0)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        # วาด contour บน mask ด้วยสีขาว
        draw = cv2.drawContours(mask, [contour], -1, (255), thickness=cv2.FILLED)

        # คำนวณค่าสีเฉลี่ยภายใน contour โดยใช้ mask
        mean_color = cv2.mean(image, mask=mask)

        # Convert image back to PIL format
        # result_image = Image.fromarray(cv2.cvtColor(draw, cv2.COLOR_BGR2RGB))
        image_new_pil = Image.fromarray(draw)
        # result_image.show()

        # แปลงภาพ PIL เป็น base64
        image_old_pil = Image.fromarray(cv2.cvtColor(image_old, cv2.COLOR_BGR2RGB))
        buffered_old = io.BytesIO()
        image_old_pil.save(buffered_old, format="PNG")
        old_image_base64 = base64.b64encode(buffered_old.getvalue()).decode('utf-8')

        buffered_new = io.BytesIO()
        image_new_pil.save(buffered_new, format="PNG")
        new_image_base64 = base64.b64encode(buffered_new.getvalue()).decode('utf-8')

        #แสดงผลบน log.html
        BuiltIn().log(f'''
            <table>
                <tr>
                    <td style="padding-right: 35px;"><h3>Old Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                    <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#11162;</h2></td>
                    <td><h3>New Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                </tr>
            </table>
        ''', html=True)

        return mean_color
    
    def convert_bgr_2_rgb(self, average_bgra ):
        """
        ***|    Description     |***
        |   *`Convert Bgr 2 Rgb`*   |   ส่ง averages blue green red alpha เพื่อไปแปลงเป็น numpy array และแปลงจาก BGR เป็น RGB |
 
        ***|    Example     |***
        | *`Convert Bgr 2 Rgb`* | image_path = C/domain/log.png | contours = contour[0] (เลือกเฉพาะ array contour ที่ต้องการจะส่ง)

        ***|    Parameters     |***
        -  average_bgra (ค่า mean สี ที่ได้จาก Keyword : 'Get Average Bgr Color Within Contour')

        *`.....`*
        """
        #ลบค่า alpha ออกจาก list average_bgra
        bgr_values = tuple(list(average_bgra)[:-1])

        # แปลงเป็น numpy array และแปลงจาก BGR เป็น RGB
        #ทำการ reshape array ให้มีขนาด (1, 1, 3) ซึ่งหมายถึงมี 1 แถว, 1 คอลัมน์, และ 3 ช่องสี (BGR)
        average_color_bgr_array = np.array(bgr_values, dtype=np.float32).reshape((1, 1, 3))

        #ใช้ฟังก์ชัน cvtColor ของ OpenCV เพื่อแปลงค่าจากสี BGR เป็นสี RGB
        average_color_rgb_array = cv2.cvtColor(average_color_bgr_array, cv2.COLOR_BGR2RGB)

        #ทำการ flatten array ให้เป็นแถวเดียว (1-dimensional array)
        average_color_rgb = average_color_rgb_array.flatten()

        return  average_color_rgb
    
    def convert_rgb_2_hsv(self, Red , Green , Blue ):
        """
        ***|    Description     |***
        |   *`Convert RGB 2 HSV`*   |   ส่ง Red , Green , Blue เพื่อไปแปลงเป็น เป็น  HSV (โดยค่า rgb สามารถหาได้จากการ
        นำรูปภาพไปเข้าเว็บ rgb Image เพื่อหาสีที่เราต้องการ https://imagecolorpicker.com/th or https://www.ginifab.com/feeds/pms/color_picker_from_image.th.php)

        ***|    Example     |***
        | *`Convert RGB 2 HSV`* | Red = 10 | Green = 10 | Blue = 10

        ***|    Parameters     |***
        -  Red (สีแดง)
        -  Green (สีเขียว)
        -  Blue (สีฟ้า)

        *`.....`*
        """
        # สี RGB
        rgb_color = np.uint8([[[Red, Green, Blue]]])

        # แปลงจาก RGB เป็น HSV
        hsv_color = cv2.cvtColor(rgb_color, cv2.COLOR_RGB2HSV)

        #reshape(-1) จะทำการแปลง array ให้เป็น array หนึ่งมิติ
        hsv_array = hsv_color.reshape(-1)

        h = hsv_array[0]
        s = hsv_array[1]
        v = hsv_array[2]

        hsv_array = [int(h),int(s),int(v)]

        return  hsv_array

    def rgb_2_matplotlib_color_name_and_hex(self, rgb_tuple ):
        """
        ***|    Description     |***
        |   *`Rgb 2 Matplotlib Color Name And Hex`*   |   ส่ง averages red green blue เพื่อไปคำนวณหา ชื่อสี และ ค่า hex ของสีนั้น |
 
        ***|    Example     |***
        | *`Rgb 2 Matplotlib Color Name And Hex`* | rgb_tuple = data rgb  (Ex : [181.69142  240.91144   21.810137])

        ***|    Parameters     |***
        -  rgb_tuple (ค่า mean สี ที่ได้จาก Keyword : 'Get Average Bgr Color Within Contour' และแปลงเป็น rgb ด้วย Keyword : 'convert_bgr_2_rgb')

        *`.....`*
        """
        # Normalize the RGB values to be between 0 and 1 | ปรับค่า RGB ให้เป็นช่วง 0-1 โดยการหารค่าของแต่ละช่องสีด้วย 255 เพื่อทำให้ข้อมูลมีมาตรฐานเดียวกัน ซึ่งช่วยให้การคำนวณระยะทางระหว่างสี
        rgb_normalized = tuple([x / 255.0 for x in rgb_tuple])

        # Find the closest color name and hex |  เป็นการคำนวณระยะทางแบบ Euclidean ระหว่างสีที่ normalized และสี CSS4 แต่ละสี
        closest_name = None
        closest_hex = None
        min_distance = float('inf')
        for name, hex_value in mcolors.CSS4_COLORS.items():
            color_rgb = mcolors.hex2color(hex_value)
            # closest_hex = hex_value
            distance = sum((component1 - component2) ** 2 for component1, component2 in zip(rgb_normalized, color_rgb))
            if distance < min_distance:
                min_distance = distance
                closest_name = name
                closest_hex = hex_value

        #ส่งคืนชื่อสีและค่า hex ของสีที่ใกล้เคียงที่สุด
        return closest_name , closest_hex
    
    def replace_capture_path(self, path ):
        """
        ***|    Description     |***
        |   *`Replace Capture Path`*   |   ส่ง path ที่ได้จากการ capture screen เข้ามา replace \\ เป็น / |
 
        ***|    Example     |***
        | *`Replace Capture Path`* | path = C\domain\log.png 

        ***|    Parameters     |***
        -  path  (ค่า path ที่ได้จาก Keyword : 'Capture Screen ของ AppiumFlutter หรือ Appium')

        *`.....`*
        """
        newpath = path.replace("\\", "/")

        return  newpath
    
    def crop_image(self, left:int, top:int, right:int, bottom:int, image_path: str):
        imgold = Image.open(image_path)
        imgnew = Image.open(image_path)
        crop_img = imgnew.crop((left, top, right, bottom))
        # crop_img.show()
        buffered_old = io.BytesIO()
        imgold.save(buffered_old, format="PNG")
        old_image_base64 = base64.b64encode(buffered_old.getvalue()).decode('utf-8')

        buffered_new = io.BytesIO()
        crop_img.save(buffered_new, format="PNG")
        new_image_base64 = base64.b64encode(buffered_new.getvalue()).decode('utf-8')

        #แสดงผลบน log.html
        BuiltIn().log(f'''
            <table>
                <tr>
                    <td style="padding-right: 35px;"><h3>Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                    <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#61;</h2></td>
                    <td style="padding-left: 35px;"><h3>Crop Image:</h3></td>
                    <td style="text-align: center; vertical-align: middle;"><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                </tr>
            </table>
        ''', html=True)

        return crop_img
    
    def compare_images(self , crop_img , path_img_compare):
        """
        ***|    Description     |***
        |   *`Compare Images`*   |   ส่ง path รูปภาพ crop_img และ path_img_compare,
        เพื่อไปคำนวณค่าความแตกต่างของภาพ โดยหาก np.array ในตั้ง 2 ภาพเท่ากัน จะ pass
 
        ***|    Example     |***
        | *`Compare Images`* | crop_img  | path_img_compare | fail_threshold (default= 5)

        ***|    Parameters     |***
        -  crop_img (img ที่ได้จากการ crop แล้วจาก  def crop_image (type file PIL))
        -  path_img_compare  (path ที่เก็บรูปที่ไว้ตรวจสอบ)

        *`หากทดสอบใน ต่างรุ่นโทรศัพจะ Fail`*
        """
        np_image_crop = np.array(crop_img)
        compare_img = Image.open(path_img_compare)
        np_image_compare = np.array(compare_img)

        #แปลง PIL เป็น base 64 
        buffered_old = io.BytesIO()
        crop_img.save(buffered_old, format="PNG")
        old_image_base64 = base64.b64encode(buffered_old.getvalue()).decode('utf-8')

        buffered_new = io.BytesIO()
        compare_img.save(buffered_new, format="PNG")
        new_image_base64 = base64.b64encode(buffered_new.getvalue()).decode('utf-8')

        # Check if shapes of the two images are same
        if np_image_crop.shape == np_image_compare.shape:
            # Compare pixel by pixel
            if np.array_equal(np_image_crop, np_image_compare):
                BuiltIn().log('The images are exactly the same.')
                BuiltIn().log(f'''
                    <table>
                        <tr>
                            <td style="padding-right: 35px;"><h3>Actual Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                            <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#61;</h2></td>
                            <td><h3>Expect Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                        </tr>
                    </table>
                ''', html=True)
            else:
                BuiltIn().log(f'''
                    <table>
                        <tr>
                            <td style="padding-right: 35px;"><h3>Actual Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                            <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#8800;</h2></td>
                            <td><h3>Expect Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                        </tr>
                    </table>
                ''', html=True)
                BuiltIn().run_keyword('Fail','The images are different.')
        else:
            BuiltIn().log(f'''
                <table>
                    <tr>
                        <td style="padding-right: 35px;"><h3>Actual Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                        <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#8800;</h2></td>
                        <td style="padding-left: 35px;"><h3>Expect Image:</h3></td>
                        <td style="text-align: center; vertical-align: middle;"><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                    </tr>
                </table>
            ''', html=True)
            BuiltIn().run_keyword('Fail','The images have different sizes and cannot be compared directly.')

    def find_fullpath_with_filename(self,filename:str,search_path:str):
        for root, dirs, files in os.walk(search_path):
            if filename in files:
                return os.path.join(root, filename)
        return None

    def save_image_on_directory(self,image,saveonpath):
        #Check isinstance PIL
        if self._is_pil_image(image):
            BuiltIn().log('This is a PIL Image object.')
            BuiltIn().log(f'Size: {image.size}')
            BuiltIn().log(f'Format: {image.format}')
            BuiltIn().log(f'Mode: {image.mode}')
            image.save(saveonpath)
            BuiltIn().log(f'Success Save Image On Path : {saveonpath}')
        else:
            BuiltIn().run_keyword('Fail','This is not a PIL Image object.')

    def compare_images_percent(self , path_img_actual:str , path_img_compare:str ,fail_threshold:int=5):
        """
        ***|    Description     |***
        |   *`Compare Images Percent`*   |   ส่ง path รูปภาพ actual และ compare, fail_threshold ค่าที่ยอมรับ 
        เพื่อไปคำนวณค่าความแตกต่างของภาพ หากค่าที่ได้มากกว่า fail_threshold ที่ให้ไปจะ fail
 
        ***|    Example     |***
        | *`Compare Images Percent`* | path_img_actual  | path_img_compare | fail_threshold (default= 5)

        ***|    Parameters     |***
        -  path_img_compare (path ที่เก็บรูป compare)
        -  path_img_actual  (path ที่เก็บรูปที่จะทดสอบ)
        -  fail_threshold (ค่าที่ยอบรับความต่างภาพ)

        ***|    Doc     |***
        -  difference (ตัวแปรนี้เก็บค่าความแตกต่างของภาพจากฟังก์ชัน cv2.absdiff() ซึ่งคำนวณความแตกต่างแบบแอบโซลูตระหว่างสองภาพ.)
        -  gray_difference (ตัวแปรนี้เก็บภาพความแตกต่างที่ถูกแปลงเป็นภาพสีเทา (cv2.cvtColor()) เพื่อลดความซับซ้อนในการประมวลผลต่อไป.)
        -  threshold_value, thresh  (threshold_value คือค่าเกณฑ์ที่ใช้ในการแยกพิกเซลที่แตกต่างออกจากภาพความแตกต่าง. thresh คือภาพที่ได้จากการใช้เกณฑ์นี้ซึ่งแสดงพิกเซลที่แตกต่างชัดเจน.)
        -  num_diff_pixels (ตัวแปรนี้เก็บจำนวนพิกเซลที่ถูกตัดสินว่าแตกต่างกันอย่างชัดเจนหลังจากใช้เกณฑ์.)
        -  total_pixels, percentage_difference (total_pixels คือจำนวนพิกเซลทั้งหมดใน thresh. percentage_difference คือเปอร์เซ็นต์ของพิกเซลที่แตกต่างกันเมื่อเทียบกับจำนวนพิกเซลทั้งหมด.)
        -  fail_threshold   (เกณฑ์ที่ใช้ตัดสินว่าภาพแตกต่างกันมากเพียงใดจึงจะถือว่าการเปรียบเทียบล้มเหลว.)
        
        *`หากทดสอบใน ต่างรุ่นโทรศัพ อาจเกิด ค่าความแตกต่างของภาพที่มาก`*
        """
        #ใช้สำหรับประมวลตวามต่าง
        image_actual = cv2.imread(path_img_actual)
        image_compare = cv2.imread(path_img_compare)
        

        #ใช้แสดงรูป
        actual_img = Image.open(path_img_actual)
        compare_img = Image.open(path_img_compare)
        #แปลง PIL เป็น base 64 
        buffered_old = io.BytesIO()
        actual_img.save(buffered_old, format="PNG")
        old_image_base64 = base64.b64encode(buffered_old.getvalue()).decode('utf-8')

        buffered_new = io.BytesIO()
        compare_img.save(buffered_new, format="PNG")
        new_image_base64 = base64.b64encode(buffered_new.getvalue()).decode('utf-8')


        # ตรวจสอบขนาดภาพ และปรับให้เท่ากัน
        if image_actual.shape != image_compare.shape:
            # ปรับขนาด image2 ให้เท่ากับ image1
            image_compare = cv2.resize(image_compare, (image_actual.shape[1], image_actual.shape[0]))

        # คำนวณความแตกต่างของภาพ
        difference = cv2.absdiff(image_actual, image_compare)

        # แปลงภาพความแตกต่างเป็นภาพสีเทา
        gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

        # ตั้งค่าความต่างที่ถือว่ายอมรับได้ (เกณฑ์)
        threshold_value = 30  # กำหนดเกณฑ์ความต่างที่ยอมรับได้

        # ทำ threshold เพื่อแยกพิกเซลที่แตกต่างกันอย่างเห็นได้ชัด
        _, thresh = cv2.threshold(gray_difference, threshold_value, 255, cv2.THRESH_BINARY)

        # คำนวณจำนวนพิกเซลที่แตกต่างกัน
        num_diff_pixels = np.count_nonzero(thresh)

        # คำนวณเปอร์เซ็นต์ของพิกเซลที่แตกต่างกัน
        total_pixels = thresh.size
        percentage_difference = (num_diff_pixels / total_pixels) * 100

        fail_thresholdFix = fail_threshold  # เกณฑ์ความแตกต่างที่ยอมรับได้ 5% (defual = 5 %)
        if percentage_difference > fail_thresholdFix:
            BuiltIn().log('Test fail: The image difference is too high.')
            BuiltIn().log(f'''
                    <table>
                        <tr>
                            <td style="padding-right: 35px;"><h3>Actual Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                            <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#8800;</h2></td>
                            <td><h3>Expect Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                        </tr>
                    </table>
            ''', html=True)
            BuiltIn().run_keyword('Fail',f'Percentage difference: {percentage_difference:.2f}% More Than Fail threshold : {fail_thresholdFix:.2f}')
        else:
            BuiltIn().log('Test pass: The images are considered similar.')
            BuiltIn().log(f"Percentage difference: {percentage_difference:.2f}% Less Than Fail threshold : {fail_thresholdFix:.2f}")
            BuiltIn().log(f'''
                    <table>
                        <tr>
                            <td style="padding-right: 35px;"><h3>Actual Image:</h3><img src="data:image/png;base64,{old_image_base64}" width="400px"></td>
                            <td style="padding-right: 35px; text-align: center; vertical-align: middle;"><h2 style="font-size: 125px; color: green;">&#61;</h2></td>
                            <td><h3>Expect Image:</h3><img src="data:image/png;base64,{new_image_base64}" width="400px"></td>
                        </tr>
                    </table>
            ''', html=True)

    #PRIVATE_FUNCTION
    
    def _is_pil_image(self,obj):
            return isinstance(obj, Image.Image)
        

    