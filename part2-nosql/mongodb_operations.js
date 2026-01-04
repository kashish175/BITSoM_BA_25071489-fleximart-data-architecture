// -----------  Task 2.2: MongoDB Implementation ----------

// Select the database 
use('fleximart_db');

// Operation 1: Load Data (1 mark)
// Run this in your terminal: 
//mongoimport --db fleximart_db --collection products --file part2-nosql/products_catalog.json --jsonArray

// Operation 2: Basic Query (2 marks)
// Find Electronics with price < 50000
db.products.find(
    { category: "Electronics", price: { $lt: 50000 } },
    { name: 1, price: 1, stock: 1, _id: 0 }
);

// Operation 3: Review Analysis (2 marks)
// Calculate average rating from reviews array
db.products.aggregate([
    { $project: { name: 1, avgRating: { $avg: "$reviews.rating" } } },
    { $match: { avgRating: { $gte: 4.0 } } }
]);

// Operation 4: Update Operation (2 marks)
// Add a new review to ELEC001
db.products.updateOne(
    { product_id: "ELEC001" },
    { $push: { 
        reviews: { user: "U999", rating: 4, comment: "Good value", date: new Date() } 
    }}
); 

// Operation 5: Complex Aggregation (3 marks)
// Avg price by category, sorted descending
db.products.aggregate([
    { $group: { _id: "$category", avg_price: { $avg: "$price" }, count: { $sum: 1 } } },
    { $sort: { avg_price: -1 } }
]);