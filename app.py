from flask import Flask, render_template, request
import pandas as pd
import nltk

app = Flask(__name__)

csv_file_path = 'project_daraz3.xlsx'

# Read the CSV file into a DataFrame
df = pd.read_excel(csv_file_path)

# Download NLTK data if not already present


# Convert DataFrame to a list of dictionaries for rendering in HTML
data = df.to_dict(orient='records')


@app.route('/')
def index():
    # Render the HTML template with the data
    return render_template('index.html', data=data)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html',
                           total_listings=len(df),
                           avg_price=df['Price'].mean(),
                           avg_ratings=df['Ratings'].mean(),
                           total_questions=df['Questions'].sum(),
                           top_products=get_top_products(df, 'Ratings', 5)
                           )
def get_top_products(df, criteria, n):
    # Get the top N products based on the specified criteria
    top_products = df.sort_values(by=criteria, ascending=False).head(n)
    return top_products.to_dict(orient='records')

@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    response = generate_response(user_message)
    return {'text': response}


def generate_response(message):
    # Lowercase the user's message and generate bigrams
    tokens = nltk.word_tokenize(message.lower())
    bigrams_list = list(nltk.bigrams(tokens))

    # Simple keyword-based response
    if 'price' in tokens:
        # Check for specific price range queries
        if ('below' in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Price'] <= price_limit]

            # Create a response message with the product details
            response_message = f'The phones with questions under : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        if ('above' in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Price'] >= price_limit]

            # Create a response message with the product details
            response_message = f'The phones with questions under : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        
        if ('is'  in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Price'] == price_limit]

            # Create a response message with the product details
            response_message = f'The phones with prices : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif 'price' in tokens:
            # Extract price range from user query
            min_price, max_price = None, None
            for i, token in enumerate(tokens):
                if token.isdigit():
                    if 'under' in tokens[i - 1:i + 1] or 'below' in tokens[i - 1:i + 1]:
                        max_price = int(token)
                    elif 'more' in tokens[i - 1:i + 1]:
                        min_price = int(token)
                    else:
                        # If no keyword is specified, consider it as an exact price
                        min_price = max_price = int(token)
            # Filter products based on the specified price range
            if min_price is not None and max_price is not None:
                filtered_products = df[(df['Price'] >= min_price) & (df['Price'] <= max_price)]
                response_message = f'Mobiles with prices between {min_price} and {max_price}:\n'
            elif min_price is not None:
                filtered_products = df[df['Price'] >= min_price]
                response_message = f'Mobiles with prices above {min_price}:\n'
            elif max_price is not None:
                filtered_products = df[df['Price'] <= max_price]
                response_message = f'Mobiles with prices under {max_price}:\n'
            else:
                response_message = 'Please specify a valid price range.'
            # Create a response message with the product details
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += "\n"  # Add a blank line between products

            return response_message
        else:
            return 'The product is not in this range'
    elif 'questions' in tokens:
         if ('under' in tokens or 'below' in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Questions'] <= price_limit]

            # Create a response message with the product details
            response_message = f'The phones with questions under : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
         elif ('above' in tokens or 'more' in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Questions'] >= price_limit]

            # Create a response message with the product details
            response_message = f'The phones with questions above  : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
         
         elif ('is' in tokens ) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Questions'] == price_limit]

            # Create a response message with the product details
            response_message = f'The phones with questions  : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
         else:
             return 'The product is not in this range'
    elif 'brand' in tokens:
        if ('samsung'  in tokens) :
            filtered_products = df[df['Company'] =='Samsung']
            response_message = f'The phones with  : Samsung are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('redmi'  in tokens) :
            filtered_products = df[df['Company'] =='Redmi']
            response_message = f'The phones with  : Redmi are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('infinix'  in tokens) :
            filtered_products = df[df['Company'] =='Infinix']
            response_message = f'The phones with  : Infinix are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('realme'  in tokens) :
            filtered_products = df[df['Company'] =='Realme']
            response_message = f'The phones with  : Realme are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('tecno'  in tokens) :
            filtered_products = df[df['Company'] =='Tecno']
            response_message = f'The phones with  : Tecno are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message

        elif ('vivo'  in tokens) :
            filtered_products = df[df['Company'] =='vivo']
            response_message = f'The phones with  : vivo are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message

        elif ('sparx'  in tokens) :
            filtered_products = df[df['Company'] =='SPARX']
            response_message = f'The phones with  : SPARX are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message 
        elif ('honor'  in tokens) :
            filtered_products = df[df['Company'] =='Honor']
            response_message = f'The phones with  : Honor are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('itel'  in tokens) :
            filtered_products = df[df['Company'] =='itel']
            response_message = f'The phones with  : itel are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('xiaomi'  in tokens) :
            filtered_products = df[df['Company'] =='Xiaomi']
            response_message = f'The phones with  : Xiaomi are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        elif ('oppo'  in tokens) :
            filtered_products = df[df['Company'] =='OPPO']
            response_message = f'The phones with  : OPPO are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
        else:
             return 'The brand yu enter is wrong or check spellings'
    elif ('best' in tokens and 'phone' in tokens and 'specs' in tokens and 'ram' in tokens and 'camera' in tokens):
        
        filtered_products = df[(df['RAM'] ==64.0) | (df['Camera'] == 48.0)]
        response_message = f'The phones with  : 64gb ram or 48mp camera  are:\n'
        for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
        return response_message
    #Show me phones under the price of 45k and over a rating of 4."
    elif('price' in tokens) and ('ratings in tokens'):
        if ('under' in tokens or 'below' in tokens) and any(token.isdigit() for token in tokens)and ('above' in tokens or 'more' in tokens) and any(token.isdigit() for token in tokens):
            min_price = [int(token) for token in tokens if token.isdigit() and ('under' in tokens or 'below' in tokens)][0]
            min_rating = [int(token) for token in tokens if token.isdigit() and ('above' in tokens or 'more' in tokens)][0]
            filtered_products = df[(df['Price'] < min_price) & (df['Ratings'] > min_rating)]
            response_message = f'The phones with  price under { min_price}and above rating { min_rating} are:\n'
            for _, product in filtered_products.iterrows():
                    response_message += f"Product ID: {product['Product id']}\n"
                    response_message += f"Name: {product['Name']}\n"
                    response_message += f"Price: {product['Price']}\n"
                    response_message += f"Ratings: {product['Ratings']}\n"
                    response_message += f"Score: {product['Score']}\n"
                    response_message += f"Questions: {product['Questions']}\n"
                    response_message += f"Specification: {product['Specification']}\n"
                    response_message += "\n"  # Add a blank line between products
            return response_message
       
        

    elif 'ratings' in tokens:
         if ('under' in tokens or 'below' in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Ratings'] <= price_limit]

            # Create a response message with the product details
            response_message = f'The phones with ratings under : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
         elif ('above' in tokens or 'more' in tokens) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Ratings'] >= price_limit]

            # Create a response message with the product details
            response_message = f'The phones with ratings above  : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
         elif ('is' in tokens ) and any(token.isdigit() for token in tokens):
            price_limit = next(token for token in tokens if token.isdigit())
            price_limit = int(price_limit)

            # Filter products based on the specified price limit
            filtered_products = df[df['Ratings'] == price_limit]

            # Create a response message with the product details
            response_message = f'The phones with ratings  : {price_limit} are:\n'
            for _, product in filtered_products.iterrows():
                response_message += f"Product ID: {product['Product id']}\n"
                response_message += f"Name: {product['Name']}\n"
                response_message += f"Price: {product['Price']}\n"
                response_message += f"Ratings: {product['Ratings']}\n"
                response_message += f"Company: {product['Company']}\n"
                response_message += f"Score: {product['Score']}\n"
                response_message += f"Questions: {product['Questions']}\n"
                response_message += f"Specification: {product['Specification']}\n"
                response_message += "\n"  # Add a blank line between products
            return response_message
         else:
             return 'The product is not in this range'

    elif 'brand' in tokens and 'rating' in tokens and 'ram' in tokens and 'camera' in tokens:
        brand_name = next((token for token in tokens if token.isalpha()), None)  # Extract the brand name
        min_rating = 4
        min_ram = 4
        min_camera = 48
        if any(token.isdigit() for token in tokens):
            min_rating = next((int(token) for token in tokens if token.isdigit() and int(token) >= 1 and int(token) <= 5), min_rating)
            min_ram = next((int(token) for token in tokens if token.isdigit() and int(token) >= 4 and int(token) <= 8), min_ram)
            min_camera = next((int(token) for token in tokens if token.isdigit()), min_camera)
        filtered_products = df[(df['Company'].str.lower() == brand_name.lower()) &
                            (df['Score'] <= min_rating) &
                            ((df['RAM'] >= min_ram) |(df['RAM'] <= 8))
                            (df['Camera'] <= min_camera)]
        sorted_products = filtered_products.sort_values(by=['RAM', 'Ratings', 'Camera'], ascending=[False, False, False])
        top_5_products = sorted_products.head(5)
        response_message = f'The top 5 {brand_name} phones with a {min_rating}-star rating, {min_ram} to 8 GB RAM, and above a {min_camera} MP camera are:\n'
        for _, product in top_5_products.iterrows():
            response_message += f"Product ID: {product['Product id']}\n"
            response_message += f"Name: {product['Name']}\n"
            response_message += f"Price: {product['Price']}\n"
            response_message += f"Ratings: {product['Ratings']}\n"
            response_message += f"Company: {product['Company']}\n"
            response_message += f"Score: {product['Score']}\n"
            response_message += f"Specification: {product['Specification']}\n"
            response_message += f"Questions: {product['Questions']}\n"
            response_message += "\n"  # Add a blank line between products
        return response_message
    else:
        return "I'm sorry, I didn't understand that. Can you please clarify?"


if __name__ == '__main__':
    app.run(debug=True)
