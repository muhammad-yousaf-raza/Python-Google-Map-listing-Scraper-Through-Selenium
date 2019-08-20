#!/usr/bin/env python3
from pyvirtualdisplay import Display
from selenium import webdriver
import re
import time


# proxy = "proxy-xxxx-xxx:80"  # HOST

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % proxy)
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(chrome_options=chrome_options)

display = Display(visible=0, size=(800, 600))
display.start()

# ---------------------------------------------------------Browser Object
driver.get('https://www.google.com/maps')
# Write Text in Search Box
search = driver.find_element_by_name('q')
search.send_keys('ZAFAR & ASSOCIATES - LLP')    # --------------------- Insert Text Here
driver.find_element_by_id('searchbox-searchbutton').click()
time.sleep(5)

MapListingUrl = driver.current_url
try:
    # ---------------------------------------------------------Check Listing Claim Status
    ListingClaimStatus = 1
    ClaimListings = driver.find_elements_by_xpath("//span[@class='widget-pane-link']")
    for ClaimListing in ClaimListings:
        if ClaimListing.text == 'Claim this business':
            ListingClaimStatus = 0

    # ---------------------------------------------------------Find Total Reviews
    TotalReviewsString = driver.find_element_by_xpath("//button[@jsaction='pane.rating.moreReviews']").text
    TotalReviewsMatch = re.search(r'(\d+)', TotalReviewsString, re.IGNORECASE)
    TotalReviewsNumber = TotalReviewsMatch.group()
except:
    TotalReviewsNumber = 0
# ---------------------------------------------------------Find Listing Name
try:
    NameListing = driver.find_element_by_tag_name('h1').text
except:
    NameListing = 0
# ---------------------------------------------------------Find Category
try:
    CategoryString = driver.find_element_by_xpath("//button[@jsaction='pane.rating.category']").text
except:
    CategoryString = 0
# ---------------------------------------------------------Find Rating
try:
    ListingRating = driver.find_element_by_xpath("//span[@class='section-star-display']").text
except:
    ListingRating = 0
# ---------------------------------------------------------Find Website
try:
    ListingWebsite = driver.find_element_by_xpath(
        "//div[@data-section-id='ap']").text
except:
    ListingWebsite = 0
# ---------------------------------------------------------Find Address
try:
    ListingAddress = driver.find_element_by_xpath(
        "//div[@data-section-id='ad']").text
except:
    ListingAddress = 0
# ---------------------------------------------------------Find Phone
try:
    ListingPhone = driver.find_element_by_xpath(
        "//div[@data-section-id='pn0']").text
except:
    ListingPhone = 0
# ---------------------------------------------------------Find Hours
try:
    ListingHours = driver.find_element_by_xpath(
        '//div[@class="section-open-hours-container section-open-hours-container-hoverable"]').\
        get_attribute("aria-label")
except:
    ListingHours = 0

if ListingHours:
    ListingHours = 1
# ---------------------------------------------------------Find Photos
try:
    ListingPhotos = driver.find_element_by_xpath('//div[@class="section-image-pack-item-2"]').text
    ListingPhotos = re.findall('\d+', ListingPhotos)
    ListingPhotos = ListingPhotos[0]
except:
    ListingPhotos = 0
# ---------------------------------------------------------Extract Reviews
if int(TotalReviewsNumber) > 0:
    # Click On Button Load Reviews
    ButtonTotalReviews = driver.find_element_by_xpath("//button[@jsaction='pane.reviewChart.moreReviews']")
    ButtonTotalReviews.click()
    time.sleep(2)
    try:
        # Scrol Page to Bottom
        scr1 = driver.find_element_by_class_name('section-scrollbox')
        for x in range(1, int(TotalReviewsNumber), 8):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
            time.sleep(2)
    except:
        scr1 = 0
    # Extract Reviews Link
    MapListingUrl = driver.current_url
    # Extract Reviews
    ReviewsList = []
    article_elements = driver.find_elements_by_class_name('section-review')
    ReviewsList = [{
        'author': article.find_element_by_xpath('.//div[@class="section-review-title"]/span').text,
        'date': article.find_element_by_xpath('.//span[@class="section-review-publish-date"]').text,
        'rating': article.find_element_by_xpath('.//span[@class="section-review-stars"]').get_attribute(
            "aria-label"),
    } for article in article_elements]
else:
    ReviewsList = []

# Print Results
print('Claim Status: ' + str(ListingClaimStatus))
print('Total Reviews: ' + str(TotalReviewsNumber))
print('Name Listing: ' + str(NameListing))
print('Category: ' + str(CategoryString))
print('Rating: ' + str(ListingRating))
print('Website: ' + str(ListingWebsite))
print('Address: ' + str(ListingAddress))
print('Phone: ' + str(ListingPhone))
print('Hours: ' + str(ListingHours))
print('Photos: ' + str(ListingPhotos))
print('Reviews:')
print(ReviewsList)

# Close Browser and Disconnect DB
driver.close()


