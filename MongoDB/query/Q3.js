var sampleReview = db.reviews.findOne();
var targetProductId = sampleReview.product_id;
db.reviews.find(
    { product_id: targetProductId }, 
    { user_name: 1, rating: 1, comment: 1, created_at: 1 })
    .sort({ created_at: -1 })
    .limit(10).explain("executionStats");
