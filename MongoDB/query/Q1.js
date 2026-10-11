var sampleOrder = db.orders.findOne();
var targetUserId = sampleOrder.user_id;
db.orders.find({ user_id: targetUserId })
    .sort({ created_at: -1 })
    .limit(10).explain("executionStats");
