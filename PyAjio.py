import csv
import os

file_to_load = os.path.join("Resources", "Ajio Fasion Clothing.csv")
file_to_save = os.path.join("analysis", "Ajio_analysis.txt")

#set containing all unique product ids
id_set = set()

#keeps track of number of sales
total_sales = 0

# function that converts from Indian Rupees to USD
def rupess_to_USD(rup):
    return 0.013 * rup

#encode with latin-1 due to nature of csv file
with open(file_to_load,encoding='latin-1') as file:

    file_reader = csv.reader(file)
    
    #skip header and store it as a list
    header = next(file_reader)

    # find index for each column of interest
    product_id_index = header.index('Id_Product')
    brand_index = header.index("Brand")
    color_index = header.index("Color")
    discount_price_index = header.index("Discount Price (in Rs.)")
    original_price_index = header.index("Original Price (in Rs.)")
    gender_index = header.index("Category_by_gender")

    # make lists containing each value for given column
    # note that prices are in Indian Rupees (INR)
    product_id_list = list()
    brand_list = list()
    color_list = list()
    discount_price_list = list()
    original_price_list = list()
    percent_off_list = list()
    gender_dict = {"Men": 0, "Women": 0}
    womens_price = list()
    mens_price = list()

    #add each product id to list
    for row in file_reader:
        
        #each row is one sale
        total_sales += 1

        # find relevant values
        prod_id = int(row[product_id_index])
        brand = row[brand_index]
        color = row[color_index]
        discount = int(row[discount_price_index].replace(',',''))
        original = int(row[original_price_index].replace(',',''))
        percent_off = int(round((original - discount) / original * 100,0))

        # add values to list
        product_id_list.append(prod_id)
        brand_list.append(brand)
        color_list.append(color)
        discount_price_list.append(discount)
        original_price_list.append(original)
        percent_off_list.append(percent_off)

        if row[gender_index] == "Men":
            gender_dict["Men"] += 1
            mens_price.append(discount)
        else:
            gender_dict["Women"] += 1
            womens_price.append(discount)       

#convert lists to sets
product_id_set = set(product_id_list)
brand_set = set(brand_list)
color_set = set(color_list)
discount_price_set = set(discount_price_list)
original_price_set = set(original_price_list)

# length of list and set are the same for product id, meaning each product is unique
# print("Length of id_list:",len(product_id_list))
# print("Length of id_set:",len(product_id_set))

# 1,975 different brands
# print("Length of brand list is:", len(brand_list))
# print("Length of brand set is:", len(brand_set))

num_colors = f"Number of colors: {len(color_set)}"
print(num_colors)

# print(percent_off_list[:10])

# function returns dictionary containing each brand and number of sales
def val_counts(category):

    # sort list
    # find length of list
    # for each index, if the list(index) = list(index+1) then add 1 to a counter

    #index of first and last element in brand_list
    rowStart = 0
    rowEnd = len(category) - 1

    # dictionary with brands as keys and number of sales as values
    number_of_sales_dict = dict()
    
    #sort the brands list
    category.sort()
    
    number_of_sales = 1

    for i in range(rowStart,rowEnd):

        theBrand = category[i]
        nextBrand = category[i+1]

        if theBrand == nextBrand:
            number_of_sales += 1
        else:
            number_of_sales_dict[theBrand] = number_of_sales
            number_of_sales = 1


    return number_of_sales_dict

#dictionary of brands and their number of sales, but can't tell which one has the most sales
sales = val_counts(brand_list)

# dict_sort sorts dictionary by values from least to greatest
#  code within dict_sort is copied from: https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/
def dict_sort(d):

    dict_sorted = dict()
    sorted_keys = sorted(d, key=d.get)

    for k in sorted_keys:
        dict_sorted[k] = d[k]
    
    return dict_sorted

#jolie-robe has the most sales, followed by max and puma
sales_sorted = dict_sort(sales)
# print(sales_sorted)

largest_percentage_brand = sales_sorted['jolie-robe'] / total_sales * 100

largest_percent_results = f"Jolie-Robe Percent of Sales: {largest_percentage_brand:.1f}%"
print(largest_percent_results)

color_dict = val_counts(color_list)

colors_sorted = dict_sort(color_dict)

# most common color is blue, followed by black and grey
# print(colors_sorted)

percent_off_dict = val_counts(percent_off_list) 
percent_off_sorted = dict_sort(percent_off_dict)

average_discount = sum(percent_off_list) / len(percent_off_list)
average_discount_results = f"The average discount is {average_discount:.1f}%."
print(average_discount_results)

# print(percent_off_sorted)

discount_dict = {'No Discount':0, '10-20% Off':0, '20-30% Off': 0, '30-50% Off':0, 'More Than 50% off':0}

for prcnt, count in percent_off_sorted.items():
    
    if prcnt == 0:
        discount_dict['No Discount'] += count
    elif prcnt >= 10 and prcnt <= 20:
        discount_dict['10-20% Off'] += count
    elif prcnt > 20 and prcnt <= 30:
        discount_dict['20-30% Off'] += count
    elif prcnt > 30 and prcnt <= 50:
        discount_dict['30-50% Off'] += count
    else:
        discount_dict['More Than 50% off'] += count

# print(dict_sort(discount_dict)) 

#each product_id is unique
# print(dict_sort(val_counts(product_id_list)))
        
# print(gender_dict)

percent_men = gender_dict["Men"] / total_sales * 100
percent_women = gender_dict["Women"] / total_sales * 100

# print(f"{percent_men:.1f}%")
# print(f"{percent_women:.1f}%")

average_price = sum(discount_price_list) / len(discount_price_list)
average_price_results = f"The average price is {average_price:,.0f} Indian Rupees"
print(average_price_results)

womens_average_price = sum(womens_price) / len(womens_price)

mens_average_price = sum(mens_price) / len(mens_price)

womens_average_price_results = f"{womens_average_price:,.0f} rupees"
mens_average_price_results = f"{mens_average_price:,.0f} rupees"
print(womens_average_price_results)
print(mens_average_price_results)

with open(file_to_save, "w") as txt_file:

    txt_file.write(average_price_results)












       
        