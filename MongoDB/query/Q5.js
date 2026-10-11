db.orders.aggregate([
  { $match: { 
      status: "COMPLETED",
      created_at: { 
        $gte: ISODate("2026-01-01T00:00:00Z"),
        $lte: ISODate("2026-12-31T23:59:59Z")}}},
  { $unwind: "$items" },
  { $group: {
      _id: "$items.category",
      total_items_sold: { $sum: "$items.qty" },
      total_revenue: { $sum: { $multiply: ["$items.qty", "$items.price"] } }
  }}, 
  { $sort: { total_revenue: -1 } } 
]).explain("executionStats");
