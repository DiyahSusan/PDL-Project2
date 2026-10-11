db.orders.aggregate([
  { $unwind: "$items" },  
  { $group: {
      _id: "$items.category",
      total_revenue: { $sum: { $multiply: ["$items.qty", "$items.price"] } } }},
    { $sort: { total_revenue: -1 } }
]).explain("executionStats");
