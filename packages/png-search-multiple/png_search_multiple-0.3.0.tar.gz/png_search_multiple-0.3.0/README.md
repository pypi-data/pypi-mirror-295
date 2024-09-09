SearchPng Python Library
-----------------------------------------
This is a python library to search for a png image file within a target png image file.

Description
------------
This library allows python users to find the location of images in pixel coordinates.
Originally the purpose of the library was to mitigate problems in test automation where control recognition does not work.


Functions:
---------------
Find Bitmap Image
-----------------------
find_bitmap_image is a function that will find one image match and return a list representing a 
location of the found image.

	ret_rectangle = find_bitmap_image(target_png, search_for_png)

where ... 

target_png: The filename of the png we want to search in (typically a screenshot).
search_for_png: The filename of the png we want to search for in target_png (often an icon).
ret_rectangle: Return value is a list with 4 items.  These items are the pixel coordinate of the search image within the target image.

		For Example the return value will be formatted.
		[top_left_x, top__left_y, bottom_right_x, bottom_right_y]



A Code Example:

    import search_png.search_png as sp

    (...)

    input_image = ".\\test_images\\testmap.png"  # main image of the map
    test_number_list = [".\\test_images\\test_14.png",  # clip of number 14 -- FORMAT FILENAME like ..._15.png
                        ".\\test_images\\test_2.png",   # clip of the number 2 -- watch for match on 20
                        ".\\test_images\\test_4.png",   # clip of the number 4
                        ".\\test_images\\test_5.png"    # clip of the number 5
                        ]
    test_img = Image.open(input_image)
    output = "{\n"
    for number_image in test_number_list:
        rectangle = sp.find_bitmap_image(input_image, number_image)  # search for one pindrop comment out
        output += "\"" + number_image.split("_")[-1].replace(".png", "") + "\": " + str(rectangle) + ",\n"
        img1 = ImageDraw.Draw(test_img)
        img1.rectangle(rectangle, outline="blue", width=3)
    output += "}\n"
    output = output[::-1].replace(",", "", 1)[::-1]  # replace last comma
    test_img.show()         # this will show in windows -- COMMENT THIS OUT IN PRODUCTION
    sleep(1)
    test_img.save(".\\test_images\\result_find_red_numbers.png")
    return output


Find N Number Bitmap Images
-----------------------------------
find_n_number_bitmap_image is a function that will find up to a number of png images and return a list of 
	rectangles for all target png images found.

	ret_rectangle = find_n_number_bitmap_image(target_image, search_for_image, occurances)

where ...

target_image: The target image often the screenshot
search_for_image: The image we want to find in the target
occurances: The number of ocurrances we expected to find. For instance if 20 then 
	return no more than 20 rectangles identifying where the image is.
ret_rectangle: Return value is a list in which each item is a list of 4 coordinates.  These coordinate represent the pixel rectangle within the target image.

	For Example the return value will be formatted.
	[[top_left_x, top__left_y, bottom_right_x, bottom_right_y], [top_left_x, top__left_y, bottom_right_x, bottom_right_y]]


A Code Example:

    import search_png.search_png as sp

    (...)

    input_image = ".\\test_images\\tigers_test_horizontalsearch.png"  # main image of the map
    tigers_eye = ".\\test_images\\tigers_eye.png"  # this file represents attempt to find all images within the png.
    rlist_tiger_eyes = sp.find_n_number_bitmap_image(input_image, tigers_eye, 50)
    test_img = Image.open(input_image)
    img1 = ImageDraw.Draw(test_img)
    for rlist in rlist_tiger_eyes:
        img1.rectangle(rlist, outline="red", width=3)
        print(rlist)
    test_img.save(".\\test_images\\result_find_many_tiger_eyes.png")
    sleep(1)
    test_img.show()
    return rlist_tiger_eyes

