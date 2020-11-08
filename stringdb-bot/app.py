import os
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

PATH = "chromedriver.exe"
gene_file = open('genes.txt', 'r')
GENES = gene_file.read().split('\n')

for gene in GENES:

    driver = webdriver.Chrome(PATH)

    driver.get("https://string-db.org/cgi/input.pl?input_page_show_search=on")

    print(f">>> searching {gene}")
    # Get the search box
    search = driver.find_element_by_id("primary_input:single_identifier")
    # Type the gene name and hit ENTER
    search.send_keys(gene)
    search.send_keys(Keys.RETURN)
    # Emulate clicking the "continue" button
    driver.execute_script("javascript:document.getElementById('proceed_form').submit();")
    print(f">>> done searching {gene}")

    print(">>> switching to settings tab")
    settings_tab = driver.find_element_by_id("bottom_page_selector_settings")
    settings_tab.click()
    print(">>> done switching to settings tab")

    print(">>> changing settings")

    # Select confidence interval
    confidence_dropdown = Select(driver.find_element_by_id("score_select"))
    confidence_dropdown.select_by_visible_text("high confidence (0.700)")

    # Select interactors limit
    interactors_dropdown = Select(driver.find_element_by_id("limit_select"))
    interactors_dropdown.select_by_visible_text("no more than 50 interactors")

    # Uncheck neighborhood
    if(driver.find_element_by_id("channel1").get_attribute("checked")): 
        driver.find_element_by_name("channel1").send_keys(Keys.SPACE)

    # Uncheck gene fusion
    if(driver.find_element_by_id("channel2").get_attribute("checked")): 
        driver.find_element_by_name("channel2").send_keys(Keys.SPACE)

    # Uncheck co occurence
    if(driver.find_element_by_id("channel3").get_attribute("checked")): 
        driver.find_element_by_name("channel3").send_keys(Keys.SPACE)

    # Uncheck co expression
    if(driver.find_element_by_id("channel4").get_attribute("checked")): 
        driver.find_element_by_name("channel4").send_keys(Keys.SPACE)

    # Uncheck text mining
    if(driver.find_element_by_id("channel7").get_attribute("checked")): 
        driver.find_element_by_name("channel7").send_keys(Keys.SPACE)

    # Apply the settings
    driver.execute_script("javascript:document.getElementById('standard_parameters').submit();")
    print(">>> done changing settings")

    print(">>> switching to export tab")
    export_tab = driver.find_element_by_id("bottom_page_selector_table")
    export_tab.click()
    print(">>> done switching to export tab")

    # Get all the download links
    print(">>> starting download")
    download_links = driver.find_elements_by_link_text("download")
    link_of_interest = ''

    # Get the download link we are interested in
    for html_element in download_links:
        if("string_network_coordinates.txt" in html_element.get_attribute('href')):
            link_of_interest = html_element.get_attribute('href')
            break
    
    # Create a directory for the gene
    if(not os.path.exists(gene)):
        os.mkdir(gene)

    # Save the download in the gene directory
    r = requests.get(link_of_interest, allow_redirects=True)
    open(f"{gene}/string_network_coordinates.txt", "wb").write(r.content)
    print(f">>> done downloading {gene} data")
    print("\n\n")

    driver.quit()
