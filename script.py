
import platform
import subprocess
from subprocess import DEVNULL, STDOUT
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import numpy as np
import scipy.interpolate as si
from time import sleep


def main(keywordSearch):
    try:
        print(f'running...')

        if platform.system() == 'Linux':
            subprocess.call(['sudo', 'service', 'tor', 'restart'],
                            stdout=DEVNULL, stderr=STDOUT)
            driverBinary = r'./webDriverLinux'

        if platform.system() == 'Darwin':
            subprocess.call(['brew', 'services', 'restart', 'tor'],
                            stdout=DEVNULL, stderr=STDOUT)
            driverBinary = r'./webDriverMac'

        fp = webdriver.FirefoxProfile()
        fp.set_preference('network.proxy.type', 1)
        fp.set_preference('network.proxy.socks', '127.0.0.1')
        fp.set_preference('network.proxy.socks_port', 9050)
        fp.set_preference('network.proxy.socks_version', 5)

        options = Options()
        options.headless = True

        driver = webdriver.Firefox(
            firefox_profile=fp, options=options, executable_path=driverBinary)

        driver.get('https://google.com')

        if 'sorry' in driver.current_url:
            returnDetails = driver.find_element_by_xpath(
                '/html/body/div[1]/div').text
            ip = returnDetails[returnDetails.find('IP address: '):returnDetails.find(
                'Time:', returnDetails.find('IP address: '))][13:]
            print(f'bad ip: {ip}')
            driver.quit()
            main(keywordSearch)

        inputElement = driver.find_element_by_xpath(
            '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

        inputElement.send_keys(keywordSearch)
        inputElement.send_keys(Keys.ENTER)

        points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]

        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=3)
        y_tup = si.splrep(t, y, k=3)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)
        y_i = si.splev(ipl_t, y_list)

        action = ActionChains(driver)
        sleep(5)
        startElement = driver.find_element_by_id('hdtb-msb-vis')

        action.move_to_element(startElement)
        action.perform()

        moves = 0

        for mouse_x, mouse_y in zip(x_i, y_i):
            action.move_by_offset(mouse_x, mouse_y)
            action.perform()
            sleep(mouse_x+mouse_y)
            moves += 1
            if moves == 4:
                break

        ad = driver.find_element_by_class_name('V0MxL')
        ad.click()
        print('click')
        driver.quit()

    except Exception as e:
        driver.quit()
        print(e)


if __name__ == '__main__':
    keywordSearch = input("enter search keyword:")
    while True:
        main(keywordSearch)
