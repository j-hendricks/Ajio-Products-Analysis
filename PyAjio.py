import csv
import os

file_to_load = os.path.join("Resources", "Ajio Fashion Clothing.csv")
file_to_save = os.path.join("analysis", "Ajio_analysis.txt")

# set containing all unique product ids
id_set = set()

# keeps track of number of sales
total_sales = 0

# function that converts from Indian Rupees to USD
def rupees_to_USD(rup):
    return round(0.013 * rup, 2)


# dict_sort sorts dictionary by values from least to greatest
# code within dict_sort is copied from: https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/
def dict_sort(d):

    dict_sorted = dict()
    sorted_keys = sorted(d, key=d.get)

    for k in sorted_keys:
        dict_sorted[k] = d[k]
    
    return dict_sorted


# function returns dictionary containing each brand and number of sales
def val_counts(category):

    # index of first and last element in brand_list
    rowStart = 0
    rowEnd = len(category) - 1

    # dictionary with brands as keys and number of sales as values
    number_of_sales_dict = dict()
    
    # sort the brands list
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

# encode with latin-1 due to nature of csv file
with open(file_to_load,encoding='latin-1') as file:

    file_reader = csv.reader(file)
    
    # skip header and store it as a list
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

    # go through each row of data
    for row in file_reader:
        
        # each row is one sale
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

        # keep track of male and female clothing sales and prices
        if row[gender_index] == "Men":
            gender_dict["Men"] += 1
            mens_price.append(discount)
        else:
            gender_dict["Women"] += 1
            womens_price.append(discount)       

# convert lists to sets in order to obtain only unique values
product_id_set = set(product_id_list)
brand_set = set(brand_list)
color_set = set(color_list)
discount_price_set = set(discount_price_list)
original_price_set = set(original_price_list)

# length of list and set are the same for product id, meaning each product_id is unique
# print("Length of id_list:",len(product_id_list))
# print("Length of id_set:",len(product_id_set))

# 1,975 different brands
# print("", len(brand_list))

# dictionary of brands and their number of sales, but can't tell which one has the most sales
sales = val_counts(brand_list)

# jolie-robe has the most sales, followed by max and puma
sales_sorted = dict_sort(sales)
most_frequent_brand = list(sales_sorted.keys())[-1]
second_most_frequent_brand = list(sales_sorted.keys())[-2]
third_most_frequent_brand = list(sales_sorted.keys())[-3]
most_frequent_brands = most_frequent_brand + ", " + second_most_frequent_brand + ", " + third_most_frequent_brand

largest_percentage_brand = sales_sorted[most_frequent_brand] / total_sales * 100

color_dict = val_counts(color_list)
colors_sorted = dict_sort(color_dict)
# most common color is blue, followed by black and grey
most_frequent_color = list(colors_sorted.keys())[-1]
second_most_frequent_color = list(colors_sorted.keys())[-2]
third_most_frequent_color = list(colors_sorted.keys())[-3]
most_frequent_colors = most_frequent_color + ", " + second_most_frequent_color + ", " + third_most_frequent_color

percent_off_dict = val_counts(percent_off_list) 
percent_off_sorted = dict_sort(percent_off_dict)

average_discount = sum(percent_off_list) / len(percent_off_list)

average_price = sum(discount_price_list) / len(discount_price_list)
womens_average_price = sum(womens_price) / len(womens_price)
mens_average_price = sum(mens_price) / len(mens_price)

# print(percent_off_sorted)

discount_dict = {'No Discount':0, '10-20% Off':0, '20-30% Off': 0, '30-50% Off':0, '>50% Off':0}

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
        discount_dict['>50% Off'] += count

for key in discount_dict.keys():
    discount_dict[key] = round(discount_dict[key] / total_sales * 100, 1)

# each product_id is unique
# print(dict_sort(val_counts(product_id_list)))
        
# print(gender_dict)

percent_men = gender_dict["Men"] / total_sales * 100
percent_women = gender_dict["Women"] / total_sales * 100


with open(file_to_save, "w") as txt_file:

    # brand information
    number_brands_results = f"Number of Brands: {len(brand_set):,}\n"
    most_frequent_brand_results = f"Brands with Most Sales: {most_frequent_brands}\n"
    largest_percent_results = f"{most_frequent_brand} Percent of Sales: {largest_percentage_brand:.1f}%\n"

    print(number_brands_results)
    print(most_frequent_brand_results)
    print(largest_percent_results)

    # sales information
    total_sales_results = f"Total Number of Sales: {total_sales:,}\n"
    average_price_results = f"Average Price: {average_price:,.0f} rupees ({rupees_to_USD(average_price)} USD)\n"
    average_discount_results = f"Average Discount: {average_discount:.1f}%\n"

    print(total_sales_results)
    print(average_discount_results)
    print(average_price_results)
    for pair in discount_dict.items():
        print(f"{pair[0]}: {pair[1]}%\n") 

    # gender demogrpahics
    womens_average_price_results = f"Average Cost of Womens Product: {womens_average_price:,.0f} rupees ({rupees_to_USD(womens_average_price)} USD)\n"
    mens_average_price_results = f"Average Cost of Mens Product: {mens_average_price:,.0f} rupees ({rupees_to_USD(mens_average_price)} USD)\n"
    men_percentage_results = f"Men's clothing: {percent_men:.1f}%\n"
    women_percentage_results = f"Women's clothing: {percent_women:.1f}%\n"
    
    print(womens_average_price_results)
    print(mens_average_price_results)
    print(men_percentage_results)
    print(women_percentage_results)

    # common colors
    number_colors_results = f"Number of colors: {len(color_set):,}\n"
    most_frequent_color_results = f"Most Common Colors: {most_frequent_colors}\n"

    print(number_colors_results)
    print(most_frequent_color_results)
    
    # title
    txt_file.write("\n*** Ajio Product Summary ***\n\n")
    
    # brand information
    txt_file.write("Brands\n")
    txt_file.write("--------------------\n")
    txt_file.write(number_brands_results)
    txt_file.write(most_frequent_brand_results)
    txt_file.write(largest_percent_results)
    txt_file.write("--------------------\n\n")

    # sales information
    txt_file.write("Sales\n")
    txt_file.write("--------------------\n")
    txt_file.write(total_sales_results)
    txt_file.write(average_price_results)
    txt_file.write(average_discount_results)
    for pair in discount_dict.items():
        txt_file.write(f"{pair[0]}: {pair[1]}%\n") 
    txt_file.write("--------------------\n\n")
    
    # gender demogrpahics
    txt_file.write("Demographics\n")
    txt_file.write("--------------------\n")
    txt_file.write(mens_average_price_results)
    txt_file.write(womens_average_price_results)
    txt_file.write(men_percentage_results)
    txt_file.write(women_percentage_results)
    txt_file.write("--------------------\n\n")

    # common colors
    txt_file.write("Color of Products\n")
    txt_file.write("--------------------\n")
    txt_file.write(number_colors_results)
    txt_file.write(most_frequent_color_results)
    txt_file.write("--------------------\n")
    
    
    













       
        