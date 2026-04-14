const mongoose = require('mongoose');

const CollectionScheduleSchema = new mongoose.Schema({
    userId: { type: String, required: true },
    scheduledDate: { type: Date, required: true },
    wasteType: { type: String, required: true },
    quantity: { type: Number, required: true },
    status: { type: String, required: true },
},{ timestamps: true });

module.exports = mongoose.model('CollectionSchedule', CollectionScheduleSchema);