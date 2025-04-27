"""
This module provides dummy data for the PetZilla application.
It replaces database functionality with in-memory data structures.
"""

def get_products():
    """
    Return a list of dummy products for the pet store with real images.
    """
    return [
        {
            "id": 1,
            "name": "Premium Dog Food",
            "category": "dog-food",
            "description": "High-quality nutrition for adult dogs of all breeds.",
            "price": 49.99,
            "stock": 100,
            "product_img": "https://images.unsplash.com/photo-1585846888097-620867d3149d?w=300&h=300&fit=crop"
        },
        {
            "id": 2,
            "name": "Cat Health Supplements",
            "category": "cat-medicine",
            "description": "Vitamins and supplements for your feline friend.",
            "price": 29.99,
            "stock": 50,
            "product_img": "https://images.unsplash.com/photo-1606851091851-e8c8c0fca5ba?w=300&h=300&fit=crop"
        },
        {
            "id": 3,
            "name": "Interactive Dog Toy",
            "category": "dog-toy",
            "description": "Keeps your dog entertained and mentally stimulated.",
            "price": 14.99,
            "stock": 75,
            "product_img": "https://images.unsplash.com/photo-1546975490-e8b92a360b24?w=300&h=300&fit=crop"
        },
        {
            "id": 4,
            "name": "Bird Seed Mix",
            "category": "bird-food",
            "description": "Nutritious seed blend for small to medium birds.",
            "price": 9.99,
            "stock": 120,
            "product_img": "https://images.unsplash.com/photo-1520808663317-647b476a81b9?w=300&h=300&fit=crop"
        },
        {
            "id": 5,
            "name": "Rabbit Probiotic",
            "category": "rabbit-medicine",
            "description": "Digestive health supplement for rabbits.",
            "price": 19.99,
            "stock": 40,
            "product_img": "https://images.unsplash.com/photo-1518796745738-41048802f99a?w=300&h=300&fit=crop"
        },
        {
            "id": 6,
            "name": "Cat Climbing Tower",
            "category": "cat-toy",
            "description": "Multi-level climbing and play structure for cats.",
            "price": 79.99,
            "stock": 25,
            "product_img": "https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=300&h=300&fit=crop"
        },
        {
            "id": 7,
            "name": "Premium Cat Food",
            "category": "cat-food",
            "description": "Balanced nutrition for indoor cats.",
            "price": 39.99,
            "stock": 90,
            "product_img": "https://images.unsplash.com/photo-1604542031658-5799ca5d7936?w=300&h=300&fit=crop"
        },
        {
            "id": 8,
            "name": "Dog Joint Supplement",
            "category": "dog-medicine",
            "description": "Supports healthy joint function in dogs.",
            "price": 34.99,
            "stock": 60,
            "product_img": "https://images.unsplash.com/photo-1598133894008-61f7fdb8cc3a?w=300&h=300&fit=crop"
        },
        {
            "id": 9,
            "name": "Catnip Mouse Toy",
            "category": "cat-toy",
            "description": "Soft plush mouse filled with premium catnip.",
            "price": 4.99,
            "stock": 150,
            "product_img": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?w=300&h=300&fit=crop"
        },
        {
            "id": 10,
            "name": "Dog Dental Chews",
            "category": "dog-food",
            "description": "Helps clean teeth and freshen breath.",
            "price": 12.99,
            "stock": 80,
            "product_img": "https://images.unsplash.com/photo-1568640347023-a616a30bc3bd?w=300&h=300&fit=crop"
        },
        {
            "id": 11,
            "name": "Hamster Wheel",
            "category": "hamster-toy",
            "description": "Silent spinner exercise wheel for small pets.",
            "price": 8.99,
            "stock": 45,
            "product_img": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?w=300&h=300&fit=crop"
        },
        {
            "id": 12,
            "name": "Bird Cage Perch",
            "category": "bird-toy",
            "description": "Natural wood perch for bird cages.",
            "price": 6.99,
            "stock": 65,
            "product_img": "https://images.unsplash.com/photo-1590674899484-11ba64a739ab?w=300&h=300&fit=crop"
        }
    ]

def get_users():
    """
    Return a list of dummy users.
    """
    return [
        {
            "user_id": 1,
            "username": "john_pet_lover",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "address": "123 Pet Street, Petville"
        },
        {
            "user_id": 2,
            "username": "sara_dog_mom",
            "email": "sara@example.com",
            "phone": "234-567-8901",
            "address": "456 Animal Avenue, Dogtown"
        },
        {
            "user_id": 3,
            "username": "mike_cat_dad",
            "email": "mike@example.com",
            "phone": "345-678-9012",
            "address": "789 Feline Road, Catsburg"
        }
    ]

def get_orders():
    """
    Return a list of dummy orders.
    """
    return [
        {
            "order_id": 1001,
            "customer_name": "John Pet Lover",
            "customer_phone": "123-456-7890",
            "customer_email": "john@example.com",
            "payment_method": "COD",
            "transaction_id": None
        },
        {
            "order_id": 1002,
            "customer_name": "Sara Dog Mom",
            "customer_phone": "234-567-8901",
            "customer_email": "sara@example.com",
            "payment_method": "Bkash",
            "transaction_id": "BK12345678"
        },
        {
            "order_id": 1003,
            "customer_name": "Mike Cat Dad",
            "customer_phone": "345-678-9012",
            "customer_email": "mike@example.com",
            "payment_method": "COD",
            "transaction_id": None
        }
    ]