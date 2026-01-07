// MongoDB Operations for FlexiMart Product Catalog

const { MongoClient } = require('mongodb');
const uri = "mongodb://localhost:27017";
const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();
    const db = client.db("fleximart");
    const products = db.collection("products");

    // -----------------------------
    // Operation 1: Load Data (1 mark)
    // -----------------------------
    // Import products_catalog.json using mongoimport CLI:
    // mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray

    // -----------------------------
    // Operation 2: Basic Query (2 marks)
    // -----------------------------
    const electronicsUnder50k = await products.find(
      { category: "Electronics", price: { $lt: 50000 } },
      { projection: { _id: 0, name: 1, price: 1, stock: 1 } }
    ).toArray();
    console.log("Electronics under 50k:", electronicsUnder50k);

    // -----------------------------
    // Operation 3: Review Analysis (2 marks)
    // -----------------------------
    const highRatedProducts = await products.aggregate([
      { $unwind: "$reviews" },
      { $group: {
          _id: "$product_id",
          name: { $first: "$name" },
          avgRating: { $avg: "$reviews.rating" }
      }},
      { $match: { avgRating: { $gte: 4.0 } } },
      { $project: { _id: 0, product_id: "$_id", name: 1, avgRating: 1 } }
    ]).toArray();
    console.log("High rated products:", highRatedProducts);

    // -----------------------------
    // Operation 4: Update Operation (2 marks)
    // -----------------------------
    await products.updateOne(
      { product_id: "ELEC001" },
      { $push: { reviews: { user: "U999", rating: 4, comment: "Good value", date: new Date() } } }
    );
    console.log("Review added to ELEC001");

    // -----------------------------
    // Operation 5: Complex Aggregation (3 marks)
    // -----------------------------
    const avgPriceByCategory = await products.aggregate([
      { $group: {
          _id: "$category",
          avg_price: { $avg: "$price" },
          product_count: { $sum: 1 }
      }},
      { $project: { _id: 0, category: "$_id", avg_price: 1, product_count: 1 } },
      { $sort: { avg_price: -1 } }
    ]).toArray();
    console.log("Average price by category:", avgPriceByCategory);

  } finally {
    await client.close();
  }
}

run().catch(console.dir);
