import requests
import pandas as pd
import time
class Product:
    def __init__(self, account_token):
        self.account_token = account_token
        self.base_url = "https://api.ready2order.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.account_token}",
            "Content-Type": "application/json"
        }

    def get_products(self, as_dataframe=True, limit=100):
        """
        Fetch and return all products from the API with pagination and rate limit handling.

        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :param limit: int, number of products to fetch per request (default is 100).
        :return: pd.DataFrame or list, a DataFrame containing the products data or raw JSON.
        """
        url = f"{self.base_url}/products"
        page = 1
        all_products = []
        max_retries = 5
        retry_count = 0

        while True:
            # Add pagination parameters to the request
            params = {'limit': limit, 'page': page}
            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                products = response.json()
                all_products.extend(products)

                # If we get fewer products than the limit, we've fetched all available products
                if len(products) < limit:
                    break

                # Move to the next page
                page += 1
                retry_count = 0  # Reset retry count after successful request

            elif response.status_code == 429:
                # Handle rate limit (HTTP 429)
                retry_after = int(
                    response.headers.get("Retry-After", 60))  # Retry after duration, default to 60 seconds
                print(f"Rate limit exceeded, retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retry_count += 1
                if retry_count >= max_retries:
                    print("Max retries reached. Exiting...")
                    return None

            else:
                # Handle other errors
                print(f"Error {response.status_code}: {response.text}")
                return None

        if as_dataframe:
            return pd.DataFrame(all_products)
        return all_products


    def get_id_by_product(self, artnr):
        products = self.get_products()
        product = products.loc[products['product_itemnumber'] == artnr]
        return product['product_id'].values[0]




    def update_product(self, product_data):
        """
        Update an existing product with the given data.

        :param product_id: The ID of the product to update.
        :param product_data: A dictionary with the product's updated data.
        :return: The updated product if successful, None otherwise.
        """

        products_old = self.get_products()

        # print(products_old)
        # print(product_data)

        product_data = product_data.rename(columns={'ArtNr_Neu':'product_itemnumber'})
        products_old = products_old[['product_itemnumber','product_id']]


        df_new = products_old.merge(product_data, on='product_itemnumber', how='left')



        # print(df_new)
        # breakpoint()

        for i,r in df_new.iterrows():

            product_id = r['product_id']
            product_data = r.to_dict()

            url = f"{self.base_url}/products/{product_id}"
            response = requests.put(url, headers=self.headers, json=product_data)
            if len(df_new) > 60:
                time.sleep(1)
            if response.status_code == 200:
                print(f"Product {product_id} updated successfully.",product_data)
                # return response.json()
            else:
                print(f"Error {response.status_code}: {response.text}")
                # return None

    def create_products(self, df):
        """
        Create new products from a pandas DataFrame.

        :param df: pd.DataFrame, a DataFrame containing product data.
                   Each row represents a product, with columns corresponding to product fields.
        :return: A list of responses from the API for each product creation attempt.
        """
        url = f"{self.base_url}/products"
        responses = []

        for index, row in df.iterrows():
            product_data = row.to_dict()  # Convert row to a dictionary
            # print(product_data)
            response = requests.post(url, headers=self.headers, json=product_data)
            if response.status_code == 201:
                responses.append({"status": "success", "product": response.json()})
            else:
                responses.append({"status": "error", "error_message": response.text, "product_data": product_data})

        return responses

    def delete_product(self, product_id = None, artnr = None):
        """
        Delete a product by its ID.

        :param product_id: The ID of the product to delete.
        :return: A message indicating whether the deletion was successful or not.
        """

        if artnr != None:
            product_id = self.get_id_by_product(artnr)




        url = f"{self.base_url}/products/{product_id}"
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 200:
            return {"status": "success", "message": "Product deleted successfully"}
        else:
            return {"status": "error", "error_message": response.text}

    def get_product_groups(self, as_dataframe=True, limit=100):
        """
        Fetch and return all product groups from the API with pagination and rate limit handling.

        :param as_dataframe: bool, whether to return the data as a DataFrame (default is True).
        :param limit: int, number of product groups to fetch per request (default is 100).
        :return: pd.DataFrame or list, a DataFrame containing the product groups data or raw JSON.
        """
        url = f"{self.base_url}/productgroups"
        page = 1
        all_product_groups = []
        max_retries = 5
        retry_count = 0

        while True:
            # Add pagination parameters to the request
            params = {'limit': limit, 'page': page}
            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code == 200:
                product_groups = response.json()
                all_product_groups.extend(product_groups)

                # If we get fewer product groups than the limit, we've fetched all available product groups
                if len(product_groups) < limit:
                    break

                # Move to the next page
                page += 1
                retry_count = 0  # Reset retry count after successful request

            elif response.status_code == 429:
                # Handle rate limit (HTTP 429)
                retry_after = int(
                    response.headers.get("Retry-After", 60))  # Retry after duration, default to 60 seconds
                print(f"Rate limit exceeded, retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retry_count += 1
                if retry_count >= max_retries:
                    print("Max retries reached. Exiting...")
                    return None

            else:
                # Handle other errors
                print(f"Error {response.status_code}: {response.text}")
                return None

        if as_dataframe:
            return pd.DataFrame(all_product_groups)
        return all_product_groups