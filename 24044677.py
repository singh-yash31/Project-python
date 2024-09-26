 #define the functions for OP1 and initiazle the variable
def discounts_highest_lowest(products, category):
    highest_discount = -1
    lowest_discount = float('inf')
    highest_discount_product_id = None
    lowest_discount_product_id = None
      #Done loop through the product
    for product in products:
        product_id = product[0].lower()
        product_category = product[1].lower()
        discounted_price = float(product[2])
        #check the product belong to specified category and solve the highest and lowest discounted price
        if product_category == category.lower():
            
            if discounted_price > highest_discount:
                highest_discount = discounted_price
                highest_discount_product_id = product_id
            elif discounted_price == highest_discount:
                if product_id < highest_discount_product_id:
                    highest_discount_product_id = product_id

            
            if discounted_price < lowest_discount:
                lowest_discount = discounted_price
                lowest_discount_product_id = product_id
            elif discounted_price == lowest_discount:
                if product_id < lowest_discount_product_id:
                    lowest_discount_product_id = product_id

    return [highest_discount_product_id, lowest_discount_product_id]
     #Returing the value for highest and lowest
def distribution_prices(products, category): #Define the functions for OP2 and initalize the varaible
    price_list = []
    rating_count_threshold = 1000
    
  #loop through all product extract relvant data
    for product in products:
        product_category = product[1].lower()
        actual_price = float(product[3])
        rating_count = float(product[6])
         # Add to price_list if product belongs to the category and meets rating threshold # Sort the list of prices
        if product_category == category.lower() and rating_count > rating_count_threshold:
            price_list.append(actual_price)
           
    price_list.sort()
    n = len(price_list)
 #If no valid products found, return default values then calcualte mean,median,mean absolute devation
    if n == 0:
        return [0.0, 0.0, 0.0]  

    
    mean_price = sum(price_list) / n

    
    if n % 2 == 1:
        median_price = int(price_list[n // 2])
    else:
        median_price = int((price_list[(n // 2) - 1] + price_list[n // 2]) / 2)

    
    mad_price = sum(abs(price - mean_price) for price in price_list) / n

    return [round(mean_price, 4), round(median_price, 4), round(mad_price, 4)]               
    #return the value of mean,median,mean absolute devation
def discounted_percentages(products): #Define the function for OP3 and Dictionary to hold discounts by category
    category_discounts = {}
    #calcuate the standard devations and variance
    def calculate_variance(discounts):
        N = len(discounts)
        mean_discount = sum(discounts) / N
        sum_squared_diff = sum( [(dp - mean_discount) ** 2 for dp in discounts])
        variance = sum_squared_diff / (N - 1)
        return variance
    def calculate_std_dev(variance):
        return variance ** 0.5
       #done loop through the products 
    for product in products:
        product_category = product[1].lower()
        discounted_percentage=float(product[4])
        
        rating = float(product[5])
        # Consider only products with rating between 3.3 and 4.3 
        if 3.3 <= rating <= 4.3:
            discount = discounted_percentage
            if product_category not in category_discounts:
                category_discounts[product_category] = []
            category_discounts[product_category].append(discount)
      #List to store the standard deviations Calculate standard deviation for each category

    
    std_devs = []
    for category, discounts in category_discounts.items():
        if len(discounts) > 1:  
            variance = calculate_variance(discounts)
            std_dev = calculate_std_dev(variance)
            std_devs.append(round(std_dev, 4))

    
    return sorted(std_devs, reverse=True)
    ## Return the standard deviations sorted in descending order

def sales_high_low_price(sales, product_ids):#Define the functions for OP4 list the product for highest and lowest discount
    highest_sales = []
    lowest_sales = []
    #calculate mean of a data set and correlation between two data sets
    def calculate_mean(data):
        return sum(data) / len(data) if data else 0

    def calculate_correlation(x, y):
        mean_x = calculate_mean(x)
        mean_y = calculate_mean(y)
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        variance_x = sum((xi - mean_x) ** 2 for xi in x)
        variance_y = sum((yi - mean_y) ** 2 for yi in y)
        if variance_x == 0 or variance_y == 0:
            return 0
        return round(numerator / (variance_x * variance_y) ** 0.5, 4)  # Avoiding manual square root
    ## Loop through each line in the sales data file and Convert each line into a dictionary with product ID as key and sales as value
    for line in sales:
        year_sales = line.strip().split(', ')
        year_sales_dict = {entry.split(': ')[0].lower(): int(entry.split(': ')[1]) for entry in year_sales}
      #Append sales of highest and lowest discounted products
        highest_sales.append(year_sales_dict.get(product_ids[0], 0))
        lowest_sales.append(year_sales_dict.get(product_ids[1], 0))
     #return the correlation between the sales of highest and lowest discounted products
    return calculate_correlation(highest_sales, lowest_sales)

def main(CSVfile, TXTfile, category):
    
    products = []
    
    with open(CSVfile, 'r') as f:
        header = f.readline().strip().split(',')
        # define the main function and List to hold product data and Open and read the CSV file and Find index positions for necessary fields in the CSV file
        
        id_index = header.index("product_id")
        category_index = header.index("category")
        discounted_price_index = header.index("discounted_price $")
        actual_price_index = header.index("actual_price $")
        rating_index = header.index("rating")
        rating_count_index = header.index("rating_count")
        discounted_percentage_index=header.index("discount_percentage %")
        # Loop through each product in the CSV file and Append product details as a list
        for line in f:
            
            columns = [col.strip() for col in line.split(',')]
            
            
            product_id = columns[id_index].lower()
            product_category = columns[category_index].lower()
            discounted_price = float(columns[discounted_price_index])
            actual_price = float(columns[actual_price_index])
            rating = float(columns[rating_index])
            rating_count = int(columns[rating_count_index])
            discounted_percentage=float(columns[discounted_percentage_index])
            
            products.append([product_id, product_category, discounted_price, actual_price, discounted_percentage,rating, rating_count])
    
    # Open and read the sales data file
    with open(TXTfile, 'r') as f:
        sales = f.readlines()

    ## Call each function to calculate the desired outputs
    OP1 = discounts_highest_lowest(products, category)

    
    OP2 = distribution_prices(products, category)

    
    OP3 = discounted_percentages(products)

   
    OP4 = sales_high_low_price(sales, OP1)
    # Return the results of the four operations
    return OP1, OP2, OP3, OP4





    



