import pandas as pd
from .models import Shop


# Load the CSV file
file_path = r"C:/Users/edwar/Downloads/DBB_Shops.csv"
shops_df = pd.read_csv(file_path)

# Map CSV data to the Shop model fields and create instances
for _, row in shops_df.iterrows():
    shop_id = row[0]
    floor_level = row[1]
    size = row[2]
    rent = float(row[3].replace(",", ""))

    # Create the Shop instance
    shop = Shop.objects.create(
        name=shop_id,
        type="A",  # Default or inferred type
        price=rent,
        no=shop_id,
        address=f"{floor_level}, {shop_id}",
        floor=floor_level[0],  # Extract the floor identifier
        size=size,
        status="vacant",  # Default status
        is_paid=False,  # Default value
        is_approved=False,  # Default value
    )

    # Save the shop instance to the database
    shop.save()
