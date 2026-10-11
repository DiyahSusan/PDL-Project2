db.orders.find({ 
    user_id: targetUserId, 
    "payment.status": "SUCCESS" 
  }).sort({ created_at: -1 })
    .limit(5).explain("executionStats");
