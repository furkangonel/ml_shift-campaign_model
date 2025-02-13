from models.models_2.processed_data_model2 import ProcessedData_Model2, ProcessedDataList_Model2
from models.models_2.incoming_data_model2 import IncomingData_Model2
from typing import List
from database.connection import db
from sklearn.preprocessing import MinMaxScaler
from mlxtend.frequent_patterns import fpgrowth, association_rules
import pandas as pd


async def process_incoming_data_m2(data_list: List[IncomingData_Model2]) -> ProcessedDataList_Model2:
    """
    Gelen veri listesini işler, FP-Growth algoritmasını uygular ve sonuçları döndürür.

    Args:
        data_list (List[IncomingData_Model2]): İşlenecek veri listesi.

    Returns:
        ProcessedDataList_Model2: İşlenmiş verilerin listesi.
    """
    processed_data_list = ProcessedDataList_Model2(processedData=[])

    # Gelen veriyi işlemek için dönüştür
    data_dict_list = []
    for data in data_list:
        for product in data.products:
            data_dict_list.append({
                "order_id": data.order_id,
                "product": product.product,
                "price": product.price,
                "profit_margin": product.profit_margin,
                "quantity": product.quantity
            })

    # Veri çerçevesine dönüştür
    orders_data = pd.DataFrame(data_dict_list)

    # Sepet formatı
    fp_growth_data = orders_data[['order_id', 'product', 'quantity']]
    basket = fp_growth_data.groupby(['order_id', 'product'])['quantity'].sum().unstack().fillna(0)
    basket = basket > 0  # Boolean format

    # FP-Growth algoritması
    frequent_itemsets = fpgrowth(basket, min_support=0.09, use_colnames=True)
    if frequent_itemsets.empty:
        return processed_data_list  # Boşsa işlenmiş veri döndür

    # Birliktelik kuralları
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.4)
    if rules.empty:
        return processed_data_list  # Boşsa işlenmiş veri döndür

    # Normalizasyon
    scaler = MinMaxScaler()
    rules[['support', 'confidence', 'lift']] = scaler.fit_transform(rules[['support', 'confidence', 'lift']])

    # Ürün bilgileri
    product_info = orders_data[['product', 'price', 'profit_margin']].drop_duplicates()

    def get_product_info(products):
        """Ürün bilgilerini birleştirir."""
        products = list(products)
        info = product_info[product_info['product'].isin(products)].to_dict(orient='records')
        return {
            'Products': products,
            'Prices': [item['price'] for item in info],
            'Profit_Margins': [item['profit_margin'] for item in info]
        }

    # Antecedent ve Consequent bilgilerini ekle
    rules['Antecedent_Info'] = rules['antecedents'].apply(get_product_info)
    rules['Consequent_Info'] = rules['consequents'].apply(get_product_info)

    # İşlenmiş verileri oluştur
    seen_combinations = set()  # Tekrar kontrolü için set
    unique_processed_data = []  # Benzersiz veriler

    for _, row in rules.iterrows():
        unique_key = (row['support'], row['confidence'], row['lift'])
        if unique_key not in seen_combinations:
            processed_data = ProcessedData_Model2(
                antecedents=", ".join(list(row['antecedents'])),
                consequents=", ".join(list(row['consequents'])),
                support=row['support'],
                confidence=row['confidence'],
                lift=row['lift'],
                antecedent_info=str(row['Antecedent_Info']),
                consequent_info=str(row['Consequent_Info'])
            )
            unique_processed_data.append(processed_data)
            seen_combinations.add(unique_key)  # Benzersiz anahtar ekle

    processed_data_list.processedData = unique_processed_data

    # Veritabanına kaydet
    if processed_data_list.processedData:
        await db.campaign_processed_collection.insert_many(
        [processed_data.model_dump() for processed_data in processed_data_list.processedData]        )

    return processed_data_list