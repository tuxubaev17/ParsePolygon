from selenium import webdriver
from PIL import Image
import time
import numpy as np
import cv2 as cv

chromedriver = '/Users/alikhantuxubayev/Desktop/work/ParsePolygon/chromedriver'
link = 'https://yandex.kz/maps'
browser = webdriver.Chrome(executable_path=chromedriver)


def ruller_coord():
    ruller_coord = browser.current_url.rsplit('rl=', 1)[-1]
    filter = ruller_coord[::-1].rsplit('lls&', 1)[1].replace('C2%', ' ').replace('~', ' ')
    coord_list = filter[::-1].split(' ')
    froms = float(coord_list[1]), float(coord_list[0])
    to = float(coord_list[3]), float(coord_list[2])
    print(froms, to)

    return to


def ruller_draw():
    path = browser.find_element_by_css_selector("div.search-placemark-icons__active > svg > g > path:nth-child(3)")
    path_location = path.location
    path_location_list = list(path_location.values())
    aOffset = path_location_list[0]
    bOffset = path_location_list[1]
    xOffset = 30
    yOffset = 30
    actions = webdriver.common.action_chains.ActionChains(browser)
    draw = actions.move_by_offset(aOffset, bOffset).click().move_by_offset(xOffset, yOffset).click().perform()

    return draw


def draw_point():
    im = Image.open("screens/output.png")
    rgb_im = im.convert('RGB')
    pixels = rgb_im.load()
    color = rgb_im.getcolors()

    magneta = (255, 0, 255)
    navy = (0, 0, 128)
    path = (254, 0, 0)
    border_black = (0, 0, 0)

    rull_points = []
    for x in range(rgb_im.size[1]):
        for y in range(rgb_im.size[0]):
            if pixels[y, x] == navy:
                coords = y, x
                npcoords = np.array(coords)
                rull_points.append(npcoords)

    list_from_x = rull_points[10]
    list_to_y = rull_points[::-1][10]

    rgb_im.putpixel(list_from_x, path)
    rgb_im.putpixel(list_to_y, magneta)
    rgb_im.save('screens/main.png')

    return list_from_x, list_to_y


def corners():
    img = cv.imread('screens/clear.png')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    corners = cv.goodFeaturesToTrack(gray, 100, 0.09, 10)
    corners = np.int0(corners)

    corners_list = []
    for corner in corners:
        x, y = corner.ravel()
        cv.circle(img, (x, y), 3, [0, 150, 0], -1)

    for i in range(1, len(corners)):
        corners_list.append(corners[i])

    cv.imwrite('screens/good_featurs.png', img)

    return corners_list


def polygon_coord():
    point3_coords = corners()
    for i in point3_coords:
        point3 = i
        from_x, to_y = draw_point()
        x = to_y[0] - from_x[0]
        y = to_y[1] - from_x[1]
        x1 = point3[0][0] - from_x[0]
        y1 = point3[0][1] - from_x[1]
        to_coord = ruller_coord()
        res_x = to_coord[0] / y
        res_y = to_coord[1] / x
        x_coord = str(res_x * y1)
        y_coord = str(res_y * x1)

        print(y_coord[:9], x_coord[:9])


def clear_img():
    im = Image.open("screens/main.png")
    rgb_im = im.convert('RGB')
    pixels = rgb_im.load()
    color = rgb_im.getcolors()

    magneta = (255, 0, 255)
    navy = (0, 0, 128)
    path = (254, 0, 0)
    border_black = (0, 0, 0)

    for x in range(rgb_im.size[1]):
        for y in range(rgb_im.size[0]):
            coords = y, x
            if pixels[coords] == navy or pixels[coords] == magneta or pixels[coords] == path:
                rgb_im.putpixel(coords, (255, 255, 255))

    rgb_im.save('screens/clear.png')

    return rgb_im


def open_browser(url):
    browser.get(url)
    browser.implicitly_wait(5)


def get_location():
    open_browser(link)
    locate = str(input("location: "))
    search = browser.find_element_by_xpath('//input[@placeholder="Поиск мест и адресов"]').send_keys(locate)
    browser.implicitly_wait(2)
    button = browser.find_element_by_css_selector('._type_search').click()
    ruler = browser.find_element_by_class_name("map-ruler-control").click()
    time.sleep(10)
    ruller_draw()
    time.sleep(5)
    ruler_balloon = browser.find_element_by_class_name("ruler-balloon__label").text
    zoom = browser.current_url.rsplit('=', 1)[-1]
    coordinates = browser.find_element_by_class_name('clipboard__content').text
    time.sleep(3)


def take_screen():
    get_location()
    title_script = 'document.styleSheets[0].insertRule(".search-placemark-view__title {display: none;}", 0 )'
    marker_script = 'document.styleSheets[0].insertRule("div.search-placemark-icons__active > svg > g > g > use:nth-child(2) {display: none;}", 0 )'
    marker2_script = 'document.styleSheets[0].insertRule("div.search-placemark-icons__active > svg > g > g > use:nth-child(1) {display: none;}", 0 )'
    marker3_script = 'document.styleSheets[0].insertRule("div.search-placemark-view__icon > div > div > div:nth-child(2) > div {display: none;}", 0 )'
    border_script = 'document.styleSheets[0].insertRule("g > g > path {stroke: #0301A0;}", 0 )'
    border_capacity_script = 'document.styleSheets[0].insertRule("g > g > path {stroke-opacity: 400;}", 0 )'
    searcher = 'document.styleSheets[0].insertRule(".search-dock-view {display: none;}", 0 )'
    lang = 'document.styleSheets[0].insertRule(".map-controls-view__lang-layout {display: none;}", 0 )'
    logo = 'document.styleSheets[0].insertRule(".map-controls-view__logo-layout {display: none;}", 0 )'
    ruller_view_point = 'document.styleSheets[0].insertRule(".ruler-view__point {background: #FF4500;}", 0 )'
    time.sleep(4)

    scripts = [title_script, marker_script, marker2_script, marker3_script, border_script,
               border_capacity_script, searcher, lang, logo, ruller_view_point]

    for script in scripts:
        browser.execute_script(script)

    element = browser.find_element_by_tag_name('ymaps')
    element.screenshot("screens/screenshot.png")

    time.sleep(3)


def location_rendering():
    im = Image.open("screens/screenshot.png").convert("RGB")
    im = im.convert("P")
    im2 = Image.new("P", im.size, 255)

    NAVY = (0, 0, 128)
    BLACK = (0, 0, 0)

    rul = [21]
    border = [118, 125, 161, 154]

    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            for j in border:
                if pix == j:
                    im2.putpixel((y, x), BLACK)
            for k in rul:
                if pix == k:
                    im2.putpixel((y, x), NAVY)

    im2.save('screens/output.png')
    polygon_coord()
    browser.quit()
    clear_img()


take_screen()
location_rendering()
