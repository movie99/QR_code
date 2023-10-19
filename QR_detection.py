"""
this code is the backend for getting length and for qr detection

"""
import json
import ast
import csv

def create_csv():
    if not os.path.exists(current_default["set_data_file_name"]+".csv"):
        # file does not exist, so create it
        with open(current_default["set_data_file_name"]+".csv", 'w', encoding='UTF8',  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(current_default['data_header'])
            #return


def write_data(filename, data):
    # Check file extension
    extension = filename.split(".")[-1]

    if extension == "json":
        with open(filename, "w") as f:
            json.dump(data, f)
    elif extension == "csv":
        # Convert data to a string if it's not already
        if not isinstance(data, str):
            data = str(data)
        
        # Parse the string to a list using ast.literal_eval
        my_data = ast.literal_eval(data)
        
        # Write data to a CSV file
        with open(filename, "a", encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(my_data)
    else:
        print("Unsupported file extension")




def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def calculate_distances_and_save_to_csv(data, output_file):
    #global counter
    # Create a dictionary to map numbers to letters
    
    #data = data['0']
    data[str(count)].pop("Dont_Display_Num")
    print('data',data)
    number_to_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}
    distances = []
    #current_default['data_format']
    data_list = ast.literal_eval(current_default['data_format'])
   
    for key1, values1 in data.items():
        for key2, points2 in values1.items():
            for key3, points3 in values1.items():
                if key2 < key3:
                    tag1 = f"1{number_to_letter[int(key2)]}"
                    tag2 = f"1{number_to_letter[int(key3)]}"
                    distance = calculate_distance(points2, points3)
                    
                    # Convert pixels to actual measurements
                    #pixels_to_cm_ratio = pixels_to_cm_ratio / length_in_pexels
                    calculated_distance_cm = distance * length_in_pexels
                    distances.append([data_list[0], count, data_list[2], tag1, tag2, f"{calculated_distance_cm:.0f}"])
    #print(output_file)
    # Save the distances to a CSV file
    file_exists = os.path.isfile(output_file)

    with open(output_file, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if not file_exists:
            csvwriter.writerow(['Control', 'Snapshot', 'date', 'Source Key', 'Target Key', 'Distance'])
        csvwriter.writerows(distances)

    print(f"Distances saved to '{output_file}'.")




    #this draw the tags and even save it to the Final_All_data_saved
def draw_tags( image,tags):          
    #global Current_ALL_data_saved , all_data_entry , Final_All_data_saved
    global Final_All_data_saved 
    #if count < 0:
    #    count = 0

    t = datetime.now()

    families = current_default['qr_family']['Option'][current_default["qr_family"]['Option_Num']]

    for tag in tags:
        #this will remove the tags if pressed buttons and will distaply any manual pressed
        if str(tag.tag_id) in str(Final_All_data_saved[str(count)]["Dont_Display_Num"]):

            continue

        if tag.tag_id > 10:
            #print("Condition met for tag:", tag)
            return image

        # Do something here if the condition is met
        tag_family = tag.tag_family
        tag_id = tag.tag_id
        center = tag.center
        corners = tag.corners
        center = (int(center[0]), int(center[1]))
        corner_01 = (int(corners[0][0]), int(corners[0][1]))
        corner_02 = (int(corners[1][0]), int(corners[1][1]))

        corner_03 = (int(corners[2][0]), int(corners[2][1]))

        corner_04 = (int(corners[3][0]), int(corners[3][1]))

        cv2.circle(image, (center[0], center[1]), 5, (0, 0, 255), 2)

        cv2.line(image, (corner_01[0], corner_01[1]),(corner_02[0], corner_02[1]), (255, 0, 0), 2)

        cv2.line(image, (corner_02[0], corner_02[1]),(corner_03[0], corner_03[1]), (255, 0, 0), 2)

        cv2.line(image, (corner_03[0], corner_03[1]),(corner_04[0], corner_04[1]), (0, 255, 0), 2)

        cv2.line(image, (corner_04[0], corner_04[1]),(corner_01[0], corner_01[1]), (0, 255, 0), 2)

        # Define text string to display

        #text = str(tag_family) + ':' + str(tag_id) + ' (' + str(center[0]) + ',' + str(center[1]) + ')'
        text = str(tag_id) + ' (' + str(center[0]) + ',' + str(center[1]) + ')'

        # Display text with larger font size and thicker stroke

        font = cv2.FONT_HERSHEY_SIMPLEX

        font_scale = 3

        thickness = 10

        #print(tag_id)

        #color = (0, 255, 0)

        color = change_color(tag_id, current_default["qr_color"])

        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)

        cv2.putText(image, text, (corner_01[0], corner_01[1] - 10 - text_size[1]), font, font_scale, color, thickness, cv2.LINE_AA)


        width = abs(corner_01[0] - corner_02[0])

        height = abs(corner_01[1] - corner_04[1])

        #print("Final_All_data_saved", Final_All_data_saved[])
        Final_All_data_saved[str(count)][str(tag_id)] = [center[0], center[1]]
    #this will display the manual numbers
    for number in Final_All_data_saved[str(count)]["Dont_Display_Num"]:        
        #loop thour each dont Display num and chow the draw circles if placed manully
        if number in Final_All_data_saved[str(count)]:
            Manual_cordinates = Final_All_data_saved[str(count)][str(number)]
            x = Manual_cordinates[0]
            y = Manual_cordinates[1]
            current_color = change_color(int(number), current_default["qr_color"])
            cv2.circle(image, (x, y), 25, current_color, 2)
            cv2.putText(image, f"({number} {x}, {y})", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 3, current_color, 10)
            #print("this is going throuth",x,y , number)



    return image 




# Callback function to handle mouse events
#draw circle is the manual way of placing the objects
def draw_circle(image, event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Draw a completely hollow circle with a smaller radius
        outer_radius = 40
        #New_tuple = [int(current_circle[0] * current_default["size_reduced"]), int(current_circle[1] * current_default['size_reduced'])]
        New_tuple = [int(x * current_default["size_reduced"]), int(y * current_default['size_reduced'])]
        
        current_button_pressed = Final_All_data_saved[str(count)]["Dont_Display_Num"][-1] 
        Final_All_data_saved[str(count)][current_button_pressed] = New_tuple


#make this a local function
#pixels_to_cm_ratio = None
#can make it work were exit the entire loop and redoing it bases on user input
#this draw the line to get the distance of the object
drawing = False
pt1 = (-1, -1)
pt2 = (-1, -1)
pixels_to_cm_ratio = 0.0
def draw_line(event, x, y, flags, img):
    #global drawing, pt1, pt2, original_img , distance , finished_line, current_num_pressed , pixels_to_cm_ratio
    global drawing, pt1, pt2, pixels_to_cm_ratio , length_in_pexels
    frame_height, frame_width, _ = img.shape
    if event == cv2.EVENT_LBUTTONDOWN:
        if not drawing:
            pt1 = (x, y)
            drawing = True
            original_img = img.copy()  # Store a copy of the original image
        else:
            pt2 = (x, y)
            drawing = False
            line_pt1 = (int(pt1[0] * current_default["size_reduced"]), int(pt1[1] * current_default["size_reduced"]))
            line_pt2 = (int(pt2[0] * current_default["size_reduced"]), int(pt2[1] * current_default["size_reduced"]))
            cv2.line(img, line_pt1, line_pt2, (0, 0, 255), 5)
            cv2.circle(img, line_pt1, 20, (255, 0, 0), 4)
            cv2.circle(img, line_pt2, 20, (255, 0, 0), 4)
            # Measurement prompt
            cv2image_resized = cv2.resize(img, (int(frame_width/int(current_default["size_reduced"])), int(frame_height/int(current_default['size_reduced']))))
            cv2.imshow('AprilTag Detect Demo', cv2image_resized)
            result = simpledialog.askfloat("Measurement", "Enter the measurement in centimeters:")
            if result is not None:
                pt1 = line_pt1
                pt2 = line_pt2
                pixels_to_cm_ratio = result
                midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)  # Calculate midpoint using original coordinates
                cv2.putText(img, f"{pixels_to_cm_ratio:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                drawing = True
                length_in_pexels = ((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2) ** 0.5
                length_in_pexels = result / length_in_pexels
                print("length_in_pexels",length_in_pexels)
            else:
                drawing = False

Current_ALL_data_saved= None


#selectroi in opencv2
#also create a line in opencv2
# Function to start the video capture and display it in a frame
def start_video_feed(files):
    global clicked_skipped_button
    global clicked_Undo_button
    global Final_All_data_saved
    global stop_ui_thread_flag 
    #this keep track of the next and undo presses
    global count
    #this keep track of the frams
    global Next_Frames_Capture

    if len(files) == 0:
        #if video_window == None:
            #return
        #video_window.destroy()
        return

    File = files.pop(0)

    at_detector = Detector(
            families=current_default['qr_family']['Option'][current_default["qr_family"]['Option_Num']],

            nthreads=int(current_default["nthreads"]),

            quad_decimate=float(current_default["quad_decimate"]),

            quad_sigma=float(current_default["quad_sigma"]),

            refine_edges=int(current_default["refine_edges"]),

            decode_sharpening=float(current_default["decode_sharpening"]),

            debug=int(current_default["debug"]),    )

    # Open the video feed

    cap = cv2.VideoCapture(File)

    file_name = os.path.splitext(os.path.basename(File))[0]


    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create a VideoCapture object to capture frames from the webcam

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the video length in seconds
    video_length = total_frames / fps

    video_length = round(video_length / current_default["skip_sec"], 2)

    ret, image = cap.read()
    copy_image = copy.deepcopy(image)

    cv2.namedWindow('AprilTag Detect Demo')
    cv2.setMouseCallback('AprilTag Detect Demo', draw_line, image)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    #print("Frames per second:", fps)

    

    while True:
        # Resize the debug image
        cv2image_resized = cv2.resize(image, (int(frame_width/int(current_default["size_reduced"])), int(frame_height/int(current_default['size_reduced']))))
        
        cv2.imshow('AprilTag Detect Demo', cv2image_resized)
        key = cv2.waitKey(1) & 0xFF
     
        if pixels_to_cm_ratio > 0.0:  # Check if distance is greater than 0.0
            #print("Distance is greater than 0.0. Exiting loop.")
            break
        if key == 27:  # Esc key
            break


    cv2.destroyAllWindows()


    #whow the new ui design in new thread 
    video_thread = threading.Thread(target=UI_video_feed,args=(fps,))
    video_thread.start()

    cv2.namedWindow("AprilTag Detect Demo")

    callback_with_image = partial(draw_circle, image)

    cv2.setMouseCallback("AprilTag Detect Demo", callback_with_image)

       # this creats a key for every frames of the video 
    frame_time = 0
    #print("video_length",video_length+1)
    for i in range(int(video_length)+1):
        Final_All_data_saved[str(i)] = {}  # Create a dictionary for each frame time
        Final_All_data_saved[str(i)]["Dont_Display_Num"] = []

   # return 

    New_tuple = None
    while pixels_to_cm_ratio > 0.0:
        ret, image = cap.read()
        if ret:
            if clicked_skipped_button == True:
                #count = int(cap.get(cv2.CAP_PROP_POS_FRAMES) + current_default["skip_sec"] * cap.get(cv2.CAP_PROP_FPS))
                Next_Frames_Capture = int(cap.get(cv2.CAP_PROP_POS_FRAMES) + current_default["skip_sec"] * cap.get(cv2.CAP_PROP_FPS))
                cap.set(cv2.CAP_PROP_POS_FRAMES, Next_Frames_Capture)
                clicked_skipped_button = False
                current_circle = None
                print("Next_Frames_Capture",Next_Frames_Capture)
                count = count + 1

            if clicked_Undo_button == True:
                Next_Frames_Capture = int(Next_Frames_Capture - (current_default["skip_sec"] * cap.get(cv2.CAP_PROP_FPS)))
                cap.set(cv2.CAP_PROP_POS_FRAMES, Next_Frames_Capture)
                clicked_Undo_button = False
                print("Next_Frames_Capture",Next_Frames_Capture)
                count  = count - 1

            # this is causing to be slow 
            cap.set(cv2.CAP_PROP_POS_FRAMES, Next_Frames_Capture)

            debug_image = copy.deepcopy(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            tags = at_detector.detect(
                image,
                estimate_tag_pose=False,
                camera_params=None,
                tag_size=None,
            )

            print("count",count)
            if count == int(video_length)+1:
                print("completee Final_All_data_saved",Final_All_data_saved)
                 # Loop through each key in the data and call the function
                for key, value in Final_All_data_saved.items():
                    #print("count",count)
                    count = key
                    calculate_distances_and_save_to_csv({key: value}, current_default["set_data_file_name"]+".csv")
                cv2.destroyAllWindows()
                break


            debug_image = draw_tags(debug_image, tags)
            key = cv.waitKey(1)

            if key == 27:  # ESC
                break

            #print("drawing", drawing)
            #drawing var should be remove or replace for drawline return
            if drawing:
                cv2.line(debug_image, pt1, pt2, (0, 0, 255), 5)
                midpoint = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2) 
                cv2.putText(debug_image, f"{pixels_to_cm_ratio:.2f} cm", midpoint, cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 10)
                cv2.circle(debug_image, pt1, 20, (255, 0, 0), 4)
                cv2.circle(debug_image, pt2, 20, (255, 0, 0), 4)

                    

            cv2image_resized = cv2.resize(debug_image, (int(frame_width/int(current_default["size_reduced"])), int(frame_height/int(current_default['size_reduced']))))
            cv2.imshow('AprilTag Detect Demo', cv2image_resized)
       
        else:
            cv2.destroyAllWindows()
            break

            #if count == 6:
                 

        """
        #close the video if there is no data frames
        else:
            if counter == 6:
                print("completee Final_All_data_saved",Final_All_data_saved)
                # Loop through each key in the data and call the function
                for key, value in Final_All_data_saved.items():
                    print("count",count)
                    counter = key
                    calculate_distances_and_save_to_csv({key: value}, current_default["set_data_file_name"]+".csv")

            cv2.destroyAllWindows()
            break
    """
    cv2.destroyAllWindows()


    return 